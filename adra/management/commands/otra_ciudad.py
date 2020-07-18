from django.core.management.base import BaseCommand, CommandError
from datetime import date
from adra.models import Persona, Alimentos


class Command(BaseCommand):

    def handle(self, *args, **options):
        persona = Persona.objects.exclude(ciudad__icontains="torrejon")
        today = date.today()
        for p in persona:
            # per_inside = Persona.objects.filter(numero_adra=p.numero_adra).update(active=False)
            print(p.ciudad)
            print(p.numero_adra)
            print(p.active)
            # print( today.year - p.fecha_nacimiento.yea
