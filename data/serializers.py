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
CurpPrevioSerializer = create_serializer(Curp, ['curp', 'nombre', 'apellido_paterno', 'apellido_materno','sexo', ])
RfcEmpleadoSerializer = create_serializer(Rfc)
RfcPrevioSerializer = create_serializer(Rfc, ['rfc',])
ClienteSerializer = create_serializer(Cliente)
DocumentosClienteSerializer = create_serializer(DocumentosCliente)
SedeSerializer = create_serializer(Sede)
CarpetaClienteGeneralesSerializer = create_serializer(CarpetaClienteGenerales)
CarpetaClientePagosSerializer = create_serializer(CarpetaClientePagos)
CarpetaClienteContactosSerializer = create_serializer(CarpetaClienteContactos)
PersonalSerializer = create_serializer(Personal)
EvaluadorEmpleadoSerializer = create_serializer(Evaluador)

OcupacionSerializer = create_serializer(Ocupacion)
AreaCursoSerializer = create_serializer(AreaCurso)
CapacitadorSerializer = create_serializer(Capacitador)
CarpetaLaboralSerializer = create_serializer(CarpetaLaboral)
PuestoSerializer = create_serializer(Puesto)
CarpetaGeneralesSerializer = create_serializer(CarpetaGenerales)
CarpetaReferenciasSerializer = create_serializer(CarpetaReferencias)
ReferenciaSerializer = create_serializer(Referencia)
CarpetaDependientesSerializer = create_serializer(CarpetaDependientes)
DependienteSerializer = create_serializer(Dependiente)
CarpetaExamenPsicologicoSerializer = create_serializer(CarpetaExamenPsicologico)
CarpetaExamenToxicologicoSerializer = create_serializer(CarpetaExamenToxicologico)
CarpetaExamenMedicoSerializer = create_serializer(CarpetaExamenMedico)
CarpetaExamenFisicoSerializer = create_serializer(CarpetaExamenFisico)
CarpetaExamenSocioeconomicoSerializer = create_serializer(CarpetaExamenSocioeconomico)
CarpetaExamenPoligrafoSerializer = create_serializer(CarpetaExamenPoligrafo)
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
CarpetaMediaFiliacionSerializer = create_serializer(CarpetaMediaFiliacion)
DocumentosDigitalesSerializer = create_serializer(DocumentosDigitales)
RepresentanteTrabajadoresSerializer = create_serializer(RepresentanteTrabajadores)
CapacitacionClienteSerializer = create_serializer(CapacitacionCliente)
PersonalPorCapacitarSerializer = create_serializer(PersonalPorCapacitar)
DomicilioSerializer = create_serializer(Domicilio)
CodigoPostalSerializer = create_serializer(CodigoPostal)
ColoniaSerializer = create_serializer(Colonia)
MunicipioSerializer = create_serializer(Municipio)
EstadoSerializer = create_serializer(Estado)
PaisSerializer = create_serializer(Pais)