import asyncio
import json

from channels.generic.websocket import AsyncWebsocketConsumer

from .scraper.amazon import scrape_amazon
from .scraper.flipkart import scrape_flipkart


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

        async for product in scrape_amazon(self.search_text):
            await self.send(json.dumps(product))

        async for product in scrape_flipkart(self.search_text):
            await self.send(json.dumps(product))

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
