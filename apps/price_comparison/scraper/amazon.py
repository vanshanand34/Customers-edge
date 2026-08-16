import json

from playwright.async_api import async_playwright

from .utils import (
    convert_str_to_url,
    create_browser_context,
)


async def scrape_amazon(search_text: str):

    if not search_text:
        return

    base_url = "https://www.amazon.in"

    search_text = convert_str_to_url(search_text)

    search_url = f"{base_url}/s?k={search_text}&ref=nb_sb_noss"

    print("Amazon URL:", search_url)

    exception_count = 0
    exceptions = []

    try:
        async with async_playwright() as p:
            browser = await p.chromium.launch(headless=True)

            context = await create_browser_context(browser)

            page = await context.new_page()
            linkToProductDataMap = {}

            try:
                await page.goto(
                    search_url,
                    wait_until="domcontentloaded",
                    timeout=30000,
                )

                try:
                    await page.wait_for_selector(
                        "div[data-component-type='s-search-result']",
                        timeout=15000,
                    )
                except Exception:
                    print("Amazon product selector was not found.")

                products = page.locator("div[data-component-type='s-search-result']")

                product_count = await products.count()

                print("Amazon products found:", product_count)

                for index in range(product_count):
                    try:
                        product = products.nth(index)

                        # ------------------------------------------
                        # NAME
                        # ------------------------------------------

                        name = None

                        name_locator = product.locator(
                            "[data-cy='title-recipe'] h2 span"
                        )

                        if await name_locator.count() > 0:
                            name = await name_locator.last.text_content(timeout=3000)

                        # Fallback
                        if not name:
                            name_locator = product.locator("h2 span")

                            if await name_locator.count() > 0:
                                name = await name_locator.last.text_content(
                                    timeout=3000
                                )

                        # ------------------------------------------
                        # PRICE
                        # ------------------------------------------

                        price = None

                        price_locator = product.locator("span.a-price-whole")

                        if await price_locator.count() > 0:
                            price_text = await price_locator.first.text_content(
                                timeout=3000
                            )

                            if price_text:
                                clean_price = price_text.replace(",", "").strip()

                                try:
                                    price = float(clean_price)
                                except ValueError:
                                    price = None

                        # ------------------------------------------
                        # RATING
                        # ------------------------------------------

                        rating = None

                        rating_locator = product.locator("[data-cy='reviews-block'] a")

                        if await rating_locator.count() > 0:
                            rating_text = await rating_locator.first.get_attribute(
                                "aria-label",
                                timeout=3000,
                            )

                            if rating_text:
                                try:
                                    rating = rating_text.split(" ")[0]
                                except Exception:
                                    rating = None

                        # ------------------------------------------
                        # PRODUCT URL
                        # ------------------------------------------

                        product_url = None

                        link_locator = product.locator(
                            "[data-cy='title-recipe'] a[target='_blank']"
                        )

                        if await link_locator.count() > 0:
                            product_url = await link_locator.first.get_attribute(
                                "href",
                                timeout=3000,
                            )

                        if product_url and product_url.startswith("/"):
                            product_url = base_url + product_url

                        # ------------------------------------------
                        # IMAGE
                        # ------------------------------------------

                        image_src = None

                        image_locator = product.locator("img.s-image")

                        if await image_locator.count() > 0:
                            image_src = await image_locator.first.get_attribute(
                                "src",
                                timeout=3000,
                            )

                        # ------------------------------------------
                        # PRODUCT DATA
                        # ------------------------------------------

                        curr_prod_data = {
                            "type": "product",
                            "name": (name.strip() if name else None),
                            "price": price,
                            "rating": rating,
                            "product_url": product_url,
                            "image_src": image_src,
                            "platform": "amazon",
                        }

                        print("Amazon product:", curr_prod_data)

                        # ------------------------------------------
                        # SEND DIRECTLY TO FRONTEND
                        # ------------------------------------------

                        if product_url in linkToProductDataMap:
                            print("Duplicate product:", curr_prod_data)
                            continue

                        linkToProductDataMap[product_url] = curr_prod_data
                        yield curr_prod_data

                    except Exception as error:
                        exception_count += 1

                        exceptions.append(f"Amazon product {index}: {error}")

            finally:
                await browser.close()

    except Exception as error:
        print("Amazon scraper error:", error)

        yield (
            json.dumps(
                {
                    "type": "error",
                    "platform": "amazon",
                    "message": str(error),
                }
            )
        )

    print("Amazon exception count:", exception_count)

    if exceptions:
        print("\n".join(exceptions))
