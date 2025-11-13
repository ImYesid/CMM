# historiales/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('', views.HistorialListView.as_view(), name='historial_list'),
    path('<int:pk>/', views.HistorialDetailView.as_view(), name='historial_detail'),
    path('crear/', views.HistorialCreateView.as_view(), name='historial_create'),
]