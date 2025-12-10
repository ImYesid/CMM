from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import *
from .models import *

@login_required(login_url = 'login')
def incidencias(request):
    filtro = request.GET.get('filtro', 'activos') 

    if filtro == 'activos':
        incidencias = Incidencia.objects.filter(estado__in=['en_proceso', 'reportada'])
    else:
        incidencias = Incidencia.objects.all()

    context = {
        'incidencias': incidencias,
        'filtro': filtro,
    }
    return render(request, 'incidencia/incidencia.html', context)


@login_required(login_url='login')
def agregar_incidencia(request):
    if request.method == 'POST':
        form = IncidenciaForm(request.POST)
        if request.POST.get("action") == "crear_ot":
            request.session['incidencia_temp'] = {
                'activo': request.POST.get('activo'),
                'descripcion_falla': request.POST.get('descripcion'),
                'usuario': request.POST.get('usuario')
            }
            return redirect('agregar_orden_trabajo')
        
        if form.is_valid():
            incidencia = form.save(commit=False)
            incidencia.usuario = request.user  #asigna automáticamente el usuario autenticado
            incidencia.save()
            messages.success(request, "Incidencia agregada correctamente.")
            return redirect('incidencias')
    else:
        temp = request.session.pop('ot_creada', None)
        if temp: 
            form = IncidenciaForm(initial=temp)
        else:
            form = IncidenciaForm()

    context = {
        'form': form, 
        'accion': 'Agregar'
    }
        
    return render(request, 'incidencia/forms/form_incidencia.html', context)

@login_required(login_url='login')
def editar_incidencia(request, id_in):
    inc = get_object_or_404(Incidencia, id=id_in)
    if request.method == "POST":
        form = IncidenciaForm(request.POST, instance=inc)
        if form.is_valid():
            form.save()
            messages.success(request, "incidencia actualizada correctamente.")
            return redirect('incidencias')
    else:
        form = IncidenciaForm(instance=inc)

    return render(request, 'incidencia/forms/form_incidencia.html', {'form': form, 'accion': 'Editar'})