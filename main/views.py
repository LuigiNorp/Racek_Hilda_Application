from django.core.files.storage import default_storage
from main.reports.report_contants import default_data
from main.reports.report_tools import (
    replace_variables_in_docx,
    convert_to_pdf,
    keep_first_page,
    scale_image_from_height,
    add_image_to_worksheet,
    xlsx_sheet_presets,
    merge_pdf_files,
)
from babel.dates import format_date
import uuid
import os
from openpyxl import load_workbook
from django.http import FileResponse, HttpResponseNotFound, HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from rest_framework.views import APIView
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views.generic import TemplateView
from django.contrib.auth.models import User
from django.contrib import messages
from .helpers import send_forget_password_mail
from django.views import View
from django.core.cache import cache
from django.db.models import Q
from dal import autocomplete
from main.forms import (
    CustomUserRegisterForm,
    CustomUserProfileForm,
    PersonalForm,
)
from main.models import (
    Profile,
    CustomUser
)

from data.models import (
    Cliente,
    CodigoPostal,
    Curp,
    Rfc,
    Ocupacion,
    PaqueteCapacitacion
)


# Create your views here.
class LoginView(View):
    template_name = 'login/login.html'

    def get(self, request):
        return render(request, self.template_name)

    def post(self, request):
        try:
            username = request.POST.get('username')
            password = request.POST.get('password')

            if not username or not password:
                messages.success(request, 'Both Username and Password are required.')
                return redirect('/login/')

            user_obj = User.objects.filter(username=username).first()
            if user_obj is None:
                messages.success(request, 'User not found.')
                return redirect('/login/')

            user = authenticate(username=username, password=password)

            if user is None:
                messages.success(request, 'Wrong password.')
                return redirect('/login/')

            login(request, user)
            return redirect('/')
        except Exception as e:
            print(e)
        return render(request, self.template_name)


class LogoutView(View):
    def get(self, request):
        logout(request)
        return redirect('/')


class ForgetPasswordView(View):
    template_name = 'login/forget-password.html'

    def get(self, request):
        return render(request, self.template_name)

    def post(self, request):
        try:
            username = request.POST.get('username')

            if not User.objects.filter(username=username).first():
                messages.success(request, 'No user found with this username.')
                return redirect('/forget-password/')

            user_obj = User.objects.get(username=username)
            token = str(uuid.uuid4())
            profile_obj = Profile.objects.get(user=user_obj)
            profile_obj.forget_password_token = token
            profile_obj.save()
            send_forget_password_mail(user_obj.email, token)
            messages.success(request, 'An email is sent.')
            return redirect('/forget-password/')
        except Exception as e:
            print(e)
        return render(request, self.template_name)


class ChangePasswordView(View):
    template_name = 'login/change-password.html'

    def get(self, request, token):
        context = {}
        profile_obj = Profile.objects.filter(forget_password_token=token).first()
        if profile_obj:
            context['user_id'] = profile_obj.user.id
        return render(request, self.template_name, context)

    def post(self, request, token):
        try:
            new_password = request.POST.get('new_password')
            confirm_password = request.POST.get('reconfirm_password')
            user_id = request.POST.get('user_id')

            if user_id is None:
                messages.success(request, 'No user id found.')
                return redirect(f'/change-password/{token}/')

            if new_password != confirm_password:
                messages.success(request, 'Both passwords should be equal.')
                return redirect(f'/change-password/{token}/')

            user_obj = User.objects.get(id=user_id)
            user_obj.set_password(new_password)
            user_obj.save()
            return redirect('/login/')
        except Exception as e:
            print(e)
        return render(request, self.template_name)


class ServeFileView(View):
    def get(self, request, file_url):
        # Assuming the file URL is relative to your media root
        file_path = default_storage.path(file_url)
        try:
            # Open the file and serve it as a response
            with open(file_path, 'rb') as file:
                response = FileResponse(file)
            return response
        except FileNotFoundError:
            return HttpResponseNotFound('File not found')


