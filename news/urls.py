from django.urls import path
from .views import home_view, NewsView, MainPage, CreateNews

urlpatterns = [
    path("", home_view),
    path("news/", MainPage.as_view()),
    path("news/<int:news_id>/", NewsView.as_view()),
    path("news/create/", CreateNews.as_view()),
]
