"""
Utility functions for the price comparison scraper.
"""


def convert_str_to_url(text: str):
    """
    Convert a string to a URL-friendly format.
    """

    text = "+".join(text.split(" "))
    return text.replace(" ", "%20")


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


async def create_browser_context(browser):
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
