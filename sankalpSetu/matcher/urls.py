from django.urls import path
from .views import ngo_matcher_view, ngo_matcher_api
urlpatterns = [
    path('api/', ngo_matcher_api, name='matcher-api'),
]