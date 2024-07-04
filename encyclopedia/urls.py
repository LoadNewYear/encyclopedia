from django.urls import path
from django.views.generic.base import RedirectView

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("wiki/<str:TITLE>", views.displayPage, name="displayPage"),
    path("new", views.new, name="new"),
    path("search", views.search, name="search"),
    path("randomPage", views.randomPage, name="randomPage"),
]
