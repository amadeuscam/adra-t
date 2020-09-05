from django.core.management.base import BaseCommand, CommandError
from django.db.models import Q

from adra.models import Persona,Hijo
from twilio.rest import Client
import sendgrid
from datetime import datetime
from dateutil.relativedelta import relativedelta
from django.db.models import Q

class Command(BaseCommand):

    def handle(self, *args, **options):
        beneficiar_mujer = Persona.objects.filter(sexo__icontains="mujer", active=True).count()
        beneficiar_hombre = Persona.objects.filter(sexo__icontains="hombre", active=True)
        familiar_mujer = Hijo.objects.filter(sexo__icontains="mujer",active=True).count()
        familiar_hombre = Hijo.objects.filter(sexo__icontains="hombre",active=True)
        print(beneficiar_mujer)
        print(familiar_mujer)
        #
        # list_0_2_fam_mujer = len([p for p in familiar_mujer if p.age >= 0 and p.age <=2])
        # list_0_2_fam_hombre = len([p for p in familiar_hombre if p.age >= 0 and p.age <=2])
        # list_0_2_ben_mujer = len([b for b in beneficiar_mujer if b.age >= 0 and b.age <= 2])
        # list_0_2_ben_hombre = len([b for b in beneficiar_hombre if b.age >= 0 and b.age <= 2])
        #
        # print(f"total 0-2 mujeres {list_0_2_fam_mujer + list_0_2_ben_mujer}")
        # print(f"total 0-2 hombre {list_0_2_fam_hombre + list_0_2_ben_hombre}")
        # print(f"total 0-2   {list_0_2_fam_mujer + list_0_2_ben_mujer +  list_0_2_fam_hombre + list_0_2_ben_hombre}")
        # # print(len(list_0_2_fam_hombre))
        # # print(len(list_0_2_ben_mujer))
        # # print(len(list_0_2_ben_hombre))
        # # print(len(list_0_2_fam_mujer) + len(list_0_2_fam_hombre) + len(list_0_2_ben_mujer) +len(list_0_2_ben_hombre))
        # # print(f"total 0-2  >{len(list_0_2_fam_mujer) + len(list_0_2_fam_hombre) + len(list_0_2_ben_mujer) +len(list_0_2_ben_hombre)}")
        # print("*"*90)

        # list_3_15_fam_mujer = [p for p in familiar_mujer if p.age >= 3 and p.age <= 15]
        # list_3_15_fam_hombre = [p for p in familiar_hombre if p.age >= 3 and p.age <= 15]
        # # list_3_15_ben = [b for b in beneficiar_mujer if b.age >= 0 and b.age <= 2]
        # print(len(list_3_15_fam_mujer))
        # print(len(list_3_15_fam_hombre))
        # print(len(list_3_15_fam_mujer) + len(list_3_15_fam_hombre))
        # print(f"total 3-15 > {len(list_3_15_fam_mujer) + len(list_3_15_fam_hombre)}")
        # print("*" * 90)

