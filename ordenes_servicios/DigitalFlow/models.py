from django.db import models

class Orden(models.Model):
    identificador = models.CharField(max_length=1)
    empresa = models.CharField(max_length=255)
    responsable = models.CharField(max_length=255)
    problematica = models.TextField()
    servicios_realizados = models.TextField()
    fecha = models.DateField()
    hora_inicio = models.TimeField()
    hora_termino = models.TimeField()
    nivel_satisfaccion = models.IntegerField(
        choices=[(1, 'Malo'), (2, 'Regular'), (3, 'Bueno'), (4, 'Excelente')]
    )
    problema_solucionado = models.BooleanField()
    nombre_encargado = models.CharField(max_length=255)
    nombre_cliente = models.CharField(max_length=255)
    telefono_cliente = models.CharField(max_length=10)
    foto_inicio = models.ImageField(upload_to='uploads/', null=True, blank=True)
    foto_fin = models.ImageField(upload_to='uploads/', null=True, blank=True)

    def __str__(self):
        return f'Orden {self.id}'
