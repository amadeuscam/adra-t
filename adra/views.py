import json
import os
import xlsxwriter
from django.conf import settings
from django.contrib import messages
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Sum
from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import (ListView, DetailView,
                                  DeleteView,
                                  UpdateView,
                                  CreateView)

from .filters import AlimentosFilters
from .forms import AlimentosFrom, HijoForm, PersonaForm, ProfileEditForm, UserEditForm
from .models import Persona, Alimentos, AlmacenAlimentos, Hijo, Profile
from django.http import HttpResponse, JsonResponse, request, HttpRequest
import io
from django.db.models import Q
import xlwt
from openpyxl import Workbook
from openpyxl.styles import Alignment, Side, PatternFill
from datetime import date
from mailmerge import MailMerge
from .serializers import PersonaSerializer, UserSerializer
from rest_framework.parsers import JSONParser
from rest_framework.decorators import api_view
from django.contrib.auth.models import User
from rest_framework import permissions
from rest_framework import viewsets
from django.utils.translation import ugettext as _
from django.contrib.auth import get_user_model
from django.urls import reverse_lazy
from PyPDF2 import PdfFileReader, PdfFileWriter
from PyPDF2.generic import BooleanObject, NameObject, IndirectObject
from django.http import FileResponse
from django.contrib import messages
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import (
    Mail, Subject, To, ReplyTo, SendAt, Content, From, CustomArg, Header)

from allauth.account.adapter import DefaultAccountAdapter
from django.conf import settings


# Create your views here.


@login_required
def edit(request):
    if request.method == 'POST':
        user_form = UserEditForm(instance=request.user, data=request.POST)
        profile_form = ProfileEditForm(
            instance=request.user.profile,
            data=request.POST,
            files=request.FILES)
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(
                request, 'El perfil se ha actualizado correctamente')
            return redirect('adra:edit-profile')
        else:
            messages.error(request, 'Error updating your profile')
    else:
        user_form = UserEditForm(instance=request.user)
        profile_form = ProfileEditForm(instance=request.user.profile)
    return render(request,
                  'account/edit-perfile.html',
                  {'user_form': user_form,
                   'profile_form': profile_form})


class PersonaListView(LoginRequiredMixin, ListView):
    template_name = 'adra/index.html'
    context_object_name = 'ultima_persona'
    model = Persona
    paginate_by = 15
    login_url = 'account_login'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # enviar al misma pagina varios contextos
        context['hijo'] = Hijo.objects
        context['hijomenor'] = Hijo
        context['nbar'] = "home"

        return context


# ir a la pagina detallada de cada persona
class PersonaDetailView(LoginRequiredMixin, DetailView):
    model = Persona
    template_name = 'adra/detail.html'
    context_object_name = 'persona'
    login_url = 'account_login'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['filter'] = AlimentosFilters(self.request.GET,
                                             queryset=self.get_queryset())
        return context


class BuscarDetailView(LoginRequiredMixin, ListView):
    model = Alimentos
    template_name = 'busqueda_a/view.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['filter'] = AlimentosFilters(self.request.GET,
                                             queryset=self.get_queryset())
        return context


class PersonaCreateView(LoginRequiredMixin, CreateView):
    model = Persona
    success_url = '/'
    form_class = PersonaForm

    def form_valid(self, form):
        form.instance.modificado_por = self.request.user
        messages.add_message(self.request, messages.SUCCESS, f'Beneficiaru sa adaugat cu success!')
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        try:
            p = Persona.objects.latest('created_at')
            context['nbar'] = "create"
            context['bas'] = p
            return context
        except Persona.DoesNotExist:
            pass


class PersonaUpdateView(LoginRequiredMixin, SuccessMessageMixin, UpdateView):
    model = Persona
    fields = [
        'nombre_apellido',
        'dni',
        'fecha_nacimiento',
        'numero_adra',
        'nacionalidad',
        'domicilio',
        'are_acte',
        'ciudad',
        'telefono',
        'mensaje',
        'sexo',
        'discapacidad',
        'domingo',
        'empadronamiento',
        'libro_familia',
        'fotocopia_dni',
        'prestaciones',
        'nomnia',
        'cert_negativo',
        'aquiler_hipoteca',
        'recibos',
        'email',
        'covid'
    ]
    success_message = 'Datele sau salvat cu success!!'

    def form_valid(self, form):
        form.instance.modificado_por = self.request.user
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['up'] = "update"
        return context


