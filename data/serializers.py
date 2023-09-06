from rest_framework import serializers
from .models import *

def create_serializer(model):
    class_name = f"{model.__name__}Serializer"
    fields = "__all__"
    meta_class = type('Meta', (object,), {'model': model, 'fields': fields})
    return type(class_name, (serializers.ModelSerializer,), {'Meta': meta_class})

CurpSerializer = create_serializer(Curp)
RfcSerializer = create_serializer(Rfc)
ClienteSerializer = create_serializer(Cliente)
SedeSerializer = create_serializer(Sede)
CarpetaClienteGeneralesSerializer = create_serializer(CarpetaClienteGenerales)
CarpetaClientePagosSerializer = create_serializer(CarpetaClientePagos)
CarpetaClienteContactosSerializer = create_serializer(CarpetaClienteContactos)
PersonalSerializer = create_serializer(Personal)
EvaluadorSerializer = create_serializer(Evaluador)
CarpetaLaboralSerializer = create_serializer(CarpetaLaboral)
PuestoSerializer = create_serializer(Puesto)
CarpetaGeneralesSerializer = create_serializer(CarpetaGenerales)
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
CapacitacionClienteSerializer = create_serializer(Capacitacion)
PersonalPorCapacitarSerializer = create_serializer(PersonalPorCapacitar)
DomicilioSerializer = create_serializer(Domicilio)
CodigoPostalSerializer = create_serializer(CodigoPostal)
ColoniaSerializer = create_serializer(Colonia)
MunicipioSerializer = create_serializer(Municipio)
EstadoSerializer = create_serializer(Estado)
PaisSerializer = create_serializer(Pais)
