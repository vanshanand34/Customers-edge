from django.contrib import messages
from django.shortcuts import render
from django.views.generic.base import View


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


class AboutView(View):
    def get(self, request, *args, **kwargs):
        return render(request, "about.html")
