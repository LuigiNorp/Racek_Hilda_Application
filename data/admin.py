from nested_admin import NestedStackedInline, NestedModelAdmin
from .models import *
from .actions import *
from django.contrib import admin
from django import forms


# Register your models here.
class DomicilioInline(NestedStackedInline):
    model = Domicilio
    extra = 0
    autocomplete_fields = ['codigo_postal']

    # Hide Domicilio when is not used (the get_fields is necessary)
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

            # Rompe el bucle tan pronto como se encuentre una instancia relacionada
            for field, field_name in related_fields.items():
                if hasattr(obj, field_name):
                    fields = [field_name]
                    has_related_instance = True
                    break

            # Configura extra en función de si existe una instancia
            # relacionada con alguno de los campos especificados
            self.extra = 1 if has_related_instance else 0

        return fields


class DocumentosClienteInline(NestedStackedInline):
    model = DocumentosCliente


class RepresentanteTrabajadoresInline(NestedStackedInline):
    model = RepresentanteTrabajadores
    extra = 0


class SedeInline(NestedStackedInline):
    model = Sede
    extra = 0


class CarpetaClienteGeneralesInline(NestedStackedInline):
    model = CarpetaClienteGenerales
    inlines = [DomicilioInline]


class CarpetaClientePagosInline(NestedStackedInline):
    model = CarpetaClientePagos
    inlines = [DomicilioInline]
    extra = 0


class CarpetaClienteContactosInline(NestedStackedInline):
    model = CarpetaClienteContactos
    extra = 0


class PaqueteCapacitacionInline(NestedStackedInline):
    model = PaqueteCapacitacion
    extra = 0
    autocomplete_fields = ['cliente', ]


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
        PaqueteCapacitacionInline,
    ]
    search_fields = ['nombre_comercial', 'razon_social',]


class EvaluadorInline(NestedStackedInline):
    model = Evaluador
    extra = 0


class CarpetaLaboralInline(NestedStackedInline):
    model = CarpetaLaboral
    extra = 0
    autocomplete_fields = ['ocupacion']


class CarpetaGeneralesInline(NestedStackedInline):
    model = CarpetaGenerales
    extra = 0


class ReferenciaInline(NestedStackedInline):
    model = Referencia
    inlines = [DomicilioInline]
    extra = 0


class DependienteInline(NestedStackedInline):
    model = Dependiente
    extra = 1


class CarpetaDependientesInline(NestedStackedInline):
    model = CarpetaDependientes
    inlines = [DependienteInline]
    extra = 0


class CarpetaExamenFisicoInline(NestedStackedInline):
    model = CarpetaExamenFisico
    extra = 0


class CarpetaExamenMedicoInline(NestedStackedInline):
    model = CarpetaExamenMedico
    extra = 0


class CarpetaExamenPsicologicoInline(NestedStackedInline):
    model = CarpetaExamenPsicologico
    extra = 0


class CarpetaExamenToxicologicoInline(NestedStackedInline):
    model = CarpetaExamenToxicologico
    extra = 0


class CarpetaExamenSocioeconomicoInline(NestedStackedInline):
    model = CarpetaExamenSocioeconomico
    extra = 0


class CarpetaExamenPoligrafoInline(NestedStackedInline):
    model = CarpetaExamenPoligrafo
    extra = 0


class EmpleoAnteriorSeguridadPublicaInline(NestedStackedInline):
    model = EmpleoAnteriorSeguridadPublica
    inlines = [DomicilioInline]
    extra = 0


# TODO: Puedes mejor convertirlo en boton
class EmpleoAnteriorInline(NestedStackedInline):
    model = EmpleoAnterior
    extra = 0
    inlines = [DomicilioInline]


class IdiomaInline(NestedStackedInline):
    model = Idioma
    extra = 0


class CapacitacionInline(NestedStackedInline):
    model = Capacitacion
    extra = 0
    autocomplete_fields = ['paq_capacitacion', 'instructor', ]


