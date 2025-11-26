# historiales/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('Historial', views.trazabilidad_historial, name='historial'),
]