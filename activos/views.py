from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import *
from .models import *


@login_required(login_url = 'login')
def activos(request):
    filtro = request.GET.get('filtro', 'activos') 

    if filtro == 'activos':
        activos = Activo.objects.filter(estado_operativo__in=['operativo', 'mantenimiento'])
    else:
        activos = Activo.objects.all()

    context = {
        'activos': activos,
        'filtro': filtro,
    }
    return render(request, 'activos/activos.html', context)
    
@login_required(login_url='login')
def agregar_activo(request):
    if request.method == 'POST':
        form = ActivoForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Activo agregado correctamente.")
            return redirect('activos')
    else:
        form = ActivoForm()

    context = {
        'form': form, 
        'accion': 'Agregar'
    }
        
    return render(request, 'activos/forms/form_activo.html', context)

@login_required(login_url='login')
def editar_activo(request, id_a):
    a = get_object_or_404(Activo, id=id_a)
    
    if request.method == "POST":
        form = ActivoForm(request.POST, instance=a)
        if form.is_valid():
            form.save()
            messages.success(request, "activo actualizado correctamente.")
            return redirect('activos')
    else:
        form = ActivoForm(instance=a)
    
    return render(request, 'activos/forms/form_activo.html', {'form': form, 'accion': 'Editar'})

