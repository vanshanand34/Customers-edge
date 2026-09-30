from django.contrib import admin
from django.urls import path

from apps.price_comparison import views

urlpatterns = [
    path("admin/", admin.site.urls),
    path("home/", views.HomeView.as_view(), name="home"),
    path("search/", views.SearchView.as_view(), name="search"),
    path("about/", views.AboutView.as_view(), name="about"),
]
