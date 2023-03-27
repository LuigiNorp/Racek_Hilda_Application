from rest_framework import viewsets
from .models import *
from .serializers import *
from rest_framework.response import Response
from rest_framework import status

# Create your views here.

class CurpViewSet(viewsets.ModelViewSet): #/api/curp/
    def list(self, request):
        curp = Curp.objects.all()
        serializer = CurpSerializer(curp, many=True)
        return Response(serializer.data)

    def create(self, request): #/api/curp/
        serializer = CurpSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def retrieve(self, request, pk=None): #/api/curp/<str:id>
        curp = Curp.objects.get(id=pk)
        serializer = CurpSerializer(curp, many=False)
        return Response(serializer.data)
    
    def update(self, request, pk=None): #/api/curp/<str:id>
        curp = Curp.objects.get(id=pk)
        serializer = CurpSerializer(instance=curp, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_202_ACCEPTED)

    def destroy(self, request, pk=None): #/api/curp/<str:id>
        curp = Curp.objects.get(id=pk)
        curp.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

class RfcViewSet(viewsets.ModelViewSet): #/api/curp/
    def list(self, request):
        rfc = Rfc.objects.all()
        serializer = RfcSerializer(rfc, many=True)
        return Response(serializer.data)

    def create(self, request): #/api/curp/
        serializer = RfcSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def retrieve(self, request, pk=None): #/api/curp/<str:id>
        rfc = Rfc.objects.get(id=pk)
        serializer = RfcSerializer(rfc, many=False)
        return Response(serializer.data)
    
    def update(self, request, pk=None): #/api/curp/<str:id>
        rfc = Rfc.objects.get(id=pk)
        serializer = RfcSerializer(instance=rfc, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_202_ACCEPTED)

    def destroy(self, request, pk=None): #/api/curp/<str:id>
        rfc = Rfc.objects.get(id=pk)
        rfc.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

class ClienteViewSet(viewsets.ModelViewSet): #/api/curp/
    def list(self, request):
        cliente = Cliente.objects.all()
        serializer = ClienteSerializer(cliente, many=True)
        return Response(serializer.data)

    def create(self, request): #/api/curp/
        serializer = ClienteSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def retrieve(self, request, pk=None): #/api/curp/<str:id>
        cliente = Cliente.objects.get(id=pk)
        serializer = ClienteSerializer(cliente, many=False)
        return Response(serializer.data)
    
    def update(self, request, pk=None): #/api/curp/<str:id>
        cliente = Cliente.objects.get(id=pk)
        serializer = ClienteSerializer(instance=cliente, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_202_ACCEPTED)

    def destroy(self, request, pk=None): #/api/curp/<str:id>
        cliente = Cliente.objects.get(id=pk)
        cliente.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    
class SedeViewSet(viewsets.ModelViewSet): #/api/curp/
    def list(self, request):
        sede = Sede.objects.all()
        serializer = SedeSerializer(sede, many=True)
        return Response(serializer.data)

    def create(self, request):
        serializer = SedeSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    
    def retrieve(self, request, pk=None):
        sede = Sede.objects.get(id=pk)
        serializer = SedeSerializer(sede, many=False)
        return Response(serializer.data)
    
    def update(self, request, pk=None):
        sede = Sede.objects.get(id=pk)
        serializer = SedeSerializer(instance=sede, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_202_ACCEPTED)
    
    def destroy(self, request, pk=None):
        sede = Sede.objects.get(id=pk)
        sede.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

class CarpetaClienteGeneralesViewSet(viewsets.ModelViewSet):
    def list(self, request):
        carpeta_cliente_generales = CarpetaClienteGenerales.objects.all()
        serializer = CarpetaClienteGeneralesSerializer(carpeta_cliente_generales, many=True)
        return Response(serializer.data)

    def create(self, request):
        serializer = CarpetaClienteGeneralesSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    
    def retrieve(self, request, pk=None):
        carpeta_cliente_generales = CarpetaClienteGenerales.objects.get(id=pk)
        serializer = CarpetaClienteGeneralesSerializer(carpeta_cliente_generales, many=False)
        return Response(serializer.data)
    
    def update(self, request, pk=None):
        carpeta_cliente_generales = CarpetaClienteGenerales.objects.get(id=pk)
        serializer = CarpetaClienteGeneralesSerializer(instance=carpeta_cliente_generales, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_202_ACCEPTED)
    
    def destroy(self, request, pk=None):
        carpeta_cliente_generales = CarpetaClienteGenerales.objects.get(id=pk)
        carpeta_cliente_generales.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

class CarpetaClientePagosViewSet(viewsets.ModelViewSet):
    def list(self, request):
        carpeta_cliente_pagos = CarpetaClientePagos.objects.all()
        serializer = CarpetaClientePagosSerializer(carpeta_cliente_pagos, many=True)
        return Response(serializer.data)

    def create(self, request):
        serializer = CarpetaClientePagosSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    
    def retrieve(self, request, pk=None):
        carpeta_cliente_pagos = CarpetaClientePagos.objects.get(id=pk)
        serializer = CarpetaClientePagosSerializer(carpeta_cliente_pagos, many=False)
        return Response(serializer.data)
    
    def update(self, request, pk=None):
        carpeta_cliente_pagos = CarpetaClientePagos.objects.get(id=pk)
        serializer = CarpetaClientePagosSerializer(instance=carpeta_cliente_pagos, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_202_ACCEPTED)
    
    def destroy(self, request, pk=None):
        carpeta_cliente_pagos = CarpetaClientePagos.objects.get(id=pk)
        carpeta_cliente_pagos.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

