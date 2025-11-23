from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import *
from .models import *

@login_required(login_url = 'login')
def orden_trabajo(request):
    ot     = OrdenTrabajo.objects.all()

    return render(request, 'orden_trabajo/orden_trabajo.html', {'ot' : ot} )

@login_required(login_url='login')
def agregar_orden_trabajo(request):
    if request.method == 'POST':
        form = OrdenTrabajoForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "OT agregada correctamente.")
            return redirect('orden_trabajo')
    else:
        form = OrdenTrabajoForm()

    context = {
        'form': form, 
        'accion': 'Agregar'
    }
        
    return render(request, 'orden_trabajo/forms/form_orden_trabajo.html', context)

@login_required(login_url='login')
def editar_orden_trabajo(request, id_OT):
    ot = get_object_or_404(OrdenTrabajo, id=id_OT)
    
    if request.method == "POST":
        form = OrdenTrabajoForm(request.POST, instance=ot)
        if form.is_valid():
            form.save()
            messages.success(request, "OT actualizada correctamente.")
            return redirect('orden_trabajo')
    else:
        form = OrdenTrabajoForm(instance=ot)
    
    return render(request, 'orden_trabajo/forms/form_orden_trabajo.html', {'form': form, 'accion': 'Editar'})

