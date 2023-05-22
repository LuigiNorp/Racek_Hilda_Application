from django.shortcuts import render,redirect
from django.contrib.auth.decorators import login_required
from django.views.generic.edit import CreateView
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import authenticate,login,logout
from .helpers import send_forget_password_mail

from django.contrib.admin.views.decorators import staff_member_required
from django.urls import reverse_lazy

from rest_framework import generics, authentication, permissions
from rest_framework.authtoken.views import ObtainAuthToken
from .serializers import CustomUserSerializer, AuthTokenSerializer
from django.shortcuts import get_object_or_404
from .forms import CustomUserAdminForm
from rest_framework.response import Response
from rest_framework.views import APIView
from .forms import *

import uuid

from .models import *


# Create your views here.

# Views for API REST
class CreateCustomUserView(generics.CreateAPIView):
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

def Login(request):
    try:
        if request.method == 'POST':
            username = request.POST.get('username')
            password = request.POST.get('password')
            
            if not username or not password:
                messages.success(request, 'Both Username and Password are required.')
                return redirect('/login/')
            user_obj = User.objects.filter(username = username).first()
            if user_obj is None:
                messages.success(request, 'User not found.')
                return redirect('/login/')
        
        
            user = authenticate(username = username , password = password)
            
            if user is None:
                messages.success(request, 'Wrong password.')
                return redirect('/login/')
        
            login(request , user)
            return redirect('/')           
    except Exception as e:
        print(e)
    return render(request , 'login/login.html')


@login_required
@staff_member_required
def Register(request):
    if request.method == 'POST':
        form = CustomUserRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            # Redirect to success page.
    else:
        form = CustomUserRegisterForm()
    
    user = request.user
    if user.groups.filter(name='Superboss').exists() or user.groups.filter(name='Manager').exists() or user.groups.filter(name='Admin').exists():
        is_register_enabled = True
    else:
        is_register_enabled = False

    context = {
        'form': form,
        'is_register_enabled': is_register_enabled,
    }

    return render(request, 'login/register.html', context)


def Logout(request):
    logout(request)
    return redirect('/')


@login_required(login_url='/login/')
@staff_member_required
def Home(request):
    user = request.user
    if user.groups.filter(name='Superboss').exists() or user.groups.filter(name='Manager').exists() or user.groups.filter(name='Admin').exists():
        is_register_enabled = True
    else:
        is_register_enabled = False
    context = {
        'is_register_enabled': is_register_enabled,
    }
    return render(request,'home.html', context)

def ChangePassword(request , token):
    context = {}    
    
    try:
        profile_obj = Profile.objects.filter(forget_password_token = token).first()
        context = {'user_id' : profile_obj.user.id}
        
        if request.method == 'POST':
            new_password = request.POST.get('new_password')
            confirm_password = request.POST.get('reconfirm_password')
            user_id = request.POST.get('user_id')
            
            if user_id is  None:
                messages.success(request, 'No user id found.')
                return redirect(f'/change-password/{token}/')
                
            
            if  new_password != confirm_password:
                messages.success(request, 'both should  be equal.')
                return redirect(f'/change-password/{token}/')
                         
            
            user_obj = User.objects.get(id = user_id)
            user_obj.set_password(new_password)
            user_obj.save()
            return redirect('/login/')
         
    except Exception as e:
        print(e)
    return render(request , 'login/change-password.html' , context)


def ForgetPassword(request):
    try:
        if request.method == 'POST':
            username = request.POST.get('username')
            
            if not User.objects.filter(username=username).first():
                messages.success(request, 'Not user found with this username.')
                return redirect('/forget-password/')
            
            user_obj = User.objects.get(username = username)
            token = str(uuid.uuid4())
            profile_obj= Profile.objects.get(user = user_obj)
            profile_obj.forget_password_token = token
            profile_obj.save()
            send_forget_password_mail(user_obj.email , token)
            messages.success(request, 'An email is sent.')
            return redirect('/forget-password/')
    
    except Exception as e:
        print(e)
    return render(request , 'login/forget-password.html')


@login_required
@staff_member_required
def UserAccount(request):
    user= request.user
    username_max_length = user._meta.get_field('username').max_length
    email_max_length = user._meta.get_field('email').max_length
    password_max_length = user._meta.get_field('password').max_length
    nombre_max_length = user._meta.get_field('nombre').max_length
    apellido_materno_max_length = user._meta.get_field('apellido_materno').max_length
    apellido_paterno_max_length = user._meta.get_field('apellido_paterno').max_length

    user = request.user
    if user.groups.filter(name='Superboss').exists() or user.groups.filter(name='Manager').exists() or user.groups.filter(name='Admin').exists():
        is_register_enabled = True
    else:
        is_register_enabled = False

    context = {
                'user':user,
                'username_max_length': username_max_length,
                'email_max_length': email_max_length,
                'password_max_length': password_max_length,
                'nombre_max_length': nombre_max_length,
                'apellido_materno_max_length': apellido_materno_max_length,
                'apellido_paterno_max_length': apellido_paterno_max_length,
                'is_register_enabled': is_register_enabled,
               }
    return render(request , 'user-account.html', context)


@staff_member_required
class CreateUserAdminView(CreateView):
    model = CustomUser
    fields = [ # lista los campos que se muestran en el formulario
        'id',
        'nombre',
        'apellido_materno',
        'apellido_paterno',
        'email',
        'departamento',
        'is_superuser',
        'username'] 
    success_url = reverse_lazy('user-account_list')
    template_name = 'admin/user-account.html'

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


