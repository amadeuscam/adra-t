from django.core.management.base import BaseCommand, CommandError
from django.db.models import Q

from adra.models import Persona
from twilio.rest import Client


class Command(BaseCommand):

    def handle(self, *args, **options):

        persona = ersona.objects.filter(nacionalidad__icontains="Marruecos")
        print(persona.count())
        count = 0
