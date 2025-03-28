import requests
from bs4 import BeautifulSoup
from pprint import pprint

from selenium import webdriver
from selenium.webdriver.common.by import By


def run():
    search_text = "samsung galaxy book 4"

    search_results = flipkart(search_text)
    for prod in search_results:
        pprint(prod)


def convert_str_to_url(text: str):
    text = "+".join(text.split(" "))
    return text.replace(" ", "%20")


def flipkart(search_text: str):
    base_url = "https://www.flipkart.com"
    search_url = (
        base_url
        + "/search?q="
        + search_text
        + "&otracker=search&otracker1=search&marketplace=FLIPKART&as-show=on&as=off"
    )

    print(search_url)

    options = webdriver.ChromeOptions()
    options.add_argument("--headless")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    driver = webdriver.Chrome(options=options)

    driver.get(search_url)

    product_elements = driver.find_elements(By.CLASS_NAME, "_75nlfW")

    search_results = []

    exception_count = 0
    exceptions_body = ""

    for product in product_elements:
        try:
            product = product.find_element(By.XPATH, ".//div[@data-tkid]")

            try:
                name = product.find_element(By.XPATH, ".//a[@title]").get_attribute(
                    "title"
                )
            except Exception as e:
                name = product.find_element(By.CSS_SELECTOR, "img").get_attribute("alt")

            price = product.find_element(By.CSS_SELECTOR, "div.Nx9bqj").text

            try:
                rating = float(
                    product.find_element(By.XPATH, ".//div[@class='XQDdHH']").text
                )
            except Exception as e:
                rating = 0.0

            website_link = product.find_element(By.TAG_NAME, "a").get_attribute("href")

            image = product.find_element(By.CSS_SELECTOR, "img").get_attribute("src")

            search_results.append(
                {
                    "name": name if name else None,
                    "price": price.replace("₹", "") if price else None,
                    "rating": rating,
                    "product_url": website_link if website_link else None,
                    "image_src": image if image else None,
                    "platform": "flipkart",
                }
            )
        except Exception as err:
            exception_count += 1
            exceptions_body += str(err)
            exceptions_body += "\n"

    print(exception_count)
    print(exceptions_body)

    driver.quit()

    return search_results