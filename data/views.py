from django.http import FileResponse
import os
from django.conf import settings


def download_csv_template(request):
    # Define la ruta al archivo
    file_path = os.path.join(settings.MEDIA_ROOT, 'file_templates', 'imports_template.csv')

    # Crea la respuesta HTTP
    response = FileResponse(open(file_path, 'rb'), content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="template.csv"'

    return response