class CarpetaClienteContactosViewSet(viewsets.ModelViewSet):
    def list(self, request):
        carpeta_cliente_contactos = CarpetaClienteContactos.objects.all()
        serializer = CarpetaClienteContactosSerializer(carpeta_cliente_contactos, many=True)
        return Response(serializer.data)

    def create(self, request):
        serializer = CarpetaClienteContactosSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    
    def retrieve(self, request, pk=None):
        carpeta_cliente_contactos = CarpetaClienteContactos.objects.get(id=pk)
        serializer = CarpetaClienteContactosSerializer(carpeta_cliente_contactos, many=False)
        return Response(serializer.data)
    
    def update(self, request, pk=None):
        carpeta_cliente_contactos = CarpetaClienteContactos.objects.get(id=pk)
        serializer = CarpetaClienteContactosSerializer(instance=carpeta_cliente_contactos, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_202_ACCEPTED)
    
    def destroy(self, request, pk=None):
        carpeta_cliente_contactos = CarpetaClienteContactos.objects.get(id=pk)
        carpeta_cliente_contactos.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

class PersonalViewSet(viewsets.ModelViewSet):
    def list(self, request):
        personal = Personal.objects.all()
        serializer = PersonalSerializer(personal, many=True)
        return Response(serializer.data)

    def create(self, request):
        serializer = PersonalSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    
    def retrieve(self, request, pk=None):
        personal = Personal.objects.get(id=pk)
        serializer = PersonalSerializer(personal, many=False)
        return Response(serializer.data)
    
    def update(self, request, pk=None):
        personal = Personal.objects.get(id=pk)
        serializer = PersonalSerializer(instance=personal, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_202_ACCEPTED)
    
    def destroy(self, request, pk=None):
        personal = Personal.objects.get(id=pk)
        personal.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    
class EvaluadorViewSet(viewsets.ModelViewSet):
    def list(self, request):
        evaluador = Evaluador.objects.all()
        serializer = EvaluadorSerializer(evaluador, many=True)
        return Response(serializer.data)

    def create(self, request):
        serializer = EvaluadorSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    
    def retrieve(self, request, pk=None):
        evaluador = Evaluador.objects.get(id=pk)
        serializer = EvaluadorSerializer(evaluador, many=False)
        return Response(serializer.data)
    
    def update(self, request, pk=None):
        evaluador = Evaluador.objects.get(id=pk)
        serializer = EvaluadorSerializer(instance=evaluador, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_202_ACCEPTED)
    
    def destroy(self, request, pk=None):
        evaluador = Evaluador.objects.get(id=pk)
        evaluador.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    
class CarpetaLaboralViewSet(viewsets.ModelViewSet):
    def list(self, request):
        carpeta_laboral = CarpetaLaboral.objects.all()
        serializer = CarpetaLaboralSerializer(carpeta_laboral, many=True)
        return Response(serializer.data)

    def create(self, request):
        serializer = CarpetaLaboralSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    
    def retrieve(self, request, pk=None):
        carpeta_laboral = CarpetaLaboral.objects.get(id=pk)
        serializer = CarpetaLaboralSerializer(carpeta_laboral, many=False)
        return Response(serializer.data)
    
    def update(self, request, pk=None):
        carpeta_laboral = CarpetaLaboral.objects.get(id=pk)
        serializer = CarpetaLaboralSerializer(instance=carpeta_laboral, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_202_ACCEPTED)
    
    def destroy(self, request, pk=None):
        carpeta_laboral = CarpetaLaboral.objects.get(id=pk)
        carpeta_laboral.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    
class PuestoViewSet(viewsets.ModelViewSet):
    def list(self, request):
        puesto = Puesto.objects.all()
        serializer = PuestoSerializer(puesto, many=True)
        return Response(serializer.data)

    def create(self, request):
        serializer = PuestoSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    
    def retrieve(self, request, pk=None):
        puesto = Puesto.objects.get(id=pk)
        serializer = PuestoSerializer(puesto, many=False)
        return Response(serializer.data)
    
    def update(self, request, pk=None):
        puesto = Puesto.objects.get(id=pk)
        serializer = PuestoSerializer(instance=puesto, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_202_ACCEPTED)
    
    def destroy(self, request, pk=None):
        puesto = Puesto.objects.get(id=pk)
        puesto.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

class CarpetaGeneralesViewSet(viewsets.ModelViewSet):
    def list(self, request):
        carpeta_generales = CarpetaGenerales.objects.all()
        serializer = CarpetaGeneralesSerializer(carpeta_generales, many=True)
        return Response(serializer.data)

    def create(self, request):
        serializer = CarpetaGeneralesSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    
    def retrieve(self, request, pk=None):
        carpeta_generales = CarpetaGenerales.objects.get(id=pk)
        serializer = CarpetaGeneralesSerializer(carpeta_generales, many=False)
        return Response(serializer.data)
    
    def update(self, request, pk=None):
        carpeta_generales = CarpetaGenerales.objects.get(id=pk)
        serializer = CarpetaGeneralesSerializer(instance=carpeta_generales, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_202_ACCEPTED)
    
    def destroy(self, request, pk=None):
        carpeta_generales = CarpetaGenerales.objects.get(id=pk)
        carpeta_generales.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    
