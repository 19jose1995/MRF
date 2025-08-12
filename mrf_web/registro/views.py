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
            mensaje = "Gracias por registrarte!"
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
            error = 'Credenciales invalidas o usuario no autorizado.'

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
    editar_id = request.GET.get('editar_id') or request.POST.get('editar_id')
    instancia = None

    if request.method == 'POST':
        if editar_id and editar_id.isdigit():
            instancia = get_object_or_404(CargoMunicipal, id=int(editar_id))
            form = CargoMunicipalForm(request.POST, instance=instancia)
        else:
            form = CargoMunicipalForm(request.POST)

        if form.is_valid():
            cargo = form.save(commit=False)
            if not instancia:
                cargo.creado_por = request.user
            cargo.save()
            return redirect('formulario_direccion_municipal')
    else:
        if editar_id and editar_id.isdigit():
            instancia = get_object_or_404(CargoMunicipal, id=int(editar_id))
            form = CargoMunicipalForm(instance=instancia)
        else:
            form = CargoMunicipalForm()

    registros = CargoMunicipal.objects.order_by('provincia', 'municipio', 'orden')
    return render(request, 'formulario_direccion_municipal.html', {
        'form': form,
        'registros': registros,
        'editar_id': editar_id,
    })


# --- FORMULARIO PROVINCIAL ---
@login_required
def formulario_direccion_provincial(request):
    editar_id = request.GET.get('editar_id') or request.POST.get('editar_id')
    instancia = None

    if request.method == 'POST':
        if editar_id and editar_id.isdigit():
            instancia = get_object_or_404(CargoProvincial, id=int(editar_id))
            form = CargoProvincialForm(request.POST, instance=instancia)
        else:
            form = CargoProvincialForm(request.POST)
        
        if form.is_valid():
            cargo = form.save(commit=False)
            if not instancia:
                cargo.creado_por = request.user
            cargo.save()
            return redirect('formulario_direccion_provincial')
    else:
        if editar_id and editar_id.isdigit():
            instancia = get_object_or_404(CargoProvincial, id=int(editar_id))
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
    editar_id = request.GET.get('editar_id') or request.POST.get('editar_id')
    cargo_a_editar = None

    if request.method == 'POST':
        # Si editar_id es un número válido, se busca la instancia a editar
        if editar_id and editar_id.isdigit():
            cargo_a_editar = get_object_or_404(CargoNacional, id=int(editar_id))
            form = CargoNacionalForm(request.POST, instance=cargo_a_editar)
        else:
            form = CargoNacionalForm(request.POST)

        if form.is_valid():
            cargo = form.save(commit=False)
            cargo.creado_por = request.user
            cargo.save()
            return redirect('formulario_direccion_nacional')
    else:
        if editar_id and editar_id.isdigit():
            cargo_a_editar = get_object_or_404(CargoNacional, id=int(editar_id))
            form = CargoNacionalForm(instance=cargo_a_editar)
        else:
            form = CargoNacionalForm()

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

from django.contrib.auth.decorators import login_required
from django.shortcuts import render

from .models import Miembro, CargoMunicipal, CargoProvincial, CargoNacional


@login_required
def reporte_general_por_usuario(request):
    # tipo: miembros | municipales | provinciales | nacionales
    tipo = request.GET.get('tipo', 'miembros')
    tipos_validos = {'miembros', 'municipales', 'provinciales', 'nacionales'}
    if tipo not in tipos_validos:
        tipo = 'miembros'

    # origen: todos | web (creado_por IS NULL) | usuarios (creado_por IS NOT NULL)
    origen = request.GET.get('origen', 'todos')
    if origen not in {'todos', 'web', 'usuarios'}:
        origen = 'todos'

    # Totales para las tarjetas (generales)
    totales = {
        'miembros': Miembro.objects.count(),
        'municipales': CargoMunicipal.objects.count(),
        'provinciales': CargoProvincial.objects.count(),
        'nacionales': CargoNacional.objects.count(),
    }
    totales['general'] = sum(totales.values())

    # Subtotales "Web" (sin usuario) para ayudar a identificar volumen
    totales_web = {
        'miembros': Miembro.objects.filter(creado_por__isnull=True).count(),
        'municipales': CargoMunicipal.objects.filter(creado_por__isnull=True).count(),
        'provinciales': CargoProvincial.objects.filter(creado_por__isnull=True).count(),
        'nacionales': CargoNacional.objects.filter(creado_por__isnull=True).count(),
    }

    # Queryset plano por tipo, con select_related a creado_por
    if tipo == 'miembros':
        qs = Miembro.objects.select_related('creado_por').order_by('-id')
    elif tipo == 'municipales':
        qs = CargoMunicipal.objects.select_related('creado_por').order_by('-id')
    elif tipo == 'provinciales':
        qs = CargoProvincial.objects.select_related('creado_por').order_by('-id')
    else:  # 'nacionales'
        qs = CargoNacional.objects.select_related('creado_por').order_by('-id')

    # Filtro por origen
    if origen == 'web':
        qs = qs.filter(creado_por__isnull=True)
    elif origen == 'usuarios':
        qs = qs.filter(creado_por__isnull=False)

    titulos = {
        'miembros': 'Miembros',
        'municipales': 'Direccion Municipal',
        'provinciales': 'Direccion Provincial',
        'nacionales': 'Direccion Nacional',
    }

    context = {
        'tipo': tipo,
        'origen': origen,
        'titulo_tipo': titulos[tipo],
        'totales': totales,
        'totales_web': totales_web,
        'records': qs,
        'total_mostrado': qs.count(),
    }
    return render(request, 'reporte_por_usuario.html', context)


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
