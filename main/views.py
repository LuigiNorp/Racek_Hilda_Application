import uuid
from PyPDF2 import PdfReader, PdfWriter
from openpyxl import load_workbook
from openpyxl.drawing.image import Image as XlsxImage
from openpyxl.worksheet.page import PageMargins
from PIL import Image as PilImage
import subprocess
from unidecode import unidecode
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
from main.forms import *


def keep_first_page(pdf_path):
    # Open the PDF file
    reader = PdfReader(pdf_path)

    # Create a new PDF writer
    writer = PdfWriter()

    # Add the first page to the writer
    writer.add_page(reader.pages[0])

    # Write the output to a new file
    with open(pdf_path, 'wb') as output_file:
        writer.write(output_file)


def verify_data(personal, datos):
    result = {}
    for key, function in datos.items():
        try:
            result[key] = function(personal)
        except AttributeError:
            result[key] = None
        except ValueError:
            result[key] = 'Invalid value'
    return result


def scale_image_from_height(image_path, desired_height_cm):
    # Load the image with PIL to get its size
    with PilImage.open(image_path) as pil_img:
        original_width, original_height = pil_img.size

    # Convert the height from cm to pixels and set the height of the image
    dpi = 96
    cm_to_pixels = lambda cm: int(dpi * cm / 2.54)  # convert cm to pixels
    desired_height_px = cm_to_pixels(desired_height_cm)

    # Calculate the new width to maintain aspect ratio
    scale_factor = desired_height_px / original_height
    desired_width_px = int(original_width * scale_factor)

    return desired_width_px, desired_height_px


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
            qs = qs.filter(zip_code__istartswith=self.q)
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


def remove_accents(text):
    # Use unidecode to remove accents and replace special characters
    return unidecode(text)


class GenerateDC3View(View):
    @staticmethod
    def add_image_to_worksheet(image_path, cell, activesheet, width, height):
        # Load and add the image with openpyxl
        img = XlsxImage(image_path)
        img.width = width
        img.height = height

        # Add image to the specified cell
        activesheet.add_image(img, cell)
    
    @staticmethod
    def convert_xlsx_to_pdf(xlsx_path, pdf_path):
        convertion_command = f"libreoffice --headless --convert-to pdf:writer_pdf_Export --outdir {os.path.dirname(pdf_path)} {xlsx_path}"
        subprocess.run(convertion_command, shell=True)
        return pdf_path

    def get(self, personal_id, request, queryset, desired_height_cm=3.5):
        original_file_path = "./media/file_templates/DC3 ACTUALIZADO.xlsx"
        modified_xlsx_path = 'media/file_templates/modified_dc3.xlsx'

        wb = load_workbook(original_file_path)
        sheet = wb.active
        sheet.page_setup.paperSize = sheet.PAPERSIZE_LETTER
        sheet.page_margins = PageMargins(
            top=0.2,
            left=0.25,
            right=0.01,
            header=0.1,
            footer=0.1,
            bottom=0.2
        )

        dc3_needed_data = {
            'nombre_completo': lambda p: p.curp.get_nombre_completo(),
            'curp': lambda p: p.curp.curp,
            'ocupacion': lambda p: p.carpetalaboral.ocupacion.nombre_ocupacion,
            'puesto': lambda p: p.carpetalaboral.puesto.nombre_puesto,
            'razon_social': lambda p: p.cliente.razon_social,
            'rfc': lambda p: p.cliente.carpetaclientegenerales.rfc,
            'nombre_curso': lambda p: p.carpetacapacitacion.capacitacion.curso,
            'horas_curso': lambda p: p.carpetacapacitacion.capacitacion.duracion,
            'fecha_inicial_capacitacion': lambda p: p.carpetacapacitacion.capacitacion.inicio,
            'fecha_final_capacitacion': lambda p: p.carpetacapacitacion.capacitacion.conclusion,
            'area_curso': lambda p: p.carpetacapacitacion.capacitacion.area_curso,
            'nombre_instructor': lambda p: p.carpetacapacitacion.capacitacion.instructor.nombre_instructor,
            'registro_instructor': lambda p: p.carpetacapacitacion.capacitacion.instructor.numero_registro,
            'representante_legal': lambda p: p.cliente.carpetaclientegenerales.representante_legal,
            'representante_trabajadores': lambda p: p.cliente.representantetrabajadores.nombre_completo,
            'logotipo': lambda p: p.cliente.documentoscliente.logotipo.path,
            'qr_code': lambda p: p.cliente.documentoscliente.qr_code.path,
        }

        for personal in queryset:
            verified_data = verify_data(personal, dc3_needed_data)

            cell_mapping = {
                'AJ5': verified_data['nombre_completo'],
                'AJ6': verified_data['curp'],
                'AJ7': verified_data['ocupacion'],
                'AJ8': verified_data['puesto'],
                'AJ9': verified_data['nombre_curso'],
                'AJ10': verified_data['horas_curso'],
                'AJ11': verified_data['fecha_inicial_capacitacion'],
                'AJ12': verified_data['fecha_final_capacitacion'],
                'AJ13': verified_data['area_curso'],
                'AJ14': verified_data['nombre_instructor'],
                'AJ15': verified_data['registro_instructor'],
                'AJ21': verified_data['razon_social'],
                'AJ22': verified_data['rfc'],
                'AJ23': verified_data['representante_legal'],
                'AJ24': verified_data['representante_trabajadores'],
            }

            for cell, value in cell_mapping.items():
                sheet[cell].value = value

            if verified_data['logotipo']:
                img_path = verified_data['logotipo']
                width, height = scale_image_from_height(img_path, desired_height_cm)
                self.add_image_to_worksheet(img_path, 'B1', sheet, width, height)

            if verified_data['qr_code']:
                img_path = verified_data['qr_code']
                width, height = scale_image_from_height(img_path, desired_height_cm)
                self.add_image_to_worksheet(img_path, 'AC1', sheet, width, height)

        wb.save(modified_xlsx_path)

        # Build the PDF filename using attributes from the first object in the queryset
        first_personal = queryset.first()
        pdf_filename = 'modified_dc3.pdf'
        pdf_path = os.path.join('media/file_templates', pdf_filename)

        # Convert the modified XLSX to PDF using LibreOffice
        self.convert_xlsx_to_pdf(modified_xlsx_path, pdf_path)

        # Keep only the first page on PDF file
        keep_first_page(pdf_path)

        # Return the PDF as a response with the desired filename
        with open(pdf_path, 'rb') as pdf_file:
            filename = f'{first_personal.curp.get_nombre_completo()}-DC3.pdf'
            pdf_response = HttpResponse(pdf_file.read(), content_type='application/pdf')
            pdf_response['Content-Disposition'] = f'attachment; filename={filename}'

        # Delete temporary file
        os.remove(modified_xlsx_path)
        os.remove(pdf_path)

        return pdf_response
