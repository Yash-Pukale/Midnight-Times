from django.urls import path
from .views import SearchNewsView, TrendingKeyPhrasesView


urlpatterns = [
    path('news/', SearchNewsView.as_view(), name='news'),
    path('key-phrases/', TrendingKeyPhrasesView.as_view(), name='key-phrases'),
]