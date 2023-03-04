from django.contrib import admin
from .models import *

# Register your models here.
    
@admin.register(Cliente)
class ClienteAdmin(admin.ModelAdmin):
    list_display = ('id','nombre_comercial','razon_social','activo',)

@admin.register(Sede)
class SedeAdmin(admin.ModelAdmin):
     list_display = ('id','clave_sede', 'nombre_sede', 'cliente')

@admin.register(ClienteGenerales)
class ClienteGeneralesAdmin(admin.ModelAdmin):
     list_display = ('id','cliente', 'rfc', 'reg_estatal', 'reg_federal', 'telefono_1', 'representante_legal', 'registro_patronal')

@admin.register(ClientePagos)
class ClientePagosAdmin(admin.ModelAdmin):
    list_display = ('id','cliente','encargado_pagos','telefono_oficina', 'rfc', 'factura_subtotal', 'factura_iva','factura_total')

@admin.register(ClienteContactos)
class ClienteContactosAdmin(admin.ModelAdmin):
    list_display = ('id','cliente','nombre_contacto','puesto','telefono_1','email_1',)

@admin.register(Empleado)
class EmpleadoAdmin(admin.ModelAdmin):
    list_display = ('id','cliente',)

@admin.register(CarpetaLaboral)
class CarpetaLaboralAdmin(admin.ModelAdmin):
    list_display = ('id','empleado','estatus_empleado','proceso_racek','estatus_empleado','cedula','rango',)

@admin.register(Puesto)
class PuestoAdmin(admin.ModelAdmin):
    list_display = ('id','nombre_puesto','carpeta_laboral')

@admin.register(CarpetaGenerales)
class CarpetaGeneralesAdmin(admin.ModelAdmin):
    list_display = ('numero_elemento','empleado','email_empleado','telefono_domicilio','estado_civil','cuip','clave_ine','nss')

@admin.register(DocumentosDigitales)
class DocumentosDigitalesAdmin(admin.ModelAdmin):
    list_display = ('id','empleado')

@admin.register(Curp)
class CurpAdmin(admin.ModelAdmin):
    list_display = ('id','curp','nombre','apellido_materno','apellido_paterno','iniciales','fecha_nacimiento','sexo')

@admin.register(Rfc)
class RfcAdmin(admin.ModelAdmin):
    list_display = ('id','rfc','razon_social','correo_contacto','validez','tipo',)

@admin.register(Domicilio)
class DomicilioAdmin(admin.ModelAdmin):
    list_display = ('id','empleado','cliente_generales','cliente_pagos','calle','numero_exterior','ciudad')

@admin.register(CodigoPostal)
class CodigoPostalAdmin(admin.ModelAdmin):
    list_display = ('id','codigo_postal')

@admin.register(Colonia)
class ColoniaAdmin(admin.ModelAdmin):
    list_display = ('id','colonia')

@admin.register(Municipio)
class MunicipioAdmin(admin.ModelAdmin):
    list_display = ('id','municipio')

@admin.register(Estado)
class EstadoAdmin(admin.ModelAdmin):
    list_display = ('id','estado')

@admin.register(Pais)
class PaisAdmin(admin.ModelAdmin):
    list_display = ('id','pais')