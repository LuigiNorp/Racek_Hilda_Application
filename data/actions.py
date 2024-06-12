from django.http import (
    HttpRequest,
    HttpResponse
)
from main.views import (
    GenerateDC3View,
    GenerateOdontologicView,
    GenerateFingerprintRecordView,
    GenerateCdmxLicenseView,
    GenerateEdomexLicenseView,
    GenerateFederalLicenseView,
    GenerateConsentFormView,
    GenerateTrainingCertificateView,
    GenerateCdmxTestsView,
    GenerateFederalTestsView,
    GenerateSocioeconomicPhotosView,
    GenerateIshiharaTestView,
    GenerateHonestyTestView,
    GeneratePolygraphTestView,
    GenerateGchPreliminaryView,
    GeneratePsychologicalView,
    GenerateCandidateView,
    GenerateSocioeconomicReportView,
    GenerateSocialWorkReportView,
    GenerateSedenaView,
)


def generate_dc3_report(self, request, queryset):
    # Extract the IDs of selected Personal objects
    personal_ids = queryset.values_list('id', flat=True)

    try:
        # Create an instance of GenerateDC3View and call its get method
        generate_dc3_view = GenerateDC3View()
        request = HttpRequest()  # Create a dummy request

        # Call the get method of GenerateDC3View with personal_ids
        response = generate_dc3_view.get(request, personal_ids, queryset)

        # Return the response directly to serve the PDF to the user
        if isinstance(response, HttpResponse):
            return response

    except Exception as e:
        # Handle the case when an exception occurs (e.g., display an error message)
        error_message = f"Falló en generar el DC-3: {str(e)}"
        return HttpResponse(error_message)


def generate_odontologic_report(self, request, queryset):
    # Extract the IDs of selected Personal objects
    personal_ids = queryset.values_list('id', flat=True)

    try:
        # Create an instance of GenerateDC3View and call its get method
        generate_odontologic_view = GenerateOdontologicView()
        request = HttpRequest()  # Create a dummy request

        # Call the get method of GenerateDC3View with personal_ids
        response = generate_odontologic_view.get(request, personal_ids, queryset)

        # Return the response directly to serve the PDF to the user
        if isinstance(response, HttpResponse):
            return response

    except Exception as e:
        # Handle the case when an exception occurs (e.g., display an error message)
        error_message = f"Falló en generar el reporte Odontológico: {str(e)}"
        return HttpResponse(error_message)


def generate_fingerprint_record_report(self, request, queryset):
    # Extract the IDs of selected Personal objects
    personal_ids = queryset.values_list('id', flat=True)

    try:
        # Create an instance of GenerateDC3View and call its get method
        generate_fingerprint_record_view = GenerateFingerprintRecordView()
        request = HttpRequest()  # Create a dummy request

        # Call the get method of GenerateDC3View with personal_ids
        response = generate_fingerprint_record_view.get(request, personal_ids, queryset)

        # Return the response directly to serve the PDF to the user
        if isinstance(response, HttpResponse):
            return response

    except Exception as e:
        # Handle the case when an exception occurs (e.g., display an error message)
        error_message = f"Falló en generar la Ficha Decadactilar: {str(e)}"
        return HttpResponse(error_message)


def generate_cdmx_license_report(self, request, queryset):
    # Extract the IDs of selected Personal objects
    personal_ids = queryset.values_list('id', flat=True)

    try:
        # Create an instance of GenerateDC3View and call its get method
        generate_cdmx_license_view = GenerateCdmxLicenseView()
        request = HttpRequest()  # Create a dummy request

        # Call the get method of GenerateDC3View with personal_ids
        response = generate_cdmx_license_view.get(request, personal_ids, queryset)

        # Return the response directly to serve the PDF to the user
        if isinstance(response, HttpResponse):
            return response

    except Exception as e:
        # Handle the case when an exception occurs (e.g., display an error message)
        error_message = f"Falló en generar la Cédula CDMX: {str(e)}"
        return HttpResponse(error_message)


