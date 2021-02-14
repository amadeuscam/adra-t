from rest_framework import serializers
from .models import Persona, Hijo, Alimentos
from django.contrib.auth.models import User
from django.contrib.auth import get_user_model


class AlimentosSerializer(serializers.ModelSerializer):
    class Meta:
        model = Alimentos
        fields = ['fecha_recogida', 'persona', 'alimento_1']


class HijosSerializer(serializers.ModelSerializer):
    class Meta:
        model = Hijo
        fields = ['nombre_apellido', 'dni', 'fecha_nacimiento', 'parentesco']


class PersonaSerializer(serializers.HyperlinkedModelSerializer):
    modificado_por = serializers.ReadOnlyField(source='modificado_por.username')
    # alimentos = serializers.PrimaryKeyRelatedField(many=True, read_only=True)
    alimentos = AlimentosSerializer(many=True, read_only=True)
    hijo = HijosSerializer(many=True, read_only=True)

    class Meta:
        model = Persona
        fields = ['id', 'nombre_apellido', 'numero_adra', 'dni', 'telefono', 'empadronamiento', 'libro_familia',
                  'mensaje', 'domingo',
                  'modificado_por', 'fecha_nacimiento', 'alimentos', 'hijo', 'fotocopia_dni', 'prestaciones',
                  'nomnia', 'cert_negativo', 'aquiler_hipoteca', 'recibos'
                  ]


class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = get_user_model()
        fields = ['id', 'username']
