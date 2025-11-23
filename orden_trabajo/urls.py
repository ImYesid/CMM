from django.urls import path
from . import views

urlpatterns = [
    path('Orden_trabajo/', views.orden_trabajo , name='orden_trabajo'),
    path('Orden_trabajo/agregar', views.agregar_orden_trabajo , name='agregar_orden_trabajo'),
    path('Orden_trabajo/editar/<int:id_OT>/', views.editar_orden_trabajo , name='editar_orden_trabajo'),
]
