from django.urls import path
from .views import *

# from .views import ShortenURLView, RedirectURLView

urlpatterns = [
    path('shorten/',shorten_url),
    path('<str:short_url>/',resolve_short_url),
]