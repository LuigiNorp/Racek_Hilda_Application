import uuid
from django.shortcuts import render,redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from rest_framework.views import APIView
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views.generic import TemplateView
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.admin.views.decorators import staff_member_required
from .helpers import send_forget_password_mail
from rest_framework import generics, authentication, permissions
from rest_framework.authtoken.views import ObtainAuthToken
from django.views import View
from django.core.cache import cache
from django.db.models import Q

from .serializers import *
from .forms import *
from .models import *


# Create your views here.

# Views for API REST
class CreateCustomUserView(generics.CreateAPIView):
    """This view is to create a CustomUser from API.

    """
    serializer_class = CustomUserSerializer
    model_class = CustomUser

class RetrieveUpdateUserView(generics.RetrieveUpdateAPIView):
    serializer_class = CustomUserSerializer
    model_class = CustomUser
    authentication_classes = (authentication.TokenAuthentication,)
    permission_classes = (permissions.IsAuthenticated,)

    def get_object(self):
        return self.request.user

class CreateTokenView(ObtainAuthToken):
    serializer_class = AuthTokenSerializer


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

class Register(LoginRequiredMixin, UserPassesTestMixin, APIView):
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


class AddUser(LoginRequiredMixin, UserPassesTestMixin, APIView):
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
            return redirect('users')
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


class EditUserView(LoginRequiredMixin, UserPassesTestMixin, APIView):
    login_url = '/login/'
    template_name = 'user/user-profile.html'

    def test_func(self):
        user = self.request.user
        if user.groups.filter(name='Superboss').exists() or user.groups.filter(name='Manager').exists() or user.groups.filter(name='Admin').exists():
            return True
        return False

    def get(self, request, pk):
        user = get_object_or_404(CustomUser, pk=pk)
        form = EditUserForm(instance=user)
        is_register_enabled = self.test_func()
        context = {
            'form': form,
            'is_register_enabled': is_register_enabled,
        }
        return render(request, self.template_name, context)

    def post(self, request, pk):
        user = get_object_or_404(CustomUser, pk=pk)
        form = EditUserForm(request.POST, instance=user)
        if form.is_valid():
            form.save()
            return redirect('/')
        else:
            messages.error(request, form.errors)
        
        is_register_enabled = self.test_func()
        context = {
            'form': form,
            'is_register_enabled': is_register_enabled,
        }
        return render(request, self.template_name, context)


class Users(LoginRequiredMixin, UserPassesTestMixin, TemplateView):
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

@login_required
@staff_member_required
def delete_selected_users(request):
    if request.method == 'POST':
        selected_users = request.POST.getlist('selected_users')
        for user_id in selected_users:
            user = CustomUser.objects.get(pk=user_id)
            user.delete()
        # messages.success(request, 'Selected users have been deleted.')
    return redirect('users')


@login_required
@staff_member_required
def AddGroup(request):
    if request.method == 'POST':
        form = UserGroupForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('/groups/')
    else:
        form = UserGroupForm()
    return render(request, 'user/add-group.html', {'form': form})


class UserGroups(LoginRequiredMixin, UserPassesTestMixin, TemplateView):
    login_url = '/login/'
    template_name = 'user/user-groups.html'

    def test_func(self):
        user = self.request.user
        if user.groups.filter(name='Superboss').exists() or user.groups.filter(name='Manager').exists() or user.groups.filter(name='Admin').exists():
            return True
        return False
    
    def get(self, request):
        groups = Group.objects.all()
        filter_text = request.GET.get('q', '')
        if filter_text:
            groups = groups.filter(
                Q(id__icontains=filter_text) |
                Q(name__icontains=filter_text)
            )
        context = self.get_context_data()
        context['groups'] = groups
        context['filter_text'] = filter_text
        return render(request, 'user/user-groups.html', context)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        groups = Group.objects.all()
        context['groups'] = groups
        context['form'] = UserGroupForm()
        context['is_register_enabled'] = self.test_func()
        return context


@login_required
@staff_member_required
def ChangeUserGroup(request):
    form = UserGroupForm()
    context = {'form': form}
    return render(request, 'user/user-group.html', context)


@login_required
@staff_member_required
def DeleteGroups(request):
    if request.method == 'POST':
        selected_groups = request.POST.getlist('selected_groups')
        for group_id in selected_groups:
            group = Group.objects.get(pk=group_id)
            group.delete()
        # messages.success(request, 'Selected groups have been deleted.')
    return redirect('groups')

# class ClientProfileView(LoginRequiredMixin, APIView):
#     login_url = '/login/'
#     template_name = 'client-profile.html'

#     def get(self, request, pk):
#         user = get_object_or_404(CustomUser, pk=pk)
#         form = EditClientProfileForm(instance=user)
#         context = {
#             'form': form,
#         }
#         return render(request, self.template_name, context)


