from django.core.management.base import BaseCommand, CommandError
from django.db.models import Q

from adra.models import Persona
from twilio.rest import Client
import sendgrid


class Command(BaseCommand):

    def handle(self, *args, **options):
        try:
            # Python 3
            import urllib.request as urllib
        except ImportError:
            # Python 2
            import urllib2 as urllib

        sg = sendgrid.SendGridAPIClient(apikey="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")
        data = {
            "from": {
                "email": "example@.sendgrid.net"
            },
            "personalizations": [
                {
                    "to": [
                        {
                            "email": "amadeuscam@yahoo.es"
                        }
                    ],
                    "dynamic_template_data": {
                        "url_cambiar": "https://adra-torrejon.herokuapp.com/",
                        "Sender_Name": "Sample Name",

                    }
                }
            ],
            "template_id": "d-ab0adafe4dd14cb4b9aba688b7200830"
        }
        try:
            response = sg.client.mail.send.post(request_body=data)
        except urllib.HTTPError as e:
            print(e.read())
            exit()
        print(response.status_code)
        print(response.body)
        print(response.headers)
        # persona = Persona.objects.filter(nacionalidad__icontains="Marruecos")
        # print(persona.count())
        count = 0
