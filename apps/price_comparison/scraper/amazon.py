import asyncio
import logging
import time
from urllib.parse import quote_plus

from playwright.async_api import Browser, Locator

from .utils import block_unnecessary_resources, create_browser_context

logger = logging.getLogger(__name__)


async def scrape_amazon(search_text: str, browser: Browser):
    """
    Scrape product information from Amazon based on the search text.
    """

    start_time = time.perf_counter()

    if not search_text:
        return

    base_url = "https://www.amazon.in"

    search_text = quote_plus(search_text)

    search_url = f"{base_url}/s?k={search_text}&ref=nb_sb_noss"

    logger.debug("Amazon URL: %s", search_url)

    exception_count = 0
    exceptions = []

    context = await create_browser_context(browser)

    logger.debug(
        "Amazon browser context created at %.2f seconds",
        time.perf_counter() - start_time,
    )

    page = await context.new_page()
    tasks = []

    try:
        await page.route("**/*", block_unnecessary_resources)
        link_to_product_data_map = {}

        await page.goto(
            search_url,
            wait_until="domcontentloaded",
            timeout=20000,
        )

        logger.debug(
            "Amazon page loaded at %.2f seconds", time.perf_counter() - start_time
        )

        products = page.locator("div[data-component-type='s-search-result']")

        product_count = await products.evaluate_all("products => products.length")

        logger.debug("Amazon products found: %d", product_count)

        logger.debug(
            "Processing Amazon products at %.2f seconds",
            time.perf_counter() - start_time,
        )

        for index in range(min(product_count, 10)):  # Limit to 10 products
            product = products.nth(index)
            tasks.append(extract_amazon_product(product, base_url))

        for index, future in enumerate(asyncio.as_completed(tasks)):
            try:
                # name = await get_product_name(product)
                # price = await get_product_price(product)
                # rating = await get_product_rating(product)
                # product_url = await get_product_url(
                #     product,
                #     base_url,
                # )
                # image_src = await get_product_image(product)

                curr_prod_data = await future
                product_url = curr_prod_data.get("product_url")

                # curr_prod_data = {
                #     "type": "product",
                #     "name": (name.strip() if name else None),
                #     "price": price,
                #     "rating": rating,
                #     "product_url": product_url,
                #     "image_src": image_src,
                #     "platform": "amazon",
                # }

                # logger.debug("Amazon product: %s", curr_prod_data)

                if product_url in link_to_product_data_map:
                    logger.debug("Duplicate product: %s", curr_prod_data)
                    continue

                link_to_product_data_map[product_url] = curr_prod_data

                yield curr_prod_data

            except Exception as error:
                exception_count += 1

                exceptions.append(f"Amazon product {index}: {error}")

        logger.debug(
            "Processed Amazon products at %.2f seconds",
            time.perf_counter() - start_time,
        )

    except Exception as error:
        logger.error("Amazon scraper error: %s", error)
        await page.screenshot(
            path="/tmp/amazon-debug.png",
            full_page=True,
        )

        yield {
            "type": "error",
            "platform": "amazon",
            "message": str(error),
        }
    finally:
        await context.close()

    logger.debug(
        "Amazon exception count: %d",
        exception_count,
    )

    if exceptions:
        logger.debug("Amazon exceptions:\n%s", "\n".join(exceptions))


async def get_product_name(product: Locator):
    """
    Get the product name from the product locator.
    """
    try:
        name_locator = product.locator("[data-cy='title-recipe'] h2 span, h2 span").last

        return await name_locator.text_content(timeout=3000)
    except Exception:
        logger.exception("Error occurred while fetching product name")
        return None


async def get_product_price(product: Locator):
    """
    Get the product price from the product locator.
    """

    try:
        price = await product.locator("span.a-price-whole").first.text_content(
            timeout=3000
        )

        if price is None:
            return None

        price = price.replace(",", "").strip()
        price = float(price)
        return price
    except Exception:
        logger.exception("Error occurred while fetching product price")
        return None


async def get_product_rating(product: Locator):
    """
    Get the product rating from the product locator.
    """

    try:
        rating_locator = product.locator("[data-cy='reviews-block'] a")
        rating_text = await rating_locator.first.get_attribute(
            "aria-label", timeout=3000
        )
        rating = rating_text.split(" ")[0] if rating_text else None
        return rating

    except Exception:
        logger.exception("Error occurred while fetching product rating")
        return None


async def get_product_url(
    product: Locator,
    base_url: str,
):
    """
    Get the product URL from the product locator.
    """

    try:
        link_locator = product.locator("[data-cy='title-recipe'] a[target='_blank']")
        product_url = await link_locator.first.get_attribute("href", timeout=3000)

        if not product_url:
            return None

        return (
            product_url
            if product_url and not product_url.startswith("/")
            else base_url + product_url
        )
    except Exception:
        logger.exception("Error occurred while fetching product URL")
        return None


async def get_product_image(product: Locator):
    """
    Get the product image URL from the product locator.
    """

    try:
        image_locator = product.locator("img.s-image")
        image_src = await image_locator.first.get_attribute("src", timeout=3000)
        return image_src
    except Exception:
        logger.exception("Error occurred while fetching product image")
        return None


async def extract_amazon_product(
    product: Locator,
    base_url: str,
) -> dict:
    """
    Extract product information from an Amazon product locator.
    Returns a dictionary containing product details.
    """

    data = await product.evaluate(
        """
        (el) => {
            const title =
                el.querySelector(
                    "[data-cy='title-recipe'] h2 span, h2 span"
                )?.textContent?.trim() || null;

            const priceText =
                el.querySelector(
                    "span.a-price-whole"
                )?.textContent?.trim() || null;

            const ratingText =
                el.querySelector(
                    "[data-cy='reviews-block'] a"
                )?.getAttribute("aria-label") || null;

            const href =
                el.querySelector(
                    "[data-cy='title-recipe'] a[target='_blank']"
                )?.getAttribute("href") || null;

            const image =
                el.querySelector(
                    "img.s-image"
                )?.getAttribute("src") || null;

            return {
                title,
                priceText,
                ratingText,
                href,
                image
            };
        }
        """
    )

    price = None

    if data["priceText"]:
        try:
            price = float(data["priceText"].replace(",", "").strip())
        except ValueError:
            pass

    rating = None

    if data["ratingText"]:
        try:
            rating = data["ratingText"].split()[0]
        except (IndexError, AttributeError):
            pass

    product_url = data["href"]

    if product_url and product_url.startswith("/"):
        product_url = base_url + product_url

    return {
        "type": "product",
        "name": data["title"],
        "price": price,
        "rating": rating,
        "product_url": product_url,
        "image_src": data["image"],
        "platform": "amazon",
    }
