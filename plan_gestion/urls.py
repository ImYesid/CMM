# planes/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('plan_gestion', views.plan_gestion, name='plan_gestion'),
]
