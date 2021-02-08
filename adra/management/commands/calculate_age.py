from django.core.management.base import BaseCommand, CommandError
from django.db.models import Q, F, Count

from adra.models import Persona, Hijo
from twilio.rest import Client
import sendgrid
from datetime import datetime
from django.db.models import Q


class Command(BaseCommand):

    def handle(self, *args, **options):
        # sexo__icontains = "mujer").exclude(covid=True)

        beneficiar = Persona.objects.prefetch_related('hijo').filter(active=True).exclude(covid=True)

        lst_02_mujer = []
        lst_02_hombre = []

        lst_3_15_mujer = []
        lst_3_15_hombre = []

        lst_16_64_mujer = []
        lst_16_64_hombre = []

        lst_64_mujer = []
        lst_64_hombre = []



        [lst_02_mujer.append(b.age) for b in beneficiar if 0 <= b.age <= 2 and b.sexo == "mujer"]
        [lst_02_hombre.append(b.age) for b in beneficiar if 0 <= b.age <= 2 and b.sexo == "hombre"]

        [lst_3_15_mujer.append(b.age) for b in beneficiar if 3 <= b.age <= 15 and b.sexo == "mujer"]
        [lst_3_15_hombre.append(b.age) for b in beneficiar if 3 <= b.age <= 15 and b.sexo == "hombre"]

        [lst_16_64_mujer.append(b.age) for b in beneficiar if 16 <= b.age <= 64 and b.sexo == "mujer"]
        [lst_16_64_hombre.append(b.age) for b in beneficiar if 16 <= b.age <= 64 and b.sexo == "hombre"]

        [lst_64_mujer.append(b.age) for b in beneficiar if b.age >= 65 and b.sexo == "mujer"]
        [lst_64_hombre.append(b.age) for b in beneficiar if b.age >= 65 and b.sexo == "hombre"]


        lst_familiares = []

        for hijo in beneficiar:
            [(lst_02_mujer.append(b.age),lst_familiares.append(b.age)) for b in hijo.hijo.all() if 0 <= b.age <= 2 and b.sexo == "m"]
            [(lst_02_hombre.append(b.age),lst_familiares.append(b.age)) for b in hijo.hijo.all() if 0 <= b.age <= 2 and b.sexo == "h"]

            [(lst_3_15_mujer.append(b.age),lst_familiares.append(b.age)) for b in hijo.hijo.all() if 3 <= b.age <= 15 and b.sexo == "m"]
            [(lst_3_15_hombre.append(b.age),lst_familiares.append(b.age)) for b in hijo.hijo.all() if 3 <= b.age <= 15 and b.sexo == "h"]

            [(lst_16_64_mujer.append(b.age),lst_familiares.append(b.age)) for b in hijo.hijo.all() if 16 <= b.age <= 64 and b.sexo == "m"]
            [(lst_16_64_hombre.append(b.age),lst_familiares.append(b.age)) for b in hijo.hijo.all() if 16 <= b.age <= 64 and b.sexo == "h"]

            [(lst_64_mujer.append(b.age),lst_familiares.append(b.age)) for b in hijo.hijo.all() if b.age >= 65 and b.sexo == "m"]
            [(lst_64_hombre.append(b.age),lst_familiares.append(b.age)) for b in hijo.hijo.all() if b.age >= 65 and b.sexo == "h"]

        # print(lst_02_mujer)
        # print(lst_02_hombre)
        print(len(lst_02_mujer))
        print(len(lst_02_hombre))

        print(len(lst_3_15_mujer))
        print(len(lst_3_15_hombre))

        print(len(lst_16_64_mujer))
        print(len(lst_16_64_hombre))

        print(len(lst_64_mujer))
        print(len(lst_64_hombre))

        data_statistics = {
            "total_per_mujer_02": len(lst_02_mujer),
            "total_per_mujer_03": len(lst_3_15_mujer),
            "total_per_mujer_16": len(lst_16_64_mujer),
            "total_per_mujer_65": len(lst_64_mujer),
            "total_mujeres": len(lst_02_mujer) + len(lst_3_15_mujer) + len(lst_16_64_mujer) + len(lst_64_mujer),

            "total_per_hombre_02": len(lst_02_hombre),
            "total_per_hombre_03": len(lst_3_15_hombre),
            "total_per_hombre_16": len(lst_16_64_hombre),
            "total_per_hombre_65": len(lst_64_hombre),
            "total_hombres": len(lst_02_hombre) + len(lst_3_15_hombre) + len(lst_16_64_hombre) + len(lst_64_hombre),
            "total_02": len(lst_02_mujer) + len(lst_02_hombre),
            "total_03": len(lst_3_15_mujer) + len(lst_3_15_hombre),
            "total_16": len(lst_16_64_mujer) + len(lst_16_64_hombre),
            "total_65": len(lst_64_mujer) + len(lst_64_hombre),
            "total_personas": len(lst_02_mujer) + len(lst_02_hombre) + len(lst_3_15_mujer) + len(lst_3_15_hombre) + len(lst_16_64_mujer) + len(lst_16_64_hombre) + len(lst_64_mujer) + len(lst_64_hombre),
            "discapacidad": Persona.objects.filter(discapacidad=True, active=True).count(),
            "total_beneficiarios": beneficiar.count(),
            "total_familiares": len(lst_familiares),
            "nbar": 'stat'

        }
        print(data_statistics)

        # #la parte de beneficarios
        # familiares_mujer = Hijo.objects.filter(active=True, sexo="m")
        # iter_familiares_mujer_02 = len([b.age for b in familiares_mujer if b.age >= 0 and b.age <= 2])
        # iter_familiares_mujer_3_15 = len([b.age for b in familiares_mujer if b.age >= 3 and b.age <= 15])
        # iter_familiares_mujer_16_64 = len([b.age for b in familiares_mujer if b.age >= 16 and b.age <= 64])
        # iter_familiares_mujer_65 = len([b.age for b in familiares_mujer if b.age >= 65])
        #
        # familiares_hombre = Hijo.objects.filter(active=True, sexo="h")
        # iter_familiares_hombre_02 = len([b.age for b in familiares_hombre if b.age >= 0 and b.age <= 2])
        # iter_familiares_hombre_3_15 = len([b.age for b in familiares_hombre if b.age >= 3 and b.age <= 15])
        # iter_familiares_hombre_16_64 = len([b.age for b in familiares_hombre if b.age >= 16 and b.age <= 64])
        # iter_familiares_hombre_65 = len([b.age for b in familiares_hombre if b.age >= 65])
        #
        # total_mujer_02 = iter_mujer_02 + iter_familiares_mujer_02
        # total_mujer_3_15 = iter_mujer_3_15 + iter_familiares_mujer_3_15
        # total_mujer_15_64 = iter_mujer_16_64 + iter_familiares_mujer_16_64
        # total_mujer_65 = iter_mujer_65 + iter_familiares_mujer_65
        # total_mujeres = total_mujer_02 + total_mujer_3_15 + total_mujer_15_64 + total_mujer_65
        # print(f"total mujeres{total_mujeres}")
        #
        # total_hombre_02 = iter_hombre_02 + iter_familiares_hombre_02
        # total_hombre_3_15 = iter_hombre_3_15 + iter_familiares_hombre_3_15
        # total_hombre_15_64 = iter_hombre_16_64 + iter_familiares_hombre_16_64
        # total_hombre_65 = iter_hombre_65 + iter_familiares_hombre_65
        # total_hombres = total_hombre_02 + total_hombre_3_15 + total_hombre_15_64 + total_hombre_65
        # print(f"total hombres{total_hombres}")
        #
        # total_02 = total_hombre_02 + total_mujer_02
        # total_3_15 = total_hombre_3_15 + total_mujer_3_15
        # total_15_64 = total_hombre_15_64 + total_mujer_15_64
        # total_65 = total_hombre_65 + total_mujer_65
        # total = total_02 + total_3_15 + total_15_64 + total_65
        # print(f"totalul total {total}")
