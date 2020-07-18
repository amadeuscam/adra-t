from django.core.management.base import BaseCommand, CommandError
from django.db.models import Q
import pyqrcode
import png
from pyqrcode import QRCode
from adra.models import Persona


class Command(BaseCommand):

    def handle(self, *args, **options):


        personas = Persona.objects.all()
        for ben in personas:

            s = f"https://adra-torrejon.herokuapp.com/persona/{ben.pk}/"

            # Generate QR code
            url = pyqrcode.create(s)
            # Create and save the svg file naming "myqr.svg"
            # url.svg("myqr.svg", scale=8)

            # Create and save the png file naming "myqr.png"
            url.png(f'{ben.numero_adra}.png', scale=6)

