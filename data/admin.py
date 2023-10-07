from nested_admin import NestedStackedInline, NestedModelAdmin
from django.http import HttpResponse
from django.contrib import admin
from .models import *
from docx import Document


# Create django admin action for reports

def generate_dc3(modeladmin, request, queryset):
    document = Document('media/file_templates/DC3.dot')

    for paragraph in document.paragraphs:
        paragraph.text = paragraph.text.replace('[nombre]', 'Juan')


generate_dc3.short_description = "Generar el archivo DC-3"


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
    list_display = ('id', 'nombre_comercial', 'razon_social', 'activo',)
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
    model = Capacitacion


class CarpetaCapacitacionAdmin(NestedStackedInline):
    model = CarpetaCapacitacion
    inlines = [CapacitacionAdmin, IdiomaAdmin]


class CarpetaMediaFilicacionAdmin(NestedStackedInline):
    model = CarpetaMediaFiliacion


class DocumentosDigitalesAdmin(NestedStackedInline):
    model = DocumentosDigitales


import openpyxl


def generate_xlsx(modeladmin, request, queryset):
    for personal in queryset:
        # Define the path to the original XLSX file
        original_file_path = "./media/file_templates/Mis archivos/DC3 ACTUALIZADO.xlsx"

        # Load the original XLSX file
        wb = openpyxl.load_workbook(original_file_path)

        # Get the first sheet of the workbook
        sheet = wb.active

        # Get the related Personal object for which you want to retrieve information
        personal = Personal.objects.get(id=personal.id)  # Use the current 'personal' object from the loop

        # Get the related Curp object for the Personal object
        curp = personal.curp

        # Get the related Rfc object for the Personal object
        rfc = personal.rfc

        # Get the related CarpetaClienteGenerales object for the Personal object
        carpeta_cliente_generales = personal.carpetagenerales

        # Get the related CarpetaClientePagos object for the Personal object
        carpeta_cliente_pagos = personal.carpetapagos

        # Retrieve the related Capacitacion objects for the Personal object
        capacitacion = personal.carpeta_capacitacion.capacitacion

        # Get the related AreaCurso object for the Personal object
        area_curso = capacitacion.area_curso

        # Get the related Capacitador object for the Personal object
        capacitador = capacitacion.capacitador

        # Define the data to be replaced in the cells
        data = {
            'nombre_apellidos': f"{curp.nombre} {curp.apellido_paterno} {curp.apellido_materno}",
            'curp': curp.curp,
            'ocupacion': carpeta_cliente_generales.puesto.nombre_puesto,
            'puesto': carpeta_cliente_generales.puesto.nombre_puesto,
            'razon_social': carpeta_cliente_pagos.razon_social,
            'rfc': rfc.rfc,
            'nombre_curso': capacitacion.curso,
            'horas_curso': capacitacion.duracion,
            'fecha_inicial_capacitacion': capacitacion.inicio,
            'fecha_final_capacitacion': capacitacion.conclusion,
            'area_curso': area_curso.nombre_area,
            'nombre_capacitador': capacitador.nombre_capacitador,
            'registro_capacitador': capacitador.numero_registro,
        }

        # Replace the values in the specified cells with the data dictionary
        cell_mapping = {
            'AJ4': data['nombre_apellidos'],
            'AJ5': data['curp'],
            'AJ6': data['ocupacion'],
            'AJ7': data['puesto'],
            'AJ20': data['razon_social'],
            'AJ21': data['rfc'],
            'AJ8': data['nombre_curso'],
            'AJ9': data['horas_curso'],
            'AJ10': data['fecha_inicial_capacitacion'],
            'AJ11': data['fecha_final_capacitacion'],
            'AJ12': data['area_curso'],
            'AJ13': data['nombre_capacitador'],
            'AJ14': data['registro_capacitador'],
        }

        for cell, value in cell_mapping.items():
            sheet[cell].value = value

        # Generate the modified XLSX file
        modified_file_path = "./media/file_templates/Mis archivos/DC3 ACTUALIZADO modified.xlsx"
        wb.save(modified_file_path)


generate_xlsx.short_description = "Generar DC-3"


@admin.register(Personal)
class PersonalAdmin(NestedModelAdmin):
    list_display = ('id', 'get_full_name', 'cliente',)
    inlines = [
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
    list_display = ('id', 'nombre_puesto',)


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


@admin.register(Curp)
class CurpAdmin(admin.ModelAdmin):
    list_display = (
    'id', 'curp', 'nombre', 'apellido_materno', 'apellido_paterno', 'iniciales', 'fecha_nacimiento', 'sexo')


@admin.register(Rfc)
class RfcAdmin(admin.ModelAdmin):
    list_display = ('id', 'rfc', 'razon_social', 'correo_contacto', 'validez', 'tipo',)


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
    list_display = ('id', 'calle', 'numero_exterior', 'ciudad', 'codigo_postal',)


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