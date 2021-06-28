from django.core.management.base import BaseCommand
from adra.models import Persona


class Command(BaseCommand):

    def handle(self, *args, **options):
        persona = Persona.objects.all()

        for p in persona:
            p.empadronamiento = False
            p.libro_familia = False
            p.fotocopia_dni = False
            p.prestaciones = False
            p.nomnia = False
            p.cert_negativo = False
            p.aquiler_hipoteca = False
            p.recibos = False
            p.are_acte = False

            # print(p.nombre_apellido)
            # print(p.empadronamiento)
            # print(p.libro_familia)
            # print(p.fotocopia_dni)
            # print(p.prestaciones)
            # print(p.nomnia)
            # print(p.cert_negativo)
            # print(p.aquiler_hipoteca)
            # print(p.recibos)
            # print("*" * 90)
            p.save()