class PersonaDeleteView(LoginRequiredMixin, SuccessMessageMixin, DeleteView):
    model = Persona
    success_message = 'Beneficirio borrado corectamente'
    success_url = '/'


def adauga_alimentos_persona(request, pk):
    persona = get_object_or_404(Persona, pk=pk)
    almacen = AlmacenAlimentos.objects.get(pk=1)

    if request.method == 'POST':
        a_form = AlimentosFrom(request.POST)
        if a_form.is_valid():
            alimentos = a_form.save(commit=False)

            almacen.alimento_1 -= alimentos.alimento_1
            almacen.alimento_2 -= alimentos.alimento_2
            almacen.alimento_3 -= alimentos.alimento_3
            almacen.alimento_4 -= alimentos.alimento_4
            # almacen.alimento_5 -= alimentos.alimento_5
            almacen.alimento_6 -= alimentos.alimento_6
            almacen.alimento_7 -= alimentos.alimento_7
            almacen.alimento_8 -= alimentos.alimento_8
            almacen.alimento_9 -= alimentos.alimento_9
            almacen.alimento_10 -= alimentos.alimento_10
            almacen.alimento_11 -= alimentos.alimento_11
            almacen.alimento_12 -= alimentos.alimento_12
            almacen.alimento_13 -= alimentos.alimento_13
            almacen.alimento_14 -= alimentos.alimento_14
            almacen.alimento_15 -= alimentos.alimento_15

            alimentos.persona = persona
            alimentos.modificado_por = request.user
            almacen.save()
            alimentos.save()
            return redirect(persona)

    else:
        a_form = AlimentosFrom()
    return render(request, 'adra/alimentos_form.html', {'form': a_form})


