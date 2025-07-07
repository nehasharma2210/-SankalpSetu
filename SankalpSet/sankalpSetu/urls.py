"""
URL configuration for sankalpSetu project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from  sankalpSetu import views

from rest_framework.routers import DefaultRouter
from ideas.views import IdeaViewSet, FeedbackViewSet
from schemes.views import SchemeViewSet
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

router = DefaultRouter()
router.register('ideas', IdeaViewSet)
router.register('feedback', FeedbackViewSet)
router.register('schemes', SchemeViewSet)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.home, name='home'),
    path('api/', include(router.urls)),
    path('api/token/', TokenObtainPairView.as_view()),
    path('api/token/refresh/', TokenRefreshView.as_view()),
    path('api/register/', views.register_user, name='register'),
    path('api/register', views.register_user, name='register_no_slash'),
    path('api/login/', views.login_user, name='login'),
    path('api/login', views.login_user, name='login_no_slash'),
]
