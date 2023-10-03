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
    list_display = ('id','nombre_comercial','razon_social','activo',)
    inlines = [SedeInline, CarpetaClienteGeneralesInline, CarpetaClientePagosInline, CarpetaClienteContactosInline]

class DomicilioInLine(NestedStackedInline):
    model = Domicilio
    
@admin.register(Puesto)
class PuestoAdmin(admin.ModelAdmin):
    list_display = ('id','nombre_puesto',)

@admin.register(Ocupacion)
class OcupacionAdmin(admin.ModelAdmin):
    list_display = ('id','nombre_ocupacion',)
    
@admin.register(Capacitador)
class CapacitadorAdmin(admin.ModelAdmin):
    list_display = ('id','nombre_capacitador', 'numero_registro',)
    
@admin.register(AreaCurso)
class AreaCursoAdmin(admin.ModelAdmin):
    list_display = ('id','nombre_area',)

@admin.register(PuestoFuncional)
class PuestoFuncionalAdmin(admin.ModelAdmin):
    list_display = ('id','nombre_puesto',)

class CarpetaLaboralAdmin(NestedStackedInline):
    model = CarpetaLaboral

class CarpetaGeneralesAdmin(NestedStackedInline):
    model = CarpetaGenerales

class ReferenciaAdmin(NestedStackedInline):
    model = Referencia
    inline = [DomicilioInLine]

class CarpetaReferenciasAdmin(NestedStackedInline):
    model = CarpetaReferencias
    inlines = [ReferenciaAdmin]

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

@admin.register(EmpleoAnteriorSeguridadPublica)
class EmpleoAnteriorSeguridadPublicaAdmin(admin.ModelAdmin):
    pass
   

@admin.register(EmpleoAnterior)
class EmpleoAnteriorAdmin(admin.ModelAdmin):
    pass
    

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
    # Define the path to the original XLSX file
    original_file_path = "./media/file_templates/Mis archivos/DC3 ACTUALIZADO.xlsx"

    # Load the original XLSX file
    wb = openpyxl.load_workbook(original_file_path)

    # Get the first sheet of the workbook
    sheet = wb.active

    for personal in queryset:
        # Define the data to be replaced in the cells for each 'personal' object
        data = {
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


@admin.register(Personal)
class PersonalAdmin(admin.ModelAdmin):
    list_display = ('id', 'get_full_name', 'cliente',)
    actions = [generate_xlsx]    
    def get_full_name(self, obj):
        return f"{obj.curp.nombre} {obj.curp.apellido_paterno} {obj.curp.apellido_materno}"

    get_full_name.short_description = 'Full Name'

@admin.register(TipoBaja)
class TipoBajaAdmin(admin.ModelAdmin):
    list_display = ('id','motivo',)

@admin.register(MotivoSeparacion)
class MotivoSeparacionAdmin(admin.ModelAdmin):
    list_display = ('id','motivo',)

@admin.register(CapacitacionCliente)
class CapacitacionClienteAdmin(admin.ModelAdmin):
    list_display = ('id','cliente', 'estatus_capacitacion', 'comentarios', 'fecha_realizacion')

@admin.register(Idioma)
class IdiomaAdmin(admin.ModelAdmin):
    pass

@admin.register(Capacitacion)
class CapacitacionAdmin(admin.ModelAdmin):
    pass

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
class DomicilioInLine(admin.ModelAdmin):
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