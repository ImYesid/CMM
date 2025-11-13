from django.urls import path
from . import views

urlpatterns = [
    path('', views.ActivoListView.as_view(), name='lista_activos'),
    path('<int:pk>/', views.ActivoDetailView.as_view(), name='activos_detail'),
    path('crear/', views.ActivoCreateView.as_view(), name='activos_create'),
    path('<int:pk>/editar/', views.ActivoUpdateView.as_view(), name='activos_update'),
    path('<int:pk>/eliminar/', views.ActivoDeleteView.as_view(), name='activos_delete'),
]
