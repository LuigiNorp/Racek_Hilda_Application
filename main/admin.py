from django.contrib import admin
from .models import *
from django.contrib.auth.models import Group
from django.contrib.auth.admin import GroupAdmin
from .forms import GroupForm

@admin.register(CustomUser)
class CustomUserAdmin(admin.ModelAdmin):
    def get_list_display(self, request):
        if request.user.is_superuser:
            return ('id', 'nombre', 'apellido_materno', 'apellido_paterno', 'email', 'departamento', 'is_superuser', 'username')
        else:
            return ('id', 'nombre', 'apellido_materno', 'apellido_paterno', 'email', 'departamento', 'username')



admin.site.unregister(Group)

@admin.register(Group)
class MyGroupAdmin(GroupAdmin):
    form = GroupForm
