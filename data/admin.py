from nested_admin import NestedStackedInline, NestedModelAdmin
from .models import *
from django.contrib import admin
from django.http import HttpResponse
# from docx import Document
import openpyxl


# Create django admin action for reports
def generate_xlsx(modeladmin, request, queryset):
    # Define the path to the original XLSX file
    original_file_path = "./media/file_templates/Mis archivos/DC3 ACTUALIZADO.xlsx"

    # Load the original XLSX file
    wb = openpyxl.load_workbook(original_file_path)

    # Load the original XLSX file
    wb = openpyxl.load_workbook(original_file_path)

    # Get the first sheet of the workbook
    sheet = wb.active

    for personal in queryset:
        data = {

            # Define the data to be replaced in the cells for each 'personal' object
            'nombre_apellidos': f"{personal.curp.nombre if personal.curp else ''} {personal.curp.apellido_paterno if personal.curp else ''} {personal.curp.apellido_materno if personal.curp else ''}",
            'curp': personal.curp.curp if personal.curp else '',
            'ocupacion': personal.carpetalaboral.ocupacion.nombre_ocupacion if personal.carpetalaboral.ocupacion else '',
            # 'puesto': personal.carpetalaboral.puesto.nombre_puesto if personal.carpetalaboral.puesto else '',
            # 'razon_social': personal.cliente.razon_social if personal.cliente else '',
            # 'rfc': personal.rfc.rfc if personal.rfc else '',
            # 'nombre_curso': personal.carpetacapacitacion.curso if personal.carpetacapacitacion else '',
            # 'horas_curso': personal.carpetacapacitacion.duracion if personal.carpetacapacitacion else '',
            # 'fecha_inicial_capacitacion': personal.carpetacapacitacion.inicio if personal.carpetacapacitacion else '',
            # 'fecha_final_capacitacion': personal.carpetacapacitacion.conclusion if personal.carpetacapacitacion else '',
            # 'area_curso': personal.carpetacapacitacion.area_curso.nombre_area if personal.carpetacapacitacion and personal.carpetacapacitacion.area_curso else '',
            # 'nombre_capacitador': personal.carpetacapacitacion.capacitador.nombre_capacitador if personal.carpetacapacitacion and personal.carpetacapacitacion.capacitador else '',
            # 'registro_capacitador': personal.carpetacapacitacion.capacitador.numero_registro if personal.carpetacapacitacion and personal.carpetacapacitacion.capacitador else '',
        }

        # Replace the values in the specified cells with the data dictionary
        cell_mapping = {
            'AJ4': data['nombre_apellidos'],
            'AJ5': data['curp'],
            'AJ6': data['ocupacion'],
            #     'AJ7': data['puesto'],
            #     'AJ20': data['razon_social'],
            #     'AJ21': data['rfc'],
            #     'AJ8': data['nombre_curso'],
            #     'AJ9': data['horas_curso'],
            #     'AJ10': data['fecha_inicial_capacitacion'],
            #     'AJ11': data['fecha_final_capacitacion'],
            #     'AJ12': data['area_curso'],
            #     'AJ13': data['nombre_capacitador'],
            #     'AJ14': data['registro_capacitador'],
        }

        for cell, value in cell_mapping.items():
            sheet[cell].value = value

    # Create a response with the modified XLSX file
    response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
    response['Content-Disposition'] = 'attachment; filename=modified_dc3.xlsx'
    wb.save(response)
    return response

generate_xlsx.short_description = "Generar DC-3"


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


@admin.register(Cliente)
class ClienteAdmin(NestedModelAdmin):
    list_display = ('id', 'nombre_comercial', 'razon_social', 'activo',)
    inlines = [
        SedeInline,
        CarpetaClienteGeneralesInline,
        CarpetaClientePagosInline,
        CarpetaClienteContactosInline
    ]


class EvaluadorInline(NestedStackedInline):
    model = Evaluador


class CurpInline(NestedStackedInline):
    model = Curp


class RfcInline(NestedStackedInline):
    model = Rfc


@admin.register(Puesto)
class PuestoAdmin(admin.ModelAdmin):
    list_display = ('id', 'nombre_puesto', 'carpeta_laboral')


@admin.register(Capacitador)
class CapacitadorAdmin(admin.ModelAdmin):
    list_display = ('id', 'nombre_capacitador', 'numero_registro', 'carpeta_laboral')


@admin.register(Ocupacion)
class OcupacionAdmin(admin.ModelAdmin):
    list_display = ('id', 'nombre_ocupacion', 'carpeta_laboral')


@admin.register(AreaCurso)
class AreaCursoAdmin(admin.ModelAdmin):
    list_display = ('id', 'nombre_area', 'carpeta_laboral')


class CarpetaLaboralInline(NestedStackedInline):
    model = CarpetaLaboral


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
    actions = [generate_xlsx]

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
class CapacitacionClienteAdmin(admin.ModelAdmin):
    list_display = ('id', 'cliente', 'estatus_capacitacion', 'comentarios', 'fecha_realizacion')


@admin.register(Capacitacion)
class CapacitacionAdmin(admin.ModelAdmin):
    list_display = (
        'id', 'institucion_empresa', 'curso', 'impartido_recibido', 'eficiencia_terminal', 'inicio', 'conclusion',
        'duracion')


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
