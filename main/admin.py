from django.contrib import admin
from .models import *


# Register your models here.
@admin.register(CustomUser)
class CustomUserAdmin(admin.ModelAdmin):
    list_display = (
        'id','nombre','apellido_materno','apellido_paterno',
        'email','departamento','is_superuser','username', 'group',
    )
    exclude = ('first_name', 'last_name', 'user_permissions')

    def group(self, obj):
        return obj.groups.first()
    group.short_description = 'Group'

    ordering = ('-id',)

