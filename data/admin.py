from nested_admin import NestedStackedInline, NestedModelAdmin
from .models import *
from .actions import *
from django.contrib import admin



# Create django admin action for reports
generate_dc3.short_description = "Generar DC-3"


# Register your models here.
class DomicilioInline(NestedStackedInline):
    model = Domicilio
    extra = 0  # Establece el valor predeterminado de extra en 0

    def get_fields(self, request, obj=None):
        fields = super().get_fields(request, obj)
        has_related_instance = False

        if obj:
            related_fields = {
                'referencia': 'referencia',
                'carpeta_cliente_generales': 'carpeta_cliente_generales',
                'carpeta_cliente_pagos': 'carpeta_cliente_pagos',
                'personal': 'personal',
                'empleo_anterior_sp': 'empleo_anterior_sp',
                'empleo_anterior': 'empleo_anterior'
            }

            for field, field_name in related_fields.items():
                if hasattr(obj, field_name):
                    fields = [field_name]
                    has_related_instance = True
                    break  # Rompe el bucle tan pronto como se encuentre una instancia relacionada

            # Configura extra en función de si existe una instancia
            # relacionada con alguno de los campos especificados
            self.extra = 1 if has_related_instance else 0

        return fields


class DocumentosClienteInline(NestedStackedInline):
    model = DocumentosCliente


class RepresentanteTrabajadoresInline(NestedStackedInline):
    model = RepresentanteTrabajadores


class SedeInline(NestedStackedInline):
    model = Sede
    extra = 1


class CarpetaClienteGeneralesInline(NestedStackedInline):
    model = CarpetaClienteGenerales
    inlines = [DomicilioInline]


class CarpetaClientePagosInline(NestedStackedInline):
    model = CarpetaClientePagos
    inlines = [DomicilioInline]


class CarpetaClienteContactosInline(NestedStackedInline):
    model = CarpetaClienteContactos
    

class CapacitacionClienteInline(NestedStackedInline):
    model = CapacitacionCliente
    extra = 1


@admin.register(Cliente)
class ClienteAdmin(NestedModelAdmin):
    list_display = ('id', 'nombre_comercial', 'razon_social', 'activo',)
    inlines = [
        DocumentosClienteInline,
        SedeInline,
        RepresentanteTrabajadoresInline,
        CarpetaClienteGeneralesInline,
        CarpetaClientePagosInline,
        CarpetaClienteContactosInline,
        CapacitacionClienteInline,
    ]


class EvaluadorInline(NestedStackedInline):
    model = Evaluador


class CurpInline(NestedStackedInline):
    model = Curp


class RfcInline(NestedStackedInline):
    model = Rfc


class PuestoInline(NestedStackedInline):
    model = Puesto
    

class InstructorInline(NestedStackedInline):
    model = Instructor


class OcupacionInline(NestedStackedInline):
    model = Ocupacion
    

class AreaCursoInline(NestedStackedInline):
    model = AreaCurso


class CarpetaLaboralInline(NestedStackedInline):
    model = CarpetaLaboral
    extra = 1
    inlines = [
        PuestoInline, 
        OcupacionInline, 
        AreaCursoInline,
        InstructorInline, 
    ]


class CarpetaGeneralesInline(NestedStackedInline):
    model = CarpetaGenerales


class ReferenciaInline(NestedStackedInline):
    model = Referencia
    inlines = [DomicilioInline]
    extra = 1


class CarpetaReferenciasInline(NestedStackedInline):
    model = CarpetaReferencias
    inlines = [ReferenciaInline]


class DependienteInline(NestedStackedInline):
    model = Dependiente
    extra = 1


class CarpetaDependientesInline(NestedStackedInline):
    model = CarpetaDependientes
    inlines = [DependienteInline]


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


class EmpleoAnteriorSeguridadPublicaInline(NestedStackedInline):
    model = EmpleoAnteriorSeguridadPublica
    inlines = [DomicilioInline]
    extra = 1


class CarpetaEmpleoAnteriorSeguridadPublicaInline(NestedStackedInline):
    model = CarpetaEmpleoAnteriorSeguridadPublica
    inlines = [EmpleoAnteriorSeguridadPublicaInline]


# TODO: Puedes mejor convertirlo en boton
class EmpleoAnteriorAdmin(NestedStackedInline):
    model = EmpleoAnterior
    inlines = [DomicilioInline]


