from datetime import date
from datetime import datetime
from django.db import models
from django.contrib.auth.models import User
from django.contrib.auth import get_user_model
from django.urls import reverse
from django.core.validators import validate_email
from adra_project import settings
from django.core.validators import MinLengthValidator


class Persona(models.Model):
    SEXO = [
        ('mujer', "Mujer"),
        ('hombre', "Hombre")
    ]
    DOMINGO = [
        ('1', "Domingo 1"),
        ('2', "Domingo 2")
    ]
    CIUDAD = [
        ('Torrejon de ardoz', "Torrejon de ardoz"),
    ]
    nombre_apellido = models.CharField(
        max_length=100, verbose_name="Nombre del beneficiario")
    dni = models.CharField(max_length=20)
    fecha_nacimiento = models.DateField(auto_now_add=False)
    numero_adra = models.IntegerField(unique=True)
    nacionalidad = models.CharField(max_length=20)
    covid = models.BooleanField(default=False, verbose_name="Covid entregas")
    domicilio = models.TextField()
    are_acte = models.BooleanField(default=False, verbose_name="Tiene papeles")
    ciudad = models.CharField(max_length=350, choices=CIUDAD)
    telefono = models.IntegerField()
    email= models.CharField(max_length=100,blank=True,default='',verbose_name="Email beneficiario",validators=[validate_email])
    mensaje = models.TextField(blank=True)
    active = models.BooleanField(default=True, verbose_name="Activo?")
    modificado_por = models.ForeignKey(User, on_delete=models.CASCADE,null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)
    sexo = models.CharField(max_length=20, choices=SEXO, )
    discapacidad = models.BooleanField(default=False)
    domingo = models.CharField(max_length=30, choices=DOMINGO)
    empadronamiento = models.BooleanField(default=False,
                                          verbose_name="Certificado de empadronamiento actualizado con fecha de menos de tres meses ")
    libro_familia = models.BooleanField(
        default=False, verbose_name="Fotocopia del Libro de Familia ")
    fotocopia_dni = models.BooleanField(default=False,
                                        verbose_name="Fotocopia del DNI/NIE o pasaporte de todos los miembros del núcleo familiar")
    prestaciones = models.BooleanField(default=False,
                                       verbose_name="Fotocopia de la documentación que acredite de prestación, pensión, paro, etc")
    nomnia = models.BooleanField(
        default=False, verbose_name="Fotocopia de la nómina en caso de trabajar.")
    cert_negativo = models.BooleanField(default=False,
                                        verbose_name="En caso de no tener ingresos: certificado negativo de rentas, de la Agencia Tributaria.")
    aquiler_hipoteca = models.BooleanField(default=False,
                                           verbose_name="Ultimo recibo alquiler o  hipoteca de vivienda familiar en la que están empadronados")
    recibos = models.BooleanField(default=False,
                                  verbose_name="Recibo de gastos básicos: luz, agua, gas, calefacción, comunidad y  comedor escolar.")

    class Meta:
        ordering = ('-created_at',)

    def __str__(self):
        return self.nombre_apellido

    def get_absolute_url(self):
        return reverse('adra:personas_detail', args=[str
                                                     (self.id)])

    @property
    def age(self):
        today = date.today()
        return today.year - self.fecha_nacimiento.year - (
                (today.month, today.day) < (self.fecha_nacimiento.month, self.fecha_nacimiento.day))


class Hijo(models.Model):
    FAMILIARES = (('esposo', "Esposo"), ("esposa", "Esposa"),
                  ('hijo', "Hijo"), ('hija', "Hija"),)
    SEXO = (
        ('mujer', "Mujer"),
        ('hombre', "Hombre")
    )
    parentesco = models.CharField(
        max_length=20, choices=FAMILIARES, )
    sexo = models.CharField(max_length=20, choices=SEXO, )
    nombre_apellido = models.CharField(max_length=50)
    dni = models.CharField(max_length=100,blank=True)
    fecha_nacimiento = models.DateField(auto_now=False)
    edad = models.IntegerField(default=0, blank=False, null=False)

    persona = models.ForeignKey(
        Persona, on_delete=models.CASCADE, related_name="hijo")
    modificado_por = models.ForeignKey(User, on_delete=models.CASCADE,
                                       null=True)

    def get_absolute_url(self):
        return reverse('adra:personas_detail', kwargs={'pk': self.persona.pk})

    def __str__(self):
        return self.nombre_apellido

    @property
    def age(self):
        today = date.today()
        return today.year - self.fecha_nacimiento.year - (
                (today.month, today.day) < (self.fecha_nacimiento.month, self.fecha_nacimiento.day))


class Alimentos(models.Model):
    persona = models.ForeignKey(
        Persona, on_delete=models.CASCADE, related_name="alimentos")
    arroz_blanco = models.IntegerField(default=None)
    garbanzo_cocido = models.IntegerField(
        default=None)  # new
    atun_sardina = models.IntegerField(verbose_name="Atun", default=None)
    sardina = models.IntegerField(default=None)  # new
    pasta_espagueti = models.IntegerField(
        default=None)  # new
    tomate_frito = models.IntegerField(default=None)
    galletas = models.IntegerField(default=None)
    macedonia_verdura_conserva = models.IntegerField(
        default=None)  # new
    fruta_conserva_pera = models.IntegerField(
        default=None)
    fruta_conserva_coctel = models.IntegerField(
        default=None)
    tarito_pollo = models.IntegerField(default=None)
    tarito_fruta = models.IntegerField(default=None)
    leche = models.IntegerField(default=None)
    batido_chocolate = models.IntegerField(default=None)
    aceite_de_oliva = models.IntegerField(default=None)

    modificado_por = models.ForeignKey(User, on_delete=models.CASCADE,
                                       null=True)
    fecha_recogida = models.DateTimeField(auto_now_add=False)
    created_at = models.DateField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-fecha_recogida']

    def get_absolute_url(self):
        return reverse("adra:personas_detail", kwargs={'pk': self.persona.id})


class AlmacenAlimentos(models.Model):
    arroz_blanco = models.IntegerField(blank=True, null=True)
    garbanzo_cocido = models.IntegerField(
        default=0, blank=True, null=True)  # new
    atun_sardina = models.IntegerField(blank=True, null=True)
    sardina = models.IntegerField(default=0, blank=True, null=True)  # new
    pasta_espagueti = models.IntegerField(
        default=0, blank=True, null=True)  # new
    tomate_frito = models.IntegerField(blank=True, null=True)
    galletas = models.IntegerField(blank=True, null=True)
    macedonia_verdura_conserva = models.IntegerField(
        default=0, blank=True, null=True)  # new
    fruta_conserva_pera = models.IntegerField(default=0, blank=True, null=True)
    fruta_conserva_coctel = models.IntegerField(
        default=0, blank=True, null=True)
    tarito_pollo = models.IntegerField(blank=True, null=True)
    tarito_fruta = models.IntegerField(blank=True, null=True)
    leche = models.IntegerField(blank=True, null=True)
    batido_chocolate = models.IntegerField(default=0, blank=True, null=True)
    aceite_de_oliva = models.IntegerField(blank=True, null=True)
    modificado_por = models.ForeignKey(User, on_delete=models.CASCADE,
                                       null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)


class Profile(models.Model):
    user = models.OneToOneField(get_user_model(), on_delete=models.CASCADE)
    date_of_birth = models.DateField(blank=True, null=True)
    photo = models.ImageField(upload_to='users/%Y/%m/%d/', blank=True)

    def __str__(self):
        return f'Profile for user {self.user.username}'
