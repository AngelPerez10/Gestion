# DigitalFlow/urls.py

from django.urls import path
from . import views

app_name = 'DigitalFlow'

from django.urls import path
from . import views

urlpatterns = [
    path("", views.listado_ordenes, name="listado_ordenes"),
    path("editar/<int:pk>/", views.editar_orden, name="editar_orden"),
    path("crear/", views.crear_orden, name="crear_orden"),
    path("eliminar/<int:pk>/", views.eliminar_orden, name="eliminar_orden"),
]