class PersonaAlimentosUpdateView(LoginRequiredMixin, UpdateView):
    model = Alimentos
    fields = [
        'alimento_1',
        'alimento_2',
        'alimento_3',
        'alimento_4',
        'alimento_6',
        'alimento_7',
        'alimento_8',
        'alimento_9',
        'alimento_10',
        'alimento_11',
        'alimento_12',
        'alimento_13',
        'alimento_14',
        'alimento_15',
        'fecha_recogida'

    ]

    def form_valid(self, form):
        clean = form.changed_data
        almacen = AlmacenAlimentos.objects.get(pk=1)

        if "alimento_1" in clean:
            valor_anterior_alimento_1 = form.initial["alimento_1"]
            if form.instance.alimento_1 > valor_anterior_alimento_1:
                restante = abs(form.instance.alimento_1 - valor_anterior_alimento_1)
                almacen.alimento_1 -= restante
            else:
                restante = abs(form.instance.alimento_1 - valor_anterior_alimento_1)
                almacen.alimento_1 += restante

        if "alimento_2" in clean:
            valor_anterior_alimento_2 = form.initial["alimento_2"]
            if form.instance.alimento_2 > valor_anterior_alimento_2:
                restante = abs(form.instance.alimento_2 - valor_anterior_alimento_2)
                almacen.alimento_2 -= restante
            else:
                restante = abs(form.instance.alimento_2 - valor_anterior_alimento_2)
                almacen.alimento_2 += restante

        if "alimento_3" in clean:
            valor_anterior_alimento_3 = form.initial["alimento_3"]
            if form.instance.alimento_3 > valor_anterior_alimento_3:
                restante = abs(form.instance.alimento_3 - valor_anterior_alimento_3)
                almacen.alimento_3 -= restante
            else:
                restante = abs(form.instance.alimento_3 - valor_anterior_alimento_3)
                almacen.alimento_3 += restante

        if "alimento_4" in clean:
            valor_anterior_alimento_4 = form.initial["alimento_4"]
            if form.instance.alimento_4 > valor_anterior_alimento_4:
                restante = abs(form.instance.alimento_4 - valor_anterior_alimento_4)
                almacen.alimento_4 -= restante
            else:
                restante = abs(form.instance.alimento_4 - valor_anterior_alimento_4)
                almacen.alimento_4 += restante

        if "alimento_6" in clean:
            valor_anterior_alimento_6 = form.initial["alimento_6"]
            if form.instance.alimento_6 > valor_anterior_alimento_6:
                restante = abs(form.instance.alimento_6 - valor_anterior_alimento_6)
                almacen.alimento_6 -= restante
            else:
                restante = abs(form.instance.alimento_6 - valor_anterior_alimento_6)
                almacen.alimento_6 += restante

        if "alimento_7" in clean:
            valor_anterior_alimento_7 = form.initial["alimento_7"]
            if form.instance.alimento_7 > valor_anterior_alimento_7:
                restante = abs(form.instance.alimento_7 - valor_anterior_alimento_7)
                almacen.alimento_7 -= restante
            else:
                restante = abs(form.instance.alimento_7 - valor_anterior_alimento_7)
                almacen.alimento_7 += restante

        if "alimento_8" in clean:
            valor_anterior_alimento_8= form.initial["alimento_8"]
            if form.instance.alimento_8 > valor_anterior_alimento_8:
                restante = abs(form.instance.alimento_8 - valor_anterior_alimento_8)
                almacen.alimento_8 -= restante
            else:
                restante = abs(form.instance.alimento_8 - valor_anterior_alimento_8)
                almacen.alimento_8 += restante

        if "alimento_9" in clean:
            valor_anterior_alimento_9 = form.initial["alimento_9"]
            if form.instance.alimento_9 > valor_anterior_alimento_9:
                restante = abs(form.instance.alimento_9 - valor_anterior_alimento_9)
                almacen.alimento_9 -= restante
            else:
                restante = abs(form.instance.alimento_9 - valor_anterior_alimento_9)
                almacen.alimento_9 += restante

        if "alimento_10" in clean:
            valor_anterior_alimento_10 = form.initial["alimento_10"]
            if form.instance.alimento_10 > valor_anterior_alimento_10:
                restante = abs(form.instance.alimento_10 - valor_anterior_alimento_10)
                almacen.alimento_10 -= restante
            else:
                restante = abs(form.instance.alimento_10 - valor_anterior_alimento_10)
                almacen.alimento_10 += restante

        if "alimento_11" in clean:
            valor_anterior_alimento_11 = form.initial["alimento_11"]
            if form.instance.alimento_11 > valor_anterior_alimento_11:
                restante = abs(form.instance.alimento_11 - valor_anterior_alimento_11)
                almacen.alimento_11 -= restante
            else:
                restante = abs(form.instance.alimento_11 - valor_anterior_alimento_11)
                almacen.alimento_11 += restante

        if "alimento_12" in clean:
            valor_anterior_alimento_12 = form.initial["alimento_12"]
            if form.instance.tarito_fruta > valor_anterior_alimento_12:
                restante = abs(form.instance.tarito_fruta - valor_anterior_alimento_12)
                almacen.tarito_fruta -= restante
            else:
                restante = abs(form.instance.tarito_fruta - valor_anterior_alimento_12)
                almacen.tarito_fruta += restante

        if "alimento_13" in clean:
            valor_anterior_alimento_13 = form.initial["alimento_13"]
            if form.instance.alimento_13 > valor_anterior_alimento_13:
                restante = abs(form.instance.alimento_13 - valor_anterior_alimento_13)
                almacen.alimento_13 -= restante
            else:
                restante = abs(form.instance.alimento_13 - valor_anterior_alimento_13)
                almacen.alimento_13 += restante

        if "alimento_14" in clean:
            valor_anterior_alimento_14 = form.initial["alimento_14"]
            if form.instance.alimento_14 > valor_anterior_alimento_14:
                restante = abs(form.instance.alimento_14 - valor_anterior_alimento_14)
                almacen.alimento_14 -= restante
            else:
                restante = abs(form.instance.alimento_14 - valor_anterior_alimento_14)
                almacen.alimento_14 += restante

        if "alimento_15" in clean:
            valor_anterior_alimento_15 = form.initial["alimento_15"]
            if form.instance.alimento_15 > valor_anterior_alimento_15:
                restante = abs(form.instance.alimento_15 - valor_anterior_alimento_15)
                almacen.alimento_15 -= restante
            else:
                restante = abs(form.instance.alimento_15 - valor_anterior_alimento_15)
                almacen.alimento_15 += restante

        # if "aceite_de_oliva" in clean:
        #     valor_anterior_aceite_de_oliva = form.initial["aceite_de_oliva"]
        #     if form.instance.aceite_de_oliva > valor_anterior_aceite_de_oliva:
        #         restante = abs(form.instance.aceite_de_oliva -
        #                        valor_anterior_aceite_de_oliva)
        #         almacen.aceite_de_oliva -= restante
        #     else:
        #         restante = abs(form.instance.aceite_de_oliva -
        #                        valor_anterior_aceite_de_oliva)
        #         almacen.aceite_de_oliva += restante

        almacen.save()
        form.instance.modificado_por = self.request.user
        return super().form_valid(form)


