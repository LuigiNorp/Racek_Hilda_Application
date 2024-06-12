import pandas as pd
from django.core.management.base import BaseCommand
from data.models import CodigoPostal
from unidecode import unidecode
from .import_tools import *


class Command(BaseCommand):
    help = 'Import data from cp.csv into the CodigoPostal model'

    def handle(self, *args, **options):
        # Calculate checksums for CSV and SQL data
        query_for_codigpostal_checksum = '''
            SELECT SHA256(GROUP_CONCAT(
            codigo_postal || ',' ||
            tipo_asentamiento || ',' ||
            asentamiento || ',' ||
            municipio || ',' ||
            estado || ',' ||
            ciudad || ',' ||
            pais
         )) AS data_checksum
        FROM data_codigopostal
        '''

        csv_checksum = calculate_checksum('media/file_templates/cp.csv')
        sql_checksum = calculate_checksum_sql('hilda_data', query_for_codigpostal_checksum)

        # Handle CodigoPostal data import
        if not sql_checksum or sql_checksum < csv_checksum:
            self.__import_or_update_codigospostales('media/file_templates/cp.csv')
            self.stdout.write(self.style.SUCCESS('CodigoPostal data import completed successfully'))
        else:
            self.stdout.write(self.style.SUCCESS('CodigoPostal data is up to date'))

    def __import_or_update_codigospostales(self, file_path):
        codigopostal_database = set(CodigoPostal.objects.values_list('codigo_postal', flat=True))
        objects = []
        df = pd.read_csv(file_path)
        total_rows = len(df)

        for i, row in df.iterrows():
            asentamiento_normalizado = unidecode(row['d_asenta'])  # Normalizar el asentamiento
            codigopostal_input = CodigoPostal(
                codigo_postal=row['d_codigo'],
                asentamiento=row['d_asenta'],
                tipo_asentamiento=row['d_tipo_asenta'],
                municipio=row['D_mnpio'],
                estado=row['d_estado'],
                ciudad=row['d_ciudad'],
                pais='México',
                asentamiento_normalizado=asentamiento_normalizado  # Asignar el asentamiento normalizado
            )

            populate_database_if_data_row_is_none(
                CodigoPostal,
                codigopostal_input,
                'codigo_postal',
                codigopostal_database,
                objects
            )

            save_and_clear_data_row(
                CodigoPostal,
                objects,
                total_rows,
                i,
                self.stdout
            )
