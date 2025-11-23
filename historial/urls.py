# historiales/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('Historial', views.historial, name='historial'),
]