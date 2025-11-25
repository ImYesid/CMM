from django.urls import path
from . import views

urlpatterns = [
    path('activos/', views.activos, name='activos'),
    path('activo/agregar', views.agregar_activo , name='agregar_activo'),
    path('activo/editar/<int:id_a>/', views.editar_activo , name='editar_activo'),
]
