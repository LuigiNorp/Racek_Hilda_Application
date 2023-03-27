from django.contrib import admin
from .models import *

# Register your models here.

@admin.register(Curp)
class CurpAdmin(admin.ModelAdmin):
    list_display = ('id','curp','nombre','apellido_materno','apellido_paterno','iniciales','fecha_nacimiento','sexo')

@admin.register(Rfc)
class RfcAdmin(admin.ModelAdmin):
    list_display = ('id','rfc','razon_social','correo_contacto','validez','tipo',)

@admin.register(Cliente)
class ClienteAdmin(admin.ModelAdmin):
    list_display = ('id','nombre_comercial','razon_social','activo',)

@admin.register(Sede)
class SedeAdmin(admin.ModelAdmin):
     list_display = ('id','clave_sede', 'nombre_sede', 'cliente')

@admin.register(CarpetaClienteGenerales)
class CarpetaClienteGeneralesAdmin(admin.ModelAdmin):
     list_display = ('id','cliente', 'rfc', 'reg_estatal', 'reg_federal', 'telefono_1', 'representante_legal', 'registro_patronal')

@admin.register(CarpetaClientePagos)
class CarpetaClientePagosAdmin(admin.ModelAdmin):
    list_display = ('id','cliente','encargado_pagos','telefono_oficina', 'rfc', 'factura_subtotal', 'factura_iva','factura_total')

@admin.register(CarpetaClienteContactos)
class CarpetaClienteContactosAdmin(admin.ModelAdmin):
    list_display = ('id','cliente','nombre_contacto','puesto','telefono_1','email_1',)

@admin.register(Personal)
class PersonalAdmin(admin.ModelAdmin):
    list_display = ('id','cliente',)

@admin.register(Evaluador)
class EvaluadorAdmin(admin.ModelAdmin):
    list_display = ('id','evaluador', 'personal')

@admin.register(CarpetaLaboral)
class CarpetaLaboralAdmin(admin.ModelAdmin):
    list_display = ('id','personal','estatus_empleado','proceso_racek','estatus_empleado','cedula','rango',)

@admin.register(Puesto)
class PuestoAdmin(admin.ModelAdmin):
    list_display = ('id','nombre_puesto','carpeta_laboral')

@admin.register(CarpetaGenerales)
class CarpetaGeneralesAdmin(admin.ModelAdmin):
    list_display = ('numero_elemento','personal','email_empleado','telefono_domicilio','estado_civil','cuip','clave_ine','nss')

@admin.register(CarpetaReferencias)
class CarpetaReferenciasAdmin(admin.ModelAdmin):
    list_display = ('id','personal')

@admin.register(Referencia)
class ReferenciaAdmin(admin.ModelAdmin):
    list_display = ('id','nombre','apellido_paterno','apellido_materno','tipo_referencia', 'parentesco')

@admin.register(CarpetaDependientes)
class CarpetasDependientesAdmin(admin.ModelAdmin):
    list_display = ('id','personal','cantidad_dependientes_economicos')

@admin.register(Dependiente)
class DependienteAdmin(admin.ModelAdmin):
    list_display = ('id','nombre','apellido_paterno','apellido_materno','parentesco')

@admin.register(CarpetaExamenPsicologico)
class CarpetaExamenPsicologicoAdmin(admin.ModelAdmin):
    list_display = ('id','personal','resultado_psicologico')

@admin.register(CarpetaExamenToxicologico)
class CarpetaExamenToxicologicoAdmin(admin.ModelAdmin):
    list_display = ('id','personal','resultado_toxicologico')

@admin.register(CarpetaExamenMedico)
class CarpetaExamenMedicoAdmin(admin.ModelAdmin):
    list_display = ('id','personal','medico_resultado','ishihara_resultado')

@admin.register(CarpetaExamenFisico)
class CarpetaExamenFisicoAdmin(admin.ModelAdmin):
    list_display = ('id','personal','resultado')

@admin.register(CarpetaExamenSocioeconomico)
class CarpetaExamenSocioeconomicoAdmin(admin.ModelAdmin):
    list_display = ('id','personal','supervisor','telefono_recados')

@admin.register(CarpetaExamenPoligrafo)
class CarpetaExamenPoligrafoAdmin(admin.ModelAdmin):
    list_display = ('id','resultado_aspirante', 'personal')

@admin.register(CarpetaEmpleoAnteriorSeguridadPublica)
class CarpetaEmpleoAnteriorSeguridadPublicaAdmin(admin.ModelAdmin):
    list_display = ('id','personal')

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
    list_display = ('id','personal')

@admin.register(EmpleoAnterior)
class EmpleoAnteriorAdmin(admin.ModelAdmin):
    list_display = ('id','emp_ant','empresa')

@admin.register(MotivoSeparacion)
class MotivoSeparacionAdmin(admin.ModelAdmin):
    list_display = ('id','motivo')

@admin.register(CarpetaCapacitacion)
class CarpetaCapacitacionAdmin(admin.ModelAdmin):
    list_display = ('id','personal')

@admin.register(CapacitacionPrevia)
class CapacitacionPreviaAdmin(admin.ModelAdmin):
    list_display = ('id','carpeta_capacitacion','institucion_empresa')

@admin.register(TipoCurso)
class TipoCursoAdmin(admin.ModelAdmin):
    list_display = ('id','tipo_curso')

@admin.register(CapacitacionEnCurso)
class CapacitacionEnCursoAdmin(admin.ModelAdmin):
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

@admin.register(CarpetaMediaFiliacion)
class CarpetaMediaFilicacionAdmin(admin.ModelAdmin):
    list_display = ('id','personal')

@admin.register(DocumentosDigitales)
class DocumentosDigitalesAdmin(admin.ModelAdmin):
    list_display = ('id','personal')

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