class PersonaAlimentosDeleteView(LoginRequiredMixin, DeleteView):
    model = Alimentos
    success_url = '/'

    def test_func(self):
        persona = self.get_object()
        if self.request.user == persona.modificado_por:
            return True
        return False


class AlmacenListView(LoginRequiredMixin, ListView):
    model = AlmacenAlimentos
    template_name = 'adra_almacen/index.html'
    context_object_name = 'almacen_adra'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['nbar'] = "almacen_a"
        return context


class HijoCreateView(LoginRequiredMixin, CreateView):
    model = Hijo
    form_class = HijoForm

    def form_valid(self, form):
        form.instance.modificado_por = self.request.user
        return super().form_valid(form)


def adauga_hijo_persona(request, pk):
    persona = get_object_or_404(Persona, pk=pk)
    if request.method == 'POST':
        h_form = HijoForm(request.POST)
        if h_form.is_valid():
            hijo = h_form.save(commit=False)
            hijo.persona = persona
            hijo.modificado_por = request.user
            hijo.save()
            return redirect(persona)

    else:
        h_form = HijoForm()
    return render(request, 'adra/hijo_form.html', {'form': h_form})


class HijoUpdateView(LoginRequiredMixin, UpdateView):
    model = Hijo
    fields = [
        'parentesco',
        'nombre_apellido',
        'dni',
        'fecha_nacimiento',
        'edad',
        'sexo'
    ]

    def form_valid(self, form):
        form.instance.modificado_por = self.request.user
        return super().form_valid(form)

    def test_func(self):
        persona = self.get_object()
        if self.request.user == persona.modificado_por:
            return True
        return


class HijoDeleteView(LoginRequiredMixin, DeleteView):
    model = Hijo
    persoan = Persona
    success_url = reverse_lazy("adra:persona-home")


@login_required
def buscar(request):
    if 'q' in request.GET and request.GET['q']:
        q = request.GET['q']

        if (q.isdigit()):
            ultima_persona = Persona.objects.filter(
                Q(numero_adra=q) | Q(telefono=q))
        else:
            ultima_persona = Persona.objects.filter(
                nombre_apellido__icontains=q)

        return render(request, 'adra/index.html',
                      {'ultima_persona': ultima_persona, 'query': q})
    else:
        return HttpResponse('<h1>Por favor buscar con otro criterio</h1>')


def calculate_age(age):
    today = date.today()
    return today.year - age.year - ((today.month, today.day) < (age.month, age.day))