class CarpetaReferenciasViewSet(viewsets.ModelViewSet):
    def list(self, request):
        carpeta_referencias = CarpetaReferencias.objects.all()
        serializer = CarpetaReferenciasSerializer(carpeta_referencias, many=True)
        return Response(serializer.data)

    def create(self, request):
        serializer = CarpetaReferenciasSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    
    def retrieve(self, request, pk=None):
        carpeta_referencias = CarpetaReferencias.objects.get(id=pk)
        serializer = CarpetaReferenciasSerializer(carpeta_referencias, many=False)
        return Response(serializer.data)
    
    def update(self, request, pk=None):
        carpeta_referencias = CarpetaReferencias.objects.get(id=pk)
        serializer = CarpetaReferenciasSerializer(instance=carpeta_referencias, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_202_ACCEPTED)
    
    def destroy(self, request, pk=None):
        carpeta_referencias = CarpetaReferencias.objects.get(id=pk)
        carpeta_referencias.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    
class ReferenciaViewSet(viewsets.ModelViewSet):
    def list(self, request):
        referencia = Referencia.objects.all()
        serializer = ReferenciaSerializer(referencia, many=True)
        return Response(serializer.data)

    def create(self, request):
        serializer = ReferenciaSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    
    def retrieve(self, request, pk=None):
        referencia = Referencia.objects.get(id=pk)
        serializer = ReferenciaSerializer(referencia, many=False)
        return Response(serializer.data)
    
    def update(self, request, pk=None):
        referencia = Referencia.objects.get(id=pk)
        serializer = ReferenciaSerializer(instance=referencia, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_202_ACCEPTED)
    
    def destroy(self, request, pk=None):
        referencia = Referencia.objects.get(id=pk)
        referencia.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    
class CarpetaDependientesViewSet(viewsets.ModelViewSet):
    def list(self, request):
        carpeta_dependientes = CarpetaDependientes.objects.all()
        serializer = CarpetaDependientesSerializer(carpeta_dependientes, many=True)
        return Response(serializer.data)

    def create(self, request):
        serializer = CarpetaDependientesSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    
    def retrieve(self, request, pk=None):
        carpeta_dependientes = CarpetaDependientes.objects.get(id=pk)
        serializer = CarpetaDependientesSerializer(carpeta_dependientes, many=False)
        return Response(serializer.data)
    
    def update(self, request, pk=None):
        carpeta_dependientes = CarpetaDependientes.objects.get(id=pk)
        serializer = CarpetaDependientesSerializer(instance=carpeta_dependientes, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_202_ACCEPTED)
    
    def destroy(self, request, pk=None):
        carpeta_dependientes = CarpetaDependientes.objects.get(id=pk)
        carpeta_dependientes.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

class DependienteViewSet(viewsets.ModelViewSet):
    def list(self, request):
        dependiente = Dependiente.objects.all()
        serializer = DependienteSerializer(dependiente, many=True)
        return Response(serializer.data)

    def create(self, request):
        serializer = DependienteSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    
    def retrieve(self, request, pk=None):
        dependiente = Dependiente.objects.get(id=pk)
        serializer = DependienteSerializer(dependiente, many=False)
        return Response(serializer.data)
    
    def update(self, request, pk=None):
        dependiente = Dependiente.objects.get(id=pk)
        serializer = DependienteSerializer(instance=dependiente, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_202_ACCEPTED)
    
    def destroy(self, request, pk=None):
        dependiente = Dependiente.objects.get(id=pk)
        dependiente.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    
class CarpetaExamenPsicologicoViewSet(viewsets.ModelViewSet):
    def list(self, request):
        carpeta_examen_psicolologico = CarpetaExamenPsicologico.objects.all()
        serializer = CarpetaExamenPsicologicoSerializer(carpeta_examen_psicolologico, many=True)
        return Response(serializer.data)

    def create(self, request):
        serializer = CarpetaExamenPsicologicoSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    
    def retrieve(self, request, pk=None):
        carpeta_examen_psicolologico = CarpetaExamenPsicologico.objects.get(id=pk)
        serializer = CarpetaExamenPsicologicoSerializer(carpeta_examen_psicolologico, many=False)
        return Response(serializer.data)
    
    def update(self, request, pk=None):
        carpeta_examen_psicolologico = CarpetaExamenPsicologico.objects.get(id=pk)
        serializer = CarpetaExamenPsicologicoSerializer(instance=carpeta_examen_psicolologico, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_202_ACCEPTED)
    
    def destroy(self, request, pk=None):
        carpeta_examen_psicolologico = CarpetaExamenPsicologico.objects.get(id=pk)
        carpeta_examen_psicolologico.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

class CarpetaExamenToxicologicoViewSet(viewsets.ModelViewSet):
    def list(self, request):
        carpeta_examen_toxicologico = CarpetaExamenToxicologico.objects.all()
        serializer = CarpetaExamenToxicologicoSerializer(carpeta_examen_toxicologico, many=True)
        return Response(serializer.data)

    def create(self, request):
        serializer = CarpetaExamenToxicologicoSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    
    def retrieve(self, request, pk=None):
        carpeta_examen_toxicologico = CarpetaExamenToxicologico.objects.get(id=pk)
        serializer = CarpetaExamenToxicologicoSerializer(carpeta_examen_toxicologico, many=False)
        return Response(serializer.data)
    
    def update(self, request, pk=None):
        carpeta_examen_toxicologico = CarpetaExamenToxicologico.objects.get(id=pk)
        serializer = CarpetaExamenToxicologicoSerializer(instance=carpeta_examen_toxicologico, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_202_ACCEPTED)
    
    def destroy(self, request, pk=None):
        carpeta_examen_toxicologico = CarpetaExamenToxicologico.objects.get(id=pk)
        carpeta_examen_toxicologico.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    
