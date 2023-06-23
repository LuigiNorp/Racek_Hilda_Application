from .models import CustomUser
from django.contrib.auth.forms import UserChangeForm, UserCreationForm
from .choices import DEPARTAMENTO
from django.contrib.admin.widgets import FilteredSelectMultiple
from django.contrib.auth.models import Group
from django import forms

from main.models import *
from data.models import *


class CustomUserRegisterForm(UserCreationForm):
    # Custom User creation form.
    username = forms.CharField(label='Username', widget=forms.TextInput(attrs={'class': 'form-control'}))
    nombre = forms.CharField(label='Nombre', widget=forms.TextInput(attrs={'class': 'form-control'}))
    apellido_paterno = forms.CharField(label='Apellido Paterno', widget=forms.TextInput(attrs={'class': 'form-control'}))
    apellido_materno = forms.CharField(label='Apellido Materno', widget=forms.TextInput(attrs={'class': 'form-control'}))
    email = forms.EmailField(label='Email', widget=forms.EmailInput(attrs={'class': 'form-control'}))
    departamento = forms.ChoiceField(label='Departamento', choices=DEPARTAMENTO, widget=forms.Select(attrs={'class': 'select'}))
    groups = forms.ModelMultipleChoiceField(
        label='Tipos de Cuenta',
        queryset=Group.objects.all(),
        widget=FilteredSelectMultiple("Groups", is_stacked=False),
        required=False,)
    password1 = forms.CharField(label='Password', widget=forms.PasswordInput(attrs={'class': 'form-control'}))
    password2 = forms.CharField(label='Password confirmation', widget=forms.PasswordInput(attrs={'class': 'form-control'}))

    class Meta:
        model = CustomUser
        fields = ('username', 'nombre', 'apellido_paterno', 'apellido_materno', 'email', 'departamento', 'is_superuser', 'is_staff', 'groups')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        is_superuser_default_help_text = CustomUser._meta.get_field('is_superuser').help_text
        is_staff_default_help_text = CustomUser._meta.get_field('is_staff').help_text
        # permissions_help_text = CustomUser._meta.get_field('user_permissions').help_text
        groups_help_text = CustomUser._meta.get_field('groups').help_text
        self.fields['is_superuser'].help_text = '<div class="help">{}</div>'.format(is_superuser_default_help_text)
        self.fields['is_staff'].help_text = '<div class="help">{}</div>'.format(is_staff_default_help_text)
        self.fields['groups'].help_text = '<div class="help">{} Mantenga presionado "Control" o "Comando" en una Mac, para seleccionar más de uno.</div>'.format(groups_help_text)
        # self.fields['permissions'].help_text = '<div class="help" id="id_permissions_helptext">{}. Mantenga presionado "Control" o "Comando" en una Mac, para seleccionar más de uno.</div>'.format(permissions_help_text)
    
    def clean_password2(self):
        # Check that both passwords match.
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Las contraseñas no coinciden")
        return password2

    def save(self, commit=True):
        # Save the provided password in hashed format
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
            self.save_m2m()  # Save many-to-many relationships (permissions)
        return user


class CustomUserProfileForm(UserChangeForm):
    nombre = forms.CharField(max_length=100, widget=forms.TextInput(attrs={'class': 'form-control'}))
    apellido_paterno = forms.CharField(max_length=100, widget=forms.TextInput(attrs={'class': 'form-control'}))
    apellido_materno = forms.CharField(max_length=100, widget=forms.TextInput(attrs={'class': 'form-control'}))
    username = forms.CharField(label='Username', widget=forms.TextInput(attrs={'class': 'form-control'}))
    password = forms.CharField(label='Password', widget=forms.PasswordInput(attrs={'class': 'form-control', 'value': 'existing_password'}))
    email = forms.EmailField(label='Email', widget=forms.EmailInput(attrs={'class': 'form-control'}))
    departamento = forms.ChoiceField(label='Departamento', choices=DEPARTAMENTO, widget=forms.Select(attrs={'class': 'form-control'}))

    class Meta:
        model = CustomUser
        fields = ('username', 'nombre', 'apellido_paterno', 'apellido_materno', 'email', 'departamento')





class ClientForm(forms.ModelForm):
    class Meta:
        model = Cliente
        fields = '__all__'

class LocationForm(forms.ModelForm):
    class Meta:
        model = Sede
        fields = '__all__'

class ClientGeneralFolderForm(forms.ModelForm):
    class Meta:
        model = CarpetaClienteGenerales
        fields = '__all__'

class ClientProfileForm(forms.Form):
    cliente_form = ClientForm()
    sede_form = LocationForm()
    carpeta_form = ClientGeneralFolderForm()