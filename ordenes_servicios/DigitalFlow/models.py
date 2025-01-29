# DigitalFlow/models.py
from django.db import models

class Orden(models.Model):
    identificador = models.CharField(max_length=10)
    empresa = models.CharField(max_length=100)
    responsable = models.CharField(max_length=100)
    nivel_satisfaccion = models.IntegerField(choices=[(1, "Malo"), (2, "Regular"), (3, "Bueno"), (4, "Excelente")])
    problematica = models.TextField()
    servicios_realizados = models.TextField()
    fecha_inicio = models.DateField()
    hora_inicio = models.TimeField()
    fecha_finalizacion = models.DateField(null=True, blank=True)
    hora_termino = models.TimeField()
    nombre_encargado = models.CharField(max_length=100)
    telefono_cliente = models.CharField(max_length=15)
    problema_solucionado = models.BooleanField()
    foto_inicio = models.ImageField(upload_to='fotos_iniciales/', null=True, blank=True)
    foto_fin = models.ImageField(upload_to='fotos_finales/', null=True, blank=True)
    pdf_generado = models.FileField(upload_to='pdfs/', null=True, blank=True)

    def __str__(self):
        return f'Orden {self.id}'