class CarpetaExamenMedicoViewSet(viewsets.ModelViewSet):
    def list(self, request):
        carpeta_examen_medico = CarpetaExamenMedico.objects.all()
        serializer = CarpetaExamenMedicoSerializer(carpeta_examen_medico, many=True)
        return Response(serializer.data)

    def create(self, request):
        serializer = CarpetaExamenMedicoSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    
    def retrieve(self, request, pk=None):
        carpeta_examen_medico = CarpetaExamenMedico.objects.get(id=pk)
        serializer = CarpetaExamenMedicoSerializer(carpeta_examen_medico, many=False)
        return Response(serializer.data)
    
    def update(self, request, pk=None):
        carpeta_examen_medico = CarpetaExamenMedico.objects.get(id=pk)
        serializer = CarpetaExamenMedicoSerializer(instance=carpeta_examen_medico, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_202_ACCEPTED)
    
    def destroy(self, request, pk=None):
        carpeta_examen_medico = CarpetaExamenMedico.objects.get(id=pk)
        carpeta_examen_medico.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

class CarpetaExamenFisicoViewSet(viewsets.ModelViewSet):
    def list(self, request):
        carpeta_examen_fisico = CarpetaExamenFisico.objects.all()
        serializer = CarpetaExamenFisicoSerializer(carpeta_examen_fisico, many=True)
        return Response(serializer.data)

    def create(self, request):
        serializer = CarpetaExamenFisicoSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    
    def retrieve(self, request, pk=None):
        carpeta_examen_fisico = CarpetaExamenFisico.objects.get(id=pk)
        serializer = CarpetaExamenFisicoSerializer(carpeta_examen_fisico, many=False)
        return Response(serializer.data)
    
    def update(self, request, pk=None):
        carpeta_examen_fisico = CarpetaExamenFisico.objects.get(id=pk)
        serializer = CarpetaExamenFisicoSerializer(instance=carpeta_examen_fisico, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_202_ACCEPTED)
    
    def destroy(self, request, pk=None):
        carpeta_examen_fisico = CarpetaExamenFisico.objects.get(id=pk)
        carpeta_examen_fisico.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    
class CarpetaExamenSocioeconomicoViewSet(viewsets.ModelViewSet):
    def list(self, request):
        carpeta_examen_socioeconomico = CarpetaExamenSocioeconomico.objects.all()
        serializer = CarpetaExamenSocioeconomicoSerializer(carpeta_examen_socioeconomico, many=True)
        return Response(serializer.data)

    def create(self, request):
        serializer = CarpetaExamenSocioeconomicoSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    
    def retrieve(self, request, pk=None):
        carpeta_examen_socioeconomico = CarpetaExamenSocioeconomico.objects.get(id=pk)
        serializer = CarpetaExamenSocioeconomicoSerializer(carpeta_examen_socioeconomico, many=False)
        return Response(serializer.data)
    
    def update(self, request, pk=None):
        carpeta_examen_socioeconomico = CarpetaExamenSocioeconomico.objects.get(id=pk)
        serializer = CarpetaExamenSocioeconomicoSerializer(instance=carpeta_examen_socioeconomico, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_202_ACCEPTED)
    
    def destroy(self, request, pk=None):
        carpeta_examen_socioeconomico = CarpetaExamenSocioeconomico.objects.get(id=pk)
        carpeta_examen_socioeconomico.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

class CarpetaExamenPoligrafoViewSet(viewsets.ModelViewSet):
    def list(self, request):
        carpeta_examen_poligrafo = CarpetaExamenPoligrafo.objects.all()
        serializer = CarpetaExamenPoligrafoSerializer(carpeta_examen_poligrafo, many=True)
        return Response(serializer.data)

    def create(self, request):
        serializer = CarpetaExamenPoligrafoSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    
    def retrieve(self, request, pk=None):
        carpeta_examen_poligrafo = CarpetaExamenPoligrafo.objects.get(id=pk)
        serializer = CarpetaExamenPoligrafoSerializer(carpeta_examen_poligrafo, many=False)
        return Response(serializer.data)
    
    def update(self, request, pk=None):
        carpeta_examen_poligrafo = CarpetaExamenPoligrafo.objects.get(id=pk)
        serializer = CarpetaExamenPoligrafoSerializer(instance=carpeta_examen_poligrafo, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_202_ACCEPTED)
    
    def destroy(self, request, pk=None):
        carpeta_examen_poligrafo = CarpetaExamenPoligrafo.objects.get(id=pk)
        carpeta_examen_poligrafo.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    
class CarpetaEmpleoAnteriorSeguridadPublicaViewSet(viewsets.ModelViewSet):
    def list(self, request):
        carpeta_empleo_anterior_seguridad_publica = CarpetaEmpleoAnteriorSeguridadPublica.objects.all()
        serializer = CarpetaEmpleoAnteriorSeguridadPublicaSerializer(carpeta_empleo_anterior_seguridad_publica, many=True)
        return Response(serializer.data)

    def create(self, request):
        serializer = CarpetaEmpleoAnteriorSeguridadPublicaSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    
    def retrieve(self, request, pk=None):
        carpeta_empleo_anterior_seguridad_publica = CarpetaEmpleoAnteriorSeguridadPublica.objects.get(id=pk)
        serializer = CarpetaEmpleoAnteriorSeguridadPublicaSerializer(carpeta_empleo_anterior_seguridad_publica, many=False)
        return Response(serializer.data)
    
    def update(self, request, pk=None):
        carpeta_empleo_anterior_seguridad_publica = CarpetaEmpleoAnteriorSeguridadPublica.objects.get(id=pk)
        serializer = CarpetaEmpleoAnteriorSeguridadPublicaSerializer(instance=carpeta_empleo_anterior_seguridad_publica, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_202_ACCEPTED)
    
    def destroy(self, request, pk=None):
        carpeta_empleo_anterior_seguridad_publica = CarpetaEmpleoAnteriorSeguridadPublica.objects.get(id=pk)
        carpeta_empleo_anterior_seguridad_publica.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    
