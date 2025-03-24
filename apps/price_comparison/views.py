from django.shortcuts import render
from django.views.generic.base import View

from scripts.amazon import amazon
from scripts.flipkart import flipkart

import logging
# Create your views here.


class HomeView(View):
    def get(self, request, *args, **kwargs):
        return render(request, "home.html")

    def post(self, request, *args, **kwargs):
        search_text = request.POST.get("search_text")
        print(search_text)

        try:
            amazon_data = amazon(search_text)
            flipkart_data = flipkart(search_text)
            search_results = [*amazon_data, *flipkart_data]
        except Exception as e:
            logging.exception(e)
            search_results = []

        for item in search_results:
            if item and item.get("product_url") and "amazon" in item.get("product_url"):
                item["platform"] = "amazon"
            else:
                item["platform"] = "flipkart"

        return render(
            request,
            "search-results.html",
            {"data": search_results, "search_text": search_text},
        )
