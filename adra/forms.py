from django import forms
from .models import Persona, Alimentos, Hijo, Profile
from django.contrib.auth.models import User
from django.forms import ModelForm, DateInput, EmailInput, Form


class AlimentosFrom(ModelForm):
    class Meta:
        model = Alimentos
        fields = (
            'alimento_1',
            'alimento_2',
            'alimento_3',
            'alimento_4',
            'alimento_5',
            'alimento_6',
            'alimento_7',
            'alimento_8',
            'alimento_9',
            'alimento_10',
            'alimento_11',
            'alimento_12',
            'fecha_recogida'
        )
        widgets = {
            'fecha_recogida': DateInput(attrs={"type": "date"}),
        }


class PersonaForm(ModelForm):
    class Meta:
        model = Persona
        fields = [
            'nombre_apellido',
            'dni',
            'fecha_nacimiento',
            'numero_adra',
            'nacionalidad',
            'domicilio',
            'are_acte',
            'ciudad',
            'telefono',
            'mensaje',
            'sexo',
            'discapacidad',
            'domingo',
            'empadronamiento',
            'libro_familia',
            'fotocopia_dni',
            'prestaciones',
            'nomnia',
            'cert_negativo',
            'aquiler_hipoteca',
            'recibos',
            'email',
            'covid',

        ]
        widgets = {
            'fecha_nacimiento': DateInput(attrs={"type": "date"}),
            'email': EmailInput(attrs={"type": "email"})
        }


class HijoForm(ModelForm):
    class Meta:
        model = Hijo
        fields = [
            'parentesco',
            'nombre_apellido',
            'dni',
            'fecha_nacimiento',

        ]
        widgets = {
            'fecha_nacimiento': DateInput(attrs={"type": "date"}),
        }


class UserEditForm(ModelForm):
    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'email')


class ProfileEditForm(ModelForm):
    class Meta:
        model = Profile
        fields = ('date_of_birth',)
        widgets = {
            'date_of_birth': DateInput(attrs={"type": "text"}),
        }


class SignupForm(Form):
    first_name = forms.CharField(max_length=30, label='Nume')
    last_name = forms.CharField(max_length=30, label='Prenume')

    def signup(self, request, user):
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']
        user.save()