class EmpleoAnteriorSeguridadPublicaViewSet(viewsets.ModelViewSet):
    def list(self, request):
        empleo_anterior_seguridad_publica = EmpleoAnteriorSeguridadPublica.objects.all()
        serializer = EmpleoAnteriorSeguridadPublicaSerializer(empleo_anterior_seguridad_publica, many=True)
        return Response(serializer.data)

    def create(self, request):
        serializer = EmpleoAnteriorSeguridadPublicaSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    
    def retrieve(self, request, pk=None):
        empleo_anterior_seguridad_publica = EmpleoAnteriorSeguridadPublica.objects.get(id=pk)
        serializer = EmpleoAnteriorSeguridadPublicaSerializer(empleo_anterior_seguridad_publica, many=False)
        return Response(serializer.data)
    
    def update(self, request, pk=None):
        empleo_anterior_seguridad_publica = EmpleoAnteriorSeguridadPublica.objects.get(id=pk)
        serializer = EmpleoAnteriorSeguridadPublicaSerializer(instance=empleo_anterior_seguridad_publica, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_202_ACCEPTED)
    
    def destroy(self, request, pk=None):
        empleo_anterior_seguridad_publica = EmpleoAnteriorSeguridadPublica.objects.get(id=pk)
        empleo_anterior_seguridad_publica.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    
class PuestoFuncionalViewSet(viewsets.ModelViewSet):
    def list(self, request):
        puesto_funcional = PuestoFuncional.objects.all()
        serializer = PuestoFuncionalSerializer(puesto_funcional, many=True)
        return Response(serializer.data)

    def create(self, request):
        serializer = PuestoFuncionalSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    
    def retrieve(self, request, pk=None):
        puesto_funcional = PuestoFuncional.objects.get(id=pk)
        serializer = PuestoFuncionalSerializer(puesto_funcional, many=False)
        return Response(serializer.data)
    
    def update(self, request, pk=None):
        puesto_funcional = PuestoFuncional.objects.get(id=pk)
        serializer = PuestoFuncionalSerializer(instance=puesto_funcional, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_202_ACCEPTED)
    
    def destroy(self, request, pk=None):
        puesto_funcional = PuestoFuncional.objects.get(id=pk)
        puesto_funcional.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

class TipoBajaViewSet(viewsets.ModelViewSet):
    def list(self, request):
        tipo_baja = TipoBaja.objects.all()
        serializer = TipoBajaSerializer(tipo_baja, many=True)
        return Response(serializer.data)

    def create(self, request):
        serializer = TipoBajaSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    
    def retrieve(self, request, pk=None):
        tipo_baja = TipoBaja.objects.get(id=pk)
        serializer = TipoBajaSerializer(tipo_baja, many=False)
        return Response(serializer.data)
    
    def update(self, request, pk=None):
        tipo_baja = TipoBaja.objects.get(id=pk)
        serializer = TipoBajaSerializer(instance=tipo_baja, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_202_ACCEPTED)
    
    def destroy(self, request, pk=None):
        tipo_baja = TipoBaja.objects.get(id=pk)
        tipo_baja.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

class CarpetaEmpleoAnteriorViewSet(viewsets.ModelViewSet):
    def list(self, request):
        carpeta_empleo_anterior = CarpetaEmpleoAnterior.objects.all()
        serializer = CarpetaEmpleoAnteriorSerializer(carpeta_empleo_anterior, many=True)
        return Response(serializer.data)

    def create(self, request):
        serializer = CarpetaEmpleoAnteriorSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    
    def retrieve(self, request, pk=None):
        carpeta_empleo_anterior = CarpetaEmpleoAnterior.objects.get(id=pk)
        serializer = CarpetaEmpleoAnteriorSerializer(carpeta_empleo_anterior, many=False)
        return Response(serializer.data)
    
    def update(self, request, pk=None):
        carpeta_empleo_anterior = CarpetaEmpleoAnterior.objects.get(id=pk)
        serializer = CarpetaEmpleoAnteriorSerializer(instance=carpeta_empleo_anterior, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_202_ACCEPTED)
    
    def destroy(self, request, pk=None):
        carpeta_empleo_anterior = CarpetaEmpleoAnterior.objects.get(id=pk)
        carpeta_empleo_anterior.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    
class EmpleoAnteriorViewSet(viewsets.ModelViewSet):
    def list(self, request):
        empleo_anterior = EmpleoAnterior.objects.all()
        serializer = EmpleoAnteriorSerializer(empleo_anterior, many=True)
        return Response(serializer.data)

    def create(self, request):
        serializer = EmpleoAnteriorSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    
    def retrieve(self, request, pk=None):
        empleo_anterior = EmpleoAnterior.objects.get(id=pk)
        serializer = EmpleoAnteriorSerializer(empleo_anterior, many=False)
        return Response(serializer.data)
    
    def update(self, request, pk=None):
        empleo_anterior = EmpleoAnterior.objects.get(id=pk)
        serializer = EmpleoAnteriorSerializer(instance=empleo_anterior, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_202_ACCEPTED)
    
    def destroy(self, request, pk=None):
        empleo_anterior = EmpleoAnterior.objects.get(id=pk)
        empleo_anterior.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    
