import logging
import time
from urllib.parse import quote_plus

from playwright.async_api import Browser, Locator

from .utils import (
    block_unnecessary_resources,
    check_if_row_is_empty,
    create_browser_context,
)

logger = logging.getLogger(__name__)


async def scrape_flipkart(search_text: str, browser: Browser):

    start_time = time.perf_counter()

    if not search_text:
        return

    base_url = "https://www.flipkart.com"

    search_query = quote_plus(search_text)

    search_url = f"{base_url}/search?q={search_query}"

    logger.debug("Flipkart URL: %s", search_url)

    exception_count = 0
    exceptions = []
    link_to_product_data_map = {}

    try:
        context = await create_browser_context(browser)

        logger.debug(
            "Created Flipkart browser context at %.2f seconds",
            time.perf_counter() - start_time,
        )

        page = await context.new_page()
        await page.route("**/*", block_unnecessary_resources)

        await page.goto(
            search_url,
            wait_until="domcontentloaded",
            timeout=10000,
        )

        logger.debug(
            "Flipkart page loaded at %.2f seconds", time.perf_counter() - start_time
        )

        try:
            close_button = page.locator("button._2KpZ6l")
            await close_button.first.click(timeout=1000)
            logger.debug("Closed Flipkart login popup")

        except Exception:
            logger.debug("Flipkart login popup not found")

        # Allow products to render.

        # PRODUCT CARDS
        products = page.locator("div[data-id]")

        product_count = await products.evaluate_all("products => products.length")

        logger.debug("Flipkart products found: %d", product_count)

        # Fallback
        if product_count == 0:
            logger.debug(
                "Flipkart primary selector returned no products. Trying fallback."
            )

            await page.wait_for_selector("div:has(a[href*='/p/'])", timeout=5000)
            products = page.locator("div:has(a[href*='/p/'])")

            product_count = await products.evaluate_all("products => products.length")

            logger.debug("Flipkart fallback products: %d", product_count)

        # PROCESS PRODUCTS

        logger.debug(
            "Processing Flipkart products at %.2f seconds",
            time.perf_counter() - start_time,
        )

        for index in range(min(product_count, 10)):  # Limit to 10 products
            try:
                product = products.nth(index)

                card = await get_product_card(product)

                # ----------------------------------------
                # EXTRACT DATA
                # ----------------------------------------

                curr_prod_data = await get_product_data(
                    card,
                    base_url,
                )

                product_url = curr_prod_data.get("product_url")

                if product_url in link_to_product_data_map:
                    logger.debug(
                        "Duplicate product: %s",
                        curr_prod_data,
                    )
                    continue

                link_to_product_data_map[product_url] = curr_prod_data

                if check_if_row_is_empty(curr_prod_data):
                    logger.debug(
                        "Flipkart product is empty: %s",
                        curr_prod_data,
                    )
                    continue

                yield curr_prod_data

            except Exception as error:
                exception_count += 1

                exceptions.append(f"Flipkart product {index}: {error}")

        logger.debug(
            "Processed Flipkart products at %.2f seconds",
            time.perf_counter() - start_time,
        )

    except Exception as error:
        logger.error("Flipkart scraper error: %s", error)

        yield {
            "type": "error",
            "platform": "flipkart",
            "message": str(error),
        }

    logger.debug(
        "Flipkart exception count: %d",
        exception_count,
    )

    if exceptions:
        logger.debug("Flipkart exceptions:\n%s", "\n".join(exceptions))


async def get_product_name(card: Locator) -> str | None:
    """
    Extract product name from a Flipkart product card.
    """

    # Preferred: product link with title
    locator = card.locator("a[title]")

    if await locator.count() > 0:
        name = await locator.first.get_attribute(
            "title",
            timeout=3000,
        )

        if name:
            return name.strip()

    # Fallback: image alt
    locator = card.locator("img[alt]")

    if await locator.count() > 0:
        name = await locator.first.get_attribute(
            "alt",
            timeout=3000,
        )

        if name:
            return name.strip()

    # Fallback: known Flipkart product-title structure
    locator = card.locator("._1psv1zeb9 h1")

    if await locator.count() > 0:
        name = await locator.first.text_content(
            timeout=3000,
        )

        if name:
            return name.strip()

    return None


