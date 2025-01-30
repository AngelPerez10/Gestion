# DigitalFlow/urls.py

from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

app_name = 'DigitalFlow'

urlpatterns = [

    path('', views.login_view, name='login'),

    path('login/', views.login_view, name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('register/', views.registrar_usuario, name='register'),
    # Rutas protegidas que requieren inicio de sesión
    path('listado_ordenes/', views.listado_ordenes, name='listado_ordenes'),
    path('crear/', views.crear_orden, name='crear_orden'),
    path('editar/<int:pk>/', views.editar_orden, name='editar_orden'),
    path('eliminar/<int:pk>/', views.eliminar_orden, name='eliminar_orden'),
    path('from_user/', views.from_user, name='from_user'),
    path('vista_pdf/<int:pk>/', views.vista_pdf, name='vista_pdf'),

    path("enviar_pdf/", views.enviar_pdf, name="enviar_pdf"),

]
