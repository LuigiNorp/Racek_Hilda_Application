from nested_admin import NestedStackedInline, NestedModelAdmin
from .models import *
from .actions import (
    generate_dc3_report,
    generate_odontologic_report,
    generate_fingerprint_record_report,
    generate_cdmx_license_report,
    generate_edomex_license_report,
    generate_federal_license_report,
    generate_consent_form_report,
    generate_training_certificate_report,
    generate_cdmx_tests_report,
    generate_federal_tests_report,
    generate_socioeconomic_photos_report,
    generate_isihara_test_report,
    generate_honesty_test_report,
    generate_polygraph_test_report,
    generate_gch_preliminary_report,
    generate_psychological_test_report,
    generate_candidate_report,
    generate_socioeconomic_report,
    generate_social_work_report,
    generate_sedena_report,
)
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


class CarpetaMediaFiliacionInline(NestedStackedInline):
    model = CarpetaMediaFiliacion
    extra = 0

    def get_readonly_fields(self, request, obj=None):
        readonly_fields = super().get_readonly_fields(request, obj)
        if obj.carpetamediafiliacion:
            if obj.carpetamediafiliacion.estatura is None or obj.carpetamediafiliacion.peso is None:
                readonly_fields += ('indice_masa_corporal', 'clasificacion_imc')
        return readonly_fields


class DocumentosDigitalesInline(NestedStackedInline):
    model = DocumentosDigitales
    extra = 0


class CurpEmpleadoInline(NestedStackedInline):
    model = CurpEmpleado
    extra = 1
    fields = (
        'personal',
        'curp',
        'nombre',
        'apellido_paterno',
        'apellido_materno',
        'sexo',
        'iniciales',
    )
    readonly_fields = (
        'fecha_nacimiento',
        'edad',
        'anio_registro',
        'numero_acta',
        'validacion_renapo',
        'estatus_curp',
        'clave_municipio_registro',
        'municipio_registro',
        'clave_entidad_registro',
        'entidad_registro',
        'transaction_id',
    )


class RfcEmpleadoInline(NestedStackedInline):
    model = RfcEmpleado
    extra = 1
    fields = (
        'personal',
        'rfc',
        'razon_social',
        'rfc_digital',
    )
    readonly_fields = (
        'estatus',
        'fecha_efectiva',
        'correo_contacto',
        'validez',
        'tipo',
    )


class ResultadosInline(NestedStackedInline):
    model = Resultado
    extra = 1


@admin.register(Personal)
class PersonalAdmin(NestedModelAdmin):
    list_display = ('id', 'nombre_completo', 'cliente',)
    search_fields = ['cliente',]
    autocomplete_fields = ['cliente',]
    inlines = [
        CurpEmpleadoInline,
        RfcEmpleadoInline,
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
        CarpetaMediaFiliacionInline,
        DocumentosDigitalesInline,
        ResultadosInline,
    ]
    generate_dc3_report.short_description = 'Generar DC-3'
    generate_odontologic_report.short_description = 'Generar Evaluación Odontológica'
    generate_fingerprint_record_report.short_description = 'Generar Registro Decadactilar'
    generate_cdmx_license_report.short_description = 'Generar Cédula CDMX'
    generate_edomex_license_report.short_description = 'Generar Cédula EDOMEX'
    generate_federal_license_report.short_description = 'Generar Cédula Federal'
    generate_consent_form_report.short_description = 'Generar Acta de Consentimiento'
    generate_training_certificate_report.short_description = 'Generar Constancia de Capacitación'
    generate_cdmx_tests_report.short_description = 'Generar Exámenes CDMX'
    generate_federal_tests_report.short_description = 'Generar Exámenes Federal'
    generate_socioeconomic_photos_report.short_description = 'Generar Reporte Fotogáfico Socioeconómicas'
    generate_isihara_test_report.short_description = 'Generar Examen Ishihara'
    generate_honesty_test_report.short_description = 'Generar Modo Honesto de Vivir'
    generate_polygraph_test_report.short_description = 'Generar Examen Poligráfico'
    generate_gch_preliminary_report.short_description = 'Generar Reporte Preliminar GCH'
    generate_psychological_test_report.short_description = 'Generar Examen Psicológico'
    generate_candidate_report.short_description = 'Generar Reporte Candidato'
    generate_socioeconomic_report.short_description = 'Generar Examen Socioeconómico'
    generate_social_work_report.short_description = 'Generar Reporte de Trabajo Social'
    generate_sedena_report.short_description = 'Generar Reporte Sedena'

    actions = [
        generate_dc3_report,
        generate_odontologic_report,
        generate_fingerprint_record_report,
        generate_cdmx_license_report,
        generate_edomex_license_report,
        generate_federal_license_report,
        generate_consent_form_report,
        generate_training_certificate_report,
        generate_cdmx_tests_report,
        generate_federal_tests_report,
        generate_socioeconomic_photos_report,
        generate_isihara_test_report,
        generate_honesty_test_report,
        generate_polygraph_test_report,
        generate_gch_preliminary_report,
        generate_psychological_test_report,
        generate_candidate_report,
        generate_socioeconomic_report,
        generate_social_work_report,
        generate_sedena_report
    ]

    def nombre_completo(self, obj):
        return f"{obj.curp.get_nombre_completo()}"

    nombre_completo.short_description = 'Nombre Completo'


