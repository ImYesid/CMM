from django.urls import path
from . import views

urlpatterns = [
    path('', views.activos, name='activos'),
    path('agregar', views.agregar_activo , name='agregar_activo'),
    path('editar/<int:id_a>/', views.editar_activo , name='editar_activo'),
]
