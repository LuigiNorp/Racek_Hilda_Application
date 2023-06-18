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
    path('add-user/', AddUser.as_view(), name="add_user"),
    path('forget-password/', ForgetPasswordView.as_view() , name="forget_password"),
    path('change-password/<token>/', ChangePasswordView.as_view() , name="change_password"),
    path('logout/' , LogoutView.as_view() , name="logout"),
    # if you want to include the main app, uncomment the following line:
    # path('api/', include('main.urls')),

    # If you want to create a page with all users in a table
    path('users/', Users.as_view(), name='users'),
    path('user/<int:pk>/profile/', CustomUserProfileView.as_view(), name="profile"),
    path('user/<int:pk>/edit/', EditUserView.as_view(), name="edit_user"),
    path('delete-selected-user/', delete_selected_users, name='delete_selected_users'),
    path('groups/', UserGroupsView.as_view(), name='groups'),
    path('add-group/', AddGroupView.as_view(), name='add_group'),
    path('edit-group/<int:pk>/', EditGroupView.as_view(), name='edit_group'),
    path('delete-groups/', DeleteGroups, name='delete_groups'),

    path('clients/', Users.as_view(), name="clients"),
    # path('client/', ClientProfileView.as_view(), name="client-profile"),

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