class CarpetaExamenFisicoPrevioInline(NestedStackedInline):
    model = CarpetaExamenFisicoPrevio
    extra = 1
    fields = (
        'fecha_examen',
        'elasticidad',
        'velocidad',
        'resistencia',
        'condicion_fisica',
        'reflejos',
        'locomocion',
        'prueba_esfuerzo',
        'resultado',
        'resultado_aspirante',
        'observacion'
    )


class CarpetaExamenMedicoPrevioInline(NestedStackedInline):
    model = CarpetaExamenMedicoPrevio
    extra = 1
    fields = (
        'fecha_examen',
        'medico_agudeza_visual',
        'medico_agudeza_auditiva',
        'medico_agudeza_motriz',
        'medico_estado_nutricional',
        'medico_cardiologico',
        'medico_pulmonar',
        'medico_resultado',
        'ishihara_visual_oi',
        'ishihara_visual_od',
        'ishihara_visual_ao',
        'ishihara_lentes',
        'ishihara_deuteranopia',
        'ishihara_protanopia',
        'ishihara_tritanopia',
        'ishihara_resultado',
        'resultado_aspirante',
        'observacion',
    )


class CarpetaExamenPsicologicoPrevioInline(NestedStackedInline):
    model = CarpetaExamenPsicologicoPrevio
    extra = 1
    fields = (
        'fecha_examen',
        'actitud',
        'inteligencia',
        'personalidad',
        'impulsividad',
        'organizacion',
        'valores',
        'temperamento',
        'confiabilidad',
        'compromiso',
        'habilidades_laborales',
        'resultado_psicologico',
        'resultado_aspirante',
        'observacion'
    )


class CarpetaExamenToxicologicoPrevioInline(NestedStackedInline):
    model = CarpetaExamenToxicologicoPrevio
    extra = 1
    fields = (
        'fecha_examen',
        'cocaina',
        'marihuana',
        'opiaceos',
        'anfetaminas',
        'metanfetaminas',
        'barbituricos',
        'benzodiacepinas',
        'resultado_toxicologico',
        'resultado_aspirante',
        'observacion'
    )


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


class CarpetaMediaFiliacionPrevioInline(NestedStackedInline):
    model = CarpetaMediaFiliacionPrevio
    extra = 1
    fields = (
        'peso',
        'estatura',
        'indice_masa_corporal',
        'clasificacion_imc',
        'tension_arterial',
        'temperatura',
        'sat02',
        'frecuencia_cardiaca',
        'cronica_degenerativa',
        'sangre',
        'rh'
    )

    def get_readonly_fields(self, request, obj=None):
        readonly_fields = super().get_readonly_fields(request, obj)
        if obj.carpetamediafiliacion:
            if obj.carpetamediafiliacion.estatura is None or obj.carpetamediafiliacion.peso is None:
                readonly_fields += ('indice_masa_corporal', 'clasificacion_imc')
        return readonly_fields


class DocumentosDigitalesPrevioInline(NestedStackedInline):
    model = DocumentosDigitalesPrevio
    fields = (
        'check_acta_nacimiento',
        'check_ine',
        'check_comprobante_estudios',
        'check_comprobante_domicilio',
        'check_curp',
        'check_rfc',
        'check_cartilla',
        'check_nss',
        'check_huellas_digitales',
        'check_fotografias',
    )
    extra = 1


