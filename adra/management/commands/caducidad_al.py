from django.core.management.base import BaseCommand, CommandError
from django.db.models import Q
from datetime import date, datetime
from adra.models import Persona, AlmacenAlimentos
from twilio.rest import Client
from django.core.mail import send_mail
import sendgrid
from django.contrib.auth.models import User
from django.conf import settings
class Command(BaseCommand):




    def handle(self, *args, **options):
        sg = sendgrid.SendGridAPIClient(settings.SENDGRID_API_KEY)

        def caduca(fecha):
            date_format = "%Y-%m-%d"
            a = datetime.strptime(str(datetime.now().date()), date_format)
            b = datetime.strptime(str(fecha), date_format)
            delta_aceite = b - a
            return delta_aceite.days

        ali = AlmacenAlimentos.objects.all()
        emails = User.objects.filter(is_active=True).values_list('email', flat=True)
        print(emails)

        for al in ali:

            arroz_blanco = al.arroz_blanco_caducidad
            garbanzo_cocido = al.garbanzo_cocido_caducidad
            atun_sardina = al.atun_sardina_caducidad
            sardina = al.sardina_caducidad
            pasta_espagueti = al.pasta_espagueti_caducidad
            tomate_frito = al.tomate_frito_caducidad
            galletas = al.galletas_caducidad
            macedonia_verdura_conserva = al.macedonia_verdura_conserva_caducidad
            fruta_conserva_coctel = al.fruta_conserva_coctel_caducidad
            tarito_pollo = al.tarito_pollo_caducidad
            tarito_fruta = al.tarito_fruta_caducidad
            leche = al.leche_caducidad
            batido_chocolate = al.batido_chocolate_caducidad
            aceite_de_oliva = al.aceite_de_oliva_caducidad

            if caduca(arroz_blanco) == 37:
                alimento_1_name = AlmacenAlimentos._meta.get_field('arroz_blanco').verbose_name
                message = sendgrid.Mail(
                    from_email=f"admin@adra.es",
                    to_emails=["amadeuscam@yahoo.es"],
                )
                message.dynamic_template_data = {
                    "alimento": f"{alimento_1_name}",
                    "Sender_Name": f"Adra Torrejon de ardoz",
                    "Sender_Address": f"calle primavera 15",
                    "Sender_City": f"Torrejon de ardoz",
                    "Sender_State": f"Madrid",
                    "Sender_Zip": f"28850"
                }
                message.template_id = 'd-b3a251b22c7442b39b79ddc901020457'
                sg.send(message)

            if caduca(garbanzo_cocido) == 37:
                alimento_2_name = AlmacenAlimentos._meta.get_field('garbanzo_cocido').verbose_name
                message = sendgrid.Mail(
                    from_email=f"admin@adra.es",
                    to_emails=["amadeuscam@yahoo.es", "amadeuscam@gmail.com"],
                )
                message.dynamic_template_data = {
                    "alimento": f"{alimento_2_name}",
                    "Sender_Name": f"Adra Torrejon de ardoz",
                    "Sender_Address": f"calle primavera 15",
                    "Sender_City": f"Torrejon de ardoz",
                    "Sender_State": f"Madrid",
                    "Sender_Zip": f"28850"
                }
                message.template_id = 'd-b3a251b22c7442b39b79ddc901020457'
                sg.send(message)

            if caduca(atun_sardina) == 37:
                alimento_3_name = AlmacenAlimentos._meta.get_field('atun_sardina').verbose_name
                message = sendgrid.Mail(
                    from_email=f"admin@adra.es",
                    to_emails=["amadeuscam@yahoo.es", "amadeuscam@gmail.com"],
                )
                message.dynamic_template_data = {
                    "alimento": f"{alimento_3_name}",
                    "Sender_Name": f"Adra Torrejon de ardoz",
                    "Sender_Address": f"calle primavera 15",
                    "Sender_City": f"Torrejon de ardoz",
                    "Sender_State": f"Madrid",
                    "Sender_Zip": f"28850"
                }
                message.template_id = 'd-b3a251b22c7442b39b79ddc901020457'
                sg.send(message)

            if caduca(sardina) == 37:
                alimento_4_name = AlmacenAlimentos._meta.get_field('sardina').verbose_name
                message = sendgrid.Mail(
                    from_email=f"admin@adra.es",
                    to_emails=["amadeuscam@yahoo.es", "amadeuscam@gmail.com"],
                )
                message.dynamic_template_data = {
                    "alimento": f"{alimento_4_name}",
                    "Sender_Name": f"Adra Torrejon de ardoz",
                    "Sender_Address": f"calle primavera 15",
                    "Sender_City": f"Torrejon de ardoz",
                    "Sender_State": f"Madrid",
                    "Sender_Zip": f"28850"
                }
                message.template_id = 'd-b3a251b22c7442b39b79ddc901020457'
                sg.send(message)

            if caduca(pasta_espagueti) == 37:
                alimento_5_name = AlmacenAlimentos._meta.get_field('pasta_espagueti').verbose_name
                message = sendgrid.Mail(
                    from_email=f"admin@adra.es",
                    to_emails=["amadeuscam@yahoo.es", "amadeuscam@gmail.com"],
                )
                message.dynamic_template_data = {
                    "alimento": f"{alimento_5_name}",
                    "Sender_Name": f"Adra Torrejon de ardoz",
                    "Sender_Address": f"calle primavera 15",
                    "Sender_City": f"Torrejon de ardoz",
                    "Sender_State": f"Madrid",
                    "Sender_Zip": f"28850"
                }
                message.template_id = 'd-b3a251b22c7442b39b79ddc901020457'
                sg.send(message)

            if caduca(tomate_frito) == 37:
                alimento_6_name = AlmacenAlimentos._meta.get_field('tomate_frito').verbose_name
                message = sendgrid.Mail(
                    from_email=f"admin@adra.es",
                    to_emails=["amadeuscam@yahoo.es", "amadeuscam@gmail.com"],
                )
                message.dynamic_template_data = {
                    "alimento": f"{alimento_6_name}",
                    "Sender_Name": f"Adra Torrejon de ardoz",
                    "Sender_Address": f"calle primavera 15",
                    "Sender_City": f"Torrejon de ardoz",
                    "Sender_State": f"Madrid",
                    "Sender_Zip": f"28850"
                }
                message.template_id = 'd-b3a251b22c7442b39b79ddc901020457'
                sg.send(message)

            if caduca(galletas) == 37:
                alimento_7_name = AlmacenAlimentos._meta.get_field('galletas').verbose_name
                message = sendgrid.Mail(
                    from_email=f"admin@adra.es",
                    to_emails=["amadeuscam@yahoo.es", "amadeuscam@gmail.com"],
                )
                message.dynamic_template_data = {
                    "alimento": f"{alimento_7_name}",
                    "Sender_Name": f"Adra Torrejon de ardoz",
                    "Sender_Address": f"calle primavera 15",
                    "Sender_City": f"Torrejon de ardoz",
                    "Sender_State": f"Madrid",
                    "Sender_Zip": f"28850"
                }
                message.template_id = 'd-b3a251b22c7442b39b79ddc901020457'
                sg.send(message)

            if caduca(macedonia_verdura_conserva) == 37:
                alimento_8_name = AlmacenAlimentos._meta.get_field('macedonia_verdura_conserva').verbose_name
                message = sendgrid.Mail(
                    from_email=f"admin@adra.es",
                    to_emails=["amadeuscam@yahoo.es", "amadeuscam@gmail.com"],
                )
                message.dynamic_template_data = {
                    "alimento": f"{alimento_8_name}",
                    "Sender_Name": f"Adra Torrejon de ardoz",
                    "Sender_Address": f"calle primavera 15",
                    "Sender_City": f"Torrejon de ardoz",
                    "Sender_State": f"Madrid",
                    "Sender_Zip": f"28850"
                }
                message.template_id = 'd-b3a251b22c7442b39b79ddc901020457'
                sg.send(message)

            if caduca(fruta_conserva_coctel) == 37:
                alimento_9_name = AlmacenAlimentos._meta.get_field('fruta_conserva_coctel').verbose_name
                message = sendgrid.Mail(
                    from_email=f"admin@adra.es",
                    to_emails=["amadeuscam@yahoo.es", "amadeuscam@gmail.com"],
                )
                message.dynamic_template_data = {
                    "alimento": f"{alimento_9_name}",
                    "Sender_Name": f"Adra Torrejon de ardoz",
                    "Sender_Address": f"calle primavera 15",
                    "Sender_City": f"Torrejon de ardoz",
                    "Sender_State": f"Madrid",
                    "Sender_Zip": f"28850"
                }
                message.template_id = 'd-b3a251b22c7442b39b79ddc901020457'
                sg.send(message)

            if caduca(tarito_pollo) == 37:
                alimento_10_name = AlmacenAlimentos._meta.get_field('tarito_pollo').verbose_name
                message = sendgrid.Mail(
                    from_email=f"admin@adra.es",
                    to_emails=["amadeuscam@yahoo.es", "amadeuscam@gmail.com"],
                )
                message.dynamic_template_data = {
                    "alimento": f"{alimento_10_name}",
                    "Sender_Name": f"Adra Torrejon de ardoz",
                    "Sender_Address": f"calle primavera 15",
                    "Sender_City": f"Torrejon de ardoz",
                    "Sender_State": f"Madrid",
                    "Sender_Zip": f"28850"
                }
                message.template_id = 'd-b3a251b22c7442b39b79ddc901020457'
                sg.send(message)

            if caduca(tarito_fruta) == 37:
                alimento_11_name = AlmacenAlimentos._meta.get_field('tarito_fruta').verbose_name
                message = sendgrid.Mail(
                    from_email=f"admin@adra.es",
                    to_emails=["amadeuscam@yahoo.es", "amadeuscam@gmail.com"],
                )
                message.dynamic_template_data = {
                    "alimento": f"{alimento_11_name}",
                    "Sender_Name": f"Adra Torrejon de ardoz",
                    "Sender_Address": f"calle primavera 15",
                    "Sender_City": f"Torrejon de ardoz",
                    "Sender_State": f"Madrid",
                    "Sender_Zip": f"28850"
                }
                message.template_id = 'd-b3a251b22c7442b39b79ddc901020457'
                sg.send(message)

            if caduca(leche) == 37:
                alimento_12_name = AlmacenAlimentos._meta.get_field('leche').verbose_name
                message = sendgrid.Mail(
                    from_email=f"admin@adra.es",
                    to_emails=["amadeuscam@yahoo.es", "amadeuscam@gmail.com"],
                )
                message.dynamic_template_data = {
                    "alimento": f"{alimento_12_name}",
                    "Sender_Name": f"Adra Torrejon de ardoz",
                    "Sender_Address": f"calle primavera 15",
                    "Sender_City": f"Torrejon de ardoz",
                    "Sender_State": f"Madrid",
                    "Sender_Zip": f"28850"
                }
                message.template_id = 'd-b3a251b22c7442b39b79ddc901020457'
                sg.send(message)

            if caduca(batido_chocolate) == 37:
                alimento_12_name = AlmacenAlimentos._meta.get_field('batido_chocolate').verbose_name
                message = sendgrid.Mail(
                    from_email=f"admin@adra.es",
                    to_emails=["amadeuscam@yahoo.es", "amadeuscam@gmail.com"],
                )
                message.dynamic_template_data = {
                    "alimento": f"{alimento_12_name}",
                    "Sender_Name": f"Adra Torrejon de ardoz",
                    "Sender_Address": f"calle primavera 15",
                    "Sender_City": f"Torrejon de ardoz",
                    "Sender_State": f"Madrid",
                    "Sender_Zip": f"28850"
                }
                message.template_id = 'd-b3a251b22c7442b39b79ddc901020457'
                sg.send(message)

            if caduca(aceite_de_oliva) == 37:
                alimento_13_name = AlmacenAlimentos._meta.get_field('aceite_de_oliva').verbose_name
                message = sendgrid.Mail(
                    from_email=f"admin@adra.es",
                    to_emails=["amadeuscam@yahoo.es", "amadeuscam@gmail.com"],
                )
                message.dynamic_template_data = {
                    "alimento": f"{alimento_13_name}",
                    "Sender_Name": f"Adra Torrejon de ardoz",
                    "Sender_Address": f"calle primavera 15",
                    "Sender_City": f"Torrejon de ardoz",
                    "Sender_State": f"Madrid",
                    "Sender_Zip": f"28850"
                }
                message.template_id = 'd-b3a251b22c7442b39b79ddc901020457'
                sg.send(message)