@login_required
def statistics_persona(request):
    # personas
    count_0_3_mujer = 0
    count_3_15_mujer = 0
    count_15_64_mujer = 0
    count_65_mujer = 0

    count_0_3_hombre = 0
    count_3_15_hombre = 0
    count_15_64_hombre = 0
    count_65_hombre = 0

    # familiares
    count_0_3_mujer_f = 0
    count_3_15_mujer_f = 0
    count_15_64_mujer_f = 0
    count_65_mujer_f = 0

    count_0_3_hijo = 0
    count_3_15_hijo = 0
    count_15_64_hijo = 0
    count_65_hijo = 0

    count_0_3_hija = 0
    count_3_15_hija = 0
    count_15_64_hija = 0
    count_65_hija = 0

    count_0_3_hombre_f = 0
    count_3_15_hombre_f = 0
    count_15_64_hombre_f = 0
    count_65_hombre_f = 0

    pers = Persona.objects.filter(active=True)
    for p in pers:

        if calculate_age(p.fecha_nacimiento) >= 0 and calculate_age(p.fecha_nacimiento) <= 3 and p.sexo == "mujer":
            count_0_3_mujer += 1
        elif calculate_age(p.fecha_nacimiento) > 3 and calculate_age(p.fecha_nacimiento) <= 15 and p.sexo == "mujer":
            count_3_15_mujer += 1
        elif calculate_age(p.fecha_nacimiento) > 15 and calculate_age(p.fecha_nacimiento) <= 64 and p.sexo == "mujer":
            count_15_64_mujer += 1
        elif calculate_age(p.fecha_nacimiento) > 64 and p.sexo == "mujer":
            count_65_mujer += 1

        elif calculate_age(p.fecha_nacimiento) >= 0 and calculate_age(p.fecha_nacimiento) <= 3 and p.sexo == "hombre":
            count_0_3_hombre += 1
        elif calculate_age(p.fecha_nacimiento) > 3 and calculate_age(p.fecha_nacimiento) <= 15 and p.sexo == "hombre":
            count_3_15_hombre += 1
        elif calculate_age(p.fecha_nacimiento) > 15 and calculate_age(p.fecha_nacimiento) <= 64 and p.sexo == "hombre":
            count_15_64_hombre += 1
        elif calculate_age(p.fecha_nacimiento) > 64 and p.sexo == "hombre":
            count_65_hombre += 1

    per = Hijo.objects.all()
    for p in per:
        # esposa
        if calculate_age(p.fecha_nacimiento) >= 0 and calculate_age(
                p.fecha_nacimiento) <= 3 and p.parentesco == "esposa":
            count_0_3_mujer_f += 1
        elif calculate_age(p.fecha_nacimiento) > 3 and calculate_age(
                p.fecha_nacimiento) <= 15 and p.parentesco == "esposa":
            count_3_15_mujer_f += 1
        elif calculate_age(p.fecha_nacimiento) > 15 and calculate_age(
                p.fecha_nacimiento) <= 64 and p.parentesco == "esposa":
            count_15_64_mujer_f += 1
        elif calculate_age(p.fecha_nacimiento) > 64 and p.parentesco == "esposa":
            count_65_mujer_f += 1

        # hija
        elif calculate_age(p.fecha_nacimiento) >= 0 and calculate_age(
                p.fecha_nacimiento) <= 3 and p.parentesco == "hija":
            count_0_3_hija += 1
        elif calculate_age(p.fecha_nacimiento) > 3 and calculate_age(
                p.fecha_nacimiento) <= 15 and p.parentesco == "hija":
            count_3_15_hija += 1
        elif calculate_age(p.fecha_nacimiento) > 15 and calculate_age(
                p.fecha_nacimiento) <= 64 and p.parentesco == "hija":
            count_15_64_hija += 1
        elif calculate_age(p.fecha_nacimiento) > 64 and p.parentesco == "hija":
            count_65_hija += 1

            # hijo
        elif calculate_age(p.fecha_nacimiento) >= 0 and calculate_age(
                p.fecha_nacimiento) <= 3 and p.parentesco == "hijo":
            count_0_3_hijo += 1
        elif calculate_age(p.fecha_nacimiento) > 3 and calculate_age(
                p.fecha_nacimiento) <= 15 and p.parentesco == "hijo":
            count_3_15_hijo += 1
        elif calculate_age(p.fecha_nacimiento) > 15 and calculate_age(
                p.fecha_nacimiento) <= 64 and p.parentesco == "hijo":
            count_15_64_hijo += 1
        elif calculate_age(p.fecha_nacimiento) > 64 and p.parentesco == "hijo":
            count_65_hijo += 1
        # esposo
        elif calculate_age(p.fecha_nacimiento) >= 0 and calculate_age(
                p.fecha_nacimiento) <= 3 and p.parentesco == "esposo":
            count_0_3_hombre += 1
        elif calculate_age(p.fecha_nacimiento) > 3 and calculate_age(
                p.fecha_nacimiento) <= 15 and p.parentesco == "esposo":
            count_3_15_hombre += 1
        elif calculate_age(p.fecha_nacimiento) > 15 and calculate_age(
                p.fecha_nacimiento) <= 64 and p.parentesco == "esposo":
            count_15_64_hombre += 1
        elif calculate_age(p.fecha_nacimiento) > 64 and p.parentesco == "esposo":
            count_65_hombre += 1

    discapacidad = Persona.objects.filter(discapacidad=True,active=True).count()
    total_beneficiarios = Persona.objects.filter(active=True).count()
    total_familiares = Hijo.objects.filter(active=True).count()

    total_mujer_02 = count_0_3_mujer + count_0_3_mujer_f + count_0_3_hija
    total_mujer_3_15 = count_3_15_mujer + count_3_15_mujer_f + count_3_15_hija
    total_mujer_15_64 = count_15_64_mujer + count_15_64_mujer_f + count_15_64_hija
    total_mujer_65 = count_65_mujer + count_65_mujer_f + count_65_hija
    total_mujeres = total_mujer_02 + total_mujer_3_15 + \
                    total_mujer_15_64 + total_mujer_65

    total_hombre_02 = count_0_3_hombre + count_0_3_hombre_f + count_0_3_hijo
    total_hombre_3_15 = count_3_15_hombre + count_3_15_hombre_f + count_3_15_hijo
    total_hombre_15_64 = count_15_64_hombre + \
                         count_15_64_hombre_f + count_15_64_hijo
    total_hombre_65 = count_65_hombre + count_65_hombre_f + count_65_hijo
    total_hombres = total_hombre_02 + total_hombre_3_15 + \
                    total_hombre_15_64 + total_hombre_65

    total_02 = total_hombre_02 + total_mujer_02
    total_3_15 = total_hombre_3_15 + total_mujer_3_15
    total_15_64 = total_hombre_15_64 + total_mujer_15_64
    total_65 = total_hombre_65 + total_mujer_65
    total = total_02 + total_3_15 + total_15_64 + total_65

    return render(request, 'statistics/index.html', {
        "total_per_mujer_02": total_mujer_02,
        "total_per_mujer_03": total_mujer_3_15,
        "total_per_mujer_16": total_mujer_15_64,
        "total_per_mujer_65": total_mujer_65,
        "total_mujeres": total_mujeres,

        "total_per_hombre_02": total_hombre_02,
        "total_per_hombre_03": total_hombre_3_15,
        "total_per_hombre_16": total_hombre_15_64,
        "total_per_hombre_65": total_hombre_65,
        "total_hombres": total_hombres,
        "total_02": total_02,
        "total_03": total_3_15,
        "total_16": total_15_64,
        "total_65": total_65,
        "total_personas": total,
        "discapacidad": discapacidad,
        "total_beneficiarios": total_beneficiarios,
        "total_familiares": total_familiares,
        "nbar": 'stat'

    })


