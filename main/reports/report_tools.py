import PyPDF2
from docx2pdf import convert
from docxtpl import DocxTemplate
from openpyxl.drawing.image import Image as XlsxImage
from openpyxl.worksheet.page import PageMargins
from PIL import Image as PilImage
import os
import subprocess
import logging

# Creation of logger
logger = logging.getLogger(__name__)


def replace_variables_in_docx(docx_file_path, variables_dict):
    if docx_file_path is None:
        raise ValueError("docx_file_path must not be None.")
    doc = DocxTemplate(docx_file_path)
    doc.render(variables_dict)
    doc.save(docx_file_path)


def keep_first_page(pdf_path):
    # Open the PDF file
    reader = PyPDF2.PdfReader(pdf_path)

    # Create a new PDF writer
    writer = PyPDF2.PdfWriter()

    # Add the first page to the writer
    writer.add_page(reader.pages[0])

    # Write the output to a new file
    with open(pdf_path, 'wb') as output_file:
        writer.write(output_file)


def cm_to_pixels(cm: float) -> int:
    """
    Convert centimeters to pixels.

    Args:
        cm: The number of centimeters to convert.

    Returns:
        The number of pixels equivalent to the provided centimeters.
    """
    dpi = 96
    return int(dpi * cm / 2.54)


def scale_image_from_height(image_path: str, desired_height_cm: float):
    # Load the image with PIL to get its size
    with PilImage.open(image_path) as pil_img:
        original_width, original_height = pil_img.size

    # Convert the height from cm to pixels and set the height of the image
    dpi = 96
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
    convertion_command = [
        "libreoffice",
        "--headless",
        "--convert-to",
        "pdf:writer_pdf_Export",
        "--outdir",
        os.path.dirname(pdf_path),
        xlsx_path
    ]
    process = subprocess.Popen(convertion_command)
    process.wait()  # Wait for the process to finish before returning
    return pdf_path if process.returncode == 0 else None  # Check return code for success


# TODO: Fix, not working properly
def convert_docx_to_pdf(docx_path, pdf_path):
    convert(docx_path, pdf_path)
    return pdf_path


def merge_pdf_files(existing_pdf_path: str, added_pdf_path: str, output_pdf_path: str):
    merger = PyPDF2.PdfMerger()
    merger.append(PyPDF2.PdfReader(open(existing_pdf_path, 'rb')))
    merger.append(PyPDF2.PdfReader(open(added_pdf_path, 'rb')))
    merger.write(open(output_pdf_path, 'wb'))
    return output_pdf_path


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
