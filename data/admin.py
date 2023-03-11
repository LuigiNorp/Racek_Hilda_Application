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

@admin.register(CarpetaReferencias)
class CarpetaReferenciasAdmin(admin.ModelAdmin):
    list_display = ('id','empleado')

@admin.register(Referencia)
class ReferenciaAdmin(admin.ModelAdmin):
    list_display = ('id','nombre','apellido_paterno','apellido_materno','tipo_referencia', 'parentesco')

@admin.register(CarpetaDependientes)
class CarpetasDependientesAdmin(admin.ModelAdmin):
    list_display = ('id','empleado','cantidad_dependientes_economicos')

@admin.register(Dependiente)
class DependienteAdmin(admin.ModelAdmin):
    list_display = ('id','nombre','apellido_paterno','apellido_materno','parentesco')

@admin.register(CarpetaExamenPsicologico)
class CarpetaExamenPsicologicoAdmin(admin.ModelAdmin):
    list_display = ('id','empleado','resultado_psicologico')

@admin.register(CarpetaExamenToxicologico)
class CarpetaExamenToxicologicoAdmin(admin.ModelAdmin):
    list_display = ('id','empleado','resultado_toxicologico')

@admin.register(CarpetaExamenMedico)
class CarpetaExamenMedicoAdmin(admin.ModelAdmin):
    list_display = ('id','empleado','medico_resultado','ishihara_resultado')

@admin.register(CarpetaExamenFisico)
class CarpetaExamenFisicoAdmin(admin.ModelAdmin):
    list_display = ('id','empleado','resultado')

@admin.register(CarpetaExamenSocioeconomico)
class CarpetaExamenSocioeconomicoAdmin(admin.ModelAdmin):
    list_display = ('id','empleado','supervisor','telefono_recados')

@admin.register(CarpetaEmpleoAnteriorSeguridadPublica)
class CarpetaEmpleoAnteriorSeguridadPublicaAdmin(admin.ModelAdmin):
    list_display = ('id','empleado')

@admin.register(EmpleoAnteriorSeguridadPublica)
class EmpleoAnteriorSeguridadPublicaAdmin(admin.ModelAdmin):
    list_display = ('id','carp_emp_ant_seg_pub','dependencia','corporacion')

@admin.register(PuestoFuncional)
class PuestoFuncionalAdmin(admin.ModelAdmin):
    list_display = ('id','emp_ant_seg_pub','nombre_puesto')

@admin.register(TipoBaja)
class TipoBajaAdmin(admin.ModelAdmin):
    list_display = ('id','emp_ant_seg_pub','motivo')

@admin.register(CarpetaEmpleoAnterior)
class CarpetaEmpleoAnteriorAdmin(admin.ModelAdmin):
    list_display = ('id','empleado')

@admin.register(EmpleoAnterior)
class EmpleoAnteriorAdmin(admin.ModelAdmin):
    list_display = ('id','emp_ant','empresa')

@admin.register(MotivoSeparacion)
class MotivoSeparacionAdmin(admin.ModelAdmin):
    list_display = ('id','motivo')

@admin.register(CarpetaCapacitacion)
class CarpetaCapacitacionAdmin(admin.ModelAdmin):
    list_display = ('id','empleado')

@admin.register(Capacitacion)
class CapacitacionAdmin(admin.ModelAdmin):
    list_display = ('id','carpeta_capacitacion','institucion_empresa')

@admin.register(TipoCurso)
class TipoCursoAdmin(admin.ModelAdmin):
    list_display = ('id','capacitacion','tipo_curso')

@admin.register(Curso)
class CursoAdmin(admin.ModelAdmin):
    list_display = ('id','carpeta_capacitacion','estudio_curso')

@admin.register(Idioma)
class IdiomaAdmin(admin.ModelAdmin):
    list_display = ('id','carpeta_capacitacion','idioma')

@admin.register(Habilidad)
class HabilidadAdmin(admin.ModelAdmin):
    list_display = ('id','carpeta_capacitacion')

@admin.register(HabilidadPersonalizada)
class HabilidadPersonalizadaAdmin(admin.ModelAdmin):
    list_display = ('id','habilidad','nombre_habilidad')

@admin.register(DocumentosDigitales)
class DocumentosDigitalesAdmin(admin.ModelAdmin):
    list_display = ('id','empleado')

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

@admin.register(Curp)
class CurpAdmin(admin.ModelAdmin):
    list_display = ('id','curp','nombre','apellido_materno','apellido_paterno','iniciales','fecha_nacimiento','sexo')
    def suma_campos(self, obj):
        return obj.campo_1 + obj.campo_2
    suma_campos.short_description = 'Suma de campos'

@admin.register(Rfc)
class RfcAdmin(admin.ModelAdmin):
    list_display = ('id','rfc','razon_social','correo_contacto','validez','tipo',)
