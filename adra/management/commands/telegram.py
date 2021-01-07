from django.contrib.sites import requests
from django.core.management.base import BaseCommand, CommandError
from django.db.models import Q

from adra.models import Persona
import logging
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
import telegram
from django.conf import settings
import subprocess
import io

class Command(BaseCommand):

    def handle(self, *args, **options):
        # Enable logging
        logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                            level=logging.INFO)

        logger = logging.getLogger(__name__)

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
            try:
                beneficiario = int(context.args[0])
                persona = Persona.objects.get(telefono=beneficiario)
                update.message.reply_text(f"Hola {persona.nombre_apellido}!,\n "
                                          f"Tu numero adra es {persona.numero_adra} y "
                                          f"perteneces al domingo  {persona.domingo}"
                                          )
                update.message.reply_text(f"Papeles\n\nEmpadronamiento->{'Tienes' if persona.empadronamiento else 'No tienes'}!,"
                                          f"\n Libro familia->{ 'Tienes' if persona.libro_familia else 'No tienes'}"
                                          f"\n Fotocopia dni->{ 'Tienes' if persona.fotocopia_dni else 'No tienes'}"
                                          f"\n Prestaciones->{ 'Tienes' if persona.prestaciones else 'No tienes'}"
                                          f"\n Nomnia->{ 'Tienes' if persona.nomnia else 'No tienes'}"
                                          f"\n Certificado negativo->{ 'Tienes' if persona.cert_negativo else 'No tienes'}"
                                          f"\n Aquiler O Hipoteca ->{ 'Tienes' if persona.aquiler_hipoteca else 'No tienes'}"
                                          f"\n Recibos -> { 'Tienes' if persona.recibos else 'No tienes'}"
                                          )
            except Persona.DoesNotExist:
                update.message.reply_text("El beneficario no existe!")

        def status_servers(update, context):
            """Send a message when the command /help is issued."""
            p = subprocess.Popen(['supervisorctl', 'status'], stdout=subprocess.PIPE)
            # status = p.stdout.read()
            # print(status)
            for line in io.TextIOWrapper(p.stdout, encoding="utf-8"):
                update.message.reply_text(f'{ str(line)}')


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

        # bot = telegram.Bot(token=settings.TELEGRAM_TOKEN_KEY)
        # # print(bot.getUpdates())
        # persona = Persona.objects.filter(active=True).filter(Q(domingo="Domingo 1") | Q(domingo=1), ciudad__icontains="Torrejon de ardoz").exclude(covid=True)
        # per_list = [p.nombre_apellido for p in persona]
        # print(len(per_list))
        # bot.send_message('-1001438819726', f"*{per_list}*",parse_mode=telegram.ParseMode.MARKDOWN_V2)
