from django.urls import path
from . import views

urlpatterns = [
    path('', views.incidencias, name='incidencias'),
    path('agregar', views.agregar_incidencia , name='agregar_incidencia'),
    path('editar/<int:id_in>/', views.editar_incidencia , name='editar_incidencia'),
]
