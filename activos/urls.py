from django.urls import path
from . import views

urlpatterns = [
    path('Activos', views.activos, name='activos'),
]
