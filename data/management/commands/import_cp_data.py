import pandas as pd
from django.core.management.base import BaseCommand
from django.db import transaction
from data.models import CodigoPostal


class Command(BaseCommand):
    help = 'Import data from cp.csv into the CodigoPostal model'

    def handle(self, *args, **options):
        with transaction.atomic():
            objects = []
            df = pd.read_csv('media/file_templates/cp.csv')
            total_rows = len(df)
            existing_codigos = set(CodigoPostal.objects.values_list('codigo_postal', flat=True))

            for i, row in df.iterrows():
                codigo_postal = CodigoPostal(
                    codigo_postal=row['d_codigo'],
                    asentamiento=row['d_asenta'],
                    tipo_asentamiento=row['d_tipo_asenta'],
                    municipio=row['D_mnpio'],
                    estado=row['d_estado'],
                    ciudad=row['d_ciudad'],
                    pais='México'
                )
                # Check if the data already exists in the database
                if codigo_postal.codigo_postal not in existing_codigos:
                    objects.append(codigo_postal)

                if i % 1000 == 0 or i == total_rows - 1:
                    CodigoPostal.objects.bulk_create(objects)
                    objects.clear()
                self.stdout.write(f'Processed row {i+1} of {total_rows}')

        self.stdout.write(self.style.SUCCESS('Data import completed successfully'))
