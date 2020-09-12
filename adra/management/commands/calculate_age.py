from django.core.management.base import BaseCommand, CommandError
from django.db.models import Q, F, Count

from adra.models import Persona,Hijo
from twilio.rest import Client
import sendgrid
from datetime import datetime
from dateutil.relativedelta import relativedelta
from django.db.models import Q

class Command(BaseCommand):

    def handle(self, *args, **options):

        beneficiar_mujer = Persona.objects.filter(active=True,sexo__icontains="mujer")
        iter_mujer_02 = len([ b.age for b in beneficiar_mujer if b.age >=0 and b.age <= 2 ])
        iter_mujer_3_15 = len([ b.age for b in beneficiar_mujer if b.age >=3 and b.age <= 15 ])
        iter_mujer_16_64 = len([ b.age for b in beneficiar_mujer if b.age >=16 and b.age <= 64 ])
        iter_mujer_65 = len([ b.age for b in beneficiar_mujer if  b.age >= 65 ])

        beneficiar_hombre = Persona.objects.filter(active=True, sexo__icontains="hombre")
        iter_hombre_02 = len([b.age for b in beneficiar_hombre if b.age >= 0 and b.age <= 2])
        iter_hombre_3_15 = len([b.age for b in beneficiar_hombre if b.age >= 3 and b.age <= 15])
        iter_hombre_16_64 = len([b.age for b in beneficiar_hombre if b.age >= 16 and b.age <= 64])
        iter_hombre_65 = len([b.age for b in beneficiar_hombre if b.age >= 65])


        #la parte de beneficarios
        familiares_mujer = Hijo.objects.filter(active=True, sexo="m")
        iter_familiares_mujer_02 = len([b.age for b in familiares_mujer if b.age >= 0 and b.age <= 2])
        iter_familiares_mujer_3_15 = len([b.age for b in familiares_mujer if b.age >= 3 and b.age <= 15])
        iter_familiares_mujer_16_64 = len([b.age for b in familiares_mujer if b.age >= 16 and b.age <= 64])
        iter_familiares_mujer_65 = len([b.age for b in familiares_mujer if b.age >= 65])

        familiares_hombre = Hijo.objects.filter(active=True, sexo="h")
        iter_familiares_hombre_02 = len([b.age for b in familiares_hombre if b.age >= 0 and b.age <= 2])
        iter_familiares_hombre_3_15 = len([b.age for b in familiares_hombre if b.age >= 3 and b.age <= 15])
        iter_familiares_hombre_16_64 = len([b.age for b in familiares_hombre if b.age >= 16 and b.age <= 64])
        iter_familiares_hombre_65 = len([b.age for b in familiares_hombre if b.age >= 65])

        total_mujer_02 = iter_mujer_02 + iter_familiares_mujer_02
        total_mujer_3_15 = iter_mujer_3_15 + iter_familiares_mujer_3_15
        total_mujer_15_64 = iter_mujer_16_64 + iter_familiares_mujer_16_64
        total_mujer_65 = iter_mujer_65 + iter_familiares_mujer_65
        total_mujeres = total_mujer_02 + total_mujer_3_15 + total_mujer_15_64 + total_mujer_65
        print(f"total mujeres{total_mujeres}")

        total_hombre_02 = iter_hombre_02 + iter_familiares_hombre_02
        total_hombre_3_15 = iter_hombre_3_15 + iter_familiares_hombre_3_15
        total_hombre_15_64 = iter_hombre_16_64 + iter_familiares_hombre_16_64
        total_hombre_65 = iter_hombre_65 + iter_familiares_hombre_65
        total_hombres = total_hombre_02 + total_hombre_3_15 + total_hombre_15_64 + total_hombre_65
        print(f"total hombres{total_hombres}")

        total_02 = total_hombre_02 + total_mujer_02
        total_3_15 = total_hombre_3_15 + total_mujer_3_15
        total_15_64 = total_hombre_15_64 + total_mujer_15_64
        total_65 = total_hombre_65 + total_mujer_65
        total = total_02 + total_3_15 + total_15_64 + total_65
        print(f"totalul total {total}")



