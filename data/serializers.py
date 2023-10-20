from rest_framework import serializers
from .models import *

def create_serializer(model, fields=None):
    """
    Creates a serializer for the given model.

    Args:
        model: The Django model for which the serializer is being created.
        fields: A list or tuple of fields to be included in the serializer. If not provided, all fields will be included.

    Returns:
        A Django Rest Framework serializer for the given model.
    """
    class_name = f"{model.__name__}Serializer"
    fields = fields if fields else "__all__"
    meta_class = type('Meta', (object,), {'model': model, 'fields': fields})
    return type(class_name, (serializers.ModelSerializer,), {'Meta': meta_class})

CurpEmpleadoSerializer = create_serializer(Curp)
CurpPrevioSerializer = create_serializer(Curp, ['curp', 'nombre', 'apellido_paterno', 'apellido_materno','sexo'])
RfcEmpleadoSerializer = create_serializer(Rfc)
RfcPrevioSerializer = create_serializer(Rfc, ['rfc', 'rfc_digital'])
ClienteEmpleadoSerializer = create_serializer(Cliente)
ClientePrevioSerializer = create_serializer(Cliente, ['id', 'nombre_comercial'])
DocumentosClienteSerializer = create_serializer(DocumentosCliente)
SedeEmpleadoSerializer = create_serializer(Sede)
SedePrevioSerializer = create_serializer(Sede, ['nombre_sede'])
CarpetaClienteGeneralesSerializer = create_serializer(CarpetaClienteGenerales)
CarpetaClientePagosSerializer = create_serializer(CarpetaClientePagos)
CarpetaClienteContactosSerializer = create_serializer(CarpetaClienteContactos)
PersonalEmpleadoSerializer = create_serializer(Personal)
PersonalPrevioSerializer = create_serializer(Personal,['folio','origen','fecha','observaciones','resultado'])
EvaluadorEmpleadoSerializer = create_serializer(Evaluador)
EvaluadorPrevioSerializer = create_serializer(Evaluador, ['solicitante'])
OcupacionSerializer = create_serializer(Ocupacion)
AreaCursoSerializer = create_serializer(AreaCurso)
CapacitadorSerializer = create_serializer(Capacitador)
CarpetaLaboralSerializer = create_serializer(CarpetaLaboral)
PuestoEmpladoSerializer = create_serializer(Puesto)
PuestoPrevioSerializer = create_serializer(Puesto, ['nombre_puesto'])
CarpetaGeneralesEmpleadoSerializer = create_serializer(CarpetaGenerales)
CarpetaGeneralesPrevioSerializer = create_serializer(CarpetaGenerales,['estado_civil', 'escolaridad', 'telefono_domicilio', 'telefono_celular', 'telefono_recados', 'email_empleado'])
CarpetaReferenciasSerializer = create_serializer(CarpetaReferencias)
ReferenciaSerializer = create_serializer(Referencia)
CarpetaDependientesSerializer = create_serializer(CarpetaDependientes)
DependienteSerializer = create_serializer(Dependiente)
CarpetaExamenPsicologicoEmpleadoSerializer = create_serializer(CarpetaExamenPsicologico)
CarpetaExamenPsicologicoPrevioSerializer = create_serializer(CarpetaExamenPsicologico, ['resultado_aspirante', 'observacion'])
CarpetaExamenToxicologicoEmpleadoSerializer = create_serializer(CarpetaExamenToxicologico)
CarpetaExamenToxicologicoPrevioSerializer = create_serializer(CarpetaExamenToxicologico, ['resultado_aspirante', 'observacion'])
CarpetaExamenMedicoEmpleadoSerializer = create_serializer(CarpetaExamenMedico)
CarpetaExamenMedicoPrevioSerializer = create_serializer(CarpetaExamenMedico, ['resultado_aspirante', 'observacion'])
CarpetaExamenFisicoEmpleadoSerializer = create_serializer(CarpetaExamenFisico)
CarpetaExamenFisicoPrevioSerializer = create_serializer(CarpetaExamenFisico, ['resultado_aspirante', 'observacion'])
CarpetaExamenSocioeconomicoEmpleadoSerializer = create_serializer(CarpetaExamenSocioeconomico)
CarpetaExamenSocioeconomicoPrevioSerializer = create_serializer(CarpetaExamenSocioeconomico, ['resultado_aspirante', 'observacion'])
CarpetaExamenPoligrafoEmpleadoSerializer = create_serializer(CarpetaExamenPoligrafo)
CarpetaExamenPoligrafoPrevioSerializer = create_serializer(CarpetaExamenPoligrafo, ['resultado_aspirante', 'observacion'])
CarpetaEmpleoAnteriorSeguridadPublicaSerializer = create_serializer(CarpetaEmpleoAnteriorSeguridadPublica)
EmpleoAnteriorSeguridadPublicaSerializer = create_serializer(EmpleoAnteriorSeguridadPublica)
PuestoFuncionalSerializer = create_serializer(PuestoFuncional)
TipoBajaSerializer = create_serializer(TipoBaja)
CarpetaEmpleoAnteriorSerializer = create_serializer(CarpetaEmpleoAnterior)
EmpleoAnteriorSerializer = create_serializer(EmpleoAnterior)
MotivoSeparacionSerializer = create_serializer(MotivoSeparacion)
CarpetaCapacitacionSerializer = create_serializer(CarpetaCapacitacion)
CapacitacionPreviaSerializer = create_serializer(Capacitacion)
TipoCursoSerializer = create_serializer(TipoCurso)
# CapacitacionEnCursoSerializer = create_serializer(CapacitacionEnCurso)
IdiomaSerializer = create_serializer(Idioma)
# HabilidadSerializer = create_serializer(Habilidad)
# HabilidadPersonalizadaSerializer = create_serializer(HabilidadPersonalizada)
CarpetaMediaFiliacionEmpleadoSerializer = create_serializer(CarpetaMediaFiliacion)
CarpetaMediaFiliacionPrevioSerializer = create_serializer(CarpetaMediaFiliacion, ['peso', 'estatura', 'tension_arterial', 'temperatura', 'indice_masa_corporal', 'clasificacion_imc', 'sat02', 'frecuencia_cardiaca', 'cronica_degenerativa', 'sangre', 'rh'])
DocumentosDigitalesEmpleadoSerializer = create_serializer(DocumentosDigitales)
DocumentosDigitalesPrevioSerializer = create_serializer(DocumentosDigitales, ['acta_nacimiento', 'ine', 'comprobante_domicilio', 'comprobante_estudios', 'curp', 'cartilla_smn', 'nss', 'huellas_digitales'])
RepresentanteTrabajadoresSerializer = create_serializer(RepresentanteTrabajadores)
CapacitacionClienteSerializer = create_serializer(CapacitacionCliente)
PersonalPorCapacitarSerializer = create_serializer(PersonalPorCapacitar)
DomicilioSerializer = create_serializer(Domicilio)
CodigoPostalSerializer = create_serializer(CodigoPostal)
ColoniaSerializer = create_serializer(Colonia)
MunicipioSerializer = create_serializer(Municipio)
EstadoSerializer = create_serializer(Estado)
PaisSerializer = create_serializer(Pais)