def export_users_csv(request):
    beneficiarios_queryset = Persona.objects.order_by('numero_adra').filter(active=True)

    response = HttpResponse(
        content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
    )
    response['Content-Disposition'] = 'attachment; filename=beneficiarios.xlsx'
    workbook = Workbook()

    # Get active worksheet/tab
    worksheet = workbook.active
    # Delete the default worksheet
    # workbook.remove(workbook.active)
    worksheet.title = 'Beneficiarios'
    # Define the titles for columns
    worksheet.column_dimensions['B'].width = 40
    worksheet.column_dimensions['C'].width = 40
    worksheet.column_dimensions['C'].width = 30
    worksheet.column_dimensions['E'].width = 40
    columns = [
        'Numar adra',
        'Nombre',
        'Dni',
        'Representante familiar'
        'Pasaporte',
        'Fecha de nacimiento',
    ]
    row_num = 1
    fill = PatternFill(start_color='43fb32',
                       fill_type='solid')
    # Assign the titles for each cell of the header
    for col_num, column_title in enumerate(columns, 1):
        cell = worksheet.cell(row=row_num, column=col_num)
        cell.value = column_title

    for ben in beneficiarios_queryset:
        row_num += 1

        # Define the data for each cell in the row
        row = [
            ben.numero_adra,
            ben.nombre_apellido,
            ben.dni,
            'x',
            ben.fecha_nacimiento.strftime("%d/%m/%Y"),
        ]
        # Assign the data for each cell of the row
        for col_num, cell_value in enumerate(row, 1):
            cell = worksheet.cell(row=row_num, column=col_num)
            cell.value = cell_value
            cell.fill = fill
            cell.alignment = Alignment(horizontal='center')

        for d in ben.hijo.all():
            row_hijos = [
                '-',
                d.nombre_apellido,
                d.dni,
                '',
                d.fecha_nacimiento.strftime("%d/%m/%Y"),
            ]
            row_num += 1

            # Assign the data for each cell of the row
            for col_num, cell_value in enumerate(row_hijos, 1):
                cell = worksheet.cell(row=row_num, column=col_num)
                cell.value = cell_value
                cell.alignment = Alignment(horizontal='center')

    workbook.save(response)

    return response


