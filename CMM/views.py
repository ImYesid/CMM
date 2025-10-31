from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required

@login_required(login_url='login')
def home(request):
    return render(request, 'home.html', {'mensaje': 'Bienvenido a la página principal'})