class CarpetaEmpleoAnteriorInline(NestedStackedInline):
    model = CarpetaEmpleoAnterior
    inlines = [EmpleoAnteriorAdmin]
    extra = 1


class IdiomaInline(NestedStackedInline):
    model = Idioma
    extra = 1


class TipoCursoInline(NestedStackedInline):
    model = TipoCurso


class CapacitacionInline(NestedStackedInline):
    model = Capacitacion
    inlines = [TipoCursoInline]
    extra = 1


class CarpetaCapacitacionInline(NestedStackedInline):
    model = CarpetaCapacitacion
    inlines = [CapacitacionInline, IdiomaInline]


class CarpetaMediaFilicacionInline(NestedStackedInline):
    model = CarpetaMediaFiliacion


class DocumentosDigitalesInline(NestedStackedInline):
    model = DocumentosDigitales


@admin.register(Personal)
class PersonalAdmin(NestedModelAdmin):
    list_display = ('id', 'get_full_name', 'cliente',)
    inlines = [
        CurpInline,
        RfcInline,
        DomicilioInline,
        EvaluadorInline,
        RepresentanteTrabajadoresInline,
        CarpetaExamenFisicoInline,
        CarpetaExamenMedicoInline,
        CarpetaExamenPsicologicoInline,
        CarpetaExamenToxicologicoInline,
        CarpetaExamenSocioeconomicoInline,
        CarpetaExamenPoligrafoInline,
        CarpetaLaboralInline,
        CarpetaGeneralesInline,
        CarpetaReferenciasInline,
        CarpetaDependientesInline,
        CarpetaEmpleoAnteriorSeguridadPublicaInline,
        CarpetaEmpleoAnteriorInline,
        CarpetaCapacitacionInline,
        CarpetaMediaFilicacionInline,
        DocumentosDigitalesInline,
    ]
    actions = [generate_dc3]

    def get_full_name(self, obj):
        return f"{obj.curp.nombre} {obj.curp.apellido_paterno} {obj.curp.apellido_materno}"

    get_full_name.short_description = 'Full Name'


@admin.register(PuestoFuncional)
class PuestoFuncionalAdmin(admin.ModelAdmin):
    list_display = ('id', 'nombre_puesto',)


@admin.register(TipoBaja)
class TipoBajaAdmin(admin.ModelAdmin):
    list_display = ('id', 'motivo',)


@admin.register(MotivoSeparacion)
class MotivoSeparacionAdmin(admin.ModelAdmin):
    list_display = ('id', 'motivo',)


@admin.register(CapacitacionCliente)
class CapacitacionClienteInline(admin.ModelAdmin):
    list_display = ('id', 'cliente', 'estatus_capacitacion', 'comentarios', 'fecha_realizacion')


@admin.register(Capacitacion)
class CapacitacionAdmin(admin.ModelAdmin):
    list_display = (
        'id', 'institucion_empresa', 'curso', 'impartido_recibido', 'eficiencia_terminal', 'inicio', 'conclusion',
        'duracion')


# TODO: Verificar si se puede eliminar
# @admin.register(CapacitacionEnCurso)
# class CapacitacionEnCursoAdmin(admin.ModelAdmin):
#     list_display = ('id','carpeta_capacitacion','estudio_curso')


# @admin.register(Habilidad)
# class HabilidadAdmin(admin.ModelAdmin):
#     list_display = ('id','carpeta_capacitacion')

# @admin.register(HabilidadPersonalizada)
# class HabilidadPersonalizadaAdmin(admin.ModelAdmin):
#     list_display = ('id','habilidad','nombre_habilidad')


@admin.register(CodigoPostal)
class CodigoPostalAdmin(admin.ModelAdmin):
    list_display = ('id', 'codigo_postal')


@admin.register(Colonia)
class ColoniaAdmin(admin.ModelAdmin):
    list_display = ('id', 'colonia')


@admin.register(Municipio)
class MunicipioAdmin(admin.ModelAdmin):
    list_display = ('id', 'municipio')


@admin.register(Estado)
class EstadoAdmin(admin.ModelAdmin):
    list_display = ('id', 'estado')


@admin.register(Pais)
class PaisAdmin(admin.ModelAdmin):
    list_display = ('id', 'pais')
