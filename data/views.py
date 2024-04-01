from django.http import HttpResponse
import csv
from data.models import (
    Cliente, Sede, DocumentosCliente, CarpetaClienteGenerales, CarpetaClientePagos, CarpetaClienteContactos, PaqueteCapacitacion, Personal, CodigoPostal, Curp, Rfc, Evaluador, Ocupacion, CarpetaLaboral, CarpetaGenerales, CarpetaDependientes,
    Dependiente, CarpetaExamenPsicologico, CarpetaExamenToxicologico, JefeMedico, MedicoOdontologico, CarpetaExamenMedico, CarpetaExamenFisico, CarpetaExamenSocioeconomico, EstructuraFamiliar, DatosFamiliar, Referencia, CarpetaExamenPoligrafo,
    MotivoSeparacion, PuestoFuncional, TipoBaja, EmpleoAnteriorSeguridadPublica, EmpleoAnterior, Instructor, Capacitacion, RepresentanteTrabajadores, Domicilio, Idioma, CarpetaMediaFiliacion, Resultado, DocumentosDigitales
)

MODELS = [
    Cliente, Sede, DocumentosCliente, CarpetaClienteGenerales, CarpetaClientePagos, CarpetaClienteContactos, PaqueteCapacitacion, Personal, CodigoPostal, Curp, Rfc, Evaluador, Ocupacion, CarpetaLaboral, CarpetaGenerales, CarpetaDependientes,
    Dependiente, CarpetaExamenPsicologico, CarpetaExamenToxicologico, JefeMedico, MedicoOdontologico, CarpetaExamenMedico, CarpetaExamenFisico, CarpetaExamenSocioeconomico, EstructuraFamiliar, DatosFamiliar, Referencia, CarpetaExamenPoligrafo,
    MotivoSeparacion, PuestoFuncional, TipoBaja, EmpleoAnteriorSeguridadPublica, EmpleoAnterior, Instructor, Capacitacion, RepresentanteTrabajadores, Domicilio, Idioma, CarpetaMediaFiliacion, Resultado, DocumentosDigitales
]


def download_csv_template(request):
    # Crea la respuesta HTTP
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="template.csv"'

    # Escribe los encabezados del CSV en la respuesta
    writer = csv.writer(response)
    csv_fields = []
    for model in MODELS:
        # Excluye el campo 'id'
        fields = [field.name for field in model._meta.fields if field.name != 'id']
        csv_fields.extend([f"{model.__name__}_{field.replace('_', '')}" for field in fields])
    writer.writerow(csv_fields)
    return response