class HomeView(LoginRequiredMixin, TemplateView):
    login_url = '/login/'
    template_name = 'home.html'

    def is_register_enabled(self):
        user = self.request.user
        if user.groups.filter(name__in=['Superboss', 'Manager', 'Admin']).exists():
            return True
        return False

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['is_register_enabled'] = self.is_register_enabled()
        return context

    def get(self, request, *args, **kwargs):
        # Clear the cache
        cache.clear()
        context = self.get_context_data(**kwargs)
        return self.render_to_response(context)


class RegisterView(LoginRequiredMixin, UserPassesTestMixin, APIView):
    login_url = '/login/'
    template_name = 'login/register.html'

    def test_func(self):
        user = self.request.user
        if user.groups.filter(name__in=['Superboss', 'Manager', 'Admin']).exists():
            return True
        return False

    def get(self, request):
        cache.clear()
        form = CustomUserRegisterForm()
        is_register_enabled = self.test_func()
        context = {
            'form': form,
            'is_register_enabled': is_register_enabled,
        }
        return render(request, self.template_name, context)

    def post(self, request):
        cache.clear()
        form = CustomUserRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            # messages.success(request, 'Usuario creado exitosamente.')
            return redirect('/')
        else:
            messages.error(request, form.errors)

        is_register_enabled = self.test_func()
        context = {
            'form': form,
            'is_register_enabled': is_register_enabled,
        }
        return render(request, self.template_name, context)


class CustomUserProfileView(LoginRequiredMixin, APIView):
    login_url = '/login/'
    template_name = 'user/user-profile.html'

    def is_register_enabled(self):
        user = self.request.user
        if user.groups.filter(name__in=['Superboss', 'Manager', 'Admin']).exists():
            return True
        return False

    def get(self, request, pk):
        user = get_object_or_404(CustomUser, pk=pk)
        form = CustomUserProfileForm(instance=user)
        is_register_enabled = self.is_register_enabled()
        context = {
            'form': form,
            'is_register_enabled': is_register_enabled,
        }
        return render(request, self.template_name, context)

    def post(self, request, pk):
        user = get_object_or_404(CustomUser, pk=pk)
        form = CustomUserProfileForm(request.POST, instance=user)
        if form.is_valid():
            form.save()
            return redirect('/')
        else:
            messages.error(request, form.errors)

        is_register_enabled = self.is_register_enabled()
        context = {
            'form': form,
            'is_register_enabled': is_register_enabled,
        }
        return render(request, self.template_name, context)


class UsersView(LoginRequiredMixin, UserPassesTestMixin, TemplateView):
    login_url = '/login/'

    def test_func(self):
        user = self.request.user
        if user.groups.filter(name__in=['Superboss', 'Manager', 'Admin']).exists():
            return True
        return False

    def get(self, request):
        users = CustomUser.objects.all()
        filter_text = request.GET.get('q', '')
        if filter_text:
            users = users.filter(
                Q(username__icontains=filter_text) |
                Q(email__icontains=filter_text) |
                Q(nombre__icontains=filter_text) |
                Q(apellido_paterno__icontains=filter_text) |
                Q(apellido_materno__icontains=filter_text) |
                Q(departamento__icontains=filter_text)
            )
        context = self.get_context_data()
        context['users'] = users
        context['filter_text'] = filter_text
        return render(request, 'user/users.html', context)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['is_register_enabled'] = self.test_func()
        return context


class ClientesView(TemplateView):
    template_name = 'client/clients.html'
    login_url = '/login/'

    def test_func(self):
        user = self.request.user
        if user.groups.filter(name__in=['Superboss', 'Manager', 'Admin']).exists():
            return True
        return False

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['is_register_enabled'] = self.test_func()
        return context


class PersonalView(TemplateView):
    template_name = 'personal/personal.html'
    login_url = '/login/'

    def test_func(self):
        user = self.request.user
        if user.groups.filter(name__in=['Superboss', 'Manager', 'Admin']).exists():
            return True
        return False

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['is_register_enabled'] = self.test_func()
        context['form'] = PersonalForm(self.request.POST or None, request=self.request)
        return context


