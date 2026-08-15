from django.shortcuts import render
from django.views.generic.base import View
from django.contrib import messages

# from scripts.temp import get_temp_data

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

        return render(
            request,
            "search-results.html",
            # {"data": search_results, "search_text": search_text},
            {"data": [], "search_text": search_text},
        )

class AboutMeView(View):
    def get(self, request, *args, **kwargs):
        return render(request, "about-me.html")
