from django import forms
from .models import CargoProvincial

class CargoProvincialForm(forms.ModelForm):
    class Meta:
        model = CargoProvincial
        fields = ['provincia','orden', 'nombre', 'cedula', 'telefono', 'email', 'oficio']

from django import forms
from .models import Miembro

class MiembroForm(forms.ModelForm):
    class Meta:
        model = Miembro
        fields = ['nombre', 'cedula', 'telefono', 'sector', 'colegio', 'email', 'oficio']

from django import forms
from .models import CargoMunicipal

class CargoMunicipalForm(forms.ModelForm):
    class Meta:
        model = CargoMunicipal
        fields = ['provincia', 'municipio', 'orden', 'nombre', 'cedula', 'telefono', 'email', 'oficio']
from django import forms
from .models import CargoNacional

class CargoNacionalForm(forms.ModelForm):
    class Meta:
        model = CargoNacional
        fields = ['orden', 'nombre', 'cedula', 'telefono', 'email', 'oficio']
        widgets = {
            'orden': forms.Select(attrs={'class': 'form-control'}),
            'nombre': forms.TextInput(attrs={'class': 'form-control'}),
            'cedula': forms.TextInput(attrs={'class': 'form-control'}),
            'telefono': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'oficio': forms.TextInput(attrs={'class': 'form-control'}),
        }