@login_required
def buscar_fecha(request):
    alimentos_list = Alimentos.objects.all()
    user_filter = AlimentosFilters(request.GET, queryset=alimentos_list)
    # EXCEL ZONE
    # # Create a workbook and add a worksheet.
    # workbook = xlsxwriter.Workbook('AlimentosEnero-Julio.xlsx')
    # worksheet = workbook.add_worksheet()
    # # Start from the first cell. Rows and columns are zero indexed.
    # row = 0
    # col = 0
    # bold = workbook.add_format({'bold': True})
    #
    #
    # for u in user_filter.qs:
    #     worksheet.write(row, col, f'{u.persona}')
    #     worksheet.write(row, col + 1, f'{u.fecha_recogida}')
    #     worksheet.write_number(row, col + 2, u.arroz_blanco)
    #     worksheet.write_number(row, col + 3, u.garbanzo_cocido)
    #     worksheet.write_number(row, col + 4, u.atun_sardina)
    #     worksheet.write_number(row, col + 5, u.sardina)
    #     worksheet.write_number(row, col + 6, u.pasta_espagueti)
    #     worksheet.write_number(row, col + 7, u.tomate_frito)
    #     worksheet.write_number(row, col + 8, u.galletas)
    #     worksheet.write_number(row, col + 9, u.macedonia_verdura_conserva)
    #     worksheet.write_number(row, col + 10, u.fruta_conserva_pera)
    #     worksheet.write_number(row, col + 11, u.fruta_conserva_coctel)
    #     worksheet.write_number(row, col + 12, u.tarito_pollo)
    #     worksheet.write_number(row, col + 13, u.tarito_fruta)
    #     worksheet.write_number(row, col + 14, u.leche)
    #     worksheet.write_number(row, col + 15, u.batido_chocolate)
    #     worksheet.write_number(row, col + 16, u.aceite_de_oliva)
    #     worksheet.write(row, col + 17, f'{u.modificado_por}')
    #     row += 1
    #
    #     print(u.fecha_recogida)
    # workbook.close()
    # print(arroz_sum)
    # alubia_sum = user_filter.qs.aggregate(Sum('alubia_blanca'))
    alimento_1 = user_filter.qs.aggregate(Sum('alimento_1'))
    alimento_2 = user_filter.qs.aggregate(Sum('alimento_2'))
    alimento_3 = user_filter.qs.aggregate(Sum('alimento_3'))
    alimento_4 = user_filter.qs.aggregate(Sum('alimento_4'))
    alimento_6 = user_filter.qs.aggregate(Sum('alimento_6'))
    alimento_7 = user_filter.qs.aggregate(Sum('alimento_7'))
    alimento_8 = user_filter.qs.aggregate(Sum('alimento_8'))
    alimento_9 = user_filter.qs.aggregate(Sum('alimento_9'))
    alimento_10 = user_filter.qs.aggregate(Sum('alimento_10'))
    alimento_11 = user_filter.qs.aggregate(Sum('alimento_11'))
    alimento_12 = user_filter.qs.aggregate(Sum('alimento_12'))
    alimento_13 = user_filter.qs.aggregate(Sum('alimento_13'))
    alimento_14 = user_filter.qs.aggregate(Sum('alimento_14'))
    alimento_15 = user_filter.qs.aggregate(Sum('alimento_15'))
    # aceite_de_oliva_sum = user_filter.qs.aggregate(Sum('aceite_de_oliva'))

    return render(request, 'busqueda_a/view.html',
                  {
                      'filter': user_filter,
                      'alimento_1': alimento_1,
                      'alimento_2': alimento_2,
                      'alimento_3': alimento_3,
                      'alimento_4': alimento_4,
                      'alimento_6': alimento_6,
                      'alimento_7': alimento_7,
                      'alimento_8': alimento_8,
                      'alimento_9': alimento_9,
                      'alimento_10': alimento_10,
                      'alimento_11': alimento_11,
                      'alimento_12': alimento_12,
                      'alimento_13': alimento_13,
                      'alimento_14': alimento_14,
                      'alimento_15': alimento_15,
                      'nbar': "buscar_av"

                  })


def set_need_appearances_writer(writer):
    """
    Helper para escribir el pdf
    :param writer: el pdf
    :return:
    """
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


def generar_hoja_entrega(request, pk):
    """
    Generador de hoja de entrega para cada beneficiario en parte
    :param request:
    :param pk: id persona
    :return: pdf generado
    """
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

    persona = Persona.objects.get(id=pk)
    familiares = persona.hijo.all()
    familiares_gr = persona.hijo.filter(edad__gt=3)

    mayores = 0
    menores = 0
    for f in familiares:
        if calculate_age(f.fecha_nacimiento) > 3:
            mayores += 1
        else:
            menores += 1

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

    pdf_writer.addPage(pdf_reader.getPage(0))
    pdf_writer.updatePageFormFieldValues(
        pdf_writer.getPage(0), field_dictionary)

    # outputStream = open(outfile, "wb")
    # pdf_writer.write(outputStream)

    # outputStream.close()

    # extractedPage = open(pdf_file_path, 'rb')
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'attachment;filename="{persona.numero_adra}.pdf"'
    pdf_writer.write(response)
    inputStream.close()
    return response



