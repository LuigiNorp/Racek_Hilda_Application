from django.contrib.auth.models import Group, Permission
from .forms import EditGroupForm
from django.contrib import admin
from .models import *

# Register your models here.
@admin.register(CustomUser)
class CustomUserAdmin(admin.ModelAdmin):
    list_display = ('id','nombre','apellido_materno','apellido_paterno','email','departamento','is_superuser','username')

class GroupAdmin(admin.ModelAdmin):
    form = EditGroupForm

    def get_form(self, request, obj=None, **kwargs):
        if obj is not None:
            # Pass an instance of the Group model to the form constructor
            kwargs['instance'] = obj
        return super().get_form(request, obj, **kwargs)