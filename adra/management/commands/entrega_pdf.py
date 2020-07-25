from django.core.management.base import BaseCommand, CommandError
from datetime import date
from adra.models import Persona
from mailmerge import MailMerge
import os
from django.conf import settings
from PyPDF2 import PdfFileReader, PdfFileWriter
from PyPDF2.generic import BooleanObject, NameObject, IndirectObject


class Command(BaseCommand):

    def handle(self, *args, **options):

        def set_need_appearances_writer(writer):
            # See 12.7.2 and 7.7.2 for more information:
            # http://www.adobe.com/content/dam/acom/en/devnet/acrobat/pdfs/PDF32000_2008.pdf
            try:
                catalog = writer._root_object
                # get the AcroForm tree and add "/NeedAppearances attribute
                if "/AcroForm" not in catalog:
                    writer._root_object.update({
                        NameObject("/AcroForm"): IndirectObject(len(writer._objects), 0, writer)})

                need_appearances = NameObject("/NeedAppearances")
                writer._root_object["/AcroForm"][need_appearances] = BooleanObject(
                    True)
                return writer

            except Exception as e:
                print('set_need_appearances_writer() catch : ', repr(e))
                return writer

        def calculate_age(age):
            today = date.today()
            return today.year - age.year - ((today.month, today.day) < (age.month, age.day))

        infile = file_path = os.path.join(settings.PROJECT_ROOT, 'entrega2020.pdf')
        inputStream = open(infile, "rb")
        pdf_reader = PdfFileReader(inputStream, strict=False)
        if "/AcroForm" in pdf_reader.trailer["/Root"]:
            pdf_reader.trailer["/Root"]["/AcroForm"].update(
                {NameObject("/NeedAppearances"): BooleanObject(True)})

        pdf_writer = PdfFileWriter()
        set_need_appearances_writer(pdf_writer)
        if "/AcroForm" in pdf_writer._root_object:
            pdf_writer._root_object["/AcroForm"].update(
                {NameObject("/NeedAppearances"): BooleanObject(True)})

        # personas = Persona.objects.exclude(covid=True).exclude(active=False)
        personas = Persona.objects.filter(active=True).exclude(covid=True)
        # print([ p.nombre_apellido for p in personas])
        # print(personas.count())
        pdf_writer.addPage(pdf_reader.getPage(0))
        for persona in personas:
            if persona.active:
                print(persona.id)
                familiares = persona.hijo.all()
                familiares_gr = persona.hijo.filter(edad__gt=3)
                # print(familiares_pq.count())
                mayores = 0
                menores = 0
                for f in familiares:
                    if calculate_age(f.fecha_nacimiento) > 3:
                        mayores += 1
                    else:
                        menores += 1

                print(mayores)
                print(menores)
                field_dictionary = {
                    "NombreOAR": "ADRA TORREJON",
                    "DireccioOAR": "C/ Primavera 15",
                    "Nombre y apellidos del representante de la unidad familiar": f"{persona.nombre_apellido}",
                    "DNINIEPasaporte 1": f"{persona.dni}",
                    "Teléfono": f"{persona.telefono}",
                    "Domicilio": f"{persona.domicilio}",
                    "Localidad": f"{persona.ciudad}",
                    "CP": "28850",
                    "TOTAL MIEMBROS UNIDAD FAMILIAR": f"{mayores + menores + 1}",
                    "Niños 02 ambos inclusive": f"{menores}",
                    "numarAdra": f"{persona.numero_adra}"
                }

                pdf_writer.updatePageFormFieldValues(
                    pdf_writer.getPage(0), field_dictionary)

                # outputStream = open(outfile, "wb")
                # pdf_writer.write(outputStream)

                # outputStream.close()
                # pdf_writer.encrypt(str.lower(f"{persona.numero_adra}"))
                with open(f"./entregas/{persona.numero_adra}.pdf", "wb") as out_file:
                    pdf_writer.write(out_file)


                # extractedPage = open(pdf_file_path, 'rb')
                # response = HttpResponse(content_type='application/pdf')
                # response['Content-Disposition'] = f'attachment;filename="{persona.numero_adra}.pdf"'
                # pdf_writer.write(stream=f'./entregas/{persona.numero_adra}.pdf')
                # inputStream.close()
