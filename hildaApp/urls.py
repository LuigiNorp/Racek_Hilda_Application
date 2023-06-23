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
    path('', HomeView.as_view(), name="home"),
    path('login/', LoginView.as_view() , name="login"),\
    path('register/', Register.as_view(), name="register"),
    path('forget-password/', ForgetPasswordView.as_view() , name="forget_password"),
    path('change-password/<token>/', ChangePasswordView.as_view() , name="change_password"),
    path('logout/' , LogoutView.as_view() , name="logout"),
    # if you want to include the main app, uncomment the following line:
    # path('api/', include('main.urls')),

    # If you want to create a page with all users in a table

    path('users/', Users.as_view(), name='users'),
    path('user/<int:pk>/profile/', CustomUserProfileView.as_view(), name="profile"),
    path('clients/', Clients.as_view(), name="clients"),
    path('employees/', Personal.as_view(), name="employees"),
    path('user/<int:pk>/history/', UserHistory.as_view(), name="history"),
]

