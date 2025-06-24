from django.db import models
from django.contrib.auth.models import User  # necesario para el campo creado_por

# Provincias de RD
PROVINCIAS_RD = [
    ('Azua', 'Azua'),
    ('Bahoruco', 'Bahoruco'),
    ('Barahona', 'Barahona'),
    ('Dajabón', 'Dajabón'),
    ('Distrito Nacional', 'Distrito Nacional'),
    ('Duarte', 'Duarte'),
    ('Elías Piña', 'Elías Piña'),
    ('El Seibo', 'El Seibo'),
    ('Espaillat', 'Espaillat'),
    ('Hato Mayor', 'Hato Mayor'),
    ('Hermanas Mirabal', 'Hermanas Mirabal'),
    ('Independencia', 'Independencia'),
    ('La Altagracia', 'La Altagracia'),
    ('La Romana', 'La Romana'),
    ('La Vega', 'La Vega'),
    ('María Trinidad Sánchez', 'María Trinidad Sánchez'),
    ('Monseñor Nouel', 'Monseñor Nouel'),
    ('Monte Cristi', 'Monte Cristi'),
    ('Monte Plata', 'Monte Plata'),
    ('Pedernales', 'Pedernales'),
    ('Peravia', 'Peravia'),
    ('Puerto Plata', 'Puerto Plata'),
    ('Samaná', 'Samaná'),
    ('Sánchez Ramírez', 'Sánchez Ramírez'),
    ('San Cristóbal', 'San Cristóbal'),
    ('San José de Ocoa', 'San José de Ocoa'),
    ('San Juan', 'San Juan'),
    ('San Pedro de Macorís', 'San Pedro de Macorís'),
    ('Santiago', 'Santiago'),
    ('Santiago Rodríguez', 'Santiago Rodríguez'),
    ('Santo Domingo', 'Santo Domingo'),
    ('Valverde', 'Valverde'),
]

# Modelo Registro
class Registro(models.Model):
    nombre = models.CharField(max_length=100)
    correo = models.EmailField()
    telefono = models.CharField(max_length=20, blank=True)

    def __str__(self):
        return self.nombre

# Modelo Miembro
class Miembro(models.Model):
    nombre = models.CharField(max_length=100)
    cedula = models.CharField(max_length=20)
    telefono = models.CharField(max_length=20)
    sector = models.CharField(max_length=100)
    colegio = models.CharField(max_length=100)
    email = models.EmailField(blank=True)
    oficio = models.CharField(max_length=100, blank=True)

    creado_por = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return self.nombre

# Modelo Cargo Provincial
class CargoProvincial(models.Model):
    provincia = models.CharField(max_length=50, choices=PROVINCIAS_RD)
    orden = models.PositiveSmallIntegerField(choices=[
        (1, "PRESIDENTE PROVINCIAL"),
        (2, "COORDINADOR OPERATIVO Y DE ORGANIZACIÓN"),
        (3, "COORDINADOR DE TECNOLOGIA Y REDES"),
        (4, "COORDINADORA DE LA MUJER"),
        (5, "COORDINADOR DE LA JUVENTUD"),
        (6, "COORDINADOR DE SECTORES PRODUCTIVOS"),
        (7, "COORDINADOR DE DEPORTES"),
        (8, "COORDINADOR DE IGLESIAS Y ORGANIZACIONES SIN FINES DE LUCRO"),
        (9, "COORDINADOR DE TRANSPORTE"),
        (10, "COORDINADOR SECTOR SALUD"),
        (11, "COORDINADOR DE PROFESIONALES INDEPENDIENTES"),
        (12, "COORDINADOR DE ASUNTOS COMUNITARIOS"),
    ], unique=True)
    nombre = models.CharField(max_length=100)
    cedula = models.CharField(max_length=20)
    telefono = models.CharField(max_length=20)
    email = models.EmailField()
    oficio = models.CharField(max_length=100)

    creado_por = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return f"{self.get_orden_display()} - {self.nombre}"

# Modelo Cargo Municipal
class CargoMunicipal(models.Model):
    CARGOS_MUNICIPALES = [
        (1, "PRESIDENTE MUNICIPAL"),
        (2, "COORDINADOR OPERATIVO Y DE ORGANIZACIÓN"),
        (3, "COORDINADOR DE TECNOLOGIA Y REDES"),
        (4, "COORDINADORA DE LA MUJER"),
        (5, "COORDINADOR DE LA JUVENTUD"),
        (6, "COORDINADOR DE SECTORES PRODUCTIVOS"),
        (7, "COORDINADOR DE DEPORTES"),
        (8, "COORDINADOR DE IGLESIAS Y ORGANIZACIONES SIN FINES DE LUCRO"),
        (9, "COORDINADOR DE TRANSPORTE"),
        (10, "COORDINADOR SECTOR SALUD"),
        (11, "COORDINADOR DE PROFESIONALES INDEPENDIENTES"),
        (12, "COORDINADOR DE ASUNTOS COMUNITARIOS"),
    ]

    provincia = models.CharField(max_length=50, choices=PROVINCIAS_RD)
    municipio = models.CharField(max_length=100)
    orden = models.PositiveSmallIntegerField(choices=CARGOS_MUNICIPALES, unique=False)
    nombre = models.CharField(max_length=100)
    cedula = models.CharField(max_length=20)
    telefono = models.CharField(max_length=20)
    email = models.EmailField(blank=True)
    oficio = models.CharField(max_length=100, blank=True)

    creado_por = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return f"{self.get_orden_display()} - {self.nombre}"

# Modelo Cargo Nacional
class CargoNacional(models.Model):
    CARGOS_CHOICES = [
        (1, 'Presidente(a)'),
        (2, 'Vicepresidente(a)'),
        (3, 'Secretario(a) de Finanzas'),
        (4, 'Coordinador(a) Operativo(a)'),
        (5, 'Coordinador(a) Nacional de la Juventud'),
        (6, 'Coordinador(a) Nacional de Cultos y Organizaciones sin fines de Lucro'),
        (7, 'Coordinadora Nacional de La Mujer'),
        (8, 'Coordinador(a) Regional Santo Domingo y Distrito Nacional'),
        (9, 'Coordinador(a) Regional Región Norte'),
        (10, 'Coordinador(a) Regional Región Sur'),
        (11, 'Coordinador(a) Regional Región Este'),
    ]

    orden = models.PositiveSmallIntegerField(choices=CARGOS_CHOICES, unique=True)
    nombre = models.CharField(max_length=100)
    cedula = models.CharField(max_length=20)
    telefono = models.CharField(max_length=20)
    email = models.EmailField()
    oficio = models.CharField(max_length=100)

    creado_por = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return f"{self.get_orden_display()} - {self.nombre}"