class MotivoSeparacionViewSet(viewsets.ModelViewSet):
    def list(self, request):
        motivo_separacion = MotivoSeparacion.objects.all()
        serializer = MotivoSeparacionSerializer(motivo_separacion, many=True)
        return Response(serializer.data)

    def create(self, request):
        serializer = MotivoSeparacionSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    
    def retrieve(self, request, pk=None):
        motivo_separacion = MotivoSeparacion.objects.get(id=pk)
        serializer = MotivoSeparacionSerializer(motivo_separacion, many=False)
        return Response(serializer.data)
    
    def update(self, request, pk=None):
        motivo_separacion = MotivoSeparacion.objects.get(id=pk)
        serializer = MotivoSeparacionSerializer(instance=motivo_separacion, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_202_ACCEPTED)
    
    def destroy(self, request, pk=None):
        motivo_separacion = MotivoSeparacion.objects.get(id=pk)
        motivo_separacion.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

class CarpetaCapacitacionViewSet(viewsets.ModelViewSet):
    def list(self, request):
        carpeta_capacitacion = CarpetaCapacitacion.objects.all()
        serializer = CarpetaCapacitacionSerializer(carpeta_capacitacion, many=True)
        return Response(serializer.data)

    def create(self, request):
        serializer = CarpetaCapacitacionSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    
    def retrieve(self, request, pk=None):
        carpeta_capacitacion = CarpetaCapacitacion.objects.get(id=pk)
        serializer = CarpetaCapacitacionSerializer(carpeta_capacitacion, many=False)
        return Response(serializer.data)
    
    def update(self, request, pk=None):
        carpeta_capacitacion = CarpetaCapacitacion.objects.get(id=pk)
        serializer = CarpetaCapacitacionSerializer(instance=carpeta_capacitacion, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_202_ACCEPTED)
    
    def destroy(self, request, pk=None):
        carpeta_capacitacion = CarpetaCapacitacion.objects.get(id=pk)
        carpeta_capacitacion.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    
class CapacitacionPreviaViewSet(viewsets.ModelViewSet):
    def list(self, request):
        capacitacion_previa = CapacitacionPrevia.objects.all()
        serializer = CapacitacionPreviaSerializer(capacitacion_previa, many=True)
        return Response(serializer.data)

    def create(self, request):
        serializer = CapacitacionPreviaSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    
    def retrieve(self, request, pk=None):
        capacitacion_previa = CapacitacionPrevia.objects.get(id=pk)
        serializer = CapacitacionPreviaSerializer(capacitacion_previa, many=False)
        return Response(serializer.data)
    
    def update(self, request, pk=None):
        capacitacion_previa = CapacitacionPrevia.objects.get(id=pk)
        serializer = CapacitacionPreviaSerializer(instance=capacitacion_previa, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_202_ACCEPTED)
    
    def destroy(self, request, pk=None):
        capacitacion_previa = CapacitacionPrevia.objects.get(id=pk)
        capacitacion_previa.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    
class TipoCursoViewSet(viewsets.ModelViewSet):
    def list(self, request):
        tipo_curso = TipoCurso.objects.all()
        serializer = TipoCursoSerializer(tipo_curso, many=True)
        return Response(serializer.data)

    def create(self, request):
        serializer = TipoCursoSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    
    def retrieve(self, request, pk=None):
        tipo_curso = TipoCurso.objects.get(id=pk)
        serializer = TipoCursoSerializer(tipo_curso, many=False)
        return Response(serializer.data)
    
    def update(self, request, pk=None):
        tipo_curso = TipoCurso.objects.get(id=pk)
        serializer = TipoCursoSerializer(instance=tipo_curso, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_202_ACCEPTED)
    
    def destroy(self, request, pk=None):
        tipo_curso = TipoCurso.objects.get(id=pk)
        tipo_curso.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    
class CapacitacionEnCursoViewSet(viewsets.ModelViewSet):
    def list(self, request):
        capacitacion_en_curso = CapacitacionEnCurso.objects.all()
        serializer = CapacitacionEnCursoSerializer(capacitacion_en_curso, many=True)
        return Response(serializer.data)

    def create(self, request):
        serializer = CapacitacionEnCursoSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    
    def retrieve(self, request, pk=None):
        capacitacion_en_curso = CapacitacionEnCurso.objects.get(id=pk)
        serializer = CapacitacionEnCursoSerializer(capacitacion_en_curso, many=False)
        return Response(serializer.data)
    
    def update(self, request, pk=None):
        capacitacion_en_curso = CapacitacionEnCurso.objects.get(id=pk)
        serializer = CapacitacionEnCursoSerializer(instance=capacitacion_en_curso, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_202_ACCEPTED)
    
    def destroy(self, request, pk=None):
        capacitacion_en_curso = CapacitacionEnCurso.objects.get(id=pk)
        capacitacion_en_curso.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    
