# planes/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('<str:tab_id>/', views.plan_gestion, name='plan_gestion'),
    path('agregar/<str:tipo>/', views.agregar_plan_tipo, name='agregar_plan_tipo'),
    path('editar/<int:plan_id>/', views.editar_plan_tipo, name='editar_plan_tipo'),
]
