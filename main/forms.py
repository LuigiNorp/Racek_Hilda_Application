from django import forms
from .models import CustomUser
from django.contrib.auth.forms import AuthenticationForm, UserChangeForm, UserCreationForm
from .choices import DEPARTAMENTO
from django.contrib.auth.models import Permission
from django.contrib.auth.forms import UserChangeForm
from django.contrib.admin.widgets import FilteredSelectMultiple
from django.contrib.auth.models import Group

from django import forms
from .models import CustomUser

# For regular website

class signupform(UserCreationForm):
    nombre = forms.CharField(max_length=150, required=True, help_text='Optional.')
    apellido_paterno = forms.CharField(max_length=150, required=True, help_text='Optional.')
    apellido_materno = forms.CharField(max_length=150, required=True, help_text='Optional.')
    email = forms.EmailField(max_length=254, help_text='Required. Inform a valid email address.')
    departamento = forms.ChoiceField(choices=DEPARTAMENTO, required=True, help_text='Optional.')

    class Meta:
        model = CustomUser
        fields = ('username', 'nombre', 'apellido_paterno', 'apellido_materno', 'password1', 'password2', 'departamento', 'email',)

    def save(self, commit=True):
        user = super(signupform, self).save(commit=False)
        user.nombre = self.cleaned_data['nombre']
        user.apellido_paterno = self.cleaned_data['apellido_paterno']
        user.apellido_materno = self.cleaned_data['apellido_materno']
        user.email = self.cleaned_data['email']
        user.departamento = self.cleaned_data['departamento']

        if commit:
            user.save()

        return user

# -------------------------------------------------------------------------------------------

# For API REST

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
    # permissions = forms.ModelMultipleChoiceField(
    #     label='Permisos',
    #     queryset=Permission.objects.all(),
    #     widget=FilteredSelectMultiple("Permissions", is_stacked=False),
    #     required=False,)
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


class EditUserForm(UserChangeForm):
    nombre = forms.CharField(max_length=100, widget=forms.TextInput(attrs={'class': 'form-control'}))
    apellido_paterno = forms.CharField(max_length=100, widget=forms.TextInput(attrs={'class': 'form-control'}))
    apellido_materno = forms.CharField(max_length=100, widget=forms.TextInput(attrs={'class': 'form-control'}))
    username = forms.CharField(label='Username', widget=forms.TextInput(attrs={'class': 'form-control'}))
    password = forms.CharField(label='Password', widget=forms.PasswordInput(attrs={'class': 'form-control', 'value': 'existing_password'}))
    email = forms.EmailField(label='Email', widget=forms.EmailInput(attrs={'class': 'form-control'}))
    departamento = forms.ChoiceField(label='Departamento', choices=DEPARTAMENTO, widget=forms.Select(attrs={'class': 'select'}))
    groups = forms.ModelMultipleChoiceField(
        label='Tipos de Cuenta',
        queryset=Group.objects.all(),
        widget=FilteredSelectMultiple(
            "Groups", 
            is_stacked=False, 
            attrs={'class': 'form-control'}),
    required=False,)        

    class Meta:
        model = CustomUser
        fields = ('username', 'nombre', 'apellido_paterno', 'apellido_materno', 'email', 'departamento', 'is_superuser', 'is_staff', 'groups')
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        is_superuser_default_help_text = CustomUser._meta.get_field('is_superuser').help_text
        is_staff_default_help_text = CustomUser._meta.get_field('is_staff').help_text
        groups_help_text = CustomUser._meta.get_field('groups').help_text
        self.fields['is_superuser'].help_text = '<div class="help">{}</div>'.format(is_superuser_default_help_text)
        self.fields['is_staff'].help_text = '<div class="help">{}</div>'.format(is_staff_default_help_text)
        self.fields['groups'].help_text = '<div class="help">{} Mantenga presionado "Control" o "Comando" en una Mac, para seleccionar más de uno.</div>'.format(groups_help_text)


class SignInForm(AuthenticationForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].widget.attrs.update({'class': 'form-control'})
        self.fields['password'].widget.attrs.update({'class': 'form-control'})

    def get_user(self):
        username = self.cleaned_data.get('username')
        password = self.cleaned_data.get('password')

        if username is not None and password:
            try:
                user = CustomUser.objects.get(username=username)
            except CustomUser.DoesNotExist:
                return None

            if user.check_password(password):
                return user

        return None
    
class UserDeleteForm(forms.Form):
    ids = forms.ModelMultipleChoiceField(
        queryset=CustomUser.objects.all(),
        widget=forms.CheckboxSelectMultiple,
    )

class AddGroupForm(forms.ModelForm):
    name = forms.CharField(label=("Name"), max_length=150)
    permissions = forms.ModelMultipleChoiceField(
        label=("Permissions"), required=False,
        queryset=Permission.objects.all(),
        widget=forms.CheckboxSelectMultiple,
    )

    class Meta:
        model = Group
        fields = ('name', 'permissions')
     

class UserGroupForm(forms.ModelForm):
    class Meta:
        model = Group
        fields = '__all__'

    widgets = {
        'name': forms.TextInput(attrs={'class': 'form-control'}),
    }