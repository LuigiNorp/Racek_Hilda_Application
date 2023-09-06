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

@admin.register(Sede)
class SedeAdmin(admin.ModelAdmin):
    list_display = ('id','clave_sede','nombre_sede',)
    
@admin.register(CarpetaClienteGenerales)
class CarpetaClienteGeneralesAdmin(admin.ModelAdmin):
    list_display = ('id','reg_estatal','reg_federal','rfc','telefono_1','telefono_2','telefono_3','representante_legal','encargado_operativo','encargado_rh','coordinador','registro_patronal','domicilio',)

@admin.register(CarpetaClientePagos)
class CarpetaClientePagosAdmin(admin.ModelAdmin):
    list_display = ('id','encargado_pagos','telefono_oficina','telefono_celular','email','rfc','facturacion_tipo','revision','pagos','factura_subtotal','factura_iva','factura_total','domicilio',)
    
@admin.register(CarpetaClienteContactos)
class CarpetaClienteContactosInline(admin.ModelAdmin):
    list_display =  ('id','nombre_contacto','telefono_1','telefono_2','telefono_3','puesto','email_1','email_2')
    
@admin.register(Cliente)
class ClienteAdmin(admin.ModelAdmin):
    list_display = ('id','nombre_comercial','razon_social','activo','carpeta_cliente_generales','carpeta_cliente_pagos','carpeta_cliente_contactos','carpeta_cliente_generales','carpeta_cliente_pagos','carpeta_cliente_contactos','sede',)


class DomicilioAdmin(NestedStackedInline):
    model = Domicilio


@admin.register(CarpetaLaboral)
class CarpetaLaboralAdmin(admin.ModelAdmin):
    pass

@admin.register(CarpetaGenerales)
class CarpetaGeneralesAdmin(admin.ModelAdmin):
    pass

class ReferenciaInline(NestedStackedInline):
    model = Referencia
    
@admin.register(CarpetaReferencias)
class CarpetaReferenciasAdmin(admin.ModelAdmin):
    inlines = [ReferenciaInline]

class DependienteInline(NestedStackedInline):
    model = Dependiente

@admin.register(CarpetaDependientes)
class CarpetaDependientesAdmin(admin.ModelAdmin):
    inlines = [DependienteInline]

@admin.register(CarpetaExamenFisico)
class CarpetaExamenFisicoAdmin(admin.ModelAdmin):
    pass

@admin.register(CarpetaExamenMedico)
class CarpetaExamenMedicoAdmin(admin.ModelAdmin):
    pass

@admin.register(CarpetaExamenPsicologico)
class CarpetaExamenPsicologicoAdmin(admin.ModelAdmin):
    pass

@admin.register(CarpetaExamenToxicologico)
class CarpetaExamenToxicologicoAdmin(admin.ModelAdmin):
    pass

@admin.register(CarpetaExamenSocioeconomico)
class CarpetaExamenSocioeconomicoAdmin(admin.ModelAdmin):
    pass

@admin.register(CarpetaExamenPoligrafo)
class CarpetaExamenPoligrafoAdmin(admin.ModelAdmin):
    pass


class EmpleoAnteriorSeguridadPublicaInline(NestedStackedInline):
    model = EmpleoAnteriorSeguridadPublica


@admin.register(CarpetaEmpleoAnteriorSeguridadPublica)
class CarpetaEmpleoAnteriorSeguridadPublicaAdmin(admin.ModelAdmin):
    inlines = [EmpleoAnteriorSeguridadPublicaInline]


class EmpleoAnteriorInline(NestedStackedInline):
    model = EmpleoAnterior
    

@admin.register(CarpetaEmpleoAnterior)
class CarpetaEmpleoAnteriorAdmin(admin.ModelAdmin):
    inlines = [EmpleoAnteriorInline]
    

@admin.register(TipoCurso)
class TipoCursoAdmin(admin.ModelAdmin):
    pass

@admin.register(CarpetaMediaFiliacion)
class CarpetaMediaFilicacionAdmin(admin.ModelAdmin):
    pass

@admin.register(DocumentosDigitales)
class DocumentosDigitalesAdmin(admin.ModelAdmin):
    pass

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
class PersonalAdmin(admin.ModelAdmin):
    list_display = ('id', 'get_full_name', 'cliente',)
    actions = [generate_xlsx]    
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

class IdiomaInline(NestedStackedInline):
    model = Idioma

class CapacitacionInline(NestedStackedInline):
    model = Capacitacion

@admin.register(CarpetaCapacitacion)
class CarpetaCapacitacionAdmin(admin.ModelAdmin):
    inlines = [IdiomaInline, CapacitacionInline]

@admin.register(AreaCurso)
class AreaCursoAdmin(admin.ModelAdmin):
    list_display = ('id','nombre_area',)
    
@admin.register(Capacitador)
class CapacitadorAdmin(admin.ModelAdmin):
    list_display = ('id','nombre_capacitador', 'numero_registro',)

@admin.register(Curp)
class CurpAdmin(admin.ModelAdmin):
    list_display = ('id','curp','nombre','apellido_materno','apellido_paterno','iniciales','fecha_nacimiento','sexo')

@admin.register(Rfc)
class RfcAdmin(admin.ModelAdmin):
    list_display = ('id','rfc','razon_social','correo_contacto','validez','tipo',)

@admin.register(Evaluador)
class EvaluadorAdmin(admin.ModelAdmin):
    list_display = ('id', 'nombre_completo')

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