from django.db import models
from django.contrib.auth.models import User


class Timestamp(models.Model):
    created = models.DateTimeField(auto_now_add=True, verbose_name="Fecha de creación")
    updated = models.DateTimeField(auto_now=True, verbose_name="Fecha de Edición")
    class Meta: 
        abstract = True




class Tarea(Timestamp):
    ESTADO=[
        ('1', 'Nuevo'),
        ('2', 'En Progreso'),
        ('3', 'En Revisión'),
        ('4', 'Completado'),
    ]

    titulo=models.CharField(max_length=100)
    descripcion=models.TextField()
    estado_actual=models.CharField(max_length=50, choices=ESTADO)

    def __str__(self):
        return self.titulo


class Profile(models.Model):

    PROCESO = (
        ('AP', 'ADMINISTRACIÓN Y PLANEACIÓN'),
        ('AO', 'APOYO ORGANIZATIVO Y SOCIOCULTURAL'),
        ('AS', 'ASEGURAMIENTO'),
        ('AC', 'ATENCION AL COMUNERO'),
        ('CI', 'CONTROL INTERNO'),
        ('FI', 'FINANCIERA'),
        ('GC', 'GARANTIA DE LA CALIDAD'),
        ('JU', 'JURIDICA'),
        ('MI', 'MINGA'),
        ('PR', 'PRESTADOR'),
        ('PO', 'PROVEEDOR'),
        ('GT', 'GESTION TIC'),
        ('RP', 'REPORTES'),
        ('NA', 'NO APLICA'),
    )

    TIPDOC = (
        ('CC', 'CÉDULA DE CIUDADANIA'),
        ('CE', 'CÉDULA DE EXTRANJERIA'),
        ('CD', 'CARNET DIPLOMATICO'),
        ('PS', 'PASAPORTE'),
    )

    ROL = (
        ('RSC', 'REGISTRO SOLICITUD DE COTIZACIONES'),
        ('PMD', 'PERTINENCIA MEDICA'),
        ('ASE', 'GESTION ASEGURAMIENTO'),
        ('SGH', 'SEGUIMIENTO HOSPITALARIO'),
        ('COV', 'SEGUIMIENTO COVID'),
        ('API', 'SERVICE WEB'),
        ('NTRL', 'PERSONA NATURAL'),
        ('JDCA', 'PERSONA JURIDICA'),
        ('ALT', 'ALTO COSTO'),
        ('RPT', 'REPORTES AIC EPSI'),
        ('GES', 'GESTANTES'),
        ('NA', 'NO APLICA'),
    )

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    avatar = models.ImageField("Avatar", upload_to='profiles', default='profiles/LogoAic2.jpeg', null=True, blank=True)
    tipdoc = models.CharField('Tipo de documento', max_length=2, choices=TIPDOC)
    identificacion = models.BigIntegerField("Nr° identificación", null=True, blank=True)
    pnombre = models.CharField("Primer nombre", max_length=60)
    snombre = models.CharField("Segundo nombre", max_length=60, null=True, blank=True)
    papellido = models.CharField("Primer apellido", max_length=60)
    sapellido = models.CharField("Segundo apellido", max_length=60, null=True, blank=True)
    fecexped = models.DateField('Fecha de Expedición', null=True, blank=True)
    lugarexpe = models.CharField("Lugar de Expedición", max_length=60, null=True, blank=True)
    fechanac = models.DateField('Fecha de Nacimiento', null=True, blank=True)
    lugarnac = models.CharField("Lugar de Nacimiento", max_length=60, null=True, blank=True)
    correo = models.CharField("Correo Electronico", max_length=60, null=True, blank=True)
    direccion = models.CharField('Dirección', max_length=100, null=True, blank=True)
    phone = models.BigIntegerField("Telefono", null=True, blank=True)
    celular = models.BigIntegerField("Celular", null=True, blank=True)
    proceso = models.CharField("Proceso", max_length=2, choices=PROCESO, default='NA')
    rol = models.CharField("Rol", max_length=4, choices=ROL, default='NA')
    #prestador = models.ForeignKey(Prestador, null=True, blank=True, on_delete=models.PROTECT)
    created = models.DateTimeField(auto_now_add=True, verbose_name="Fecha de creación")
    updated = models.DateTimeField(auto_now=True, verbose_name="Fecha de Edición")

    objects = models.Manager()

    def __str__(self):
        return str(self.user) if self.user else ''

    class Meta:
        ordering = ["id"]