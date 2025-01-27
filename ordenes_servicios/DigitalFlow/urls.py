# DigitalFlow/urls.py

from django.urls import path
from . import views

app_name = 'DigitalFlow'

urlpatterns = [
    path('', views.listado_ordenes, name='listado_ordenes'),
    path('crear/', views.crear_orden, name='crear_orden'),
    path('editar/<int:pk>/', views.editar_orden, name='editar_orden'),
    path('eliminar/<int:pk>/', views.eliminar_orden, name='eliminar_orden'),
    path('from_user/', views.from_user, name='from_user'),
    path('vista_pdf/<int:pk>/', views.vista_pdf, name='vista_pdf'),
]