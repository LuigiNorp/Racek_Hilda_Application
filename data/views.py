from rest_framework import viewsets
from .models import *
from .serializers import *
from rest_framework.response import Response
from rest_framework import status


# Create your views here.

class BaseViewSet(viewsets.ModelViewSet):
    serializer_class = None
    model_class = None

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


class CurpViewSet(BaseViewSet):
    serializer_class = CurpSerializer
    model_class = Curp

class RfcViewSet(BaseViewSet):
    serializer_class = RfcSerializer
    model_class = Rfc

class ClienteViewSet(BaseViewSet):
    serializer_class = ClienteSerializer
    model_class = Cliente

class DocumentosClienteViewSet(BaseViewSet):
    serializer_class = DocumentosClienteSerializer
    model_class = DocumentosCliente

class SedeViewSet(BaseViewSet):
    serializer_class = SedeSerializer
    model_class = Sede

class CarpetaClienteGeneralesViewSet(BaseViewSet):
    serializer_class = CarpetaClienteGeneralesSerializer
    model_class = CarpetaClienteGenerales

class CarpetaClientePagosViewSet(BaseViewSet):
    serializer_class = CarpetaClientePagosSerializer
    model_class = CarpetaClientePagos

class CarpetaClienteContactosViewSet(BaseViewSet):
    serializer_class = CarpetaClienteContactosSerializer
    model_class = CarpetaClienteContactos

class PersonalViewSet(BaseViewSet):
    serializer_class = PersonalSerializer
    model_class = Personal

class EvaluadorViewSet(BaseViewSet):
    serializer_class = EvaluadorSerializer
    model_class = Evaluador

class OcupacionViewSet(BaseViewSet):
    serializer_class = OcupacionSerializer
    model_class = Ocupacion
    
class AreaCursoViewSet(BaseViewSet):
    serializer_class = AreaCursoSerializer
    model_class = AreaCurso
    
class CapacitadorViewSet(BaseViewSet):
    serializer_class = CapacitadorSerializer
    model_class = Capacitador

class CarpetaLaboralViewSet(BaseViewSet):
    serializer_class = CarpetaLaboralSerializer
    model_class = CarpetaLaboral

class PuestoViewSet(BaseViewSet):
    serializer_class = PuestoSerializer
    model_class = Puesto

class CarpetaGeneralesViewSet(BaseViewSet):
    serializer_class = CarpetaGeneralesSerializer
    model_class = CarpetaGenerales

class CarpetaReferenciasViewSet(BaseViewSet):
    serializer_class = CarpetaReferenciasSerializer
    model_class = CarpetaReferencias

class ReferenciaViewSet(BaseViewSet):
    serializer_class = ReferenciaSerializer
    model_class = Referencia

class CarpetaDependientesViewSet(BaseViewSet):
    serializer_class = CarpetaDependientesSerializer
    model_class = CarpetaDependientes

class DependienteViewSet(BaseViewSet):
    serializer_class = DependienteSerializer
    model_class = Dependiente

class CarpetaExamenPsicologicoViewSet(BaseViewSet):
    serializer_class = CarpetaExamenPsicologicoSerializer
    model_class = CarpetaExamenPsicologico

class CarpetaExamenToxicologicoViewSet(BaseViewSet):
    serializer_class = CarpetaExamenToxicologicoSerializer
    model_class = CarpetaExamenToxicologico

class CarpetaExamenMedicoViewSet(BaseViewSet):
    serializer_class = CarpetaExamenMedicoSerializer
    model_class = CarpetaExamenMedico

class CarpetaExamenFisicoViewSet(BaseViewSet):
    serializer_class = CarpetaExamenFisicoSerializer
    model_class = CarpetaExamenFisico

class CarpetaExamenSocioeconomicoViewSet(BaseViewSet):
    serializer_class = CarpetaExamenSocioeconomicoSerializer
    model_class = CarpetaExamenSocioeconomico

