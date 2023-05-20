from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import CustomUser
from django.contrib.auth.forms import AuthenticationForm
from django.utils.safestring import mark_safe
from django.forms.widgets import CheckboxInput
from .choices import DEPARTAMENTO

from django import forms
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.forms import ReadOnlyPasswordHashField
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

class CustomUserRegisterForm(forms.ModelForm):
    
    # Custom User creation form.
    password1 = forms.CharField(label='Password', widget=forms.PasswordInput(attrs={'class': 'form-control'}))
    password2 = forms.CharField(label='Password confirmation', widget=forms.PasswordInput(attrs={'class': 'form-control'}))
    username = forms.CharField(label='Username', widget=forms.TextInput(attrs={'class': 'form-control'}))
    nombre = forms.CharField(label='Nombre', widget=forms.TextInput(attrs={'class': 'form-control'}))
    apellido_paterno = forms.CharField(label='Apellido Paterno', widget=forms.TextInput(attrs={'class': 'form-control'}))
    apellido_materno = forms.CharField(label='Apellido Materno', widget=forms.TextInput(attrs={'class': 'form-control'}))
    email = forms.EmailField(label='Email', widget=forms.EmailInput(attrs={'class': 'form-control'}))
    departamento = forms.ChoiceField(label='Departamento', choices=DEPARTAMENTO, widget=forms.Select(attrs={'class': 'select'}))

    class Meta:
        model = CustomUser
        fields = ('username', 'nombre', 'apellido_paterno', 'apellido_materno', 'email','departamento', 'is_superuser', 'is_staff',)

    # Agregar div entre boolean y helptext
    def __init__(self, *args, **kwargs):
        super(CustomUserRegisterForm, self).__init__(*args, **kwargs)
        is_superuser_default_help_text = CustomUser._meta.get_field('is_superuser').help_text
        is_staff_default_help_text = CustomUser._meta.get_field('is_staff').help_text
        self.fields['is_superuser'].help_text = '<div class="help">{}</div>'.format(is_superuser_default_help_text)
        self.fields['is_staff'].help_text = '<div class="help">{}</div>'.format(is_staff_default_help_text)

    def clean_password2(self):
        # Check that both passwords match.
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Passwords don't match")
        return password2

    def save(self, commit=True):
        # Save the provided password in hashed format
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user

class CustomUserChangeForm(forms.ModelForm):
    # Custom User change form.
    # Password is hidden by default, but can be changed if desired.
    password = ReadOnlyPasswordHashField()

    class Meta:
        model = CustomUser
        fields = ('email', 'password', 'first_name', 'last_name', 'is_active')

    def clean_password(self):
        # Regardless of the provided value, don't return the password in plain text format.
        return self.initial["password"]

class CustomUserAdminForm(UserAdmin):
    # The form to add and change user instances
    form = CustomUserChangeForm
    add_form = CustomUserRegisterForm

    # The fields to be used in displaying the User model.
    list_display = ('username', 'nombre', 'apellido_paterno', 'apellido_materno', 'password1', 'password2', 'departamento', 'email', 'is_active', 'is_admin')
    list_filter = ('is_admin',)
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Personal Information', {'fields': ('nombre', 'apellido_paterno', 'apellido_materno')}),
        ('Permissions', {'fields': ('is_active', 'is_admin')}),
    )
    
    # Customize admin templates to use the new form.
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'nombre', 'apellido_paterno', 'apellido_materno', 'password1', 'password2', 'departamento', 'email', 'is_active', 'is_admin')
        }),
    )
    search_fields = ('email',)
    ordering = ('email',)
    filter_horizontal = ()

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