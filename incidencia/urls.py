from django.urls import path
from . import views

urlpatterns = [
    path('', views.IncidenciaListView.as_view(), name='incidencias_list'),
    path('<int:pk>/', views.IncidenciaDetailView.as_view(), name='incidencias_detail'),
    path('crear/', views.IncidenciaCreateView.as_view(), name='incidencias_create'),
    path('<int:pk>/estado/', views.IncidenciaEstadoUpdateView.as_view(), name='incidencias_estado_update'),
]
