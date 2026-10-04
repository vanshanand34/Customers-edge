import asyncio
import logging

from playwright.async_api import Browser, Playwright, async_playwright

logger = logging.getLogger(__name__)


class BrowserManager:
    """
    Keeps one Playwright/Chromium instance alive for the lifetime
    of the Django/Uvicorn worker.

    Individual searches should create their own BrowserContext.
    """

    def __init__(self):
        self._playwright: Playwright | None = None
        self._browser: Browser | None = None
        self._lock = asyncio.Lock()

    async def get_browser(self) -> Browser:
        """
        Lazily start Playwright + Chromium.

        The lock prevents multiple simultaneous WebSocket searches
        from launching multiple Chromium processes.
        """

        if self._browser and self._browser.is_connected():
            return self._browser

        async with self._lock:
            if self._browser and self._browser.is_connected():
                return self._browser

            logger.info("Starting Playwright Chromium")

            self._playwright = await async_playwright().start()

            self._browser = await self._playwright.chromium.launch(
                headless=True,
                args=[
                    "--disable-gpu",
                    "--disable-dev-shm-usage",
                    "--disable-background-networking",
                    "--disable-background-timer-throttling",
                    "--disable-renderer-backgrounding",
                    "--disable-features=Translate,BackForwardCache",
                    "--no-first-run",
                    "--no-default-browser-check",
                ],
            )

            logger.info("Playwright Chromium started")

            return self._browser

    async def close(self):
        """
        Gracefully close Chromium and Playwright.
        """

        async with self._lock:
            if self._browser:
                try:
                    await self._browser.close()
                except Exception:
                    logger.exception("Error closing Chromium")

                self._browser = None

            if self._playwright:
                try:
                    await self._playwright.stop()
                except Exception:
                    logger.exception("Error stopping Playwright")

                self._playwright = None


browser_manager = BrowserManager()
