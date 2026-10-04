from playwright.async_api import Browser, BrowserContext

"""
Utility functions for the price comparison scraper.
"""


def check_if_row_is_empty(prod_data):
    """
    Check if the product data row is empty.
    """

    return (
        not prod_data["name"]
        or not prod_data["price"]
        or not prod_data["product_url"]
        or not prod_data["image_src"]
    )


async def create_browser_context(browser: Browser) -> BrowserContext:
    """
    Creates a new browser context with specific settings.
    """
    return await browser.new_context(
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


async def block_unnecessary_resources(route):
    """
    Block resources that are not required for extracting
    product information.

    Product images from Flipkart are allowed because their
    URLs are returned to the frontend.
    """

    request = route.request
    resource_type = request.resource_type
    url = request.url.lower()

    # We need Flipkart product images because we send their
    # URLs back to the frontend.
    if resource_type == "image" and "rukmin" in url:
        await route.continue_()
        return

    # We don't need any other images.
    if resource_type == "image":
        await route.abort()
        return

    if resource_type in {
        "font",
        "media",
    }:
        await route.abort()
        return

    await route.continue_()
