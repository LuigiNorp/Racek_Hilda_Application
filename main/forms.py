from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import Usuario
from .choices import DEPARTAMENTO

class signupform(UserCreationForm):
    nombre = forms.CharField(max_length=150, required=True, help_text='Optional.')
    apellido_paterno = forms.CharField(max_length=150, required=True, help_text='Optional.')
    apellido_materno = forms.CharField(max_length=150, required=True, help_text='Optional.')
    email = forms.EmailField(max_length=254, help_text='Required. Inform a valid email address.')
    departamento = forms.ChoiceField(choices=DEPARTAMENTO, required=True, help_text='Optional.')

    class Meta:
        model = Usuario
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