import os
from django.http import HttpRequest
from main.views import GenerateDC3View


def generate_dc3_report(personal_instance):
    # Create an instance of GenerateDC3View and call its get method
    generate_dc3_view = GenerateDC3View()
    request = HttpRequest()  # Create a dummy request
    response = generate_dc3_view.get(request, personal_instance.id)
    # Handle the response as needed (e.g., save it to a file or return it)