class PersonalPrevioView(TemplateView):
    template_name = 'personal/personalprevio.html'
    login_url = '/login/'

    def test_func(self):
        user = self.request.user
        if user.groups.filter(name__in=['Superboss', 'Manager', 'Admin']).exists():
            return True
        return False

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['is_register_enabled'] = self.test_func()
        context['form'] = PersonalForm(self.request.POST or None, request=self.request)
        return context


class UserHistoryView(LoginRequiredMixin, TemplateView):
    template_name = 'user/history.html'
    login_url = '/login/'

    def is_register_enabled(self):
        user = self.request.user
        if user.groups.filter(name__in=['Superboss', 'Manager', 'Admin']).exists():
            return True
        return False

    def get(self, request, pk):
        user = get_object_or_404(CustomUser, pk=pk)
        form = CustomUserProfileForm(instance=user)
        is_register_enabled = self.is_register_enabled()
        context = {
            'form': form,
            'is_register_enabled': is_register_enabled,
        }
        return render(request, self.template_name, context)

    def post(self, request, pk):
        user = get_object_or_404(CustomUser, pk=pk)
        form = CustomUserProfileForm(request.POST, instance=user)
        if form.is_valid():
            form.save()
            return redirect('/')
        else:
            messages.error(request, form.errors)

        is_register_enabled = self.is_register_enabled()
        context = {
            'form': form,
            'is_register_enabled': is_register_enabled,
        }
        return render(request, self.template_name, context)


class ClienteAutocomplete(autocomplete.Select2QuerySetView):
    def get_queryset(self):
        qs = Cliente.objects.all()
        if self.q:
            qs = qs.filter(nombre_comercial__istartswith=self.q)
        return qs


class CodigoPostalAutocomplete(autocomplete.Select2QuerySetView):
    def get_queryset(self):
        qs = CodigoPostal.objects.all()
        if self.q:
            qs = qs.filter(codigo_postal__istartswith=self.q)
        return qs


class CurpAutocomplete(autocomplete.Select2QuerySetView):
    def get_queryset(self):
        qs = Curp.objects.all()
        if self.q:
            qs = qs.filter(curp__istartswith=self.q)
        return qs


class RfcAutocomplete(autocomplete.Select2QuerySetView):
    def get_queryset(self):
        qs = Rfc.objects.all()
        if self.q:
            qs = qs.filter(rfc__istartswith=self.q)
        return qs


class OcupacionAutocomplete(autocomplete.Select2QuerySetView):
    def get_queryset(self):
        qs = Ocupacion.objects.all()
        if self.q:
            qs = qs.filter(clave_subarea__istartswith=self.q)
        return qs


class PaqueteCapacitacionAutocomplete(autocomplete.Select2QuerySetView):
    def get_queryset(self):
        qs = PaqueteCapacitacion.objects.all()
        if self.q:
            qs = qs.filter(fecha_realizacion__istartswith=self.q)
        return qs