def generate_edomex_license_report(self, request, queryset):
    # Extract the IDs of selected Personal objects
    personal_ids = queryset.values_list('id', flat=True)

    try:
        # Create an instance of GenerateDC3View and call its get method
        generate_edomex_license_view = GenerateEdomexLicenseView()
        request = HttpRequest()  # Create a dummy request

        # Call the get method of GenerateDC3View with personal_ids
        response = generate_edomex_license_view.get(request, personal_ids, queryset)

        # Return the response directly to serve the PDF to the user
        if isinstance(response, HttpResponse):
            return response

    except Exception as e:
        # Handle the case when an exception occurs (e.g., display an error message)
        error_message = f"Falló en generar la Cédula Edomex: {str(e)}"
        return HttpResponse(error_message)


def generate_federal_license_report(self, request, queryset):
    # Extract the IDs of selected Personal objects
    personal_ids = queryset.values_list('id', flat=True)

    try:
        # Create an instance of GenerateDC3View and call its get method
        generate_federal_license_view = GenerateFederalLicenseView()
        request = HttpRequest()  # Create a dummy request

        # Call the get method of GenerateDC3View with personal_ids
        response = generate_federal_license_view.get(request, personal_ids, queryset)

        # Return the response directly to serve the PDF to the user
        if isinstance(response, HttpResponse):
            return response

    except Exception as e:
        # Handle the case when an exception occurs (e.g., display an error message)
        error_message = f"Falló en generar la Cédula Federal: {str(e)}"
        return HttpResponse(error_message)


def generate_consent_form_report(self, request, queryset):
    # Extract the IDs of selected Personal objects
    personal_ids = queryset.values_list('id', flat=True)

    try:
        # Create an instance of GenerateDC3View and call its get method
        generate_consent_form_view = GenerateConsentFormView()
        request = HttpRequest()  # Create a dummy request

        # Call the get method of GenerateDC3View with personal_ids
        response = generate_consent_form_view.get(request, personal_ids, queryset)

        # Return the response directly to serve the PDF to the user
        if isinstance(response, HttpResponse):
            return response

    except Exception as e:
        # Handle the case when an exception occurs (e.g., display an error message)
        error_message = f"Falló en generar el Acta de Consentimiento: {str(e)}"
        return HttpResponse(error_message)


def generate_training_certificate_report(self, request, queryset):
    # Extract the IDs of selected Personal objects
    personal_ids = queryset.values_list('id', flat=True)

    try:
        # Create an instance of GenerateDC3View and call its get method
        generate_training_certificate_view = GenerateTrainingCertificateView()
        request = HttpRequest()  # Create a dummy request

        # Call the get method of GenerateDC3View with personal_ids
        response = generate_training_certificate_view.get(request, personal_ids, queryset)

        # Return the response directly to serve the PDF to the user
        if isinstance(response, HttpResponse):
            return response

    except Exception as e:
        # Handle the case when an exception occurs (e.g., display an error message)
        error_message = f"Falló en generar la Constancia de Capacitación: {str(e)}"
        return HttpResponse(error_message)


def generate_cdmx_tests_report(self, request, queryset):
    # Extract the IDs of selected Personal objects
    personal_ids = queryset.values_list('id', flat=True)

    try:
        # Create an instance of GenerateDC3View and call its get method
        generate_cdmx_test_view = GenerateCdmxTestsView()
        request = HttpRequest()  # Create a dummy request

        # Call the get method of GenerateDC3View with personal_ids
        response = generate_cdmx_test_view.get(request, personal_ids, queryset)

        # Return the response directly to serve the PDF to the user
        if isinstance(response, HttpResponse):
            return response

    except Exception as e:
        # Handle the case when an exception occurs (e.g., display an error message)
        error_message = f"Falló en generar el reporte de Examen CDMX: {str(e)}"
        return HttpResponse(error_message)


