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
    path('users/', include('main.urls')),
    path('index/', Index, name='index'),

    # if you want to include the main app, uncomment the following line:
    # path('api/', include('main.urls')),
 
    path('' , Home , name="home"),
    path('login/' , Login , name="login"),\
    path('register/' , Register , name="register"),
    path('forget-password/' , ForgetPassword , name="forget_password"),
    path('change-password/<token>/' , ChangePassword , name="change_password"),
    path('logout/' , Logout , name="logout"),

    path('employees/' , Employees , name="employees"),
    
]