# Report views
class GenerateDC3View(View):
    def get(self, personal_id: int, request: any, queryset: any, desired_height_cm=3.5):
        original_file_path = 'media/file_templates/DC3 ACTUALIZADO.xlsx'
        modified_xlsx_path = 'media/file_templates/modified_dc3.xlsx'
        wb = load_workbook(original_file_path)
        sheet = wb.active

        # Set paper size to letter and setting margins
        xlsx_sheet_presets(sheet)

        for personal in queryset:
            # Access data from personal object and related objects
            data = default_data

            # Try to access each attribute individually and handle exceptions separately
            try:
                data['nombre_completo_personal'] = personal.curp.get_nombre_completo()
            except AttributeError:
                pass
            try:
                data['curp_personal'] = f'{personal.curp.curp}'
            except AttributeError:
                pass
            try:
                data['ocupacion_personal'] = f'{personal.carpetalaboral.ocupacion.get_ocupacion_fullname()}'
            except AttributeError:
                pass
            try:
                data['puesto_personal'] = f'{personal.carpetalaboral.display_choice_value("puesto")}'
            except AttributeError:
                pass
            try:
                data['razon_social'] = f'{personal.cliente.razon_social}'
            except AttributeError:
                pass
            try:
                data['rfc_personal'] = f'{personal.cliente.carpetaclientegenerales.rfc}'
            except AttributeError:
                pass
            try:
                data['nombre_curso'] = f'{personal.capacitaciones.all().last().curso}'
            except AttributeError:
                pass
            try:
                data['horas_curso'] = f'{personal.capacitaciones.all().last().duracion}'
            except AttributeError:
                pass
            try:
                data[
                    'fecha_inicial_capacitacion'] = f'{personal.capacitaciones.all().last().inicio.strftime("%d/%m/%Y")}'
            except AttributeError:
                pass
            try:
                data[
                    'fecha_final_capacitacion'] = f'{personal.capacitaciones.all().last().conclusion.strftime("%d/%m/%Y")}'
            except AttributeError:
                pass
            try:
                data['area_curso'] = f'{personal.capacitaciones.all().last().display_choice_value("area_curso")}'
            except AttributeError:
                pass
            try:
                data['nombre_capacitador'] = f'{personal.capacitaciones.all().last().instructor.nombre_instructor}'
            except AttributeError:
                pass
            try:
                data['registro_capacitador'] = f'{personal.capacitaciones.all().last().instructor.numero_registro}'
            except AttributeError:
                pass
            try:
                data['representante_legal'] = f'{personal.cliente.carpetaclientegenerales.representante_legal}'
            except AttributeError:
                pass
            try:
                data['representante_trabajadores'] = f'{personal.cliente.representantetrabajadores.nombre_completo}'
            except AttributeError:
                pass
            try:
                data['logotipo'] = f'{personal.cliente.documentoscliente.logotipo.path}'
            except ValueError:
                pass
            try:
                data['qr_code'] = f'{personal.cliente.documentoscliente.qr_code.path}'
            except ValueError:
                pass

            cell_mapping = {
                'AJ5': data['nombre_completo_personal'],
                'AJ6': data['curp_personal'],
                'AJ7': data['ocupacion_personal'],
                'AJ8': data['puesto_personal'],
                'AJ9': data['nombre_curso'],
                'AJ10': data['horas_curso'],
                'AJ11': data['fecha_inicial_capacitacion'],
                'AJ12': data['fecha_final_capacitacion'],
                'AJ13': data['area_curso'],
                'AJ14': data['nombre_capacitador'],
                'AJ15': data['registro_capacitador'],
                'AJ21': data['razon_social'],
                'AJ22': data['rfc_personal'],
                'AJ23': data['representante_legal'],
                'AJ24': data['representante_trabajadores'],
            }
            for cell, value in cell_mapping.items():
                sheet[cell].value = value
            if data['logotipo']:
                img_path = data['logotipo']
                width, height = scale_image_from_height(img_path, desired_height_cm)
                add_image_to_worksheet(img_path, 'B1', sheet, width, height)
            if data['qr_code']:
                img_path = data['qr_code']
                width, height = scale_image_from_height(img_path, desired_height_cm)
                add_image_to_worksheet(img_path, 'AC1', sheet, width, height)
        wb.save(modified_xlsx_path)
        # Build the PDF filename using attributes from the first object in the queryset
        first_personal = queryset.first()
        pdf_filename = 'modified_dc3.pdf'
        front_pdf = os.path.join('media/file_templates', pdf_filename)

        # Convert the modified XLSX to PDF using LibreOffice
        convert_to_pdf(modified_xlsx_path, front_pdf)

        # Keep only the first page on PDF file
        keep_first_page(front_pdf)

        # Add reverse sheet to report
        reverese_pdf = 'media/file_templates/dc3_reverse.pdf'
        pdf_merged = 'merged_dc3.pdf'
        merged_path = os.path.join('media/file_templates', pdf_merged)
        merge_pdf_files(front_pdf, reverese_pdf, merged_path)

        # Return the PDF as a response with the desired filename
        with open(merged_path, 'rb') as pdf_file:
            filename = f'{first_personal.curp.get_nombre_completo()}-DC3.pdf'
            pdf_response = HttpResponse(pdf_file.read(), content_type='application/pdf')
            pdf_response['Content-Disposition'] = f'attachment; filename={filename}'

        # Delete temporary file
        os.remove(modified_xlsx_path)
        os.remove(front_pdf)
        os.remove(merged_path)

        return pdf_response


