import json
from urllib.parse import quote_plus

from playwright.async_api import async_playwright

from .utils import (
    check_if_row_is_empty,
    create_browser_context,
)


async def scrape_flipkart(search_text: str):

    if not search_text:
        return

    base_url = "https://www.flipkart.com"

    search_query = quote_plus(search_text)

    search_url = f"{base_url}/search?q={search_query}"

    print("Flipkart URL:", search_url)

    exception_count = 0
    exceptions = []
    linkToProductDataMap = {}

    try:
        async with async_playwright() as p:
            browser = await p.chromium.launch(headless=True)

            context = await create_browser_context(browser)

            page = await context.new_page()

            try:
                await page.goto(
                    search_url,
                    wait_until="domcontentloaded",
                    timeout=30000,
                )

                # ----------------------------------------------
                # CLOSE LOGIN POPUP IF IT APPEARS
                # ----------------------------------------------

                try:
                    close_button = page.locator("button._2KpZ6l")

                    if await close_button.count() > 0:
                        await close_button.first.click(timeout=3000)

                        print("Closed Flipkart login popup")

                except Exception:
                    print("Flipkart login popup not found")
                    pass

                # Give Flipkart time to render products.
                await page.wait_for_timeout(1500)

                # ----------------------------------------------
                # PRODUCT CARDS
                # ----------------------------------------------

                products = page.locator("div._75nlfW")

                product_count = await products.count()

                print("Flipkart products found:", product_count)

                # Fallback if the class has changed.
                if product_count == 0:
                    print(
                        "Flipkart primary selector "
                        "returned no products. "
                        "Trying fallback."
                    )

                    products = page.locator("div:has(a[href*='/p/'])")

                    product_count = await products.count()

                    print("Flipkart fallback products:", product_count)

                for index in range(product_count):
                    try:
                        product = products.nth(index)

                        # --------------------------------------
                        # FIND ACTUAL PRODUCT CARD
                        # --------------------------------------

                        card = product

                        data_tkid = product.locator("[data-tkid]")

                        if await data_tkid.count() > 0:
                            card = data_tkid.first

                        # --------------------------------------
                        # NAME
                        # --------------------------------------

                        name = None

                        # Preferred:
                        # <a title="Product name">
                        name_locator = card.locator("a[title]")

                        if await name_locator.count() > 0:
                            name = await name_locator.first.get_attribute(
                                "title",
                                timeout=3000,
                            )

                        # Fallback: image alt
                        if not name:
                            image_alt_locator = card.locator("img[alt]")

                            if await image_alt_locator.count() > 0:
                                name = await image_alt_locator.first.get_attribute(
                                    "alt",
                                    timeout=3000,
                                )
                            else:
                                name_locator = card.locator("._1psv1zeb9 h1")
                                if await name_locator.count() > 0:
                                    name = await name.first.text_content(timeout=3000)
                                else:
                                    print(
                                        "Flipkart product name not found, skipping..."
                                    )

                        # --------------------------------------
                        # PRICE
                        # --------------------------------------

                        price = None

                        price_locator = card.locator("div.css-g5y9jx").filter(
                            has_text="₹"
                        )

                        if await price_locator.count() == 0:
                            # Fallback
                            print("Flipkart price fallback\n\n")
                            price_locator = card.locator("a").locator("div:text('₹')")

                        if await price_locator.count() > 0:
                            price_text = await price_locator.first.text_content(
                                timeout=3000
                            )

                            if price_text:
                                clean_price = (
                                    price_text.replace("₹", "").replace(",", "").strip()
                                )

                                # Keep only numbers and decimal.
                                price_chars = []

                                for char in clean_price:
                                    if char.isdigit() or char == ".":
                                        price_chars.append(char)

                                clean_price = "".join(price_chars)

                                if clean_price:
                                    try:
                                        print(clean_price + "\n\n")
                                        price = float(clean_price)
                                    except ValueError:
                                        price = None

                        if not price:
                            print("Flipkart price not found, skipping...")
                            continue

                        # --------------------------------------
                        # RATING
                        # --------------------------------------

                        rating = 0.0

                        rating_locator = card.locator("div.XQDdHH")

                        if await rating_locator.count() == 0:
                            rating_locator = card.locator("div:has-text('★')")

                        if await rating_locator.count() > 0:
                            rating_text = await rating_locator.first.text_content(
                                timeout=3000
                            )

                            if rating_text:
                                rating_text = rating_text.replace("★", "").strip()

                                try:
                                    rating = float(rating_text.split()[0])

                                except (
                                    ValueError,
                                    IndexError,
                                ):
                                    rating = 0.0

                        # --------------------------------------
                        # PRODUCT URL
                        # --------------------------------------

                        product_url = None

                        link_locator = card.locator("a[href*='/p/']")

                        if await link_locator.count() > 0:
                            product_url = await link_locator.first.get_attribute(
                                "href",
                                timeout=3000,
                            )

                        # Fallback to any link
                        if not product_url:
                            link_locator = card.locator("a")

                            if await link_locator.count() > 0:
                                product_url = await link_locator.first.get_attribute(
                                    "href",
                                    timeout=3000,
                                )

                        if product_url and product_url.startswith("/"):
                            product_url = base_url + product_url

                        # --------------------------------------
                        # IMAGE
                        # --------------------------------------

                        image_src = None

                        image_locator = card.locator("img")

                        if await image_locator.count() > 0:
                            image_src = await image_locator.first.get_attribute(
                                "src",
                                timeout=3000,
                            )

                            # Lazy-loaded image fallback
                            if not image_src:
                                image_src = await image_locator.first.get_attribute(
                                    "data-src",
                                    timeout=3000,
                                )

                            # srcset fallback
                            if not image_src:
                                image_src = await image_locator.first.get_attribute(
                                    "srcset",
                                    timeout=3000,
                                )

                        # --------------------------------------
                        # IGNORE NON-PRODUCT CARDS
                        # --------------------------------------

                        if not name and not product_url:
                            continue

                        # --------------------------------------
                        # PRODUCT DATA
                        # --------------------------------------

                        curr_prod_data = {
                            "type": "product",
                            "name": (name.strip() if name else None),
                            "price": price,
                            "rating": rating,
                            "product_url": product_url,
                            "image_src": image_src,
                            "platform": "flipkart",
                        }

                        print("Flipkart product:", curr_prod_data)

                        if product_url in linkToProductDataMap:
                            print("Duplicate product:", curr_prod_data)
                            continue

                        linkToProductDataMap[product_url] = curr_prod_data

                        # --------------------------------------
                        # SEND DIRECTLY TO FRONTEND
                        # --------------------------------------

                        if check_if_row_is_empty(curr_prod_data):
                            print("Flipkart product is empty:", curr_prod_data)
                            continue

                        yield curr_prod_data

                    except Exception as error:
                        exception_count += 1

                        exceptions.append(f"Flipkart product {index}: {error}")

            finally:
                await browser.close()

    except Exception as error:
        print("Flipkart scraper error:", error)

        yield json.dumps(
            {
                "type": "error",
                "platform": "flipkart",
                "message": str(error),
            }
        )

    print("Flipkart exception count:", exception_count)

    if exceptions:
        print("\n".join(exceptions))
