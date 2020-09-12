from django.core.management.base import BaseCommand, CommandError
from django.db.models import Q
import pyqrcode
import png
from pyqrcode import QRCode
from adra.models import Persona,Hijo


class Command(BaseCommand):

    def handle(self, *args, **options):


        personas = Hijo.objects.all()
        for ben in personas:
            print(ben.nombre_apellido)
            print(ben.id)
            if ben.parentesco == "hijo":
                Hijo.objects.filter(id=ben.id).update(sexo="h")
            if ben.parentesco == "hija":
                Hijo.objects.filter(id=ben.id).update(sexo="m")
            if ben.parentesco == "esposo":
                Hijo.objects.filter(id=ben.id).update(sexo="h")
            if ben.parentesco == "esposa":
                Hijo.objects.filter(id=ben.id).update(sexo="m")

            # s = f"https://adra-torrejon.herokuapp.com/persona/{ben.pk}/"
            #
            # # Generate QR code
            # url = pyqrcode.create(s)
            # # Create and save the svg file naming "myqr.svg"
            # # url.svg("myqr.svg", scale=8)
            #
            # # Create and save the png file naming "myqr.png"
            # url.png(f'{ben.numero_adra}.png', scale=6)

