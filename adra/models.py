from datetime import date
from django.contrib.auth import get_user_model
from django.contrib.auth.models import User
from django.core.validators import validate_email
from django.db import models
from django.urls import reverse


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
    email = models.CharField(max_length=100, blank=True, default='', verbose_name="Email beneficiario", validators=[validate_email])
    mensaje = models.TextField(blank=True)
    active = models.BooleanField(default=True, verbose_name="Activo?")
    modificado_por = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
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
    dni = models.CharField(max_length=100, blank=True)
    fecha_nacimiento = models.DateField(auto_now=False)
    edad = models.IntegerField(default=0, blank=False, null=False)
    active = models.BooleanField(default=True, verbose_name="Activo?")
    persona = models.ForeignKey(
        Persona, on_delete=models.CASCADE, related_name="hijo")
    modificado_por = models.ForeignKey(User, on_delete=models.CASCADE,
                                       null=True)

    def save(self, *args, **kwargs):
        if self.parentesco =="esposa":
            self.sexo="m"
        if self.parentesco =="esposo":
            self.sexo="h"
        if self.parentesco =="hijo":
            self.sexo="h"
        if self.parentesco =="hija":
            self.sexo="m"

        super(Hijo, self).save(*args, **kwargs)

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
    alimento_1 = models.IntegerField(default=None, verbose_name="Arroz Blanco")
    alimento_2 = models.IntegerField(default=None, verbose_name="Alubia cocida")
    alimento_3 = models.IntegerField(verbose_name="Conserva de atún", default=None)
    alimento_4 = models.IntegerField(default=None, verbose_name="Conserva de sardina")
    alimento_5 = models.IntegerField(default=None,blank=True,null=True,verbose_name="Conserva de carne (magro de cerdo)")
    alimento_6 = models.IntegerField(default=None, verbose_name="Pasta alimenticia tipo macarrón")
    alimento_7 = models.IntegerField(default=None, verbose_name="Tomate frito en conserva")
    alimento_8 = models.IntegerField(default=None, verbose_name="Galletas")
    alimento_9 = models.IntegerField(default=None, verbose_name="Macedonia de verduras en conserva")
    alimento_10 = models.IntegerField(default=None, verbose_name="Fruta en conserva")
    alimento_11 = models.IntegerField(default=None, verbose_name="Tarritos infantiles con pollo")
    alimento_12 = models.IntegerField(default=None, verbose_name="Tarritos infantiles de fruta")
    alimento_13 = models.IntegerField(default=None, verbose_name="Leche entera UHT")
    alimento_14 = models.IntegerField(default=None, verbose_name="Batidos de chocolate")
    alimento_15 = models.IntegerField(default=None, verbose_name="Aceite de oliva")

    modificado_por = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    persona = models.ForeignKey(Persona, on_delete=models.CASCADE, related_name="alimentos")
    fecha_recogida = models.DateTimeField(auto_now_add=False)
    created_at = models.DateField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-fecha_recogida']

    def get_absolute_url(self):
        return reverse("adra:personas_detail", kwargs={'pk': self.persona.id})


class AlmacenAlimentos(models.Model):
    alimento_1 = models.IntegerField(blank=True, null=True, verbose_name="Arroz Blanco")
    alimento_2 = models.IntegerField(blank=True, null=True, verbose_name="Alubia cocida")
    alimento_3 = models.IntegerField(blank=True, null=True, verbose_name="Conserva de atún")
    alimento_4 = models.IntegerField(blank=True, null=True, verbose_name="Conserva de sardina")
    alimento_5 = models.IntegerField(blank=True, null=True, verbose_name="Conserva de carne (magro de cerdo)")
    alimento_6 = models.IntegerField(blank=True, null=True, verbose_name="Pasta alimenticia tipo macarrón")
    alimento_7 = models.IntegerField(blank=True, null=True, verbose_name="Tomate frito en conserva")
    alimento_8 = models.IntegerField(blank=True, null=True, verbose_name="Galletas")
    alimento_9 = models.IntegerField(blank=True, null=True, verbose_name="Macedonia de verduras en conserva")
    alimento_10 = models.IntegerField(blank=True, null=True, verbose_name="Fruta en conserva")
    alimento_11 = models.IntegerField(blank=True, null=True, verbose_name="Tarritos infantiles con pollo")
    alimento_12 = models.IntegerField(blank=True, null=True, verbose_name="Tarritos infantiles de fruta")
    alimento_13 = models.IntegerField(blank=True, null=True, verbose_name="Leche entera UHT")
    alimento_14 = models.IntegerField(blank=True, null=True, verbose_name="Batidos de chocolate")
    alimento_15 = models.IntegerField(blank=True, null=True, verbose_name="Aceite de oliva")

    modificado_por = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)

    alimento_1_caducidad = models.DateField(auto_now_add=False, blank=True, default=None)
    alimento_2_caducidad = models.DateField(auto_now_add=False, blank=True, default=None)
    alimento_3_caducidad = models.DateField(auto_now_add=False, blank=True, default=None)
    alimento_4_caducidad = models.DateField(auto_now_add=False, blank=True, default=None)
    # alimento_5_caducidad = models.DateField(auto_now_add=False, blank=True, default=None)
    alimento_6_caducidad = models.DateField(auto_now_add=False, blank=True, default=None)
    alimento_7_caducidad = models.DateField(auto_now_add=False, blank=True, default=None)
    alimento_8_caducidad = models.DateField(auto_now_add=False, blank=True, default=None)
    alimento_9_caducidad = models.DateField(auto_now_add=False, blank=True, default=None)
    alimento_10_caducidad = models.DateField(auto_now_add=False, blank=True, default=None)
    alimento_11_caducidad = models.DateField(auto_now_add=False, blank=True, default=None)
    alimento_12_caducidad = models.DateField(auto_now_add=False, blank=True, default=None)
    alimento_13_caducidad = models.DateField(auto_now_add=False, blank=True, default=None)
    alimento_14_caducidad = models.DateField(auto_now_add=False, blank=True, default=None)
    alimento_15_caducidad = models.DateField(auto_now_add=False, blank=True, default=None)


class Profile(models.Model):
    user = models.OneToOneField(get_user_model(), on_delete=models.CASCADE)
    date_of_birth = models.DateField(blank=True, null=True)
    # photo = models.ImageField(upload_to='profile_pics',default='profile_pics/default.png', blank=True)

    def __str__(self):
        return f'Profile for user {self.user.username}'
