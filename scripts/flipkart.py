import requests
from bs4 import BeautifulSoup
from pprint import pprint


def run():
    search_text = "samsung galaxybook 4"
    search_results = flipkart(search_text)
    # search_results = amazon(search_text)
    for prod in search_results:
        pprint(prod)


def flipkart(search_text: str):
    search_text = convert_str_to_url(search_text)

    base_url = "https://www.flipkart.com"
    search_url = (
        base_url
        + "/search?q="
        + search_text
        + "&otracker=search&otracker1=search&marketplace=FLIPKART&as-show=on&as=off"
    )

    r = requests.get(search_url)

    soup = BeautifulSoup(r.content, "html.parser")

    # First find all the product div elements

    product_elements = soup.find_all("div", class_="_75nlfW")

    search_results = []

    for product in product_elements:
        price = product.select("div.Nx9bqj._4b5DiR")
        name = product.select("div.KzDlHZ")
        rating = product.select("div.XQDdHH")
        website_link = product.select("a.CGtC98")
        image = product.select("img.DByuf4")

        search_results.append(
            {
                "name": name[0].text if name else None,
                "price": price[0].text if price else None,
                "rating": rating[0].text if rating else None,
                "product_url": (
                    base_url + "/" + website_link[0].get("href", "")
                    if website_link
                    else None
                ),
                "image_src": image[0].get("src") if image else None,
            }
        )

    return search_results


def convert_str_to_url(text: str):
    text = "+".join(text.split(" "))
    return text.replace(" ", "%20")


