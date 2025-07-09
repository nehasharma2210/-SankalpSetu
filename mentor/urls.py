from django.urls import path
from . import views

urlpatterns = [
         path('mentor-chatbot/', views.mentor_chatbot, name='mentor_chatbot'),
     ]