class IdiomaViewSet(viewsets.ModelViewSet):
    def list(self, request):
        idioma = Idioma.objects.all()
        serializer = IdiomaSerializer(idioma, many=True)
        return Response(serializer.data)

    def create(self, request):
        serializer = IdiomaSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    
    def retrieve(self, request, pk=None):
        idioma = Idioma.objects.get(id=pk)
        serializer = IdiomaSerializer(idioma, many=False)
        return Response(serializer.data)
    
    def update(self, request, pk=None):
        idioma = Idioma.objects.get(id=pk)
        serializer = IdiomaSerializer(instance=idioma, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_202_ACCEPTED)
    
    def destroy(self, request, pk=None):
        idioma = Idioma.objects.get(id=pk)
        idioma.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

class HabilidadViewSet(viewsets.ModelViewSet):
    def list(self, request):
        habilidad = Habilidad.objects.all()
        serializer = HabilidadSerializer(habilidad, many=True)
        return Response(serializer.data)

    def create(self, request):
        serializer = HabilidadSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    
    def retrieve(self, request, pk=None):
        habilidad = Habilidad.objects.get(id=pk)
        serializer = HabilidadSerializer(habilidad, many=False)
        return Response(serializer.data)
    
    def update(self, request, pk=None):
        habilidad = Habilidad.objects.get(id=pk)
        serializer = HabilidadSerializer(instance=habilidad, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_202_ACCEPTED)
    
    def destroy(self, request, pk=None):
        habilidad = Habilidad.objects.get(id=pk)
        habilidad.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    
class HabilidadPersonalizadaViewSet(viewsets.ModelViewSet):
    def list(self, request):
        habilidad_personalizada = HabilidadPersonalizada.objects.all()
        serializer = HabilidadPersonalizadaSerializer(habilidad_personalizada, many=True)
        return Response(serializer.data)

    def create(self, request):
        serializer = HabilidadPersonalizadaSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    
    def retrieve(self, request, pk=None):
        habilidad_personalizada = HabilidadPersonalizada.objects.get(id=pk)
        serializer = HabilidadPersonalizadaSerializer(habilidad_personalizada, many=False)
        return Response(serializer.data)
    
    def update(self, request, pk=None):
        habilidad_personalizada = HabilidadPersonalizada.objects.get(id=pk)
        serializer = HabilidadPersonalizadaSerializer(instance=habilidad_personalizada, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_202_ACCEPTED)
    
    def destroy(self, request, pk=None):
        habilidad_personalizada = HabilidadPersonalizada.objects.get(id=pk)
        habilidad_personalizada.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

class CarpetaMediaFiliacionViewSet(viewsets.ModelViewSet):
    def list(self, request):
        carpeta_media_filicacion = CarpetaMediaFiliacion.objects.all()
        serializer = CarpetaMediaFiliacionSerializer(carpeta_media_filicacion, many=True)
        return Response(serializer.data)

    def create(self, request):
        serializer = CarpetaMediaFiliacionSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    
    def retrieve(self, request, pk=None):
        carpeta_media_filicacion = CarpetaMediaFiliacion.objects.get(id=pk)
        serializer = CarpetaMediaFiliacionSerializer(carpeta_media_filicacion, many=False)
        return Response(serializer.data)
    
    def update(self, request, pk=None):
        carpeta_media_filicacion = CarpetaMediaFiliacion.objects.get(id=pk)
        serializer = CarpetaMediaFiliacionSerializer(instance=carpeta_media_filicacion, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_202_ACCEPTED)
    
    def destroy(self, request, pk=None):
        carpeta_media_filicacion = CarpetaMediaFiliacion.objects.get(id=pk)
        carpeta_media_filicacion.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

class DocumentosDigitalesViewSet(viewsets.ModelViewSet):
    def list(self, request):
        documentos_digitales = DocumentosDigitales.objects.all()
        serializer = DocumentosDigitalesSerializer(documentos_digitales, many=True)
        return Response(serializer.data)

    def create(self, request):
        serializer = DocumentosDigitalesSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    
    def retrieve(self, request, pk=None):
        documentos_digitales = DocumentosDigitales.objects.get(id=pk)
        serializer = DocumentosDigitalesSerializer(documentos_digitales, many=False)
        return Response(serializer.data)
    
    def update(self, request, pk=None):
        documentos_digitales = DocumentosDigitales.objects.get(id=pk)
        serializer = DocumentosDigitalesSerializer(instance=documentos_digitales, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_202_ACCEPTED)
    
    def destroy(self, request, pk=None):
        documentos_digitales = DocumentosDigitales.objects.get(id=pk)
        documentos_digitales.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

class CapacitacionClienteViewSet(viewsets.ModelViewSet):
    def list(self, request):
        capacitacion_cliente = CapacitacionCliente.objects.all()
        serializer = CapacitacionClienteSerializer(capacitacion_cliente, many=True)
        return Response(serializer.data)

    def create(self, request):
        serializer = CapacitacionClienteSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    
    def retrieve(self, request, pk=None):
        capacitacion_cliente = CapacitacionCliente.objects.get(id=pk)
        serializer = CapacitacionClienteSerializer(capacitacion_cliente, many=False)
        return Response(serializer.data)
    
    def update(self, request, pk=None):
        capacitacion_cliente = CapacitacionCliente.objects.get(id=pk)
        serializer = CapacitacionClienteSerializer(instance=capacitacion_cliente, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_202_ACCEPTED)
    
    def destroy(self, request, pk=None):
        capacitacion_cliente = CapacitacionCliente.objects.get(id=pk)
        capacitacion_cliente.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

