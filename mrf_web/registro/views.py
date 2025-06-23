from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from .forms import CargoMunicipalForm
from .models import CargoMunicipal


def index(request):
    return render(request, 'index.html')

def admin_login(request):
    if request.user.is_authenticated:
        return redirect('panel_admin')  # Redirige si ya está logueado

    error = None
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None and user.is_staff:
            login(request, user)
            return redirect('panel_admin')
        else:
            error = 'Credenciales inválidas o usuario no autorizado.'

    return render(request, 'admin_login.html', {'error': error})

@login_required
def panel_admin(request):
    return render(request, 'panel_admin.html')

@login_required
def formulario_miembros(request):
    return render(request, 'formulario_miembros.html')

@login_required
def formulario_direccion_municipal(request):
    return render(request, 'formulario_direccion_municipal.html')

from django.shortcuts import render, redirect
from .forms import CargoProvincialForm
from .models import CargoProvincial
from django.contrib.auth.decorators import login_required

@login_required
def formulario_direccion_provincial(request):
    if request.method == 'POST':
        form = CargoProvincialForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('formulario_direccion_provincial')
    else:
        form = CargoProvincialForm()

    registros = CargoProvincial.objects.order_by('orden')
    return render(request, 'formulario_direccion_provincial.html', {
        'form': form,
        'registros': registros
    })

from django.db.models import Count
from django.contrib.auth.decorators import login_required
from .models import CargoProvincial
from django.shortcuts import render

@login_required
def resumen_provincial(request):
    provincias = CargoProvincial.objects.values('provincia') \
        .annotate(total=Count('id')) \
        .order_by('provincia')

    cargos_por_provincia = {}
    for provincia in provincias:
        nombre = provincia['provincia']
        cargos = CargoProvincial.objects.filter(provincia=nombre).order_by('orden')
        cargos_por_provincia[nombre] = cargos

    return render(request, 'resumen_provincial.html', {
        'cargos_por_provincia': cargos_por_provincia
    })

from .models import Miembro
from .forms import MiembroForm

@login_required
def formulario_miembros(request):
    if request.method == 'POST':
        form = MiembroForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('formulario_miembros')
    else:
        form = MiembroForm()

    miembros = Miembro.objects.all().order_by('-id')
    return render(request, 'formulario_miembros.html', {
        'form': form,
        'miembros': miembros
    })

@login_required
def formulario_direccion_municipal(request):
    if request.method == 'POST':
        form = CargoMunicipalForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('formulario_direccion_municipal')
    else:
        form = CargoMunicipalForm()

    registros = CargoMunicipal.objects.order_by('provincia', 'municipio', 'orden')
    return render(request, 'formulario_direccion_municipal.html', {
        'form': form,
        'registros': registros
    })

from .forms import MiembroForm
from django.shortcuts import render, redirect

def index(request):
    form = MiembroForm()
    mensaje = None

    if request.method == 'POST':
        form = MiembroForm(request.POST)
        if form.is_valid():
            form.save()
            mensaje = "¡Gracias por registrarte!"
            form = MiembroForm()  # limpia el formulario

    return render(request, 'index.html', {'form': form, 'mensaje': mensaje})

from django.shortcuts import get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from .models import CargoMunicipal

@login_required
def eliminar_cargo_municipal(request, id):
    cargo = get_object_or_404(CargoMunicipal, id=id)
    if request.method == 'POST':
        cargo.delete()
        return redirect('formulario_direccion_municipal')
    return redirect('formulario_direccion_municipal')

from django.shortcuts import redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Miembro

@login_required
def eliminar_miembro(request, miembro_id):
    if request.method == 'POST':
        miembro = get_object_or_404(Miembro, id=miembro_id)
        miembro.delete()
    return redirect('formulario_miembros')

