from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('api/register', views.api_register, name='api_register'),
    path('panel-admin/', views.panel_admin, name='panel_admin'),
    path('formulario-miembros/', views.formulario_miembros, name='formulario_miembros'),

]
