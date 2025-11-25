from django.urls import path
from . import views

urlpatterns = [
    path('incidencias/', views.incidencias, name='incidencias'),
    path('incidencia/agregar', views.agregar_incidencia , name='agregar_incidencia'),
    path('incidencia/editar/<int:id_in>/', views.editar_incidencia , name='editar_incidencia'),
]
