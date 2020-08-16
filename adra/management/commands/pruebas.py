from django.core.management.base import BaseCommand, CommandError
from django.db.models import Q

from adra.models import Persona,Hijo,Alimentos
from twilio.rest import Client


class Command(BaseCommand):

    def handle(self, *args, **options):

        for _ in range(1000):
            total_per = Alimentos(
                alimento_1=2,
                alimento_2=3,
                alimento_3=0,
                alimento_4=5,
                alimento_6=2,
                alimento_7=3,
                alimento_8=2,
                alimento_9=2,
                alimento_10=2,
                alimento_11=2,
                alimento_12=3,
                alimento_13=2,
                alimento_14=3,
                alimento_15=3,modificado_por_id=3,
                persona_id=3,
                fecha_recogida= "2020-08-10"

            )
            total_per.save()