class PersonalPorCapacitarViewSet(viewsets.ModelViewSet):
    def list(self, request):
        personal_por_capacitar = PersonalPorCapacitar.objects.all()
        serializer = PersonalPorCapacitarSerializer(personal_por_capacitar, many=True)
        return Response(serializer.data)

    def create(self, request):
        serializer = PersonalPorCapacitarSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    
    def retrieve(self, request, pk=None):
        personal_por_capacitar = PersonalPorCapacitar.objects.get(id=pk)
        serializer = PersonalPorCapacitarSerializer(personal_por_capacitar, many=False)
        return Response(serializer.data)
    
    def update(self, request, pk=None):
        personal_por_capacitar = PersonalPorCapacitar.objects.get(id=pk)
        serializer = PersonalPorCapacitarSerializer(instance=personal_por_capacitar, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_202_ACCEPTED)
    
    def destroy(self, request, pk=None):
        personal_por_capacitar = PersonalPorCapacitar.objects.get(id=pk)
        personal_por_capacitar.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    
class DomicilioViewSet(viewsets.ModelViewSet):
    def list(self, request):
        domicilio = Domicilio.objects.all()
        serializer = DomicilioSerializer(domicilio, many=True)
        return Response(serializer.data)

    def create(self, request):
        serializer = DomicilioSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    
    def retrieve(self, request, pk=None):
        domicilio = Domicilio.objects.get(id=pk)
        serializer = DomicilioSerializer(domicilio, many=False)
        return Response(serializer.data)
    
    def update(self, request, pk=None):
        domicilio = Domicilio.objects.get(id=pk)
        serializer = DomicilioSerializer(instance=domicilio, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_202_ACCEPTED)
    
    def destroy(self, request, pk=None):
        domicilio = Domicilio.objects.get(id=pk)
        domicilio.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

class CodigoPostalViewSet(viewsets.ModelViewSet):
    def list(self, request):
        codigo_postal = CodigoPostal.objects.all()
        serializer = CodigoPostalSerializer(codigo_postal, many=True)
        return Response(serializer.data)

    def create(self, request):
        serializer = CodigoPostalSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    
    def retrieve(self, request, pk=None):
        codigo_postal = CodigoPostal.objects.get(id=pk)
        serializer = CodigoPostalSerializer(codigo_postal, many=False)
        return Response(serializer.data)
    
    def update(self, request, pk=None):
        codigo_postal = CodigoPostal.objects.get(id=pk)
        serializer = CodigoPostalSerializer(instance=codigo_postal, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_202_ACCEPTED)
    
    def destroy(self, request, pk=None):
        codigo_postal = CodigoPostal.objects.get(id=pk)
        codigo_postal.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

class ColoniaViewSet(viewsets.ModelViewSet):
    def list(self, request):
        colonia = Colonia.objects.all()
        serializer = ColoniaSerializer(colonia, many=True)
        return Response(serializer.data)

    def create(self, request):
        serializer = ColoniaSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    
    def retrieve(self, request, pk=None):
        colonia = Colonia.objects.get(id=pk)
        serializer = ColoniaSerializer(colonia, many=False)
        return Response(serializer.data)
    
    def update(self, request, pk=None):
        colonia = Colonia.objects.get(id=pk)
        serializer = ColoniaSerializer(instance=colonia, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_202_ACCEPTED)
    
    def destroy(self, request, pk=None):
        colonia = Colonia.objects.get(id=pk)
        colonia.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

class MunicipioViewSet(viewsets.ModelViewSet):
    def list(self, request):
        municipio = Municipio.objects.all()
        serializer = MunicipioSerializer(municipio, many=True)
        return Response(serializer.data)

    def create(self, request):
        serializer = MunicipioSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    
    def retrieve(self, request, pk=None):
        municipio = Municipio.objects.get(id=pk)
        serializer = MunicipioSerializer(municipio, many=False)
        return Response(serializer.data)
    
    def update(self, request, pk=None):
        municipio = Municipio.objects.get(id=pk)
        serializer = MunicipioSerializer(instance=municipio, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_202_ACCEPTED)
    
    def destroy(self, request, pk=None):
        municipio = Municipio.objects.get(id=pk)
        municipio.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

class EstadoViewSet(viewsets.ModelViewSet):
    def list(self, request):
        estado = Estado.objects.all()
        serializer = EstadoSerializer(estado, many=True)
        return Response(serializer.data)

    def create(self, request):
        serializer = EstadoSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    
    def retrieve(self, request, pk=None):
        estado = Estado.objects.get(id=pk)
        serializer = EstadoSerializer(estado, many=False)
        return Response(serializer.data)
    
    def update(self, request, pk=None):
        estado = Estado.objects.get(id=pk)
        serializer = EstadoSerializer(instance=estado, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_202_ACCEPTED)
    
    def destroy(self, request, pk=None):
        estado = Estado.objects.get(id=pk)
        estado.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

class PaisViewSet(viewsets.ModelViewSet):
    def list(self, request):
        pais = Pais.objects.all()
        serializer = PaisSerializer(pais, many=True)
        return Response(serializer.data)

    def create(self, request):
        serializer = PaisSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    
    def retrieve(self, request, pk=None):
        pais = Pais.objects.get(id=pk)
        serializer = PaisSerializer(pais, many=False)
        return Response(serializer.data)
    
    def update(self, request, pk=None):
        pais = Pais.objects.get(id=pk)
        serializer = PaisSerializer(instance=pais, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_202_ACCEPTED)
    
    def destroy(self, request, pk=None):
        pais = Pais.objects.get(id=pk)
        pais.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)