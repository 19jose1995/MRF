from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required, user_passes_test
from django.db.models import Count
from .forms import (
    CargoMunicipalForm, CargoProvincialForm, MiembroForm, CargoNacionalForm
)
from .models import (
    CargoMunicipal, CargoProvincial, CargoNacional, Miembro
)
from django.contrib.auth.models import User

# --- VISTAS PÚBLICAS ---
def index(request):
    form = MiembroForm()
    mensaje = None
    if request.method == 'POST':
        form = MiembroForm(request.POST)
        if form.is_valid():
            form.save()
            mensaje = "¡Gracias por registrarte!"
            form = MiembroForm()
    return render(request, 'index.html', {'form': form, 'mensaje': mensaje})

def admin_login(request):
    if request.user.is_authenticated:
        return redirect('panel_admin')

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

# --- PANEL PRINCIPAL ---
@login_required
def panel_admin(request):
    return render(request, 'panel_admin.html')

# --- FORMULARIO MIEMBROS ---
@login_required
def formulario_miembros(request):
    if request.method == 'POST':
        form = MiembroForm(request.POST)
        if form.is_valid():
            miembro = form.save(commit=False)
            miembro.creado_por = request.user
            miembro.save()
            return redirect('formulario_miembros')
    else:
        form = MiembroForm()

    miembros = Miembro.objects.all().order_by('-id')
    return render(request, 'formulario_miembros.html', {
        'form': form,
        'miembros': miembros
    })

# --- FORMULARIO MUNICIPAL ---
@login_required
def formulario_direccion_municipal(request):
    editar_id = request.POST.get('editar_id') or request.GET.get('editar_id')
    if editar_id:
        instancia = get_object_or_404(CargoMunicipal, id=editar_id)
    else:
        instancia = None

    if request.method == 'POST':
        form = CargoMunicipalForm(request.POST, instance=instancia)
        if form.is_valid():
            cargo = form.save(commit=False)
            cargo.creado_por = request.user
            cargo.save()
            return redirect('formulario_direccion_municipal')
    else:
        form = CargoMunicipalForm(instance=instancia)

    registros = CargoMunicipal.objects.order_by('provincia', 'municipio', 'orden')
    return render(request, 'formulario_direccion_municipal.html', {
        'form': form,
        'registros': registros,
        'editar_id': editar_id,
    })

# --- FORMULARIO PROVINCIAL ---
def formulario_direccion_provincial(request):
    editar_id = request.GET.get('editar_id')
    if request.method == 'POST':
        editar_id = request.POST.get('editar_id')
        if editar_id:
            instancia = get_object_or_404(CargoProvincial, id=editar_id)
            form = CargoProvincialForm(request.POST, instance=instancia)
        else:
            form = CargoProvincialForm(request.POST)
        
        if form.is_valid():
            cargo = form.save(commit=False)
            if not editar_id:
                cargo.creado_por = request.user
            cargo.save()
            return redirect('formulario_direccion_provincial')
    else:
        if editar_id:
            instancia = get_object_or_404(CargoProvincial, id=editar_id)
            form = CargoProvincialForm(instance=instancia)
        else:
            form = CargoProvincialForm()

    registros = CargoProvincial.objects.order_by('provincia', 'orden')
    return render(request, 'formulario_direccion_provincial.html', {
        'form': form,
        'registros': registros,
        'editar_id': editar_id,
    })

# --- FORMULARIO NACIONAL ---
@login_required
def formulario_direccion_nacional(request):
    editar_id = request.GET.get('editar_id')
    cargo_a_editar = None

    if editar_id:
        cargo_a_editar = get_object_or_404(CargoNacional, id=editar_id)
        form = CargoNacionalForm(instance=cargo_a_editar)
    else:
        form = CargoNacionalForm()

    if request.method == 'POST':
        if 'editar_id' in request.POST and request.POST['editar_id']:
            cargo_a_editar = get_object_or_404(CargoNacional, id=request.POST['editar_id'])
            form = CargoNacionalForm(request.POST, instance=cargo_a_editar)
        else:
            form = CargoNacionalForm(request.POST)

        if form.is_valid():
            cargo = form.save(commit=False)
            cargo.creado_por = request.user
            cargo.save()
            return redirect('formulario_direccion_nacional')

    registros = CargoNacional.objects.order_by('orden')
    return render(request, 'formulario_direccion_nacional.html', {
        'form': form,
        'registros': registros,
        'editar_id': editar_id
    })

# --- SOLO SUPERUSUARIO PUEDE ELIMINAR ---
@user_passes_test(lambda u: u.is_superuser)
def eliminar_cargo_municipal(request, id):
    cargo = get_object_or_404(CargoMunicipal, id=id)
    if request.method == 'POST':
        cargo.delete()
    return redirect('formulario_direccion_municipal')

@user_passes_test(lambda u: u.is_superuser)
def eliminar_cargo_provincial(request, id):
    cargo = get_object_or_404(CargoProvincial, id=id)
    if request.method == 'POST':
        cargo.delete()
    return redirect('formulario_direccion_provincial')

@user_passes_test(lambda u: u.is_superuser)
def eliminar_cargo_nacional(request, id):
    cargo = get_object_or_404(CargoNacional, id=id)
    if request.method == 'POST':
        cargo.delete()
    return redirect('formulario_direccion_nacional')

@user_passes_test(lambda u: u.is_superuser)
def eliminar_miembro(request, miembro_id):
    miembro = get_object_or_404(Miembro, id=miembro_id)
    if request.method == 'POST':
        miembro.delete()
    return redirect('formulario_miembros')

# --- REPORTE GENERAL POR USUARIO ---
@login_required
def reporte_general_por_usuario(request):
    vista = request.GET.get('vista', 'resumen')
    usuarios = User.objects.all()
    data = []

    for user in usuarios:
        miembros = Miembro.objects.filter(creado_por=user)
        municipales = CargoMunicipal.objects.filter(creado_por=user)
        provinciales = CargoProvincial.objects.filter(creado_por=user)
        nacionales = CargoNacional.objects.filter(creado_por=user)

        if miembros.exists() or municipales.exists() or provinciales.exists() or nacionales.exists():
            data.append({
                'usuario': user,
                'miembros': miembros,
                'municipales': municipales,
                'provinciales': provinciales,
                'nacionales': nacionales,
            })

    return render(request, 'reporte_por_usuario.html', {
        'data': data,
        'vista': vista
    })

@login_required
@user_passes_test(lambda u: u.is_superuser)
def editar_miembro(request, miembro_id):
    miembro = get_object_or_404(Miembro, id=miembro_id)
    if request.method == 'POST':
        form = MiembroForm(request.POST, instance=miembro)
        if form.is_valid():
            form.save()
            return redirect('formulario_miembros')
    else:
        form = MiembroForm(instance=miembro)
    return render(request, 'formulario_miembros.html', {'form': form, 'miembros': Miembro.objects.all(), 'editar': True})
