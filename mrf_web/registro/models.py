from django.db import models

class Registro(models.Model):
    nombre = models.CharField(max_length=100)
    correo = models.EmailField()
    telefono = models.CharField(max_length=20, blank=True)

    def __str__(self):
        return self.nombre
