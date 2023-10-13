from django.http import HttpResponse
# from docx import Document
import openpyxl

def generate_xlsx(modeladmin, request, queryset):
    # Define the path to the original XLSX file
    original_file_path = "./media/file_templates/Mis archivos/DC3 ACTUALIZADO.xlsx"

    # Load the original XLSX file
    wb = openpyxl.load_workbook(original_file_path)

    # Get the first sheet of the workbook
    sheet = wb.active

    for personal in queryset:
        data = {}

        # Try to access each attribute individually and handle exceptions separately
        try:
            data['nombre_apellidos'] = f"{personal.curp.nombre} {personal.curp.apellido_paterno} {personal.curp.apellido_materno}"
        except AttributeError:
            data['nombre_apellidos'] = ''

        try:
            data['curp'] = personal.curp.curp
        except AttributeError:
            data['curp'] = ''

        # Update the attribute paths based on your models
        try:
            data['ocupacion'] = personal.carpetalaboral.ocupacion.nombre_ocupacion
        except AttributeError:
            data['ocupacion'] = ''

        try:
            data['puesto'] = personal.carpetalaboral.puesto.nombre_puesto
        except AttributeError:
            data['puesto'] = ''

        try:
            data['razon_social'] = personal.cliente.razon_social
        except AttributeError:
            data['razon_social'] = ''

        try:
            data['rfc'] = personal.cliente.carpetaclientegenerales.rfc
        except AttributeError:
            data['rfc'] = ''
            
        try:
            data['nombre_curso'] = personal.carpetacapacitacion.curso
        except AttributeError:
            data['nombre_curso'] = ''

        try:
            data['horas_curso'] = personal.carpetacapacitacion.duracion
        except AttributeError:
            data['horas_curso'] = ''

        try:
            data['fecha_inicial_capacitacion'] = personal.carpetacapacitacion.inicio
        except AttributeError:
            data['fecha_inicial_capacitacion'] = ''

        try:
            data['fecha_final_capacitacion'] = personal.carpetacapacitacacion.conclusion
        except AttributeError:
            data['fecha_final_capacitacion'] = ''

        try:
            data['area_curso'] = personal.carpetacapacitacion.area_curso.nombre_area
        except AttributeError:
            data['area_curso'] = ''

        try:
            data['nombre_capacitador'] = personal.carpetacapacitacion.capacitador.nombre_capacitador
        except AttributeError:
            data['nombre_capacitador'] = ''

        try:
            data['registro_capacitador'] = personal.carpetacapacitacion.capacitador.numero_registro
        except AttributeError:
            data['registro_capacitador'] = ''
            
        try:
            data['representante_legal'] = personal.cliente.carpetaclientegenerales.representante_legal
        except AttributeError:
            data['representante_legal'] = ''
            
        try:
            data['representante_trabajadores'] = personal.cliente.representantetrabajadores.nombre_completo
        except AttributeError:
            data['representante_trabajadores'] = ''

        # Define the data to be replaced in the cells for each 'personal' object
        cell_mapping = {
            'AJ4': data['nombre_apellidos'],
            'AJ5': data['curp'],
            'AJ6': data['ocupacion'],
            'AJ7': data['puesto'],
            'AJ8': data['nombre_curso'],
            'AJ9': data['horas_curso'],
            'AJ10': data['fecha_inicial_capacitacion'],
            'AJ11': data['fecha_final_capacitacion'],
            'AJ12': data['area_curso'],
            'AJ13': data['nombre_capacitador'],
            'AJ14': data['registro_capacitador'],
            'AJ20': data['razon_social'],
            'AJ21': data['rfc'],
            'AJ22': data['representante_legal'],
            'AJ23': data['representante_trabajadores'],
        }

        for cell, value in cell_mapping.items():
            sheet[cell].value = value

    # Create a response with the modified XLSX file
    response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
    response['Content-Disposition'] = 'attachment; filename=modified_dc3.xlsx'
    wb.save(response)
    return response