class GenerateOdontologicView(View):
    def get(self, personal_id: int, request: any, queryset: any):
        verified_queries = default_data
        docx_file_path = 'media/file_templates/odontologico.docx'

        for personal in queryset:
            # Specific data access for odontologico document
            try:
                fecha_odontolico = personal.carpetaexamenmedico.fecha_examen
                fecha_odontolico_mx = format_date(fecha_odontolico, 'd \'de\' MMMM \'de\' yyyy', locale='es_MX')
                verified_queries['fecha_odontologico'] = f'{fecha_odontolico_mx}'.upper()
            except AttributeError:
                pass
            try:
                verified_queries['nombre_completo_personal'] = f'{personal.curp.get_nombre_completo()}'
            except AttributeError:
                pass
            try:
                verified_queries['id_racek'] = f'{personal.id}'
            except AttributeError:
                pass
            try:
                verified_queries['rfc_personal'] = f'{personal.rfc.rfc}'
            except AttributeError:
                pass
            try:
                verified_queries['sexo_personal'] = f'{personal.curp.sexo}'
            except AttributeError:
                pass
            try:
                verified_queries['edad_personal'] = f'{personal.curp.edad}'
            except AttributeError:
                pass
            try:
                verified_queries['ocupacion_personal'] = f'{personal.carpetalaboral.ocupacion.get_ocupacion_fullname()}'
            except AttributeError:
                pass
            try:
                verified_queries['empresa'] = f'{personal.cliente.razon_social}'
            except AttributeError:
                pass
            try:
                verified_queries[
                    'nombre_completo_dentista'] = f'{personal.carpetaexamenmedico.medico_odontologico.nombre_completo}'
            except AttributeError:
                pass
            try:
                verified_queries['firma_dentista'] = f'{personal.carpetaexamenmedico.medicoodontologico.firma.path}'
            except AttributeError:
                pass

            # Generate the PDF file name based on the person's full name
            pdf_file_path = f'media/file_templates/temporal.pdf'
            temporary_docx_path = replace_variables_in_docx(docx_file_path, verified_queries)
            temporary_pdf_path = convert_to_pdf(temporary_docx_path, pdf_file_path)

            with open(temporary_pdf_path, 'rb') as pdf_file:
                filename = f'{personal.curp.get_nombre_completo()}-ODONTOLOGICO.pdf'
                pdf_response = HttpResponse(pdf_file.read(), content_type='application/pdf')
                pdf_response['Content-Disposition'] = f'attachment; filename={filename}'

            # Delete temporary files
            os.remove(temporary_docx_path)
            os.remove(temporary_pdf_path)

            return pdf_response


class GenerateFingerprintRecordView(View):
    pass


class GenerateCdmxLicenseView(View):
    pass


class GenerateEdomexLicenseView(View):
    pass


class GenerateFederalLicenseView(View):
    pass


class GenerateConsentFormView(View):
    pass


class GenerateTrainingCertificateView(View):
    pass


class GenerateCdmxTestsView(View):
    pass


class GenerateFederalTestsView(View):
    pass


class GenerateSocioeconomicPhotosView(View):
    pass


