from django.core.management.base import BaseCommand, CommandError
from django.db.models import Q

from adra.models import Persona
from twilio.rest import Client
import sendgrid


class Command(BaseCommand):

    def handle(self, *args, **options):
        pass