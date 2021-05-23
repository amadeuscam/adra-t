from rest_framework import serializers
from .models import Persona, Hijo, Alimentos, AlmacenAlimentos
from django.contrib.auth.models import User
from django.contrib.auth import get_user_model


class AlimentosSerializer(serializers.ModelSerializer):
    class Meta:
        model = Alimentos
        fields = ['fecha_recogida', 'persona', 'alimento_1']


class AlacenAlimentosSerializer(serializers.ModelSerializer):
    alimento_1_name = serializers.CharField(default=f"{AlmacenAlimentos._meta.get_field('alimento_1').verbose_name}",
                                            read_only=True)
    alimento_2_name = serializers.CharField(default=f"{AlmacenAlimentos._meta.get_field('alimento_2').verbose_name}",
                                            read_only=True)
    alimento_3_name = serializers.CharField(default=f"{AlmacenAlimentos._meta.get_field('alimento_3').verbose_name}",
                                            read_only=True)
    alimento_4_name = serializers.CharField(default=f"{AlmacenAlimentos._meta.get_field('alimento_4').verbose_name}",
                                            read_only=True)

    # alimento_5_name = serializers.CharField(default=f"{AlmacenAlimentos._meta.get_field('alimento_5').verbose_name}",
    #                                         read_only=True)
    alimento_6_name = serializers.CharField(default=f"{AlmacenAlimentos._meta.get_field('alimento_6').verbose_name}",
                                            read_only=True)
    alimento_7_name = serializers.CharField(default=f"{AlmacenAlimentos._meta.get_field('alimento_7').verbose_name}",
                                            read_only=True)
    alimento_8_name = serializers.CharField(default=f"{AlmacenAlimentos._meta.get_field('alimento_8').verbose_name}",
                                            read_only=True)

    alimento_9_name = serializers.CharField(default=f"{AlmacenAlimentos._meta.get_field('alimento_9').verbose_name}",
                                            read_only=True)
    alimento_10_name = serializers.CharField(default=f"{AlmacenAlimentos._meta.get_field('alimento_10').verbose_name}",
                                             read_only=True)
    alimento_11_name = serializers.CharField(default=f"{AlmacenAlimentos._meta.get_field('alimento_11').verbose_name}",
                                             read_only=True)
    alimento_12_name = serializers.CharField(default=f"{AlmacenAlimentos._meta.get_field('alimento_12').verbose_name}",
                                             read_only=True)

    alimento_13_name = serializers.CharField(default=f"{AlmacenAlimentos._meta.get_field('alimento_13').verbose_name}",
                                             read_only=True)
    alimento_14_name = serializers.CharField(default=f"{AlmacenAlimentos._meta.get_field('alimento_14').verbose_name}",
                                             read_only=True)
    alimento_15_name = serializers.CharField(default=f"{AlmacenAlimentos._meta.get_field('alimento_15').verbose_name}",
                                             read_only=True)

    class Meta:
        model = AlmacenAlimentos
        fields = '__all__'


class HijosSerializer(serializers.ModelSerializer):
    class Meta:
        model = Hijo
        fields = ['nombre_apellido', 'dni', 'fecha_nacimiento', 'parentesco']


class PersonaSerializer(serializers.HyperlinkedModelSerializer):
    modificado_por = serializers.ReadOnlyField(source='modificado_por.username')
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
        fields = ['id', 'username', 'email']
