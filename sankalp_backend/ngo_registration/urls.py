from django.urls import path
from . import views

app_name = 'ngo_registration'

urlpatterns = [
    path('', views.registration_form, name='registration_form'),
    path('register/', views.register_ngo, name='register_ngo'),
    path('success/', views.registration_success, name='registration_success'),
    path('list/', views.ngo_list, name='ngo_list'),
]