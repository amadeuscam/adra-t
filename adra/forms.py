from django import forms
from .models import Persona, Alimentos, Hijo,Profile
from django.contrib.auth.models import User


class DateInput(forms.DateTimeInput):
    input_type = 'date'

class EmailInput(forms.EmailInput):
    input_type = 'email'




class AlimentosFrom(forms.ModelForm):
    class Meta:
        model = Alimentos
        fields = (
            'alimento_1',
            'alimento_2',
            'alimento_3',
            'alimento_4',
            'alimento_6',
            'alimento_7',
            'alimento_8',
            'alimento_9',
            'alimento_10',
            'alimento_11',
            'alimento_12',
            'alimento_13',
            'alimento_14',
            'alimento_15',
            'fecha_recogida'
        )
        widgets = {
            'fecha_recogida': DateInput(),
        }


class PersonaForm(forms.ModelForm):
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
            'fecha_nacimiento': DateInput(),
            'email':EmailInput()
        }


class HijoForm(forms.ModelForm):
    class Meta:
        model = Hijo
        fields = [
            'parentesco',
            'sexo',
            'nombre_apellido',
            'dni',
            'fecha_nacimiento',

        ]
        widgets = {
            'fecha_nacimiento': DateInput(),
        }

class UserEditForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'email')


class ProfileEditForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ('date_of_birth',)
        widgets = {
            'date_of_birth': forms.DateInput(),
        }



class SignupForm(forms.Form):
    first_name = forms.CharField(max_length=30, label='Nume')
    last_name = forms.CharField(max_length=30, label='Prenume')

    def signup(self, request, user):
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']
        user.save()

