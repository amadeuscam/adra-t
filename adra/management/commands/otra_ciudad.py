from django.core.management.base import BaseCommand
from adra.models import Persona, Hijo


class Command(BaseCommand):

    def handle(self, *args, **options):
        persona = Persona.objects.filter(active=True, domingo=2).exclude(covid=True)
        # persona = Persona.objects.filter(active=True).exclude(covid=True)
        # dom1 = Persona.objects.filter(active=True, domingo=1).exclude(covid=True)
        # dom2 = Persona.objects.filter(active=True, domingo=2).exclude(covid=True)
        # print([ p.numero_adra for p in dom1])
        # print(dom1.count())
        print(persona.count())
        fam = Hijo.objects.filter(persona__in=persona)
        # # fam = Hijo.objects.get(nombre_apellido="MOHAMED EL MORABIT")
        print(fam.count())
