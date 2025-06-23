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
    path('resumen-provincial/', views.resumen_provincial, name='resumen_provincial'),
    path('formulario-miembros/', views.formulario_miembros, name='formulario_miembros'),
    path('formulario-direccion-municipal/', views.formulario_direccion_municipal, name='formulario_direccion_municipal'),
    path('logout/', auth_views.LogoutView.as_view(next_page='admin_login'), name='logout'),
    path('eliminar-cargo-municipal/<int:id>/', views.eliminar_cargo_municipal, name='eliminar_cargo_municipal'),
    path('eliminar-miembro/<int:miembro_id>/', views.eliminar_miembro, name='eliminar_miembro'),


]