class CurpPrevioInline(NestedStackedInline):
    model = CurpPrevio
    extra = 1
    fields = (
        'personal',
        'curp',
        'nombre',
        'apellido_paterno',
        'apellido_materno',
        'sexo',
        'iniciales',
    )
    readonly_fields = (
        'fecha_nacimiento',
        'edad',
        'anio_registro',
        'numero_acta',
        'validacion_renapo',
        'estatus_curp',
        'clave_municipio_registro',
        'municipio_registro',
        'clave_entidad_registro',
        'entidad_registro',
        'transaction_id',
    )


class RfcPrevioInline(NestedStackedInline):
    model = RfcPrevio
    extra = 1
    fields = (
        'personal',
        'rfc',
        'razon_social',
        'rfc_digital',
    )
    readonly_fields = (
        'estatus',
        'fecha_efectiva',
        'correo_contacto',
        'validez',
        'tipo',
    )


@admin.register(PersonalPrevio)
class PersonalPrevioAdmin(NestedModelAdmin):
    list_display = ('id', 'nombre_completo', 'cliente',)
    search_fields = ['cliente',]
    autocomplete_fields = ['cliente',]
    inlines = [
        CurpPrevioInline,
        RfcPrevioInline,
        DomicilioInline,
        EvaluadorInline,
        CarpetaExamenFisicoPrevioInline,
        CarpetaExamenMedicoPrevioInline,
        CarpetaExamenPsicologicoPrevioInline,
        CarpetaExamenToxicologicoPrevioInline,
        CarpetaExamenSocioeconomicoPrevioInline,
        CarpetaGeneralesPrevioInline,
        CarpetaMediaFiliacionPrevioInline,
        DocumentosDigitalesPrevioInline,
        ResultadosInline,
    ]

    def nombre_completo(self, obj):
        return f"{obj.curp.get_nombre_completo()}"

    nombre_completo.short_description = 'Nombre Completo'


@admin.register(Curp)
class CurpAdmin(admin.ModelAdmin):
    list_display = ('id', 'curp', 'nombre', 'apellido_paterno', 'apellido_materno', 'fecha_nacimiento', 'sexo',)
    search_fields = ['curp', 'nombre', 'apellido_paterno', 'apellido_materno',]


@admin.register(CurpEmpleado)
class CurpEmpleadoAdmin(admin.ModelAdmin):
    list_display = ('id', 'curp', 'nombre', 'apellido_paterno', 'apellido_materno', 'sexo',)
    search_fields = ['curp', 'nombre', 'apellido_paterno', 'apellido_materno',]

    def get_form(self, request, obj=None, **kwargs):
        form = super().get_form(request, obj, **kwargs)

        # Hide all other fields
        for field in form.base_fields:
            if field not in self.list_display:
                form.base_fields[field].widget = forms.HiddenInput()
        return form


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


@admin.register(RfcEmpleado)
class RfcEmpleadoAdmin(admin.ModelAdmin):
    list_display = ('id', 'rfc', 'razon_social',)
    search_fields = ['rfc', 'razon_social',]

    def get_form(self, request, obj=None, **kwargs):
        form = super().get_form(request, obj, **kwargs)

        # Hide all other fields
        for field in form.base_fields:
            if field not in self.list_display:
                form.base_fields[field].widget = forms.HiddenInput()
        return form


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


@admin.register(PuestoFuncional)
class PuestoFuncionalAdmin(admin.ModelAdmin):
    list_display = ('id', 'nombre_puesto',)


@admin.register(JefeMedico)
class JefeMedicoAdmin(admin.ModelAdmin):
    list_display = ('id', 'nombre_completo', 'cedula_profesional',)
    search_fields = ['nombre_completo', 'cedula_profesional',]


@admin.register(MedicoOdontologico)
class MedicoOdontologicoAdmin(admin.ModelAdmin):
    list_display = ('id', 'nombre_completo', 'cedula_profesional',)
    search_fields = ['nombre_completo', 'cedula_profesional',]


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


@admin.register(ReportAuthenticity)
class ReportAuthenticityAdmin(admin.ModelAdmin):
    list_display = ('id', 'authenticity_chain', 'report_name', 'content', 'created_at')
    search_fields = ['authenticity_chain', 'report_name', 'created_at']
