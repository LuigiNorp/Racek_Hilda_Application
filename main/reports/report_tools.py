from django.http import HttpResponse
from PyPDF2 import PdfReader, PdfWriter
from openpyxl.drawing.image import Image as XlsxImage
from openpyxl.worksheet.page import PageMargins
from PIL import Image as PilImage
import os
import subprocess


def keep_first_page(pdf_path):
    # Open the PDF file
    reader = PdfReader(pdf_path)

    # Create a new PDF writer
    writer = PdfWriter()

    # Add the first page to the writer
    writer.add_page(reader.pages[0])

    # Write the output to a new file
    with open(pdf_path, 'wb') as output_file:
        writer.write(output_file)


def verify_text_data(field: str, model, data_dict: dict):
    try:
        result = getattr(model, data_dict[field])
    except AttributeError:
        result = None
    return result


def verify_media_data(field: str, model, data_dict: dict):
    try:
        result = getattr(model, data_dict[field])
    except ValueError:
        result = None
    return result


def verify_date_data(field: str, model, data_dict: dict, date_format: str):
    try:
        date_field = getattr(model, data_dict[field])
        formatted_date = date_field.strftime(date_format)
        return formatted_date
    except AttributeError:
        return None


def verify_function_value(field: str, model, data_dict: dict, params=None):
    try:
        function_name = data_dict[field]
        if params is not None:
            result = getattr(model, function_name)(*params)  # Call the function with the provided parameters
        else:
            result = getattr(model, function_name)()  # Call the function without parameters
    except AttributeError:
        result = None
    return result


def scale_image_from_height(image_path: str, desired_height_cm: float):
    # Load the image with PIL to get its size
    with PilImage.open(image_path) as pil_img:
        original_width, original_height = pil_img.size

    # Convert the height from cm to pixels and set the height of the image
    dpi = 96
    cm_to_pixels = lambda cm: int(dpi * cm / 2.54)  # convert cm to pixels
    desired_height_px = cm_to_pixels(desired_height_cm)

    # Calculate the new width to maintain aspect ratio
    scale_factor = desired_height_px / original_height
    desired_width_px = int(original_width * scale_factor)

    return desired_width_px, desired_height_px


def add_image_to_worksheet(image_path: str, cell: str, activesheet, width: int, height: int):
    # Load and add the image with openpyxl
    img = XlsxImage(image_path)
    img.width = width
    img.height = height

    # Add image to the specified cell
    activesheet.add_image(img, cell)


def convert_xlsx_to_pdf(xlsx_path: str, pdf_path: str):
    convertion_command = f"libreoffice --headless --convert-to pdf:writer_pdf_Export --outdir {os.path.dirname(pdf_path)} {xlsx_path}"
    subprocess.run(convertion_command, shell=True)
    return pdf_path


def xlsx_sheet_presets(sheet):
    sheet.page_setup.paperSize = sheet.PAPERSIZE_LETTER
    sheet.page_margins = PageMargins(
        top=0.2,
        left=0.25,
        right=0.01,
        header=0.1,
        footer=0.1,
        bottom=0.2
    )
