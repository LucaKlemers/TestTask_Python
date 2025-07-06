from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path('statistics/', views.statistics, name="statistics"),
    path('add_quote/', views.add_quote, name="add_quote"),
    path('<int:source_id>/source_info/', views.source_info, name="source_info"),
    path('add_source/', views.add_source, name="add_source"),
]