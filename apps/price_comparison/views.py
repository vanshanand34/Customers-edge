from django.shortcuts import render
from django.views.generic.base import View
from django.contrib import messages

from scripts.amazon import amazon
from scripts.flipkart import flipkart

from scripts.temp import get_temp_data

import logging
# Create your views here.


class HomeView(View):
    def get(self, request, *args, **kwargs):
        return render(request, "home.html")

    def post(self, request, *args, **kwargs):
        search_text = request.POST.get("search_text")
        if not search_text:
            messages.error(request, "Please enter a search text")
            return render(request, "home.html")
        print(search_text)

        # search_results = get_temp_data()

        try:
            amazon_data = amazon(search_text)
            flipkart_data = flipkart(search_text)
            search_results = [*amazon_data, *flipkart_data]

        except Exception as e:
            logging.exception(e)
            search_results = []

        search_results = [item for item in search_results if None not in search_results]
        for item in search_results:
            item["price"] = float(item.get("price", 0).replace(",", ""))
            item["rating"] = float(item.get("rating", 0))

        return render(
            request,
            "search-results.html",
            {"data": search_results, "search_text": search_text},
        )