class GenerateIshiharaTestView(View):
    def get(self, personal_id: int, request: any, queryset: any):
        verified_queries = default_data
        docx_file_path = 'media/file_templates/ishihara.docx'

        for personal in queryset:
            # Specific data access for ishihara document
            try:
                if personal.carpetaexamenmedico.jefemedico.sexo_medico == 'FEMENINO':
                    verified_queries['articulo_determinado'] = f'la'.capitalize()
                elif personal.telefono_domicilio:
                    verified_queries['articulo_determinado'] = f'el'.capitalize()
            except AttributeError:
                pass
            try:
                if personal.carpetaexamenmedico.jefemedico.sexo_medico == 'FEMENINO':
                    verified_queries['genero_sustantivo'] = f'a'
                elif personal.telefono_domicilio:
                    verified_queries['genero_sustantivo'] = f'o'
            except AttributeError:
                pass
            try:
                verified_queries[
                    'nombre_completo_medico'] = f'{personal.carpetaexamenmedico.jefemedico.nombre_completo}'
            except AttributeError:
                pass
            try:
                verified_queries[
                    'cedula_profesional_medico'] = f'{personal.carpetaexamenmedico.jefemedico.cedula_profesional}'
            except AttributeError:
                pass
            try:
                fecha_examen_medico = personal.carpetaexamenmedico.fecha_examen
                fecha_examen_medico_mx = format_date(fecha_examen_medico, 'd \'de\' MMMM \'de\' yyyy', locale='es_MX')
                verified_queries['fecha_examen_medico'] = f"{fecha_examen_medico_mx}"
            except AttributeError:
                pass
            try:
                verified_queries['nombre_completo_personal'] = f'{personal.curp.get_nombre_completo()}'
            except AttributeError:
                pass
            try:
                verified_queries['curp'] = f'{personal.curp.curp}'
            except AttributeError:
                pass
            try:
                verified_queries['empresa'] = f'{personal.cliente.razon_social}'
            except AttributeError:
                pass
            try:
                verified_queries['oi'] = f'{personal.carpetaexamenmedico.ishihara_visual_oi}'
            except AttributeError:
                pass
            try:
                verified_queries['od'] = f'{personal.carpetaexamenmedico.ishihara_visual_od}'
            except AttributeError:
                pass
            try:
                verified_queries['ao'] = f'{personal.carpetaexamenmedico.ishihara_visual_ao}'
            except AttributeError:
                pass
            try:
                verified_queries['lentes'] = f'{personal.carpetaexamenmedico.ishihara_lentes}'
            except AttributeError:
                pass
            try:
                verified_queries['deuteranopia'] = f'{personal.carpetaexamenmedico.ishihara_deuteranopia}'
            except AttributeError:
                pass
            try:
                verified_queries['protanopia'] = f'{personal.carpetaexamenmedico.ishihara_protanopia}'
            except AttributeError:
                pass
            try:
                verified_queries['tritanopia'] = f'{personal.carpetaexamenmedico.ishihara_tritanopia}'
            except AttributeError:
                pass
            try:
                verified_queries['acromatopsia'] = f'{personal.carpetaexamenmedico.ishihara_acromatopsia}'
            except AttributeError:
                pass
            try:
                verified_queries['resultado_ishihara'] = f'{personal.carpetaexamenmedico.ishihara_resultado}'
            except AttributeError:
                pass

            # Generate the PDF file name based on the person's full name
            pdf_file_path = f'media/file_templates/temporal.pdf'
            temporary_docx_path = replace_variables_in_docx(docx_file_path, verified_queries)
            temporary_pdf_path = convert_to_pdf(temporary_docx_path, pdf_file_path)

            with open(temporary_pdf_path, 'rb') as pdf_file:
                filename = f'{personal.curp.get_nombre_completo()}-ISHIHARA.pdf'
                pdf_response = HttpResponse(pdf_file.read(), content_type='application/pdf')
                pdf_response['Content-Disposition'] = f'attachment; filename={filename}'

            # Delete temporary files
            os.remove(temporary_docx_path)
            os.remove(temporary_pdf_path)

            return pdf_response