async def get_product_price(card: Locator) -> float | None:
    """
    Extract product price from a Flipkart product card.
    """

    # Preferred selector
    locator = card.locator("div.css-g5y9jx").filter(has_text="₹")

    # Fallback
    if await locator.count() == 0:
        locator = card.locator("a").locator("div:text('₹')")

    if await locator.count() == 0:
        return None

    price_text = await locator.first.text_content(timeout=3000)

    if not price_text:
        return None

    # Remove currency and commas
    clean_price = price_text.replace("₹", "").replace(",", "").strip()

    # Keep only digits and decimal point
    clean_price = "".join(char for char in clean_price if char.isdigit() or char == ".")

    if not clean_price:
        return None

    try:
        return float(clean_price)
    except ValueError:
        return None


async def get_product_rating(card: Locator) -> float | None:
    """
    Extract product rating from a Flipkart product card.

    Important:
    The rating lookup is scoped to `card`, so ratings from
    other products on the search page cannot be accidentally
    picked up.
    """

    locator = card.locator("div.MKiFS6")

    if await locator.count() == 0:
        return None

    rating_text = await locator.first.text_content(timeout=3000)
    rating = parse_rating(rating_text)
    return rating


def parse_rating(text: str | None) -> float | None:
    """
    Convert rating text such as:
        '4.3'
        '4.3 ★'
        '4.3 12,345 Ratings'

    into:
        4.3
    """

    if not text:
        return None

    text = text.replace("★", " ").strip()

    # First token should normally be the rating.
    first_token = text.split()[0] if text.split() else ""

    try:
        rating = float(first_token)
    except ValueError:
        return None

    # Sanity check.
    if 0 <= rating <= 5:
        return rating

    return None


async def get_product_url(
    card: Locator,
    base_url: str,
) -> str | None:
    """
    Extract product URL from a Flipkart product card.
    """

    # Preferred: actual product link
    locator = card.locator("a[href*='/p/']")

    if await locator.count() > 0:
        product_url = await locator.first.get_attribute(
            "href",
            timeout=3000,
        )

        if product_url:
            return normalize_product_url(
                product_url,
                base_url,
            )

    # Fallback: any anchor
    locator = card.locator("a")

    if await locator.count() == 0:
        return None

    product_url = await locator.first.get_attribute(
        "href",
        timeout=3000,
    )

    if product_url:
        return normalize_product_url(
            product_url,
            base_url,
        )

    return None


def normalize_product_url(
    product_url: str,
    base_url: str,
) -> str:
    """
    Convert relative Flipkart URLs into absolute URLs.
    """

    if product_url.startswith("/"):
        return base_url + product_url

    return product_url


async def get_product_image(card: Locator) -> str | None:
    """
    Extract product image URL.
    """

    locator = card.locator("img")

    if await locator.count() == 0:
        return None

    image = locator.first

    # Normal image
    image_src = await image.get_attribute(
        "src",
        timeout=3000,
    )

    if image_src:
        return image_src

    # Lazy-loaded image
    image_src = await image.get_attribute(
        "data-src",
        timeout=3000,
    )

    if image_src:
        return image_src

    # srcset fallback
    image_src = await image.get_attribute(
        "srcset",
        timeout=3000,
    )

    if image_src:
        # srcset may contain multiple URLs, Take the first one.
        return image_src.split(",")[0].strip().split(" ")[0]

    return None


# ============================================================
# CARD HELPERS
# ============================================================


async def get_product_card(product: Locator) -> Locator:
    """
    Find the actual product card inside a Flipkart result.
    """

    data_tkid = product.locator("[data-tkid]")

    if await data_tkid.count() > 0:
        return data_tkid.first

    return product


async def get_product_data(
    card: Locator,
    base_url: str,
) -> dict:
    """
    Extract all supported fields from one product card.
    """

    name = await get_product_name(card)
    price = await get_product_price(card)
    rating = await get_product_rating(card)
    product_url = await get_product_url(
        card,
        base_url,
    )

    image_src = await get_product_image(card)

    return {
        "type": "product",
        "name": name,
        "price": price,
        "rating": rating,
        "product_url": product_url,
        "image_src": image_src,
        "platform": "flipkart",
    }
