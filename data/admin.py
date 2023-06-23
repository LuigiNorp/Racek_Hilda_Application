from django.contrib import admin
from .models import *

# Register your models here.

@admin.register(Curp)
class CurpAdmin(admin.ModelAdmin):
    list_display = ('id','curp','nombre','apellido_materno','apellido_paterno','iniciales','fecha_nacimiento','sexo')


@admin.register(Rfc)
class RfcAdmin(admin.ModelAdmin):
    list_display = ('id','rfc','razon_social','correo_contacto','validez','tipo',)






class SedeInline(admin.StackedInline):
    model = Sede
class CarpetaClienteGeneralesInline(admin.StackedInline):
    model = CarpetaClienteGenerales
class CarpetaClientePagosInline(admin.StackedInline):
    model = CarpetaClientePagos
class CarpetaClienteContactosInline(admin.StackedInline):
    model = CarpetaClienteContactos

@admin.register(Cliente)
class ClienteAdmin(admin.ModelAdmin):
    list_display = ('id','nombre_comercial','razon_social','activo',)
    inlines = [SedeInline, CarpetaClienteGeneralesInline, CarpetaClientePagosInline, CarpetaClienteContactosInline]







class CarpetaLaboralAdmin(admin.StackedInline):
    model = CarpetaLaboral

class CarpetaGeneralesAdmin(admin.StackedInline):
    model = CarpetaGenerales

class CarpetaReferenciasAdmin(admin.StackedInline):
    model = CarpetaReferencias

class CarpetaDependientesAdmin(admin.StackedInline):
    model = CarpetaDependientes
    
class CarpetaExamenFisicoInline(admin.StackedInline):
    model = CarpetaExamenFisico

class CarpetaExamenMedicoInline(admin.StackedInline):
    model = CarpetaExamenMedico

class CarpetaExamenPsicologicoInline(admin.StackedInline):
    model = CarpetaExamenPsicologico

class CarpetaExamenToxicologicoInline(admin.StackedInline):
    model = CarpetaExamenToxicologico

class CarpetaExamenSocioeconomicoInline(admin.StackedInline):
    model = CarpetaExamenSocioeconomico

class CarpetaExamenPoligrafoInline(admin.StackedInline):
    model = CarpetaExamenPoligrafo

class CarpetaEmpleoAnteriorSeguridadPublicaAdmin(admin.StackedInline):
    model = CarpetaEmpleoAnteriorSeguridadPublica

class CarpetaEmpleoAnteriorAdmin(admin.StackedInline):
    model = CarpetaEmpleoAnterior

class CarpetaCapacitacionAdmin(admin.StackedInline):
    model = CarpetaCapacitacion

class CarpetaMediaFilicacionAdmin(admin.StackedInline):
    model = CarpetaMediaFiliacion


class DocumentosDigitalesAdmin(admin.StackedInline):
    model = DocumentosDigitales

@admin.register(Personal)
class PersonalAdmin(admin.ModelAdmin):
    list_display = ('id', 'get_full_name', 'cliente',)
    inlines =     inlines = [
        CarpetaExamenFisicoInline,
        CarpetaExamenMedicoInline,
        CarpetaExamenPsicologicoInline,
        CarpetaExamenToxicologicoInline,
        CarpetaExamenSocioeconomicoInline,
        CarpetaExamenPoligrafoInline,
        CarpetaLaboralAdmin,
        CarpetaGeneralesAdmin,
        CarpetaReferenciasAdmin,
        CarpetaDependientesAdmin,
        CarpetaEmpleoAnteriorSeguridadPublicaAdmin,
        CarpetaEmpleoAnteriorAdmin,
        CarpetaCapacitacionAdmin,
        CarpetaMediaFilicacionAdmin,
        DocumentosDigitalesAdmin,
    ]
    
    def get_full_name(self, obj):
        return f"{obj.curp.nombre} {obj.curp.apellido_paterno} {obj.curp.apellido_materno}"

    get_full_name.short_description = 'Full Name'







@admin.register(Evaluador)
class EvaluadorAdmin(admin.ModelAdmin):
    list_display = ('id','evaluador', 'personal')

@admin.register(Puesto)
class PuestoAdmin(admin.ModelAdmin):
    list_display = ('id','nombre_puesto','carpeta_laboral')

@admin.register(Referencia)
class ReferenciaAdmin(admin.ModelAdmin):
    list_display = ('id','nombre','apellido_paterno','apellido_materno','tipo_referencia', 'parentesco')

@admin.register(Dependiente)
class DependienteAdmin(admin.ModelAdmin):
    list_display = ('id','nombre','apellido_paterno','apellido_materno','parentesco')

@admin.register(EmpleoAnteriorSeguridadPublica)
class EmpleoAnteriorSeguridadPublicaAdmin(admin.ModelAdmin):
    list_display = ('id','carp_emp_ant_seg_pub','dependencia','corporacion')

@admin.register(PuestoFuncional)
class PuestoFuncionalAdmin(admin.ModelAdmin):
    list_display = ('id','emp_ant_seg_pub','nombre_puesto')

@admin.register(TipoBaja)
class TipoBajaAdmin(admin.ModelAdmin):
    list_display = ('id','emp_ant_seg_pub','motivo')

@admin.register(EmpleoAnterior)
class EmpleoAnteriorAdmin(admin.ModelAdmin):
    list_display = ('id','emp_ant','empresa')

@admin.register(MotivoSeparacion)
class MotivoSeparacionAdmin(admin.ModelAdmin):
    list_display = ('id','motivo')

@admin.register(Capacitacion)
class CapacitacionPreviaAdmin(admin.ModelAdmin):
    list_display = ('id','carpeta_capacitacion','institucion_empresa')

@admin.register(TipoCurso)
class TipoCursoAdmin(admin.ModelAdmin):
    list_display = ('id','tipo_curso')

# @admin.register(CapacitacionEnCurso)
# class CapacitacionEnCursoAdmin(admin.ModelAdmin):
#     list_display = ('id','carpeta_capacitacion','estudio_curso')

@admin.register(Idioma)
class IdiomaAdmin(admin.ModelAdmin):
    list_display = ('id','carpeta_capacitacion','idioma')

# @admin.register(Habilidad)
# class HabilidadAdmin(admin.ModelAdmin):
#     list_display = ('id','carpeta_capacitacion')

# @admin.register(HabilidadPersonalizada)
# class HabilidadPersonalizadaAdmin(admin.ModelAdmin):
#     list_display = ('id','habilidad','nombre_habilidad')


@admin.register(CapacitacionCliente)
class CapacitacionClienteAdmin(admin.ModelAdmin):
    list_display = ('id','cliente')

@admin.register(PersonalPorCapacitar)
class PersonalPorCapacitarAdmin(admin.ModelAdmin):
    list_display = ('id','capacitacion_cliente','personal', 'resultado_capacitacion')

@admin.register(Domicilio)
class DomicilioAdmin(admin.ModelAdmin):
    list_display = ('id','personal','cliente_generales','cliente_pagos','calle','numero_exterior','ciudad')

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