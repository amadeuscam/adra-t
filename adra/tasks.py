import subprocess
from datetime import datetime
import sendgrid
from django.conf import settings
from celery.schedules import crontab
from celery.utils.log import get_task_logger
from adra_project.celery import app
from adra.api_consume.get_api_data import get_caducidades

logger = get_task_logger(__name__)


def send_email_sendgrid(name: str, email_lst: list) -> None:
    sg = sendgrid.SendGridAPIClient(settings.SENDGRID_API_KEY)
    message = sendgrid.Mail(
        from_email="admin@adra.es",
        subject=f'El {name} va a caducar pronto',
        to_emails=email_lst,
    )
    message.dynamic_template_data = {
        "alimento": f"{name}",
        "Sender_Name": "Adra Torrejon de ardoz",
        "Sender_Address": "calle primavera 15",
        "Sender_City": "Torrejon de ardoz",
        "Sender_State": "Madrid",
        "Sender_Zip": "28850"
    }
    message.template_id = 'd-b3a251b22c7442b39b79ddc901020457'
    res = sg.send(message)


def check_caducidad(fecha):
    date_format = "%Y-%m-%d"
    a = datetime.strptime(str(datetime.now().date()), date_format)
    b = datetime.strptime(str(fecha), date_format)
    delta_aceite = b - a
    return delta_aceite.days


@app.on_after_finalize.connect
def setup_periodic_tasks(**kwargs):
    # Executes every day  at 8 am
    app.add_periodic_task(crontab(minute=0, hour='8'), caducidad_alimentos,
                          name="comprobar las caducidades de los alimentos")
    # Executes every day  at 6 am and 18 pm
    app.add_periodic_task(crontab(minute=0, hour='6,18'), restart_telefram_bot,
                          name="reiniciar el bot de telegram")
    # Executes every sunday at 15:15 pm
    app.add_periodic_task(crontab(hour=15, minute=15, day_of_week='sun'), make_backup_mysql,
                          name="hacer una copia de la base de datos")


@app.task
def caducidad_alimentos():
    ds = get_caducidades(['almacen', 'users'])

    users_data = ds['users']
    data_aliemntos = ds['almacen'][0]

    list_email = [e['email'] for e in users_data]

    for number in range(1, 13):
        if check_caducidad(data_aliemntos[f'alimento_{number}_caducidad']) == 37:
            send_email_sendgrid(data_aliemntos[f'alimento_{number}_name'], list_email)


@app.task
def restart_telefram_bot():
    subprocess.call(["supervisorctl", "restart", "telegram"])


@app.task
def make_backup_mysql():
    username = settings.USER_DB
    password = settings.PASSWORD_DB
    database = settings.NAME_DB

    command_line = f"mysqldump -u {username} -p{password}  {database} > /home/lucian/adra-t/backup_mysql/{datetime.now().day}-{datetime.now().month}.sql"
    dc = subprocess.Popen(command_line, shell=True)
    dc.wait()

# @shared_task
# def restart():
#     print("borrar la carpeta de los zip")
#     shutil.rmtree('./valoracion')
#
#
# @shared_task
# def export_zip(fecha):
#     persona = Persona.objects.filter(active=True).exclude(covid=True).order_by("numero_adra")
#
#     dirN = "./valoracion"
#     if not os.path.exists(dirN):
#         os.makedirs(dirN)
#         print("Directory ", dirN, " created")
#     else:
#         print("Directory ", dirN, " exists")
#
#     template = "./vl.docx"
#     for p in persona:
#         print(p.nombre_apellido)
#         hijos = []
#         document = MailMerge(template)
#         for h in p.hijo.all():
#             hijo_dict = {}
#             hijo_dict['parentesco'] = f'{h.parentesco}'
#             hijo_dict['nombre_apellido_hijo'] = f'{h.nombre_apellido}'
#             hijo_dict['dni_hijo'] = f'{h.dni}'
#             hijo_dict['fecha_nacimiento_hijo'] = f"{'{:%d-%m-%Y}'.format(h.fecha_nacimiento)}"
#             hijos.append(hijo_dict)
#         document.merge(
#             numar_adra=f'{p.numero_adra}',
#             nombre_apellido=f'{p.nombre_apellido}',
#             dni=f'{p.dni}',
#             fecha_nacimiento=f"{'{:%d-%m-%Y}'.format(p.fecha_nacimiento)}",
#             nacionalidad=f'{p.nacionalidad}',
#             domicilio=f'{p.domicilio}',
#             ciudad=f'{p.ciudad}',
#             numar_telefon=f'{p.telefono}',
#             # fecha_hoy=f"{'{:%d-%m-%Y}'.format(date.today())}",
#             fecha_hoy=f"{fecha}",
#
#         )
#         if p.empadronamiento:
#             document.merge(a="x")
#         if p.libro_familia:
#             document.merge(b="x")
#         if p.fotocopia_dni:
#             document.merge(c="x")
#         if p.prestaciones:
#             document.merge(d="x")
#         if p.nomnia:
#             document.merge(e="x")
#         if p.cert_negativo:
#             document.merge(f="x")
#         if p.aquiler_hipoteca:
#             document.merge(g="x")
#         if p.recibos:
#             document.merge(h="x")
#         document.merge_rows('parentesco', hijos)
#         document.write(f'./valoracion/{p.numero_adra}.docx')
#
#     filenames = []
#     os.chdir("./valoracion")
#     for file in glob.glob("*.docx"):
#         filenames.append(str(file))
#
#     zip_subdir = f"valoracion_social"
#     zip_filename = "%s.zip" % zip_subdir
#
#     # Open StringIO to grab in-memory ZIP contents
#     zip_io = BytesIO()
#     # response = HttpResponse(content_type='application/zip')
#     # The zip compressor
#     print(filenames)
#     with zipfile.ZipFile(zip_io, mode='w', compression=zipfile.ZIP_BZIP2) as backup_zip:
#
#         for file in filenames:
#             # Calculate path for file in zip
#             fdir, fname = os.path.split(file)
#             zip_path = os.path.join(zip_subdir, fname)
#             # # Add file, at correct path
#             backup_zip.write(file, zip_path)
#
#     response = HttpResponse(zip_io.getvalue(), content_type="application/x-zip-compressed")
#     response['Content-Disposition'] = 'attachment; filename=%s' % zip_filename
#     return response