# API ADRA
# @api_view(['GET', 'POST'])
# def persona_list(request,format=None):
#     """
#     Listado todas las personas
#     """
#     if request.method == 'GET':
#         personas = Persona.objects.all()
#         serializer = PersonaSerializer(personas, many=True)
#         return Response(serializer.data)
#
#     elif request.method == 'POST':
#         serializer = PersonaSerializer(data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data, status=status.HTTP_201_CREATED)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
#
#
# @api_view(['GET', 'PUT', 'DELETE'])
# def persona_detail(request, pk,format=None):
#     """
#     Crud persona.
#     """
#     try:
#         persona = Persona.objects.get(pk=pk)
#     except Persona.DoesNotExist:
#         return Response(status=status.HTTP_404_NOT_FOUND)
#
#     if request.method == 'GET':
#         serializer = PersonaSerializer(persona)
#         return Response(serializer.data)
#
#     elif request.method == 'PUT':
#         serializer = PersonaSerializer(persona, data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
#
#     elif request.method == 'DELETE':
#         persona.delete()
#         return Response(status=status.HTTP_204_NO_CONTENT)


class PersonaViewSet(viewsets.ModelViewSet):
    """
        This viewset automatically provides `list`, `create`, `retrieve`,
        `update` and `destroy` actions.
        """
    queryset = Persona.objects.all().order_by("-numero_adra")
    serializer_class = PersonaSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(modificado_por=self.request.user)


class UserViewSet(viewsets.ReadOnlyModelViewSet):
    """
    This viewset automatically provides `list` and `detail` actions.
    """

    queryset = get_user_model().objects.all()
    serializer_class = UserSerializer


def get_data(request):
    """" manda datos a los graficos de echats """
    list_ano = []
    registro_2018 = Persona.objects.filter(created_at__year=2018)
    list_ano.append(registro_2018.count())
    registro_2019 = Persona.objects.filter(created_at__year=2019)
    list_ano.append(registro_2019.count())
    registro_2020 = Persona.objects.filter(created_at__year=2020)
    list_ano.append(registro_2020.count())

    return JsonResponse({"reg": list_ano})


class CustomAllauthAdapter(DefaultAccountAdapter):

    def send_mail(self, template_prefix, email, context):

        if context.get('activate_url'):
            account_confirm_email = 'accounts/confirm-email/'
            # prod
            context['activate_url'] = (
                    str(context.get('current_site')) +
                    account_confirm_email + context['key']
            )
            # local dev
            # context['activate_url'] = (
            #         str("http://127.0.0.1:8000/") + account_confirm_email + context['key']
            # )

            user = context.get('user')

            sg = SendGridAPIClient(settings.SENDGRID_API_KEY)
            message = Mail(
                from_email=f"admin@adra.es",
                to_emails=f"{user.email}",
            )
            message.dynamic_template_data = {
                "activate_url": f"{context.get('activate_url')}",
                "user": f"{context.get('user')}",
                "Sender_Name": f"Adra Torrejon de ardoz",
                "Sender_Address": f"calle primavera 15",
                "Sender_City": f"Torrejon de ardoz",
                "Sender_State": f"Madrid",
                "Sender_Zip": f"28850"
            }
            message.template_id = 'd-8dddee085b5e4479a28b7dace0adf686'
            response = sg.send(message)

        elif context.get('password_reset_url'):

            user = context.get('user')
            sg = SendGridAPIClient(settings.SENDGRID_API_KEY)
            message = Mail(
                from_email=f"admin@adra.es",
                to_emails=f"{user.email}",
            )
            message.dynamic_template_data = {
                "url_cambiar": f"{context.get('password_reset_url')}",
                "user": f"{user}",
                "Sender_Name": f"Adra Torrejon de ardoz",
                "Sender_Address": f"calle primavera 15",
                "Sender_City": f"Torrejon de ardoz",
                "Sender_State": f"Madrid",
                "Sender_Zip": f"28850"
            }

            message.template_id = 'd-ab0adafe4dd14cb4b9aba688b7200830'
            response = sg.send(message)
