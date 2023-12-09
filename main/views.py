from main.reports.report_tools import *
import uuid
from openpyxl import load_workbook
from openpyxl.drawing.image import Image as XlsxImage
from openpyxl.worksheet.page import PageMargins
import subprocess
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


class GenerateDC3View(View):

	def get(self, personal_id, request, queryset, desired_height_cm=3.5):
		original_file_path = 'media/file_templates/DC3 ACTUALIZADO.xlsx'
		modified_xlsx_path = 'media/file_templates/modified_dc3.xlsx'
		wb = load_workbook(original_file_path)
		sheet = wb.active

		# Set paper size to letter and setting margins
		xlsx_sheet_presets(sheet)

		for personal in queryset:
			curp = personal.curp
			carpeta_laboral = personal.carpetalaboral
			ocupacion = carpeta_laboral.ocupacion
			capacitacion = personal.capacitaciones.all().last()
			instructor = capacitacion.instructor
			cliente = personal.cliente
			documentos_cliente = cliente.documentoscliente
			representante_trabajadores = cliente.representantetrabajadores
			carpeta_cliente_generales = cliente.carpetaclientegenerales
			
			data = {
				'nombre_completo': f'get_nombre_completo',
				'curp': f'curp',
				'ocupacion': f'get_ocupacion_fullname',
				'puesto': f'display_choice_value',
				'razon_social': f'razon_social',
				'rfc': f'rfc',
				'nombre_curso': f'curso',
				'horas_curso': f'duracion',
				'fecha_inicial_capacitacion': f'inicio',
				'fecha_final_capacitacion': f'conclusion',
				'area_curso': f'display_choice_value',
				'nombre_instructor': f'nombre_instructor',
				'registro_instructor': f'numero_registro',
				'representante_legal': f'representante_legal',
				'representante_trabajadores': f'nombre_completo',
				'logotipo': f'logotipo',
				'qr_code': f'qr_code',
			}

			verified_data = {
				'nombre_completo': verify_function_value('nombre_completo', curp, data),
				'curp': verify_text_data('curp', curp, data),
				'ocupacion': verify_function_value('ocupacion', ocupacion, data),
				'puesto': verify_function_value('puesto', carpeta_laboral, data, ['puesto']),
				'razon_social': verify_text_data('razon_social', cliente, data),
				'rfc': verify_text_data('rfc', carpeta_cliente_generales, data),
				'nombre_curso': verify_text_data('nombre_curso', capacitacion, data),
				'horas_curso': verify_text_data('horas_curso', capacitacion, data),
				'fecha_inicial_capacitacion': verify_date_data('fecha_inicial_capacitacion', capacitacion, data, '%d/%m/%Y'),
				'fecha_final_capacitacion': verify_date_data('fecha_final_capacitacion', capacitacion, data, '%d/%m/%Y'),
				'area_curso': verify_function_value('area_curso', capacitacion, data, ['area_curso']),
				'nombre_instructor': verify_text_data('nombre_instructor', instructor, data),
				'registro_instructor': verify_text_data('registro_instructor', instructor, data),
				'representante_legal': verify_text_data('representante_legal', carpeta_cliente_generales, data),
				'representante_trabajadores': verify_text_data('representante_trabajadores', representante_trabajadores, data),
				'logotipo': verify_media_data('logotipo', documentos_cliente, data),
				'qr_code': verify_media_data('qr_code', documentos_cliente, data),
			}

			# Define the data to be replaced in the cells for each 'personal' object
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

			if data['logotipo']:
				img_path = verified_data['logotipo']
				width, height = scale_image_from_height(img_path, desired_height_cm)
				add_image_to_worksheet(img_path, 'B1', sheet, width, height)

			if data['qr_code']:
				img_path = verified_data['qr_code']
				width, height = scale_image_from_height(img_path, desired_height_cm)
				add_image_to_worksheet(img_path, 'AC1', sheet, width, height)

		wb.save(modified_xlsx_path)

		# Build the PDF filename using attributes from the first object in the queryset
		first_personal = queryset.first()
		pdf_filename = 'modified_dc3.pdf'
		pdf_path = os.path.join('media/file_templates', pdf_filename)

		# Convert the modified XLSX to PDF using LibreOffice
		convert_xlsx_to_pdf(modified_xlsx_path, pdf_path)

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
