import logging

from django.contrib import messages
from django.shortcuts import redirect, render
from django.views.generic.base import View

from apps.price_comparison.utils import SearchHistoryHelper

logger = logging.getLogger(__name__)


def redirect_to_home(request, exception=None):
    """Redirects all invalid URLs to the home page."""
    return redirect("home")


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

        logger.info("Search text: %s", search_text)

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
