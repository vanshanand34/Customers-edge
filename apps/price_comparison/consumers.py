import asyncio
import json
import logging

from channels.db import database_sync_to_async
from channels.generic.websocket import AsyncWebsocketConsumer

from apps.price_comparison.utils import SearchHistoryHelper

from .scraper.amazon import scrape_amazon
from .scraper.browser import browser_manager
from .scraper.flipkart import scrape_flipkart

logger = logging.getLogger(__name__)


class SearchResultsConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.search_text = ""
        await self.accept()

        logger.info("WebSocket connected")

    async def disconnect(self, code):
        logger.info("WebSocket disconnected: %s", code)

    async def receive(self, text_data=None, bytes_data=None):
        if not text_data:
            return

        try:
            text_data_json = json.loads(text_data)

            self.search_text = text_data_json.get(
                "search_text",
                "",
            ).strip()

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
            logger.exception("WebSocket receive error")

            await self.send(
                text_data=json.dumps(
                    {
                        "type": "error",
                        "message": "An unexpected error occurred.",
                    }
                )
            )

    async def send_amazon_results(self, browser, session):
        """
        Scrape Amazon and stream products to the frontend.
        """

        logger.info(
            "Starting Amazon search for: %s",
            self.search_text,
        )

        try:
            async for product in scrape_amazon(
                self.search_text,
                browser,
            ):
                SearchHistoryHelper.update_search_url_if_url_empty(
                    session,
                    self.search_text,
                    product.get("image_src", ""),
                )

                await self.send(text_data=json.dumps(product))

        except Exception:
            logger.exception("Error occurred while scraping Amazon")

    async def send_flipkart_results(self, browser, session):
        """
        Scrape Flipkart and stream products to the frontend.
        """

        logger.info(
            "Starting Flipkart search for: %s",
            self.search_text,
        )

        try:
            async for product in scrape_flipkart(
                self.search_text,
                browser,
            ):
                SearchHistoryHelper.update_search_url_if_url_empty(
                    session,
                    self.search_text,
                    product.get("image_src", ""),
                )

                await self.send(text_data=json.dumps(product))

        except Exception:
            logger.exception("Error occurred while scraping Flipkart")

    async def send_search_results(self):
        """
        Run Amazon and Flipkart concurrently using one shared
        Chromium browser instance.

        Each scraper creates its own isolated BrowserContext.
        """

        logger.info(
            "Starting search for: %s",
            self.search_text,
        )

        session = self.scope.get("session")

        if not session:
            raise RuntimeError("Session is not available in the scope")

        browser = await browser_manager.get_browser()

        # await asyncio.gather(
        #     self.send_flipkart_results(
        #         browser,
        #         session,
        #     ),
        #     self.send_amazon_results(
        #         browser,
        #         session,
        #     ),
        # )

        await self.send_amazon_results(
            browser,
            session
        )

        logger.info("All scraping completed")

        await self.send(
            text_data=json.dumps(
                {
                    "type": "search_complete",
                    "message": "Search completed",
                }
            )
        )

        await database_sync_to_async(session.save)()
