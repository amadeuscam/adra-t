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
        print(iter_mujer_02)
        print(iter_mujer_3_15)
        print(iter_mujer_16_64)
        print(iter_mujer_65)
        print("*"*90)
        beneficiar_hombre = Persona.objects.filter(active=True, sexo__icontains="hombre")
        iter_hombre_02 = len([b.age for b in beneficiar_hombre if b.age >= 0 and b.age <= 2])
        iter_hombre_3_15 = len([b.age for b in beneficiar_hombre if b.age >= 3 and b.age <= 15])
        iter_hombre_16_64 = len([b.age for b in beneficiar_hombre if b.age >= 16 and b.age <= 64])
        iter_hombre_65 = len([b.age for b in beneficiar_hombre if b.age >= 65])

        print(iter_hombre_02)
        print(iter_hombre_3_15)
        print(iter_hombre_16_64)
        print(iter_hombre_65)
        print("*" * 90)

