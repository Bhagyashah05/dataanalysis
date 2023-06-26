# users/urls.py

from django.urls import path
from . import views

urlpatterns = [
    path('', views.rel_form, name='rel_form'),
    path('rel_value/', views.rel_value, name='rel_value'),
    # Other URL patterns in your application
]
