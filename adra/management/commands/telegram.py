import io
import json
import logging
import subprocess
import requests
from django.conf import settings
from django.core.management.base import BaseCommand
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters


class Command(BaseCommand):

    def handle(self, *args, **options):

        token = settings.TOKEN_KEY_USER

        # Enable logging
        logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                            level=logging.INFO)

        # logger = logging.getLogger(__name__)

        # Define a few command handlers. These usually take the two arguments update and
        # context. Error handlers also receive the raised TelegramError object in error.
        def start(update, context):
            """Send a message when the command /start is issued."""
            update.message.reply_text('Hi world!')

        def help_command(update, context):
            """Send a message when the command /help is issued."""
            update.message.reply_text('Help brother!')

        def numero_adra_command(update, context):
            """Send a message when the command /help is issued."""

            beneficiario = int(context.args[0])

            # hace una llamada a la api por los datos del beneficiario
            url = f'{settings.SITE_DOAMIN}api/personas/{beneficiario}/'
            headers = {'Authorization': f'Token {token}', 'Content-Type': 'application/json'}
            r = requests.get(url, headers=headers)
            data = json.loads(r.content.decode('utf-8'))
            if data:
                update.message.reply_text(f"Hola {data['nombre_apellido']}!,\n "
                                          f"Tu numero adra es {data['numero_adra']} y "
                                          f"perteneces al domingo  {data['domingo']}"
                                          )
                update.message.reply_text(
                    f"Papeles\n\nEmpadronamiento->{'Tienes' if data['empadronamiento'] else 'No tienes'}!,"
                    f"\n Libro familia->{'Tienes' if data['libro_familia'] else 'No tienes'}"
                    f"\n Fotocopia dni->{'Tienes' if data['fotocopia_dni'] else 'No tienes'}"
                    f"\n Prestaciones->{'Tienes' if data['prestaciones'] else 'No tienes'}"
                    f"\n Nomnia->{'Tienes' if data['nomnia'] else 'No tienes'}"
                    f"\n Certificado negativo->{'Tienes' if data['cert_negativo'] else 'No tienes'}"
                    f"\n Aquiler O Hipoteca ->{'Tienes' if data['aquiler_hipoteca'] else 'No tienes'}"
                    f"\n Recibos -> {'Tienes' if data['recibos'] else 'No tienes'}"
                )
            else:
                update.message.reply_text("El beneficario no existe!")

        def status_servers(update, context):
            """Send a message when the command /help is issued."""
            p = subprocess.Popen(['supervisorctl', 'status'], stdout=subprocess.PIPE)
            # status = p.stdout.read()
            # print(status)
            for line in io.TextIOWrapper(p.stdout, encoding="utf-8"):
                update.message.reply_text(f'{str(line)}')

        def echo(update, context):
            """Echo the user message."""
            update.message.reply_text(update.message.text)

        """Start the bot."""
        # Create the Updater and pass it your bot's token.
        # Make sure to set use_context=True to use the new context based callbacks
        # Post version 12 this will no longer be necessary
        updater = Updater(settings.TELEGRAM_TOKEN_KEY, use_context=True)

        # Get the dispatcher to register handlers
        dp = updater.dispatcher

        # on different commands - answer in Telegram
        dp.add_handler(CommandHandler("start", start))
        dp.add_handler(CommandHandler("help", help_command))
        dp.add_handler(CommandHandler("buscar", numero_adra_command))
        dp.add_handler(CommandHandler("status", status_servers))

        # on noncommand i.e message - echo the message on Telegram
        dp.add_handler(MessageHandler(Filters.text, echo))

        # Start the Bot
        updater.start_polling()

        # Run the bot until you press Ctrl-C or the process receives SIGINT,
        # SIGTERM or SIGABRT. This should be used most of the time, since
        # start_polling() is non-blocking and will stop the bot gracefully.
        updater.idle()
