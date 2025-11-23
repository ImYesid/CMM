from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import *


@login_required(login_url = 'login')
def plan_gestion(request):
    plan_gestion     = PlanGestion.objects.all()

    return render(request, 'plan_gestion/plan_gestion.html', {'plan_gestion' : plan_gestion} )