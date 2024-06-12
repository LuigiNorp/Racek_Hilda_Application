import pandas as pd
from django.core.management.base import BaseCommand
from data.models import Ocupacion
from .import_tools import *


class Command(BaseCommand):
    help = 'Import data from cp.csv into the Ocupacion model'

    def handle(self, *args, **options):
        # Calculate checksums for Ocupaciones CSV and SQL data
        query_for_ocupaciones_checksum = '''
            SELECT SHA256(GROUP_CONCAT(
                clave_subarea || ',' ||
                subarea || ',' ||
                clave_area || ',' ||
                area
            )) AS data_checksum
            FROM data_ocupacion
        '''

        csv_checksum = calculate_checksum('media/file_templates/ocupaciones.csv')
        sql_checksum = calculate_checksum_sql('hilda_data', query_for_ocupaciones_checksum)

        # Handle Ocupaciones data import
        if sql_checksum is None or csv_checksum > sql_checksum:
            self.__import_or_update_ocupaciones('media/file_templates/ocupaciones.csv')
            self.stdout.write(self.style.SUCCESS('Ocupaciones data import completed successfully'))
        else:
            self.stdout.write(self.style.SUCCESS('Ocupaciones data is up to date'))

    def __import_or_update_ocupaciones(self, file_path):
        ocupacion_database = set(Ocupacion.objects.values_list('clave_subarea', flat=True))
        objects = []
        df = pd.read_csv(file_path)
        total_rows = len(df)

        for i, row in df.iterrows():
            ocupacion_input = Ocupacion(
                # To complete the digits with zeros in the left in a float variable
                clave_subarea=str(row['clave_subarea']).rjust(4, '0'),
                subarea=row['subarea'],
                # To complete the digits with zeros in the left in a float variable
                clave_area=str(row['clave_area']).rjust(2, '0'),
                area=row['area']
            )

            populate_database_if_data_row_is_none(
                Ocupacion,
                ocupacion_input,
                'clave_subarea',
                ocupacion_database,
                objects
            )

            save_and_clear_data_row(
                Ocupacion,
                objects,
                total_rows,
                i,
                self.stdout
            )
