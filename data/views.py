from rest_framework import viewsets
from .models import *
from .serializers import *
from rest_framework.response import Response
from rest_framework import status


# Create your views here.

class BaseViewSet(viewsets.ModelViewSet):
    """
    A base ViewSet class that provides the standard actions for a Django model.

    Attributes:
        serializer_class: The serializer class to be used for this ViewSet.
        model_class: The Django model for which the ViewSet is being created.
        employee_serializer_class: The serializer to be used when the URL contains 'employees'.
        previous_serializer_class: The serializer to be used when the URL contains 'previous'.

    Methods:
        list(self, request): Returns a list of all model instances.
        create(self, request): Creates and returns a new model instance.
        retrieve(self, request, pk=None): Retrieves and returns a specific model instance.
        update(self, request, pk=None): Updates and returns a specific model instance.
        destroy(self, request, pk=None): Deletes a specific model instance.
    """
    serializer_class = None
    model_class = None
    employee_serializer_class = None
    previous_serializer_class = None

    def list(self, request):
        items = self.model_class.objects.all()
        serializer = self.serializer_class(items, many=True)
        return Response(serializer.data)

    def create(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def retrieve(self, request, pk=None):
        item = self.model_class.objects.get(id=pk)
        serializer = self.serializer_class(item, many=False)
        return Response(serializer.data)

    def update(self, request, pk=None):
        item = self.model_class.objects.get(id=pk)
        serializer = self.serializer_class(instance=item, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_202_ACCEPTED)

    def destroy(self, request, pk=None):
        item = self.model_class.objects.get(id=pk)
        item.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    

def create_viewset(model, employee_serializer, previous_serializer=None):
    """
    Creates a ViewSet class for the provided model and serializers.

    Args:
        model: The Django model for which the ViewSet is being created.
        employee_serializer: The serializer to be used when the URL contains 'employees'.
        previous_serializer: The serializer to be used when the URL contains 'previous'. If not provided, employee_serializer will be used.

    Returns:
        A Django Rest Framework ViewSet class for the given model.
    """
    class_name = f"{model.__name__}ViewSet"

    class MetaViewSet(BaseViewSet):
        model_class = model
        employee_serializer_class = employee_serializer
        previous_serializer_class = previous_serializer

        def get_serializer_class(self):
            if 'employees' in self.request.path:
                return self.employee_serializer_class
            elif 'previous' in self.request.path and self.previous_serializer_class is not None:
                return self.previous_serializer_class
            else:
                return self.employee_serializer_class

    MetaViewSet.__name__ = class_name
    return MetaViewSet


create_viewset(Curp, CurpEmpleadoSerializer, CurpPrevioSerializer)
create_viewset(Rfc, RfcEmpleadoSerializer, RfcPrevioSerializer)
create_viewset(Cliente, ClienteEmpleadoSerializer, ClientePrevioSerializer)
create_viewset(DocumentosCliente, DocumentosClienteSerializer)
create_viewset(Sede, SedeEmpleadoSerializer, SedePrevioSerializer)
create_viewset(CarpetaClienteGenerales, CarpetaClienteGeneralesSerializer)
create_viewset(CarpetaClientePagos, CarpetaClientePagosSerializer)
create_viewset(CarpetaClienteContactos, CarpetaClienteContactosSerializer)
create_viewset(Personal, PersonalEmpleadoSerializer, PersonalPrevioSerializer)
create_viewset(Evaluador, EvaluadorEmpleadoSerializer, EvaluadorPrevioSerializer)
create_viewset(Ocupacion, OcupacionSerializer)
create_viewset(AreaCurso, AreaCursoSerializer)
create_viewset(Capacitador, CapacitadorSerializer)
create_viewset(CarpetaLaboral, CarpetaLaboralSerializer)
create_viewset(Puesto, PuestoEmpladoSerializer, PuestoPrevioSerializer)
create_viewset(CarpetaGenerales, CarpetaGeneralesEmpleadoSerializer, CarpetaGeneralesPrevioSerializer)
create_viewset(CarpetaReferencias, CarpetaReferenciasSerializer)
create_viewset(Referencia, ReferenciaSerializer)
create_viewset(CarpetaDependientes, CarpetaDependientesSerializer)
create_viewset(Dependiente, DependienteSerializer)
create_viewset(CarpetaExamenPsicologico, CarpetaExamenPsicologicoEmpleadoSerializer, CarpetaExamenPsicologicoPrevioSerializer)
create_viewset(CarpetaExamenToxicologico, CarpetaExamenToxicologicoEmpleadoSerializer, CarpetaExamenToxicologicoPrevioSerializer)
create_viewset(CarpetaExamenMedico, CarpetaExamenMedicoEmpleadoSerializer, CarpetaExamenMedicoPrevioSerializer)
create_viewset(CarpetaExamenFisico, CarpetaExamenFisicoEmpleadoSerializer, CarpetaExamenFisicoPrevioSerializer)
create_viewset(CarpetaExamenSocioeconomico, CarpetaExamenSocioeconomicoEmpleadoSerializer, CarpetaExamenSocioeconomicoPrevioSerializer)
create_viewset(CarpetaExamenPoligrafo, CarpetaExamenPoligrafoEmpleadoSerializer, CarpetaExamenPoligrafoPrevioSerializer)
create_viewset(CarpetaEmpleoAnteriorSeguridadPublica, CarpetaEmpleoAnteriorSeguridadPublicaSerializer)
create_viewset(EmpleoAnteriorSeguridadPublica, EmpleoAnteriorSeguridadPublicaSerializer)
create_viewset(PuestoFuncional, PuestoFuncionalSerializer)
create_viewset(TipoBaja, TipoBajaSerializer)
create_viewset(CarpetaEmpleoAnterior, CarpetaEmpleoAnteriorSerializer)
create_viewset(EmpleoAnterior, EmpleoAnteriorSerializer)
create_viewset(MotivoSeparacion, MotivoSeparacionSerializer)
create_viewset(CarpetaCapacitacion, CarpetaCapacitacionSerializer)
create_viewset(Capacitacion, CapacitacionPreviaSerializer)
create_viewset(TipoCurso, TipoCursoSerializer)

# class CapacitacionEnCursoViewSet(BaseViewSet):
#     serializer_class = CapacitacionEnCursoSerializer
#     model_class = CapacitacionEnCurso

# class HabilidadViewSet(BaseViewSet):
#     serializer_class = HabilidadSerializer
#     model_class = Habilidad

# class HabilidadPersonalizadaViewSet(BaseViewSet):
#     serializer_class = HabilidadPersonalizadaSerializer
#     model_class = HabilidadPersonalizada

create_viewset(Idioma, IdiomaSerializer)
create_viewset(CarpetaMediaFiliacion, CarpetaMediaFiliacionEmpleadoSerializer, CarpetaMediaFiliacionPrevioSerializer)
create_viewset(DocumentosDigitales, DocumentosDigitalesEmpleadoSerializer, DocumentosDigitalesPrevioSerializer)
create_viewset(RepresentanteTrabajadores, RepresentanteTrabajadoresSerializer)
create_viewset(CapacitacionCliente, CapacitacionClienteSerializer)
create_viewset(PersonalPorCapacitar, PersonalPorCapacitarSerializer)
create_viewset(Domicilio, DomicilioSerializer)
create_viewset(CodigoPostal, CodigoPostalSerializer)
create_viewset(Colonia, ColoniaSerializer)
create_viewset(Municipio, MunicipioSerializer)
create_viewset(Estado, EstadoSerializer)
create_viewset(Pais, PaisSerializer)
