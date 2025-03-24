from pprint import pprint

from selenium import webdriver
from selenium.webdriver.common.by import By

from scripts.flipkart import convert_str_to_url

base_url = "https://www.amazon.in"


def run():
    # search_text = "shirts for men"
    search_text = "samsung galaxy book 4"
    for item in amazon(search_text):
        pprint(item)


def amazon(search_text: str):
    search_text = convert_str_to_url(search_text)

    search_url = base_url + "/s?k=" + search_text + "&ref=nb_sb_noss"

    print(search_url)

    options = webdriver.ChromeOptions()
    options.add_argument("--headless")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    driver = webdriver.Chrome(options=options)

    driver.get(search_url)

    product_elements = driver.find_elements(
        By.XPATH, "//div[@data-component-type='s-search-result']"
    )

    search_results = []

    exception_count = 0
    exceptions_body = ""

    for product in product_elements:
        try:

            price = product.find_element(By.CSS_SELECTOR, "span.a-price-whole").text

            name = product.find_element(
                By.XPATH, ".//div[@data-cy='title-recipe']//h2//span"
            ).text

            rating = product.find_element(
                By.XPATH, ".//div[@data-cy='reviews-block']//a"
            ).get_attribute("aria-label")

            website_link = product.find_element(
                By.XPATH, ".//span[@data-component-type='s-product-image']//a"
            ).get_attribute("href")

            image = product.find_element(
                By.CSS_SELECTOR, "img.s-image"
            ).get_attribute("src")

            search_results.append(
                {
                    "name": name if name else None,
                    "price": price if price else None,
                    "rating": clean_rating(rating) if rating else None,
                    "product_url": website_link if website_link else None,
                    "image_src": image if image else None,
                    "platform": "amazon"
                }
            )
        except Exception as err:
            exception_count += 1
            exceptions_body += str(err)
            exceptions_body += "\n"

    print(exception_count)
    print(exceptions_body)

    return search_results


def clean_rating(rating_text: str) -> str:
    """
    convert rating text fetched from website in the form 
    `3.9 out of 5 stars, rating details` into `3.9`
    """

    return rating_text.split(" ")[0]
