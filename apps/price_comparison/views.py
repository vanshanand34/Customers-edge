from django.contrib import messages
from django.shortcuts import render
from django.views.generic.base import View

from apps.price_comparison.utils import SearchHistoryHelper


class HomeView(View):
    def get(self, request, *args, **kwargs):
        return render(
            request,
            "home.html",
            {
                "search_history_list": SearchHistoryHelper.get_search_history(
                    request.session
                )
            },
        )


class SearchView(View):
    def get(self, request, *args, **kwargs):
        search_text = request.GET.get("search-text")
        if not search_text:
            messages.error(request, "Please enter a search text")
            return render(request, "home.html")

        print(search_text)

        # Store the search text in the session
        SearchHistoryHelper.add_search_history(request.session, search_text)

        return render(
            request,
            "search-results.html",
            {"data": [], "search_text": search_text},
        )


class AboutView(View):
    def get(self, request, *args, **kwargs):
        return render(request, "about.html")
