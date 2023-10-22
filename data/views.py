from data.models import *
from data.serializers import *
from rest_framework.response import Response
from rest_framework import status
from rest_framework import generics, authentication, permissions
from rest_framework.authtoken.models import Token
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework import viewsets


# Create your views here.
class CreateCustomUserView(generics.CreateAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = CustomUserSerializer

class CreateTokenView(ObtainAuthToken):
    serializer_class = AuthTokenSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        token, created = Token.objects.get_or_create(user=user)
        return Response({'token': token.key})

class RetrieveUpdateUserView(generics.RetrieveUpdateAPIView):
    serializer_class = CustomUserSerializer
    authentication_classes = (authentication.TokenAuthentication,)
    permission_classes = (permissions.IsAuthenticated,)

    def get_object(self):
        return self.request.user

class EditProfileView(generics.UpdateAPIView):
    serializer_class = EditProfileSerializer
    authentication_classes = (authentication.TokenAuthentication,)
    permission_classes = (permissions.IsAuthenticated,)

    def get_object(self):
        return self.request.user


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


CurpViewset = create_viewset(Curp, CurpEmpleadoSerializer, CurpPrevioSerializer)
RfcViewset =  create_viewset(Rfc, RfcEmpleadoSerializer, RfcPrevioSerializer)
ClienteViewset = create_viewset(Cliente, ClienteEmpleadoSerializer, ClientePrevioSerializer)
DocumentosClienteViewset = create_viewset(DocumentosCliente, DocumentosClienteSerializer)
SedeViewset = create_viewset(Sede, SedeEmpleadoSerializer, SedePrevioSerializer)
CarpetaClienteGeneralesViewset = create_viewset(CarpetaClienteGenerales, CarpetaClienteGeneralesSerializer)
CarpetaClientePagosViewset = create_viewset(CarpetaClientePagos, CarpetaClientePagosSerializer)
CarpetaClienteContactosViewset = create_viewset(CarpetaClienteContactos, CarpetaClienteContactosSerializer)
PersonalViewset = create_viewset(Personal, PersonalEmpleadoSerializer, PersonalPrevioSerializer)
EvaluadorViewset = create_viewset(Evaluador, EvaluadorEmpleadoSerializer, EvaluadorPrevioSerializer)
OcupacionViewset = create_viewset(Ocupacion, OcupacionSerializer)
AreaCursoViewset = create_viewset(AreaCurso, AreaCursoSerializer)
InstructorViewset = create_viewset(Instructor, InstructorSerializer)
CarpetaLaboralViewset = create_viewset(CarpetaLaboral, CarpetaLaboralSerializer)
PuestoViewset = create_viewset(Puesto, PuestoEmpladoSerializer, PuestoPrevioSerializer)
CarpetaGeneralesViewset = create_viewset(CarpetaGenerales, CarpetaGeneralesEmpleadoSerializer, CarpetaGeneralesPrevioSerializer)
CarpetaReferenciasViewset = create_viewset(CarpetaReferencias, CarpetaReferenciasSerializer)
ReferenciaViewset = create_viewset(Referencia, ReferenciaSerializer)
CarpetaDependienteViewset = create_viewset(CarpetaDependientes, CarpetaDependientesSerializer)
DependienteViewset = create_viewset(Dependiente, DependienteSerializer)
CarpetaExamenPsicologicoViewset = create_viewset(CarpetaExamenPsicologico, CarpetaExamenPsicologicoEmpleadoSerializer, CarpetaExamenPsicologicoPrevioSerializer)
CarpetaExamenToxicologicoViewset = create_viewset(CarpetaExamenToxicologico, CarpetaExamenToxicologicoEmpleadoSerializer, CarpetaExamenToxicologicoPrevioSerializer)
CarpetaExamenMedicoViewset = create_viewset(CarpetaExamenMedico, CarpetaExamenMedicoEmpleadoSerializer, CarpetaExamenMedicoPrevioSerializer)
CarpetaExamenFisicoViewset = create_viewset(CarpetaExamenFisico, CarpetaExamenFisicoEmpleadoSerializer, CarpetaExamenFisicoPrevioSerializer)
CarpetaExamenSocioeconomicoViewset = create_viewset(CarpetaExamenSocioeconomico, CarpetaExamenSocioeconomicoEmpleadoSerializer, CarpetaExamenSocioeconomicoPrevioSerializer)
CarpetaExamenPoligrafoViewset = create_viewset(CarpetaExamenPoligrafo, CarpetaExamenPoligrafoEmpleadoSerializer, CarpetaExamenPoligrafoPrevioSerializer)
CarpetaEmpleoAnteriorSeguridadPublicaViewset = create_viewset(CarpetaEmpleoAnteriorSeguridadPublica, CarpetaEmpleoAnteriorSeguridadPublicaSerializer)
EmpleoAnteriorSeguridadPublicaViewset = create_viewset(EmpleoAnteriorSeguridadPublica, EmpleoAnteriorSeguridadPublicaSerializer)
PuestoFuncionalViewset = create_viewset(PuestoFuncional, PuestoFuncionalSerializer)
TipoBajaViewset = create_viewset(TipoBaja, TipoBajaSerializer)
CarpetaEmpleoAnteriorViewset = create_viewset(CarpetaEmpleoAnterior, CarpetaEmpleoAnteriorSerializer)
EmpleoAnteriorViewset = create_viewset(EmpleoAnterior, EmpleoAnteriorSerializer)
MotivoSeparacionViewset = create_viewset(MotivoSeparacion, MotivoSeparacionSerializer)
CarpetaCapacitacionViewset = create_viewset(CarpetaCapacitacion, CarpetaCapacitacionSerializer)
CapacitacionViewset = create_viewset(Capacitacion, CapacitacionSerializer)
TipoCursoViewset = create_viewset(TipoCurso, TipoCursoSerializer)

# TODO: Verificar si sigue en pie esta función
# class CapacitacionEnCursoViewSet(BaseViewSet):
#     serializer_class = CapacitacionEnCursoSerializer
#     model_class = CapacitacionEnCurso
IdiomaViewset = create_viewset(Idioma, IdiomaSerializer)
# TODO: Verificar si sigue en pie esta función
# class HabilidadViewSet(BaseViewSet):
#     serializer_class = HabilidadSerializer
#     model_class = Habilidad
# class HabilidadPersonalizadaViewSet(BaseViewSet):
#     serializer_class = HabilidadPersonalizadaSerializer
#     model_class = HabilidadPersonalizada

CarpetaMediaFiliacionViewset = create_viewset(CarpetaMediaFiliacion, CarpetaMediaFiliacionEmpleadoSerializer, CarpetaMediaFiliacionPrevioSerializer)
DocumentosDigitalesViewset = create_viewset(DocumentosDigitales, DocumentosDigitalesEmpleadoSerializer, DocumentosDigitalesPrevioSerializer)
RepresentanteTrabajadoresViewset = create_viewset(RepresentanteTrabajadores, RepresentanteTrabajadoresSerializer)
CapacitacionClienteViewset = create_viewset(CapacitacionCliente, CapacitacionClienteSerializer)
PersonalPorCapacitarViewset = create_viewset(PersonalPorCapacitar, PersonalPorCapacitarSerializer)
DomicilioViewset = create_viewset(Domicilio, DomicilioSerializer)
CodigoPostalViewset = create_viewset(CodigoPostal, CodigoPostalSerializer)
ColoniaViewset = create_viewset(Colonia, ColoniaSerializer)
MunicipioViewset = create_viewset(Municipio, MunicipioSerializer)
EstadoViewset = create_viewset(Estado, EstadoSerializer)
PaisViewset = create_viewset(Pais, PaisSerializer)