@login_required
@staff_member_required
def EmploymentPortfolio(request):
    user = request.user
    if user.groups.filter(name='Superboss').exists() or user.groups.filter(name='Manager').exists() or user.groups.filter(name='Admin').exists():
        is_register_enabled = True
    else:
        is_register_enabled = False
    context = {
        'is_register_enabled': is_register_enabled,
    }
    return render(request,'employment-portfolio.html', context)

@login_required
@staff_member_required
def DependentsPortfolio(request):
    user = request.user
    if user.groups.filter(name='Superboss').exists() or user.groups.filter(name='Manager').exists() or user.groups.filter(name='Admin').exists():
        is_register_enabled = True
    else:
        is_register_enabled = False
    context = {
        'is_register_enabled': is_register_enabled,
    }
    return render(request,'dependents-portfolio.html', context)


@login_required
@staff_member_required
def GeneralPortfolio(request):
    user = request.user
    if user.groups.filter(name='Superboss').exists() or user.groups.filter(name='Manager').exists() or user.groups.filter(name='Admin').exists():
        is_register_enabled = True
    else:
        is_register_enabled = False
    context = {
        'is_register_enabled': is_register_enabled,
    }
    return render(request,'general-portfolio.html', context)


@login_required
@staff_member_required
def ReferencesPortfolio(request):
    user = request.user
    if user.groups.filter(name='Superboss').exists() or user.groups.filter(name='Manager').exists() or user.groups.filter(name='Admin').exists():
        is_register_enabled = True
    else:
        is_register_enabled = False
    context = {
        'is_register_enabled': is_register_enabled,
    }
    return render(request,'references-portfolio.html', context)


@login_required
@staff_member_required
def ExamsPortfolio(request):
    user = request.user
    if user.groups.filter(name='Superboss').exists() or user.groups.filter(name='Manager').exists() or user.groups.filter(name='Admin').exists():
        is_register_enabled = True
    else:
        is_register_enabled = False
    context = {
        'is_register_enabled': is_register_enabled,
        'pages': pages,
    }
    pages = {
    'page1': 'home2.html',
    'page2': 'page2.html',
    'page3': 'page3.html',
    } 
    return render(request,'exams-portfolio.html', context)


@login_required
@staff_member_required
def PsychologicalPortfolio(request):
    user = request.user
    if user.groups.filter(name='Superboss').exists() or user.groups.filter(name='Manager').exists() or user.groups.filter(name='Admin').exists():
        is_register_enabled = True
    else:
        is_register_enabled = False
    context = {
        'is_register_enabled': is_register_enabled,
    }
    return render(request,'psychological-portfolio.html', context)


@login_required
@staff_member_required
def ToxicologicalPortfolio(request):
    user = request.user
    if user.groups.filter(name='Superboss').exists() or user.groups.filter(name='Manager').exists() or user.groups.filter(name='Admin').exists():
        is_register_enabled = True
    else:
        is_register_enabled = False
    context = {
        'is_register_enabled': is_register_enabled,
    }
    return render(request,'toxicological-portfolio.html', context)


@login_required
@staff_member_required
def MedicalPortfolio(request):
    user = request.user
    if user.groups.filter(name='Superboss').exists() or user.groups.filter(name='Manager').exists() or user.groups.filter(name='Admin').exists():
        is_register_enabled = True
    else:
        is_register_enabled = False
    context = {
        'is_register_enabled': is_register_enabled,
    }
    return render(request,'medical-portfolio.html', context)


@login_required
@staff_member_required
def PhysicalPortfolio(request):
    user = request.user
    if user.groups.filter(name='Superboss').exists() or user.groups.filter(name='Manager').exists() or user.groups.filter(name='Admin').exists():
        is_register_enabled = True
    else:
        is_register_enabled = False
    context = {
        'is_register_enabled': is_register_enabled,
    }
    return render(request,'physical-portfolio.html', context)


@login_required
@staff_member_required
def SocioeconomicPortfolio(request):
    user = request.user
    if user.groups.filter(name='Superboss').exists() or user.groups.filter(name='Manager').exists() or user.groups.filter(name='Admin').exists():
        is_register_enabled = True
    else:
        is_register_enabled = False
    context = {
        'is_register_enabled': is_register_enabled,
    }
    return render(request,'socioeconomic-portfolio.html', context)


@login_required
@staff_member_required
def PolygraphPortfolio(request):
    user = request.user
    if user.groups.filter(name='Superboss').exists() or user.groups.filter(name='Manager').exists() or user.groups.filter(name='Admin').exists():
        is_register_enabled = True
    else:
        is_register_enabled = False
    context = {
        'is_register_enabled': is_register_enabled,
    }
    return render(request,'polygraph-portfolio.html', context)


