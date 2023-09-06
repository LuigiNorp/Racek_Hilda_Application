import openpyxl
from openpyxl.drawing.image import Image
from openpyxl.utils import get_column_letter
from fpdf import FPDF
from data.models import Personal, Curp, Rfc, CarpetaClienteGenerales, CarpetaClientePagos

# Define the path to the original XLSX file
original_file_path = "./media/file_templates/Mis archivos/DC3 ACTUALIZADO.xlsx"

# Load the original XLSX file
wb = openpyxl.load_workbook(original_file_path)

# Get the first sheet of the workbook
sheet = wb.active

# Get the Personal object for which you want to retrieve information
personal = Personal.objects.get(id=1)

# Get the related Curp object for the Personal object
curp = personal.curp

# Get the related Rfc object for the Personal object
rfc = personal.rfc

# Get the related CarpetaClienteGenerales object for the Personal object
carpeta_cliente_generales = personal.carpetagenerales

# Get the related CarpetaClientePagos object for the Personal object
carpeta_cliente_pagos = personal.carpetapagos

# Retrieve the related Capacitacion objects for the Personal object
capacitacion = personal.carpeta_capacitacion.capacitacion

# Get the related AreaCurso object for the Personal object
area_curso = capacitacion.area_curso

# Get the related AreaCurso object for the Personal object
capacitador = capacitacion.capacitador

# Define the data to be replaced in the cells
data = {
    'nombre_apellidos': f"{curp.nombre} {curp.apellido_paterno} {curp.apellido_materno}",
    'curp': curp.curp,
    'ocupacion': carpeta_cliente_generales.puesto.nombre_puesto,
    'puesto': carpeta_cliente_generales.puesto.nombre_puesto,
    'razon_social': carpeta_cliente_pagos.razon_social,
    'rfc': rfc.rfc,
    'nombre_curso': capacitacion.curso,
    'horas_curso': capacitacion.duracion,
    'fecha_inicial_capacitacion': capacitacion.inicio,
    'fecha_final_capacitacion': capacitacion.conclusion,
    'area_curso': area_curso.nombre_area,
    'nombre_capacitador': capacitador.nombre_capacitador,
    'registro_capacitador': capacitador.numero_registro,
}

# Replace the values in the specified cells with the data dictionary
cell_mapping = {
    'AJ4': data['nombre_apellidos'],
    'AJ5': data['curp'],
    'AJ6': data['ocupacion'],
    'AJ7': data['puesto'],
    'AJ20': data['razon_social'],
    'AJ21': data['rfc'],
    'AJ8': data['nombre_curso'],
    'AJ9': data['horas_curso'],
    'AJ10': data['fecha_inicial_capacitacion'],
    'AJ11': data['fecha_final_capacitacion'],
    'AJ12': data['area_curso'],
    'AJ13': data['nombre_capacitador'],
    'AJ14': data['registro_capacitador'],
}

for cell, value in cell_mapping.items():
    sheet[cell].value = value

# Generate the modified XLSX file
modified_file_path = "./media/file_templates/Mis archivos/DC3 ACTUALIZADO modified.xlsx"
wb.save(modified_file_path)