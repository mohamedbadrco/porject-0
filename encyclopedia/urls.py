from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("random", views.random, name="random"),
    path("wiki/add", views.add, name="add"),
    path("wiki/<str:name>", views.view, name="view"),
     path("wiki/<str:name>/edit", views.edit, name="edit")

  ]