def generate_federal_tests_report(self, request, queryset):
    # Extract the IDs of selected Personal objects
    personal_ids = queryset.values_list('id', flat=True)

    try:
        # Create an instance of GenerateDC3View and call its get method
        generate_federal_tests_view = GenerateFederalTestsView()
        request = HttpRequest()  # Create a dummy request

        # Call the get method of GenerateDC3View with personal_ids
        response = generate_federal_tests_view.get(request, personal_ids, queryset)

        # Return the response directly to serve the PDF to the user
        if isinstance(response, HttpResponse):
            return response

    except Exception as e:
        # Handle the case when an exception occurs (e.g., display an error message)
        error_message = f"Falló en generar el reporte de Examen Federal: {str(e)}"
        return HttpResponse(error_message)


def generate_socioeconomic_photos_report(self, request, queryset):
    # Extract the IDs of selected Personal objects
    personal_ids = queryset.values_list('id', flat=True)

    try:
        # Create an instance of GenerateDC3View and call its get method
        generate_socioeconomic_photos_view = GenerateSocioeconomicPhotosView()
        request = HttpRequest()  # Create a dummy request

        # Call the get method of GenerateDC3View with personal_ids
        response = generate_socioeconomic_photos_view.get(request, personal_ids, queryset)

        # Return the response directly to serve the PDF to the user
        if isinstance(response, HttpResponse):
            return response

    except Exception as e:
        # Handle the case when an exception occurs (e.g., display an error message)
        error_message = f"Falló en generar el reporte Fotográfico: {str(e)}"
        return HttpResponse(error_message)


def generate_isihara_test_report(self, request, queryset):
    # Extract the IDs of selected Personal objects
    personal_ids = queryset.values_list('id', flat=True)

    try:
        # Create an instance of GenerateDC3View and call its get method
        generate_ishihara_test_view = GenerateIshiharaTestView()
        request = HttpRequest()  # Create a dummy request

        # Call the get method of GenerateDC3View with personal_ids
        response = generate_ishihara_test_view.get(request, personal_ids, queryset)

        # Return the response directly to serve the PDF to the user
        if isinstance(response, HttpResponse):
            return response

    except Exception as e:
        # Handle the case when an exception occurs (e.g., display an error message)
        error_message = f"Falló en generar el examen Ishihara: {str(e)}"
        return HttpResponse(error_message)


def generate_honesty_test_report(self, request, queryset):
    # Extract the IDs of selected Personal objects
    personal_ids = queryset.values_list('id', flat=True)

    try:
        # Create an instance of GenerateDC3View and call its get method
        generate_honesty_test_view = GenerateHonestyTestView()
        request = HttpRequest()  # Create a dummy request

        # Call the get method of GenerateDC3View with personal_ids
        response = generate_honesty_test_view.get(request, personal_ids, queryset)

        # Return the response directly to serve the PDF to the user
        if isinstance(response, HttpResponse):
            return response

    except Exception as e:
        # Handle the case when an exception occurs (e.g., display an error message)
        error_message = f"Falló en generar el Modo Honesto de Vivir: {str(e)}"
        return HttpResponse(error_message)


def generate_polygraph_test_report(self, request, queryset):
    # Extract the IDs of selected Personal objects
    personal_ids = queryset.values_list('id', flat=True)

    try:
        # Create an instance of GenerateDC3View and call its get method
        generate_polygraph_test_view = GeneratePolygraphTestView()
        request = HttpRequest()  # Create a dummy request

        # Call the get method of GenerateDC3View with personal_ids
        response = generate_polygraph_test_view.get(request, personal_ids, queryset)

        # Return the response directly to serve the PDF to the user
        if isinstance(response, HttpResponse):
            return response

    except Exception as e:
        # Handle the case when an exception occurs (e.g., display an error message)
        error_message = f"Falló en generar el reporte de Exámen Poligráfico: {str(e)}"
        return HttpResponse(error_message)


def generate_gch_preliminary_report(self, request, queryset):
    # Extract the IDs of selected Personal objects
    personal_ids = queryset.values_list('id', flat=True)

    try:
        # Create an instance of GenerateDC3View and call its get method
        generate_gch_preliminary_view = GenerateGchPreliminaryView()
        request = HttpRequest()  # Create a dummy request

        # Call the get method of GenerateDC3View with personal_ids
        response = generate_gch_preliminary_view.get(request, personal_ids, queryset)

        # Return the response directly to serve the PDF to the user
        if isinstance(response, HttpResponse):
            return response

    except Exception as e:
        # Handle the case when an exception occurs (e.g., display an error message)
        error_message = f"Falló en generar el reporte Preliminar Gch: {str(e)}"
        return HttpResponse(error_message)


