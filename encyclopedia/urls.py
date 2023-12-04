from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("wiki/<str:title>/edit", views.edit_page, name="edit_page"),
    path('new/', views.new_page, name='new_page'),
    path('search/', views.search_results, name='search_results'),
    path("wiki/", views.entry_page, name="entry_page"),
    path("wiki/<str:title>", views.entry_page, name="entry_page"),
]
