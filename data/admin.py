from nested_admin import NestedStackedInline, NestedModelAdmin
from django.contrib import admin
from .models import *

# Register your models here.

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




class DomicilioAdmin(NestedStackedInline):
    model = Domicilio

class CarpetaLaboralAdmin(NestedStackedInline):
    model = CarpetaLaboral

class CarpetaGeneralesAdmin(NestedStackedInline):
    model = CarpetaGenerales

class ReferenciaAdmin(NestedStackedInline):
    model = Referencia
    inline = [DomicilioAdmin]

class CarpetaReferenciasAdmin(NestedStackedInline):
    model = CarpetaReferencias
    inlines = [ReferenciaAdmin]

class DependienteAdmin(NestedStackedInline):
    model = Dependiente

class CarpetaDependientesAdmin(NestedStackedInline):
    model = CarpetaDependientes
    inlines = [DependienteAdmin]
    
class CarpetaExamenFisicoInline(NestedStackedInline):
    model = CarpetaExamenFisico

class CarpetaExamenMedicoInline(NestedStackedInline):
    model = CarpetaExamenMedico

class CarpetaExamenPsicologicoInline(NestedStackedInline):
    model = CarpetaExamenPsicologico

class CarpetaExamenToxicologicoInline(NestedStackedInline):
    model = CarpetaExamenToxicologico

class CarpetaExamenSocioeconomicoInline(NestedStackedInline):
    model = CarpetaExamenSocioeconomico

class CarpetaExamenPoligrafoInline(NestedStackedInline):
    model = CarpetaExamenPoligrafo

class EmpleoAnteriorSeguridadPublicaAdmin(NestedStackedInline):
    model = EmpleoAnteriorSeguridadPublica
    
class CarpetaEmpleoAnteriorSeguridadPublicaAdmin(NestedStackedInline):
    model = CarpetaEmpleoAnteriorSeguridadPublica
    inlines = [EmpleoAnteriorSeguridadPublicaAdmin]


# Puedes mejor convertirlo en boton
class EmpleoAnteriorAdmin(NestedStackedInline):
    model = EmpleoAnterior

class CarpetaEmpleoAnteriorAdmin(NestedStackedInline):
    model = CarpetaEmpleoAnterior
    inlines = [EmpleoAnteriorAdmin]

class IdiomaAdmin(NestedStackedInline):
    model = Idioma

class TipoCursoAdmin(NestedStackedInline):
    model = TipoCurso

class CapacitacionAdmin(NestedStackedInline):
    model= Capacitacion

class CarpetaCapacitacionAdmin(NestedStackedInline):
    model = CarpetaCapacitacion
    inlines = [CapacitacionAdmin, IdiomaAdmin]

class CarpetaMediaFilicacionAdmin(NestedStackedInline):
    model = CarpetaMediaFiliacion

class DocumentosDigitalesAdmin(NestedStackedInline):
    model = DocumentosDigitales

@admin.register(Personal)
class PersonalAdmin(NestedModelAdmin):
    list_display = ('id', 'get_full_name', 'cliente',)
    inlines =  [
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

@admin.register(Puesto)
class PuestoAdmin(admin.ModelAdmin):
    list_display = ('id','nombre_puesto',)

@admin.register(PuestoFuncional)
class PuestoFuncionalAdmin(admin.ModelAdmin):
    list_display = ('id','nombre_puesto',)

@admin.register(TipoBaja)
class TipoBajaAdmin(admin.ModelAdmin):
    list_display = ('id','motivo',)

@admin.register(MotivoSeparacion)
class MotivoSeparacionAdmin(admin.ModelAdmin):
    list_display = ('id','motivo',)

@admin.register(CapacitacionCliente)
class CapacitacionClienteAdmin(admin.ModelAdmin):
    list_display = ('id','cliente', 'estatus_capacitacion', 'comentarios', 'fecha_realizacion')

@admin.register(Capacitacion)
class CapacitacionAdmin(admin.ModelAdmin):
    list_display = ('id','institucion_empresa', 'curso', 'impartido_recibido', 'eficiencia_terminal', 'inicio', 'conclusion', 'duracion')

@admin.register(Curp)
class CurpAdmin(admin.ModelAdmin):
    list_display = ('id','curp','nombre','apellido_materno','apellido_paterno','iniciales','fecha_nacimiento','sexo')

@admin.register(Rfc)
class RfcAdmin(admin.ModelAdmin):
    list_display = ('id','rfc','razon_social','correo_contacto','validez','tipo',)



# @admin.register(CapacitacionEnCurso)
# class CapacitacionEnCursoAdmin(admin.ModelAdmin):
#     list_display = ('id','carpeta_capacitacion','estudio_curso')


# @admin.register(Habilidad)
# class HabilidadAdmin(admin.ModelAdmin):
#     list_display = ('id','carpeta_capacitacion')

# @admin.register(HabilidadPersonalizada)
# class HabilidadPersonalizadaAdmin(admin.ModelAdmin):
#     list_display = ('id','habilidad','nombre_habilidad')


@admin.register(Domicilio)
class DomicilioAdmin(admin.ModelAdmin):
    list_display = ('id','calle','numero_exterior','ciudad','codigo_postal',)

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