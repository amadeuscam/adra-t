from django.core.management.base import BaseCommand, CommandError
from datetime import date
from adra.models import Persona
from mailmerge import MailMerge


class Command(BaseCommand):

    def handle(self, *args, **options):
        persona = Persona.objects.all()

        for p in persona:
            if p.active:
                # print(p.nombre_apellido)
                template = "0_VALORACIÓN_SOCIAL.docx"
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
                    fecha_hoy=f"{'{:%d-%m-%Y}'.format(date.today())}"
                )
                document.merge_rows('parentesco', hijos)

                document.write(f'./valoraciones/{p.numero_adra}.docx')
