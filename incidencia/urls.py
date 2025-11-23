from django.urls import path
from . import views

urlpatterns = [
    path('Incidencia', views.incidencia, name='incidencia'),
]
