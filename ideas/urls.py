from django.urls import path
from rest_framework.routers import DefaultRouter
from .views import IdeaViewSet, get_user_ideas

router = DefaultRouter()
router.register(r'', IdeaViewSet, basename='idea')  # or 'ideas' depending on structure

urlpatterns = [
    path('user/<int:user_id>', get_user_ideas, name='get_user_ideas'),
]

urlpatterns += router.urls
