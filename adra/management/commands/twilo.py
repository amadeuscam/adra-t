from django.core.management.base import BaseCommand, CommandError
from django.db.models import Q

from adra.models import Persona
from twilio.rest import Client


class Command(BaseCommand):

    def handle(self, *args, **options):

        # Your Account Sid and Auth Token from twilio.com/console
        # DANGER! This is insecure. See http://twil.io/secure
        account_sid = 'ACcdece9488b6849f46039263e133bd525'
        auth_token = 'a244d86555ef55ecf5b4499cf5216d9b'
        client = Client(account_sid, auth_token)

        # message = client.messages.create(
        #     body="Hola a todos!Soy lucian de adra torrejon!",
        #     from_='+12025591005',
        #     to='+34604150313'
        # )
        # filter(Q(domingo="Domingo 1") | Q(domingo=1), ciudad__icontains="Torrejon de ardoz")
        persona = Persona.objects.filter(active=True).exclude(covid=True)
        print(persona.count())
        count = 0
        for p in persona:



            if p.telefono == 0  or len(str(p.telefono)) < 9:
                continue
            count += 1
            # print(len(str(p.telefono)))
            print(p.telefono)
            # message = client.messages.create(
            #     body="Adra Torrejon informa:Tenemos un anuncio importante:accede al enlace ",
            #     from_='+12025591005',
            #     to=f'+34{p.telefono}'
            # )
            #
            # # print(p.telefono)
            #
            # print(message.sid)
        # print(count)