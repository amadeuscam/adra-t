from django.core.management.base import BaseCommand, CommandError
from datetime import date
from adra.models import Persona
from mailmerge import MailMerge
from pathlib import Path
import shutil
import time
import glob, os

class Command(BaseCommand):

    def handle(self, *args, **options):
        persona = Persona.objects.filter(active=True,numero_adra__gt=203,numero_adra__lt=229).order_by("numero_adra")
        Path("./valoracion").mkdir(parents=True, exist_ok=True)

        for p in persona[10:50]:

            print(p.numero_adra)
            # print(p.nombre_apellido)
            template = "adra/management/commands/vl.docx"
            document = MailMerge(template)
            # print(document.get_merge_fields())
            hijos = []

            for h in p.hijo.all():
                hijo_dict = {}
                hijo_dict['parentesco'] = f'{h.parentesco}'
                hijo_dict['nombre_apellido_hijo'] = f'{h.nombre_apellido}'
                hijo_dict['dni_hijo'] = f'{h.dni}'
                hijo_dict['fecha_nacimiento_hijo'] = f"{'{:%d-%m-%Y}'.format(h.fecha_nacimiento)}"
                hijos.append(hijo_dict)
            document.merge(
                numar_adra=f'{p.numero_adra}',
                nombre_apellido=f'{p.nombre_apellido}',
                dni=f'{p.dni}',
                fecha_nacimiento=f"{'{:%d-%m-%Y}'.format(p.fecha_nacimiento)}",
                nacionalidad=f'{p.nacionalidad}',
                domicilio=f'{p.domicilio}',
                ciudad=f'{p.ciudad}',
                numar_telefon=f'{p.telefono}',
                # fecha_hoy=f"{'{:%d-%m-%Y}'.format(p.created_at)}",
                fecha_hoy=f"03-02-2020",

            )
            if p.empadronamiento:
                document.merge(a = "x")
            if p.libro_familia:
                document.merge(b = "x")
            if p.fotocopia_dni:
                document.merge(c = "x")
            if p.prestaciones:
                document.merge(d = "x")
            if p.nomnia:
                document.merge(e = "x")
            if p.cert_negativo:
                document.merge(f = "x")
            if p.aquiler_hipoteca:
                document.merge(g="x")
            if p.recibos:
                document.merge(h="x")
            document.merge_rows('parentesco', hijos)

            document.write(f'./valoracion/{p.numero_adra}.docx')


        os.chdir("./valoracion")
        for file in glob.glob("*.docx"):
            print(file)

        time.sleep(10)
        shutil.rmtree('./valoracion', ignore_errors=True)
