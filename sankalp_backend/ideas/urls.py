from django.urls import path
from . import views

app_name = 'ideas'

urlpatterns = [
    path('', views.idea_list, name='idea_list'),
    path('submit/', views.submit_idea, name='submit_idea'),
    path('<int:idea_id>/', views.idea_detail, name='idea_detail'),
]