from django.shortcuts import render
from django.http import JsonResponse
from .models import Registro
import json

def index(request):
    return render(request, 'index.html')

def api_register(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        Registro.objects.create(
            nombre=data.get('name', ''),
            correo=data.get('email', ''),
            telefono=data.get('phone', '')
        )
        return JsonResponse({'message': 'success'})
    return JsonResponse({'error': 'Método no permitido'}, status=405)