class GenerateHonestyTestView(View):
    pass


class GeneratePolygraphTestView(View):
    def get(self, personal_id: int, request: any, queryset: any):
        verified_queries = default_data
        docx_file_path = 'media/file_templates/poligrafo.docx'

        for personal in queryset:
            # Specific data access for poligraph test document
            try:
                fecha_reporte = personal.carpetaexamenpoligrafo.fechareporte
                fecha_reporte_mx = format_date(fecha_reporte, 'd \'de\' MMMM \'de\' yyyy', locale='es_MX')
                verified_queries['fecha_reporte'] = f'{fecha_reporte_mx}'.upper()
            except AttributeError:
                pass
            try:
                verified_queries['cliente'] = f'{personal.cliente.razon_social}'
            except AttributeError:
                pass
            try:
                fecha_poligrafo = personal.carpetaexamenpoligrafo.fechapoligrafo
                fecha_poligrafo_mx = format_date(fecha_poligrafo, 'd \'de\' MMMM \'de\' yyyy', locale='es_MX')
                verified_queries['fecha_poligrafo'] = f'{fecha_poligrafo_mx}'.upper()
            except AttributeError:
                pass
            try:
                verified_queries['nombre_completo_personal'] = f'{personal.curp.get_nombre_completo()}'
            except AttributeError:
                pass
            try:
                verified_queries['puesto'] = f'{personal.carpetalaboral.display_choice_value("puesto")}'
            except AttributeError:
                pass
            try:
                verified_queries['edad'] = f'{personal.curp.edad}'
            except AttributeError:
                pass
            try:
                verified_queries['nivel_academico'] = f'{personal.carpetagenerales.get_escolaridad_display()}'
            except AttributeError:
                pass
            try:
                verified_queries['estado_civil'] = f'{personal.carpetagenerales.get_estado_civil_display()}'
            except AttributeError:
                pass
            try:
                verified_queries['curp'] = f'{personal.curp.curp}'
            except AttributeError:
                pass
            try:
                if personal.telefono_celular:
                    verified_queries['telefono'] = f'{personal.telefono_celular}'
                elif personal.telefono_domicilio:
                    verified_queries['telefono'] = f'{personal.telefono_domicilio}'
                elif personal.telefono_recados:
                    verified_queries['telefono'] = f'{personal.telefono_recados}'
            except AttributeError:
                pass
            try:
                verified_queries['domicilio'] = f'{personal.domicilio.get_full_address()}'
            except AttributeError:
                pass
            try:
                verified_queries['poligrafista'] = f'{personal.carpetaexamenpoligrafo.poligrafista}'
            except AttributeError:
                pass
            try:
                verified_queries['supervisor_poligrafo'] = f'{personal.carpetaexamenpoligrafo.supervisor}'
            except AttributeError:
                pass

            # Generate the PDF file name based on the person's full name
            pdf_file_path = f'media/file_templates/temporal.pdf'
            temporary_docx_path = replace_variables_in_docx(docx_file_path, verified_queries)
            temporary_pdf_path = convert_to_pdf(temporary_docx_path, pdf_file_path)

            with open(temporary_pdf_path, 'rb') as pdf_file:
                filename = f'{personal.curp.get_nombre_completo()}-POLIGRAFO.pdf'
                pdf_response = HttpResponse(pdf_file.read(), content_type='application/pdf')
                pdf_response['Content-Disposition'] = f'attachment; filename={filename}'

            # Delete temporary files
            os.remove(temporary_docx_path)
            os.remove(temporary_pdf_path)

            return pdf_response


class GenerateGchPreliminaryView(View):
    pass


class GeneratePsychologicalView(View):
    pass


class GenerateCandidateView(View):
    pass


class GenerateSocioeconomicReportView(View):
    pass


class GenerateSocialWorkReportView(View):
    pass


class GenerateSedenaView(View):
    pass
