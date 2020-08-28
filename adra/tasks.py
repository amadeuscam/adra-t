from datetime import datetime
import sendgrid
from celery.decorators import periodic_task
from celery.task.schedules import crontab
from django.contrib.auth.models import User
from .models import AlmacenAlimentos
from django.conf import settings
import  subprocess
# crontab(minute=0, hour='6,18')
@periodic_task(
    run_every=crontab(minute=0, hour='5,20'),
    name="caducidad_alimentos",
    ignore_result=True
)
def caducidad_alimentos():

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

            alimento_1 = al.alimento_1_caducidad
            alimento_2 = al.alimento_2_caducidad
            alimento_3 = al.alimento_3_caducidad
            alimento_4 = al.alimento_4_caducidad
            alimento_6 = al.alimento_6_caducidad
            alimento_7 = al.alimento_7_caducidad
            alimento_8 = al.alimento_8_caducidad
            alimento_9 = al.alimento_9_caducidad
            alimento_10 = al.alimento_10_caducidad
            alimento_11 = al.alimento_11_caducidad
            alimento_12 = al.alimento_12_caducidad
            alimento_13 = al.alimento_13_caducidad
            alimento_14 = al.alimento_14_caducidad
            alimento_15 = al.alimento_15_caducidad
            print(caduca(alimento_1))

            if caduca(alimento_1) == 37:
                alimento_1_name = AlmacenAlimentos._meta.get_field('alimento_1').verbose_name

                message = sendgrid.Mail(
                    from_email=f"admin@adra.es",
                    to_emails=emails,
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
            if caduca(alimento_2) == 37:
                alimento_2_name = AlmacenAlimentos._meta.get_field('alimento_2').verbose_name
                message = sendgrid.Mail(
                    from_email=f"admin@adra.es",
                    to_emails=emails,
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

            if caduca(alimento_3) == 37:
                alimento_3_name = AlmacenAlimentos._meta.get_field('alimento_3').verbose_name
                message = sendgrid.Mail(
                    from_email=f"admin@adra.es",
                    to_emails=emails,
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

            if caduca(alimento_4) == 37:
                alimento_4_name = AlmacenAlimentos._meta.get_field('alimento_4').verbose_name
                message = sendgrid.Mail(
                    from_email=f"admin@adra.es",
                    to_emails=emails,
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

            if caduca(alimento_6) == 37:
                alimento_6_name = AlmacenAlimentos._meta.get_field('alimento_6').verbose_name
                message = sendgrid.Mail(
                    from_email=f"admin@adra.es",
                    to_emails=emails,
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

            if caduca(alimento_7) == 37:
                alimento_7_name = AlmacenAlimentos._meta.get_field('alimento_7').verbose_name
                message = sendgrid.Mail(
                    from_email=f"admin@adra.es",
                    to_emails=emails,
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

            if caduca(alimento_8) == 37:
                alimento_8_name = AlmacenAlimentos._meta.get_field('alimento_8').verbose_name
                message = sendgrid.Mail(
                    from_email=f"admin@adra.es",
                    to_emails=emails,
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

            if caduca(alimento_9) == 37:
                alimento_9_name = AlmacenAlimentos._meta.get_field('alimento_9').verbose_name
                message = sendgrid.Mail(
                    from_email=f"admin@adra.es",
                    to_emails=emails,
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

            if caduca(alimento_10) == 37:
                alimento_10_name = AlmacenAlimentos._meta.get_field('alimento_10').verbose_name
                message = sendgrid.Mail(
                    from_email=f"admin@adra.es",
                    to_emails=emails,
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

            if caduca(alimento_11) == 37:
                alimento_11_name = AlmacenAlimentos._meta.get_field('alimento_11').verbose_name
                message = sendgrid.Mail(
                    from_email=f"admin@adra.es",
                    to_emails=emails,
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

            if caduca(alimento_12) == 37:
                alimento_12_name = AlmacenAlimentos._meta.get_field('alimento_12').verbose_name
                message = sendgrid.Mail(
                    from_email=f"admin@adra.es",
                    to_emails=emails,
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

            if caduca(alimento_13) == 37:
                alimento_13_name = AlmacenAlimentos._meta.get_field('alimento_13').verbose_name
                message = sendgrid.Mail(
                    from_email=f"admin@adra.es",
                    to_emails=emails,
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

            if caduca(alimento_14) == 37:
                alimento_14_name = AlmacenAlimentos._meta.get_field('alimento_14').verbose_name
                message = sendgrid.Mail(
                    from_email=f"admin@adra.es",
                    to_emails=emails,
                )
                message.dynamic_template_data = {
                    "alimento": f"{alimento_14_name}",
                    "Sender_Name": f"Adra Torrejon de ardoz",
                    "Sender_Address": f"calle primavera 15",
                    "Sender_City": f"Torrejon de ardoz",
                    "Sender_State": f"Madrid",
                    "Sender_Zip": f"28850"
                }
                message.template_id = 'd-b3a251b22c7442b39b79ddc901020457'
                sg.send(message)

            if caduca(alimento_15) == 37:
                alimento_15_name = AlmacenAlimentos._meta.get_field('alimento_15').verbose_name
                message = sendgrid.Mail(
                    from_email=f"admin@adra.es",
                    to_emails=emails,
                )
                message.dynamic_template_data = {
                    "alimento": f"{alimento_15_name}",
                    "Sender_Name": f"Adra Torrejon de ardoz",
                    "Sender_Address": f"calle primavera 15",
                    "Sender_City": f"Torrejon de ardoz",
                    "Sender_State": f"Madrid",
                    "Sender_Zip": f"28850"
                }
                message.template_id = 'd-b3a251b22c7442b39b79ddc901020457'
                sg.send(message)


@periodic_task(
    run_every=crontab(minute=2),
    name="restart_telefram_bot",
    ignore_result=True
)
def restart_telefram_bot:
    subprocess.call(["supervisorctl", "restart", "telegram"])