class CarpetaExamenPoligrafoViewSet(BaseViewSet):
    serializer_class = CarpetaExamenPoligrafoSerializer
    model_class = CarpetaExamenPoligrafo

class CarpetaEmpleoAnteriorSeguridadPublicaViewSet(BaseViewSet):
    serializer_class = CarpetaEmpleoAnteriorSeguridadPublicaSerializer
    model_class = CarpetaEmpleoAnteriorSeguridadPublica

class EmpleoAnteriorSeguridadPublicaViewSet(BaseViewSet):
    serializer_class = EmpleoAnteriorSeguridadPublicaSerializer
    model_class = EmpleoAnteriorSeguridadPublica

class PuestoFuncionalViewSet(BaseViewSet):
    serializer_class = PuestoFuncionalSerializer
    model_class = PuestoFuncional

class TipoBajaViewSet(BaseViewSet):
    serializer_class = TipoBajaSerializer
    model_class = TipoBaja

class CarpetaEmpleoAnteriorViewSet(BaseViewSet):
    serializer_class = CarpetaEmpleoAnteriorSerializer
    model_class = CarpetaEmpleoAnterior

class EmpleoAnteriorViewSet(BaseViewSet):
    serializer_class = EmpleoAnteriorSerializer
    model_class = EmpleoAnterior

class MotivoSeparacionViewSet(BaseViewSet):
    serializer_class = MotivoSeparacionSerializer
    model_class = MotivoSeparacion

class CarpetaCapacitacionViewSet(BaseViewSet):
    serializer_class = CarpetaCapacitacionSerializer
    model_class = CarpetaCapacitacion

class CapacitacionPreviaViewSet(BaseViewSet):
    serializer_class = CapacitacionPreviaSerializer
    model_class = Capacitacion

class TipoCursoViewSet(BaseViewSet):
    serializer_class = TipoCursoSerializer
    model_class = TipoCurso

# class CapacitacionEnCursoViewSet(BaseViewSet):
#     serializer_class = CapacitacionEnCursoSerializer
#     model_class = CapacitacionEnCurso

class IdiomaViewSet(BaseViewSet):
    serializer_class = IdiomaSerializer
    model_class = Idioma

# class HabilidadViewSet(BaseViewSet):
#     serializer_class = HabilidadSerializer
#     model_class = Habilidad

# class HabilidadPersonalizadaViewSet(BaseViewSet):
#     serializer_class = HabilidadPersonalizadaSerializer
#     model_class = HabilidadPersonalizada

class CarpetaMediaFiliacionViewSet(BaseViewSet):
    serializer_class = CarpetaMediaFiliacionSerializer
    model_class = CarpetaMediaFiliacion

class DocumentosDigitalesViewSet(BaseViewSet):
    serializer_class = DocumentosDigitalesSerializer
    model_class = DocumentosDigitales
    
class RepresentanteTrabajadoresViewSet(BaseViewSet):
    serializer_class = RepresentanteTrabajadoresSerializer
    model_class = RepresentanteTrabajadores

class CapacitacionClienteViewSet(BaseViewSet):
    serializer_class = CapacitacionClienteSerializer
    model_class = CapacitacionCliente

class PersonalPorCapacitarViewSet(BaseViewSet):
    serializer_class = PersonalPorCapacitarSerializer
    model_class = PersonalPorCapacitar

class DomicilioViewSet(BaseViewSet):
    serializer_class = DomicilioSerializer
    model_class = Domicilio

class CodigoPostalViewSet(BaseViewSet):
    serializer_class = CodigoPostalSerializer
    model_class = CodigoPostal

class ColoniaViewSet(BaseViewSet):
    serializer_class = ColoniaSerializer
    model_class = Colonia

class MunicipioViewSet(BaseViewSet):
    serializer_class = MunicipioSerializer
    model_class = Municipio

class EstadoViewSet(BaseViewSet):
    serializer_class = EstadoSerializer
    model_class = Estado

class PaisViewSet(BaseViewSet):
    serializer_class = PaisSerializer
    model_class = Pais