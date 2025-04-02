from django.urls import re_path

from apps.price_comparison import consumers

websocket_urlpatterns = [
    re_path(r"ws/search-results/$", consumers.SearchResultsConsumer.as_asgi()),
]