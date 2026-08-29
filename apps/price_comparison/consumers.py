import asyncio
import json
import sys
from urllib.parse import quote_plus

from channels.generic.websocket import AsyncWebsocketConsumer
from playwright.async_api import async_playwright

from scripts.flipkart import convert_str_to_url
from scripts.temp import get_temp_data


class SearchResultsConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        loop = asyncio.get_running_loop()

        print("================================")
        print("ASYNCIO LOOP:")
        print(type(loop))
        print("================================")

        self.search_text = ""

        await self.accept()

        print("WebSocket connected")

    async def disconnect(self, code):
        print("WebSocket disconnected:", code)

    async def receive(self, text_data=None, bytes_data=None):
        if not text_data:
            return

        try:
            text_data_json = json.loads(text_data)

            print("Received from frontend:", text_data_json)

            self.search_text = text_data_json.get("search_text", "").strip()

            if not self.search_text:
                await self.send(
                    text_data=json.dumps(
                        {
                            "type": "error",
                            "message": "Search text is required",
                        }
                    )
                )
                return

            await self.send_search_results()

        except json.JSONDecodeError:
            await self.send(
                text_data=json.dumps(
                    {
                        "type": "error",
                        "message": "Invalid JSON received",
                    }
                )
            )

        except Exception as error:
            print("Receive error:", error)

            await self.send(
                text_data=json.dumps(
                    {
                        "type": "error",
                        "message": str(error),
                    }
                )
            )

    # ==========================================================
    # SEARCH RESULTS
    # ==========================================================

    async def send_search_results(self):
        """
        Run Amazon and Flipkart concurrently.

        Because both use async Playwright, there is no need
        for threads or queues.
        """

        print("Starting search for:", self.search_text)

        await asyncio.gather(
            self.send_amazon_data_playwright(),
            self.send_flipkart_data_playwright(),
        )

        print("All scraping completed")

        # Optional completion message.
        await self.send(
            text_data=json.dumps(
                {
                    "type": "search_complete",
                    "message": "Search completed",
                }
            )
        )

    # ==========================================================
    # TEMPORARY DATA
    # ==========================================================

    async def send_temp_search_results(self):
        search_results = get_temp_data()

        for item in search_results:
            await self.send(text_data=json.dumps(item))

    # ==========================================================
    # AMAZON
    # ==========================================================

    async def send_amazon_data_playwright(self):
        """
        Scrape Amazon using Playwright's ASYNC API.

        Products are sent directly to the frontend using:

            await self.send(...)

        No thread or queue is required.
        """

        if not self.search_text:
            return

        base_url = "https://www.amazon.in"

        search_text = convert_str_to_url(self.search_text)

        search_url = f"{base_url}/s?k={search_text}&ref=nb_sb_noss"

        print("Amazon URL:", search_url)

        exception_count = 0
        exceptions = []

        try:
            async with async_playwright() as p:
                browser = await p.chromium.launch(headless=True)

                context = await browser.new_context(
                    user_agent=(
                        "Mozilla/5.0 "
                        "(Windows NT 10.0; Win64; x64) "
                        "AppleWebKit/537.36 "
                        "(KHTML, like Gecko) "
                        "Chrome/131.0.0.0 "
                        "Safari/537.36"
                    ),
                    viewport={
                        "width": 1920,
                        "height": 1080,
                    },
                )

                page = await context.new_page()

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

                    products = page.locator(
                        "div[data-component-type='s-search-result']"
                    )

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
                                name = await name_locator.last.text_content(
                                    timeout=3000
                                )

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

                            rating_locator = product.locator(
                                "[data-cy='reviews-block'] a"
                            )

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

                            link_locator = product.locator("h2 a")

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

                            await self.send(text_data=json.dumps(curr_prod_data))

                        except Exception as error:
                            exception_count += 1

                            exceptions.append(f"Amazon product {index}: {error}")

                finally:
                    await browser.close()

        except Exception as error:
            print("Amazon scraper error:", error)

            await self.send(
                text_data=json.dumps(
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

    # ==========================================================
    # FLIPKART
    # ==========================================================

    async def send_flipkart_data_playwright(self):
        """
        Scrape Flipkart using Playwright's ASYNC API.

        Products are sent directly to the frontend using:

            await self.send(...)
        """

        if not self.search_text:
            return

        base_url = "https://www.flipkart.com"

        search_query = quote_plus(self.search_text)

        search_url = f"{base_url}/search?q={search_query}"

        print("Flipkart URL:", search_url)

        exception_count = 0
        exceptions = []

        try:
            async with async_playwright() as p:
                browser = await p.chromium.launch(headless=True)

                context = await browser.new_context(
                    user_agent=(
                        "Mozilla/5.0 "
                        "(Windows NT 10.0; Win64; x64) "
                        "AppleWebKit/537.36 "
                        "(KHTML, like Gecko) "
                        "Chrome/131.0.0.0 "
                        "Safari/537.36"
                    ),
                    viewport={
                        "width": 1920,
                        "height": 1080,
                    },
                )

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

                            # --------------------------------------
                            # PRICE
                            # --------------------------------------

                            price = None

                            price_locator = card.locator("div.v1zwn20").filter(
                                has_text="₹"
                            )

                            if await price_locator.count() == 0:
                                # Fallback
                                print("Flipkart price fallback\n\n")
                                price_locator = card.locator("a").locator(
                                    "div:text('₹')"
                                )

                            if await price_locator.count() > 0:
                                price_text = await price_locator.first.text_content(
                                    timeout=3000
                                )

                                if price_text:
                                    clean_price = (
                                        price_text.replace("₹", "")
                                        .replace(",", "")
                                        .strip()
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
                                    product_url = await (
                                        link_locator.first.get_attribute(
                                            "href",
                                            timeout=3000,
                                        )
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

                            # --------------------------------------
                            # SEND DIRECTLY TO FRONTEND
                            # --------------------------------------

                            await self.send(text_data=json.dumps(curr_prod_data))

                        except Exception as error:
                            exception_count += 1

                            exceptions.append(f"Flipkart product {index}: {error}")

                finally:
                    await browser.close()

        except Exception as error:
            print("Flipkart scraper error:", error)

            await self.send(
                text_data=json.dumps(
                    {
                        "type": "error",
                        "platform": "flipkart",
                        "message": str(error),
                    }
                )
            )

        print("Flipkart exception count:", exception_count)

        if exceptions:
            print("\n".join(exceptions))
