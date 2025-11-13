from django.urls import path
from . import views

urlpatterns = [
    path('', views.OrdenListView.as_view(), name='ordenes_list'),
    path('<int:pk>/', views.OrdenDetailView.as_view(), name='ordenes_detail'),
    path('crear/', views.OrdenCreateView.as_view(), name='ordenes_create'),
    path('<int:pk>/cerrar/', views.OrdenCerrarView.as_view(), name='ordenes_cerrar'),
]
