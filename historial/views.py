from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import *


@login_required(login_url = 'login')
def historial(request):
    historial     = HistorialGestion.objects.all()

    return render(request, 'activos/activos.html', {'historial' : historial} )