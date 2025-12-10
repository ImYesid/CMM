from django.urls import path
from . import views

urlpatterns = [
    path('', views.orden_trabajo , name='orden_trabajo'),
    path('agregar', views.agregar_orden_trabajo , name='agregar_orden_trabajo'),
    path('editar/<int:id_OT>/', views.editar_orden_trabajo , name='editar_orden_trabajo'),
    path('<int:notificacion_id>/', views.marcar_notificacion_leida, name='marcar_notificacion_leida'),
    path('leidas/', views.marcar_todas_leidas, name='marcar_todas_leidas'),
]
