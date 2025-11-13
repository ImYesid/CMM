# planes/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('', views.PlanListView.as_view(), name='planes_list'),
    path('<int:pk>/', views.PlanDetailView.as_view(), name='planes_detail'),
    path('crear/', views.PlanCreateView.as_view(), name='planes_create'),
]
