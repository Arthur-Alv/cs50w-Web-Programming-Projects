from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("wiki/<str:title>", views.result, name="result"),
    path("search/", views.search, name="search"),
    path("new/", views.newPage, name="newPage")
]
