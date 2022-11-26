from django.urls import path
from .views import FacebookScraper, InstagramScraper, TiktokScraper

urlpatterns = {
    path('facebook/', FacebookScraper.as_view(), name=''),
    path('instagram/', InstagramScraper.as_view(), name=''),
    path('tiktok/', TiktokScraper.as_view(), name='')
}
