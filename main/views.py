import uuid
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


# Create your views here.

# Views for Website
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


class PreviosView(TemplateView):
    template_name = 'personal/personal.html'
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


class EmpleadosView(TemplateView):
    template_name = 'personal/personal.html'
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