def generate_psychological_test_report(self, request, queryset):
    # Extract the IDs of selected Personal objects
    personal_ids = queryset.values_list('id', flat=True)

    try:
        # Create an instance of GenerateDC3View and call its get method
        generate_psychological_test_view = GeneratePsychologicalView()
        request = HttpRequest()  # Create a dummy request

        # Call the get method of GenerateDC3View with personal_ids
        response = generate_psychological_test_view.get(request, personal_ids, queryset)

        # Return the response directly to serve the PDF to the user
        if isinstance(response, HttpResponse):
            return response

    except Exception as e:
        # Handle the case when an exception occurs (e.g., display an error message)
        error_message = f"Falló en generar el reporte de Examen Psicológico: {str(e)}"
        return HttpResponse(error_message)


def generate_candidate_report(self, request, queryset):
    # Extract the IDs of selected Personal objects
    personal_ids = queryset.values_list('id', flat=True)

    try:
        # Create an instance of GenerateDC3View and call its get method
        generate_candidate_view = GenerateCandidateView()
        request = HttpRequest()  # Create a dummy request

        # Call the get method of GenerateDC3View with personal_ids
        response = generate_candidate_view.get(request, personal_ids, queryset)

        # Return the response directly to serve the PDF to the user
        if isinstance(response, HttpResponse):
            return response

    except Exception as e:
        # Handle the case when an exception occurs (e.g., display an error message)
        error_message = f"Falló en generar el reporte de Candidato: {str(e)}"
        return HttpResponse(error_message)


def generate_socioeconomic_report(self, request, queryset):
    # Extract the IDs of selected Personal objects
    personal_ids = queryset.values_list('id', flat=True)

    try:
        # Create an instance of GenerateDC3View and call its get method
        generate_socioeconomic_report_view = GenerateSocioeconomicReportView()
        request = HttpRequest()  # Create a dummy request

        # Call the get method of GenerateDC3View with personal_ids
        response = generate_socioeconomic_report_view.get(request, personal_ids, queryset)

        # Return the response directly to serve the PDF to the user
        if isinstance(response, HttpResponse):
            return response

    except Exception as e:
        # Handle the case when an exception occurs (e.g., display an error message)
        error_message = f"Falló en generar el reporte de Examen Socioeconómico: {str(e)}"
        return HttpResponse(error_message)


def generate_social_work_report(self, request, queryset):
    # Extract the IDs of selected Personal objects
    personal_ids = queryset.values_list('id', flat=True)

    try:
        # Create an instance of GenerateDC3View and call its get method
        generate_social_work_report_view = GenerateSocialWorkReportView()
        request = HttpRequest()  # Create a dummy request

        # Call the get method of GenerateDC3View with personal_ids
        response = generate_social_work_report_view.get(request, personal_ids, queryset)

        # Return the response directly to serve the PDF to the user
        if isinstance(response, HttpResponse):
            return response

    except Exception as e:
        # Handle the case when an exception occurs (e.g., display an error message)
        error_message = f"Falló en generar el reporte de Trabajo Social: {str(e)}"
        return HttpResponse(error_message)


def generate_sedena_report(self, request, queryset):
    # Extract the IDs of selected Personal objects
    personal_ids = queryset.values_list('id', flat=True)

    try:
        # Create an instance of GenerateDC3View and call its get method
        generate_sedena_view = GenerateSedenaView()
        request = HttpRequest()  # Create a dummy request

        # Call the get method of GenerateDC3View with personal_ids
        response = generate_sedena_view.get(request, personal_ids, queryset)

        # Return the response directly to serve the PDF to the user
        if isinstance(response, HttpResponse):
            return response

    except Exception as e:
        # Handle the case when an exception occurs (e.g., display an error message)
        error_message = f"Falló en generar el reporte de Sedena: {str(e)}"
        return HttpResponse(error_message)