class CarpetaMediaFilicacionInline(NestedStackedInline):
    model = CarpetaMediaFiliacion
    extra = 0


class DocumentosDigitalesInline(NestedStackedInline):
    model = DocumentosDigitales
    extra = 0


@admin.register(Personal)
class PersonalAdmin(NestedModelAdmin):
    list_display = ('id', 'nombre_completo', 'cliente',)
    search_fields = ['curp', 'rfc', 'cliente', ]
    autocomplete_fields = ['cliente', 'curp', 'rfc', ]
    inlines = [
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
        ReferenciaInline,
        CarpetaDependientesInline,
        EmpleoAnteriorSeguridadPublicaInline,
        EmpleoAnteriorInline,
        CapacitacionInline,
        IdiomaInline,
        CarpetaMediaFilicacionInline,
        DocumentosDigitalesInline,
    ]
    generate_dc3_report.short_description = 'Generar DC-3'
    actions = [generate_dc3_report]

    def nombre_completo(self, obj):
        return f"{obj.curp.get_nombre_completo()}"

    nombre_completo.short_description = 'Nombre Completo'


class CarpetaExamenFisicoPrevioInline(NestedStackedInline):
    model = CarpetaExamenFisicoPrevio
    extra = 1
    fields = ('resultado_aspirante', 'observacion')


class CarpetaExamenMedicoPrevioInline(NestedStackedInline):
    model = CarpetaExamenMedicoPrevio
    extra = 1
    fields = ('resultado_aspirante', 'observacion')


class CarpetaExamenPsicologicoPrevioInline(NestedStackedInline):
    model = CarpetaExamenPsicologicoPrevio
    extra = 1
    fields = ('resultado_aspirante', 'observacion')


class CarpetaExamenToxicologicoPrevioInline(NestedStackedInline):
    model = CarpetaExamenToxicologicoPrevio
    extra = 1
    fields = ('resultado_aspirante', 'observacion')


class CarpetaExamenSocioeconomicoPrevioInline(NestedStackedInline):
    model = CarpetaExamenSocioeconomicoPrevio
    extra = 1
    fields = ('resultado_aspirante', 'comentarios_generales')


class CarpetaExamenPoligrafoPrevioInline(NestedStackedInline):
    model = CarpetaExamenPoligrafoPrevio
    extra = 1
    fields = ('resultado_aspirante', 'observacion')


class CarpetaGeneralesPrevioInline(NestedStackedInline):
    model = CarpetaGeneralesPrevio
    extra = 1
    fields = (
        'estado_civil',
        'escolaridad',
        'telefono_domicilio',
        'telefono_celular',
        'telefono_recados',
        'email_empleado'
    )


class CarpetaMediaFilicacionPrevioInline(NestedStackedInline):
    model = CarpetaMediaFiliacionPrevio
    extra = 1

    fields = (
        'peso',
        'estatura',
        'tension_arterial',
        'temperatura',
        'indice_masa_corporal',
        'clasificacion_imc',
        'sat02',
        'frecuencia_cardiaca',
        'cronica_degenerativa',
        'sangre',
        'rh'
    )


class DocumentosDigitalesPrevioInline(NestedStackedInline):
    model = DocumentosDigitalesPrevio
    extra = 1
    fields = (
        'acta_nacimiento',
        'ine',
        'comprobante_domicilio',
        'comprobante_estudios',
        'curp',
        'cartilla_smn',
        'nss',
        'huellas_digitales'
    )


