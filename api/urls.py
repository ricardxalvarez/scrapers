from django.urls import path
from .views import FacebookScraper

urlpatterns={
    path('facebook/', FacebookScraper.as_view(), name='')
}