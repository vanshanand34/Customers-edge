import json
import time
from channels.generic.websocket import AsyncWebsocketConsumer, WebsocketConsumer
from scripts.temp import get_temp_data
from pprint import pprint

from selenium import webdriver
from selenium.webdriver.common.by import By

from scripts.flipkart import convert_str_to_url


class SearchResultsConsumer(WebsocketConsumer):
    def connect(self):
        self.search_text = ""
        self.accept()

    def receive(self, text_data=None, bytes_data=None):
        text_data_json = json.loads(text_data)
        search_text = text_data_json.get("search_text")
        print(text_data_json)

        self.search_text = search_text

        # Uncomment below to send temporary data in case of testing
        # self.send_temp_search_results()

        self.send_search_results()

    def send_search_results(self):
        self.send_amazon_data()
        self.send_flipkart_data()

    def send_temp_search_results(self):
        search_results = get_temp_data()
        for item in search_results:
            self.send(json.dumps(item))

    def send_amazon_data(self):
        if not self.search_text:
            return
        base_url = "https://www.amazon.in"
        search_text = convert_str_to_url(self.search_text)

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

                name = product.find_elements(
                    By.XPATH, ".//div[@data-cy='title-recipe']//h2//span"
                )[-1].text

                rating = product.find_element(
                    By.XPATH, ".//div[@data-cy='reviews-block']//a"
                ).get_attribute("aria-label")

                website_link = product.find_element(
                    By.XPATH, ".//span[@data-component-type='s-product-image']//a"
                ).get_attribute("href")

                image = product.find_element(
                    By.CSS_SELECTOR, "img.s-image"
                ).get_attribute("src")

                curr_prod_data = {
                    "name": name if name else None,
                    "price": float(price.replace(",", "")) if price else None,
                    "rating": rating.split(" ")[0] if rating else None,
                    "product_url": website_link if website_link else None,
                    "image_src": image if image else None,
                    "platform": "amazon",
                }

                self.send(json.dumps(curr_prod_data))

                search_results.append(curr_prod_data)
            except Exception as err:
                exception_count += 1
                exceptions_body += str(err)
                exceptions_body += "\n"

        print(exception_count)
        print(exceptions_body)

        driver.quit()

    def send_flipkart_data(self):
        if not self.search_text:
            return

        base_url = "https://www.flipkart.com"
        search_url = (
            base_url
            + "/search?q="
            + self.search_text
            + "&otracker=search&otracker1=search&marketplace=FLIPKART&as-show=on&as=off"
        )

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
                    name = product.find_element(By.CSS_SELECTOR, "img").get_attribute(
                        "alt"
                    )

                price = product.find_element(By.CSS_SELECTOR, "div.Nx9bqj").text

                try:
                    rating = float(
                        product.find_element(By.XPATH, ".//div[@class='XQDdHH']").text
                    )
                except Exception as e:
                    rating = 0.0

                website_link = product.find_element(By.TAG_NAME, "a").get_attribute(
                    "href"
                )

                image = product.find_element(By.CSS_SELECTOR, "img").get_attribute(
                    "src"
                )

                curr_prod_data = {
                    "name": name if name else None,
                    "price": float(price.replace("₹", "").replace(",", ""))
                    if price
                    else None,
                    "rating": rating,
                    "product_url": website_link if website_link else None,
                    "image_src": image if image else None,
                    "platform": "flipkart",
                }

                self.send(json.dumps(curr_prod_data))

                search_results.append(curr_prod_data)
            except Exception as err:
                exception_count += 1
                exceptions_body += str(err)
                exceptions_body += "\n"

        print(exception_count)
        print(exceptions_body)

        driver.quit()
