from io import BytesIO
from django.http import HttpResponse
import openpyxl
from openpyxl.drawing.image import Image as XlsxImage
from openpyxl.utils import get_column_letter
from openpyxl.worksheet.page import PageMargins
from PIL import Image as PilImage



def scale_image(image_path, height_cm):
    """
    Scales an image to the specified height in centimeters while maintaining the aspect ratio.

    Args:
        image_path (str): The path to the image file.
        height_cm (float): The desired height in centimeters.

    Returns:
        bytes: The image data as a PNG byte array.
    """
    if image_path:
        with open(image_path, 'rb') as f:
            img = PilImage.open(f)
            original_width, original_height = img.size
            width_cm = round(float(original_width * (height_cm / original_height)), 2)
            img = img.resize((int(width_cm * 37.8), int(height_cm * 37.8)))  # 37.8 pixels per centimeter
    else:
        # Create a blank image with the desired dimensions
        width_cm = height_cm  # Set the width equal to the height
        img = PilImage.new('RGBA', (int(width_cm * 37.8), int(height_cm * 37.8)), (0, 0, 0, 0))

    # Convert the image to PNG format
    image_buffer = BytesIO()
    img.save(image_buffer, format='PNG')
    image_data = image_buffer.getvalue()

    return image_data


def generate_dc3(modeladmin, request, queryset):
    """
    Generates an XLSX file based on a template and data from a queryset.

    Args:
        modeladmin: The model admin object.
        request: The HTTP request object.
        queryset: The queryset containing data.

    Returns:
        HttpResponse: An HTTP response with the generated XLSX file
    """
    # Define the path to the original XLSX file
    original_file_path = "./media/file_templates/DC3 ACTUALIZADO.xlsx"

    # Load the original XLSX file
    wb = openpyxl.load_workbook(original_file_path)

    # Get the first sheet of the workbook
    sheet = wb.active
    
    # Set the page size to letter size (8.5 x 11 inches)
    sheet.page_setup.paperSize = sheet.PAPERSIZE_LETTER

    # Set the page margins
    sheet.page_margins = PageMargins(
        top=0.2,
        left=0.25,
        right=0.01,
        header=0.1,
        footer=0.1,
        bottom=.2
    )

    for personal in queryset:
        data = {
            'nombre_completo': '',
            'curp': '',
            'ocupacion': '',
            'puesto': '',
            'razon_social': '',
            'rfc': '',
            'nombre_curso': '',
            'horas_curso': '',
            'fecha_inicial_capacitacion': '',
            'fecha_final_capacitacion': '',
            'area_curso': '',
            'nombre_capacitador': '',
            'registro_capacitador': '',
            'representante_legal': '',
            'representante_trabajadores': '',
            'logotipo': None,
            'qr_code': None,
        }

        # Try to access each attribute individually and handle exceptions separately
        try:
            data['nombre_completo'] = f"{personal.curp.nombre} {personal.curp.apellido_paterno} {personal.curp.apellido_materno}"
        except AttributeError:
            pass

        try:
            data['curp'] = personal.curp.curp
        except AttributeError:
            pass

        # Update the attribute paths based on your models
        try:
            data['ocupacion'] = personal.carpetalaboral.ocupacion.nombre_ocupacion
        except AttributeError:
            pass

        try:
            data['puesto'] = personal.carpetalaboral.puesto.nombre_puesto
        except AttributeError:
            pass

        try:
            data['razon_social'] = personal.cliente.razon_social
        except AttributeError:
            pass

        try:
            data['rfc'] = personal.cliente.carpetaclientegenerales.rfc
        except AttributeError:
            pass

        try:
            data['nombre_curso'] = personal.carpetacapacitacion.curso
        except AttributeError:
            pass

        try:
            data['horas_curso'] = personal.carpetacapacitacion.duracion
        except AttributeError:
            pass

        try:
            data['fecha_inicial_capacitacion'] = personal.carpetacapacitacion.inicio
        except AttributeError:
            pass

        try:
            data['fecha_final_capacitacion'] = personal.carpetacapacitacion.conclusion
        except AttributeError:
            pass

        try:
            data['area_curso'] = personal.carpetacapacitacion.area_curso.nombre_area
        except AttributeError:
            pass

        try:
            data['nombre_capacitador'] = personal.carpetacapacitacion.capacitador.nombre_capacitador
        except AttributeError:
            pass

        try:
            data['registro_capacitador'] = personal.carpetacapacitacion.capacitador.numero_registro
        except AttributeError:
            pass

        try:
            data['representante_legal'] = personal.cliente.carpetaclientegenerales.representante_legal
        except AttributeError:
            pass

        try:
            data['representante_trabajadores'] = personal.cliente.representantetrabajadores.nombre_completo
        except AttributeError:
            pass

        try:
            data['logotipo'] = personal.cliente.documentoscliente.logotipo.path
        except ValueError:
            pass

        try:
            data['qr_code'] = personal.cliente.documentoscliente.qr_code.path
        except ValueError:
            pass

        # Define the data to be replaced in the cells for each 'personal' object
        cell_mapping = {
            'AJ6': data['nombre_completo'],
            'AJ7': data['curp'],
            'AJ8': data['ocupacion'],
            'AJ9': data['puesto'],
            'AJ10': data['nombre_curso'],
            'AJ11': data['horas_curso'],
            'AJ12': data['fecha_inicial_capacitacion'],
            'AJ13': data['fecha_final_capacitacion'],
            'AJ14': data['area_curso'],
            'AJ15': data['nombre_capacitador'],
            'AJ16': data['registro_capacitador'],
            'AJ22': data['razon_social'],
            'AJ23': data['rfc'],
            'AJ24': data['representante_legal'],
            'AJ25': data['representante_trabajadores'],
        }

        for cell, value in cell_mapping.items():
            sheet[cell].value = value

        def add_image_to_worksheet(img_path, cell_range, desired_height):
            img = scale_image(img_path, desired_height)
            img = XlsxImage(img_path)
            sheet.add_image(img, cell_range)

        # Add the images to the worksheet
        if data['logotipo']:
            img_path = personal.cliente.documentoscliente.logotipo.path
            desired_height = 3.5 * 37.8  # 3.5 centimeters
            add_image_to_worksheet(img_path, 'A1', desired_height)

        if data['qr_code']:
            img_path = personal.cliente.documentoscliente.qr_code.path
            desired_height = 3.5 * 37.8  # 3.5 centimeters
            add_image_to_worksheet(img_path, 'AH1', desired_height)
            
            # Adjust the image position to align AH1 from right to left
            img_column = 'AH'
            img = sheet.images[-1]
            
            # Get the row number for AH1
            img_row = img.anchor.row
            
            # Set the anchor for AH1 to align it from right to left
            img.anchor = img.anchor.move(col_offset=-img.width, to_col=img_column, row_offset=0, to_row=img_row)

    # Create a response with the modified XLSX file
    response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
    response['Content-Disposition'] = 'attachment; filename=modified_dc3.xlsx'
    wb.save(response)
    return response
