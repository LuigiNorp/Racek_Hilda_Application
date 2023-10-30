import os
from django.http import HttpRequest, HttpResponse
from main.views import GenerateDC3View


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
        error_message = f"Failed to generate DC-3 report: {str(e)}"
        return HttpResponse(error_message)
