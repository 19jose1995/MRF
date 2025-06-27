from django.contrib import admin
from django.urls import path
from registro import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.index, name='index'),
    path('admin-login/', views.admin_login, name='admin_login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='admin_login'), name='logout'),
    path('panel-admin/', views.panel_admin, name='panel_admin'),
    path('formulario-miembros/', views.formulario_miembros, name='formulario_miembros'),
    path('formulario-direccion-municipal/', views.formulario_direccion_municipal, name='formulario_direccion_municipal'),
    path('formulario-direccion-provincial/', views.formulario_direccion_provincial, name='formulario_direccion_provincial'),   
    path('formulario-miembros/', views.formulario_miembros, name='formulario_miembros'),
    path('formulario-direccion-municipal/', views.formulario_direccion_municipal, name='formulario_direccion_municipal'),
    path('logout/', auth_views.LogoutView.as_view(next_page='admin_login'), name='logout'),
    path('eliminar-cargo-municipal/<int:id>/', views.eliminar_cargo_municipal, name='eliminar_cargo_municipal'),
    path('eliminar-miembro/<int:miembro_id>/', views.eliminar_miembro, name='eliminar_miembro'),
    path('direccion-nacional/', views.formulario_direccion_nacional, name='formulario_direccion_nacional'),
    path('eliminar-cargo-nacional/<int:id>/', views.eliminar_cargo_nacional, name='eliminar_cargo_nacional'),    
    path('eliminar-cargo-provincial/<int:id>/', views.eliminar_cargo_provincial, name='eliminar_cargo_provincial'),
    path('reporte-por-usuario/', views.reporte_general_por_usuario, name='reporte_por_usuario'),
    path('miembros/editar/<int:miembro_id>/', views.editar_miembro, name='editar_miembro'),
    path('direccion-provincial/', views.formulario_direccion_provincial, name='formulario_direccion_provincial'),


]
