from django.contrib import admin
from django.urls import path, include
from . import views
from django.conf.urls.static import static
from django.conf import settings


urlpatterns = [
    path('admin/', admin.site.urls),
    path('home/', views.home, name='home'),
    path('home/data/', views.dashboard_data, name='dashboard_data'),
    path('', include('usuarios.urls')),
    path('activos/', include('activos.urls')),
    path('historiales/', include('historial.urls')),
    path('incidencias/', include('incidencia.urls')),
    path('ordenes/', include('orden_trabajo.urls')),
    path('planes/', include('plan_gestion.urls')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
