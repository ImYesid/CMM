from django.urls import path
from django.views.generic import TemplateView
from . import views

urlpatterns = [
    path('', views.login, name='login'),
    path('logout/', views.logout, name='logout'),
    path('profile/', TemplateView.as_view(template_name='usuarios/profile.html'), name='profile'),
    path('forgot_password/', views.forgot_password, name='forgot_password'),
    path('reset_password_validate/<uidb64>/<token>/', views.reset_password_validate, name='reset_password_validate'),
    path('reset_password/', views.reset_password, name='reset_password'),
    path('theme_settings/', views.theme_settings, name='theme_settings'),
    path('update_profile/', views.update_profile, name='update_profile'),
]    