import uuid
from django.http import FileResponse, HttpResponseNotFound, HttpResponse
from django.shortcuts import render,redirect, get_object_or_404
from rest_framework.views import APIView
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views.generic import TemplateView
from django.contrib.auth.models import User
from django.contrib import messages
from .helpers import send_forget_password_mail
from django.views import View
from django.core.cache import cache
from django.db.models import Q
from .forms import *
from .models import *
from data.actions import *
from openpyxl import load_workbook
from openpyxl.worksheet.page import PageMargins
from openpyxl.drawing.image import Image as XlsxImage
from PIL import Image as PilImage
import subprocess
from unidecode import unidecode


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
        if user.groups.filter(name='Superboss').exists() or user.groups.filter(name='Manager').exists() or user.groups.filter(name='Admin').exists():
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
        if user.groups.filter(name='Superboss').exists() or user.groups.filter(name='Manager').exists() or user.groups.filter(name='Admin').exists():
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
        if user.groups.filter(name='Superboss').exists() or user.groups.filter(name='Manager').exists() or user.groups.filter(name='Admin').exists():
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
        if user.groups.filter(name='Superboss').exists() or user.groups.filter(name='Manager').exists() or user.groups.filter(name='Admin').exists():
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
        if user.groups.filter(name='Superboss').exists() or user.groups.filter(name='Manager').exists() or user.groups.filter(name='Admin').exists():
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
        if (
                user.groups.filter(name='Superboss').exists() or
                user.groups.filter(name='Manager').exists() or
                user.groups.filter(name='Admin').exists()):
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
        if user.groups.filter(name='Superboss').exists() or user.groups.filter(name='Manager').exists() or user.groups.filter(name='Admin').exists():
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


class GenerateDC3View(View):
    def remove_accents(self, text):
        # Use unidecode to remove accents and replace special characters
        return unidecode(text)

    def add_image_to_worksheet(self, image_path, cell, activesheet, width, height):
        # Load and add the image with openpyxl
        img = XlsxImage(image_path)
        img.width = width
        img.height = height

        # Add the image to the specified cell
        activesheet.add_image(img, cell)

    def convert_xlsx_to_pdf(self, xlsx_path):
        # Specify the sheet index (0 for the first sheet)
        sheet_index = 0
        command = f"libreoffice --headless --convert-to pdf:writer_pdf_Export --outdir {os.path.dirname(xlsx_path)}"
        subprocess.run(command, shell=True)

    def get(self, request, personal_id, desired_height_cm=3.5):
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
            bottom=.2
        )

        personal = get_object_or_404(Personal, id=personal_id)

        data = {
            'nombre_completo': '',
            'curp': '',
            'ocupacion': '',
            'puesto': '',
            'razon_social': '',
            'rfc': '',
            'nombre_curso': '',
            'horas_curso': '',
            'fecha_inicial_capacitacion': '',
            'fecha_final_capacitacion': '',
            'area_curso': '',
            'nombre_capacitador': '',
            'registro_capacitador': '',
            'representante_legal': '',
            'representante_trabajadores': '',
            'logotipo': None,
            'qr_code': None,
        }

        # Try to access each attribute individually and handle exceptions separately
        try:
            data['nombre_completo'] = personal.curp.get_full_name()
        except AttributeError:
            pass

        try:
            data['curp'] = personal.curp.curp
        except AttributeError:
            pass

        # Update the attribute paths based on your models
        try:
            data['ocupacion'] = personal.carpetalaboral.ocupacion.nombre_ocupacion
        except AttributeError:
            pass

        try:
            data['puesto'] = personal.carpetalaboral.puesto.nombre_puesto
        except AttributeError:
            pass

        try:
            data['razon_social'] = personal.cliente.razon_social
        except AttributeError:
            pass

        try:
            data['rfc'] = personal.cliente.carpetaclientegenerales.rfc
        except AttributeError:
            pass

        try:
            data['nombre_curso'] = personal.carpetacapacitacion.curso
        except AttributeError:
            pass

        try:
            data['horas_curso'] = personal.carpetacapacitacion.duracion
        except AttributeError:
            pass

        try:
            data['fecha_inicial_capacitacion'] = personal.carpetacapacitacion.inicio
        except AttributeError:
            pass

        try:
            data['fecha_final_capacitacion'] = personal.carpetacapacitacion.conclusion
        except AttributeError:
            pass

        try:
            data['area_curso'] = personal.carpetacapacitacion.area_curso.nombre_area
        except AttributeError:
            pass

        try:
            data['nombre_capacitador'] = personal.carpetacapacitacion.capacitador.nombre_capacitador
        except AttributeError:
            pass

        try:
            data['registro_capacitador'] = personal.carpetacapacitacion.capacitador.numero_registro
        except AttributeError:
            pass

        try:
            data['representante_legal'] = personal.cliente.carpetaclientegenerales.representante_legal
        except AttributeError:
            pass

        try:
            data['representante_trabajadores'] = personal.cliente.representantetrabajadores.nombre_completo
        except AttributeError:
            pass

        try:
            data['logotipo'] = personal.cliente.documentoscliente.logotipo.path
        except ValueError:
            pass

        try:
            data['qr_code'] = personal.cliente.documentoscliente.qr_code.path
        except ValueError:
            pass

        cell_mapping = {
            'AJ5': data['nombre_completo'],
            'AJ6': data['curp'],
            'AJ7': data['ocupacion'],
            'AJ8': data['puesto'],
            'AJ9': data['nombre_curso'],
            'AJ10': data['horas_curso'],
            'AJ11': data['fecha_inicial_capacitacion'],
            'AJ12': data['fecha_final_capacitacion'],
            'AJ13': data['area_curso'],
            'AJ14': data['nombre_capacitador'],
            'AJ15': data['registro_capacitador'],
            'AJ21': data['razon_social'],
            'AJ22': data['rfc'],
            'AJ23': data['representante_legal'],
            'AJ24': data['representante_trabajadores'],
        }

        for cell, value in cell_mapping.items():
            sheet[cell].value = value

        wb.save(modified_xlsx_path)

        # Build the PDF filename using attributes from the first object in the queryset
        pdf_filename = 'modified_dc3.pdf'
        pdf_path = os.path.join('media/file_templates', pdf_filename)

        # Convert the modified XLSX to PDF using LibreOffice
        self.convert_xlsx_to_pdf(modified_xlsx_path)

        # Return the PDF as a response with the desired filename
        with open(pdf_path, 'rb') as pdf_file:
            filename = f'{personal.curp.get_full_name()}-dc3.pdf'
            pdf_response = HttpResponse(pdf_file.read(), content_type='application/pdf')
            pdf_response['Content-Disposition'] = f'attachment; filename={filename}'

        return pdf_response
