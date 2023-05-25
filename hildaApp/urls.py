"""hildaApp URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from data.views import *
from main.views import *

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('data.urls')),

    # if you want to include the main app, uncomment the following line:
    # path('api/', include('main.urls')),

    path('users/', UserAccountView, name="users"),
    path('', Home, name="home"),
    path('login/', Login , name="login"),\
    path('register/', Register.as_view(), name="register"),
    path('forget-password/', ForgetPassword , name="forget_password"),
    path('change-password/<token>/', ChangePassword , name="change_password"),
    path('logout/' , Logout , name="logout"),
    path('employment-portfolio/', EmploymentPortfolio, name="employment-portfolio"),
    path('general-portfolio/', GeneralPortfolio, name="general-portfolio"),
    path('references-portfolio/', ReferencesPortfolio, name="references-portfolio"),
    path('dependents-portfolio/', DependentsPortfolio, name="dependents-portfolio"),
    path('exams-portfolio/', ExamsPortfolio, name="exams-portfolio"),
    path('psychological-portfolio/', PsychologicalPortfolio, name="psychological-portfolio"),
    path('toxicological-portfolio/', ToxicologicalPortfolio, name="toxicological-portfolio"),
    path('medical-portfolio/', MedicalPortfolio, name="medical-portfolio"),
    path('physical-portfolio/', PhysicalPortfolio, name="physical-portfolio"),
    path('socioeconomic-portfolio/', SocioeconomicPortfolio, name="socioeconomic-portfolio"),
    path('polygraph-portfolio/', PolygraphPortfolio, name="polygraph-portfolio"),
    
]