@admin.register(PersonalPrevio)
class PersonalPrevioAdmin(NestedModelAdmin):
    list_display = ('id', 'nombre_completo', 'cliente',)
    search_fields = ['curp', 'rfc', 'cliente',]
    autocomplete_fields = ['cliente', 'curp', 'rfc']
    inlines = [
        DomicilioInline,
        EvaluadorInline,
        CarpetaExamenFisicoPrevioInline,
        CarpetaExamenMedicoPrevioInline,
        CarpetaExamenPsicologicoPrevioInline,
        CarpetaExamenToxicologicoPrevioInline,
        CarpetaExamenSocioeconomicoPrevioInline,
        CarpetaExamenPoligrafoPrevioInline,
        CarpetaGeneralesPrevioInline,
        CarpetaMediaFilicacionPrevioInline,
        DocumentosDigitalesPrevioInline,
    ]

    def nombre_completo(self, obj):
        return f"{obj.curp.get_nombre_completo()}"

    nombre_completo.short_description = 'Nombre Completo'


@admin.register(PuestoFuncional)
class PuestoFuncionalAdmin(admin.ModelAdmin):
    list_display = ('id', 'nombre_puesto',)


@admin.register(TipoBaja)
class TipoBajaAdmin(admin.ModelAdmin):
    list_display = ('id', 'motivo',)


@admin.register(MotivoSeparacion)
class MotivoSeparacionAdmin(admin.ModelAdmin):
    list_display = ('id', 'motivo',)


@admin.register(Instructor)
class InstructorAdmin(admin.ModelAdmin):
    list_display = ('id', 'nombre_instructor', 'numero_registro',)
    search_fields = ['nombre_instructor', 'numero_registro',]

@admin.register(CodigoPostal)
class CodigoPostalAdmin(admin.ModelAdmin):
    list_display = ('id', 'codigo_postal', 'tipo_asentamiento', 'asentamiento', 'municipio', 'estado', 'ciudad', 'pais')
    search_fields = ['codigo_postal', 'tipo_asentamiento', 'asentamiento',]


@admin.register(Curp)
class CurpAdmin(admin.ModelAdmin):
    list_display = ('id', 'curp', 'nombre', 'apellido_paterno', 'apellido_materno', 'fecha_nacimiento', 'sexo',)
    search_fields = ['curp', 'nombre', 'apellido_paterno', 'apellido_materno',]


@admin.register(CurpPrevio)
class CurpPrevioAdmin(admin.ModelAdmin):
    list_display = ('curp', 'nombre', 'apellido_paterno', 'apellido_materno', 'sexo',)
    search_fields = ['curp', 'nombre', 'apellido_paterno', 'apellido_materno',]

    def get_form(self, request, obj=None, **kwargs):
        form = super().get_form(request, obj, **kwargs)

        # Hide all other fields
        for field in form.base_fields:
            if field not in self.list_display:
                form.base_fields[field].widget = forms.HiddenInput()
        return form


@admin.register(Rfc)
class RfcAdmin(admin.ModelAdmin):
    list_display = ('id', 'rfc', 'razon_social',)
    search_fields = ['rfc', 'razon_social',]


@admin.register(RfcPrevio)
class RfcPrevioAdmin(admin.ModelAdmin):
    list_display = ('rfc', 'razon_social',)
    search_fields = ['rfc', 'razon_social',]

    def get_form(self, request, obj=None, **kwargs):
        form = super().get_form(request, obj, **kwargs)

        # Hide all other fields
        for field in form.base_fields:
            if field not in self.list_display:
                form.base_fields[field].widget = forms.HiddenInput()
        return form


@admin.register(Ocupacion)
class OcupacionAdmin(admin.ModelAdmin):
    list_display = ('id', 'clave_subarea', 'subarea',)
    search_fields = ['clave_subarea', 'subarea', ]


# This one is the only repeate as Inline and ModelAdmin
@admin.register(PaqueteCapacitacion)
class PaqueteCapacitacionAdmin(admin.ModelAdmin):
    list_display = ('id', 'cliente', 'fecha_solicitud', 'fecha_realizacion',)
    search_fields = ['cliente', 'fecha_realizacion',]
    autocomplete_fields = ['cliente',]
