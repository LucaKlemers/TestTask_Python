from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path('<int:quote_id>/vote/', views.vote, name="vote"),
    path('statistics/', views.statistics, name="statistics"),
    path('add_quote/', views.add_quote, name="add_quote"),
    path('int:source_id/info/', views.source_info, name="source_info"),
    path('add_source/', views.add_source, name="add_source"),
]