from django.db import connection, utils
import pandas as pd
from data.models import Cliente, CarpetaClienteGenerales, Domicilio, CodigoPostal, CarpetaClienteContactos
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help = 'Import data from lista_empresas.csv into the Cliente model and related models'

    def handle(self, *args, **options):
        self.create_cliente_table_if_not_exists()
        self.create_temp_table()
        self.load_data_into_temp_table('media/file_templates/lista_empresas.csv')
        results = self.compare_data()
        if not results:
            self.stdout.write(self.style.SUCCESS('Cliente data is up to date'))
        else:
            self.import_data_to_db(results)

    def create_temp_table(self):
        with connection.cursor() as cursor:
            cursor.execute("""
                SELECT name FROM sqlite_master WHERE type='table' AND name='temp_cliente';
            """)
            result = cursor.fetchone()
            if not result:  # If the table does not exist, create it
                try:
                    cursor.execute("""
                        CREATE TEMPORARY TABLE temp_cliente (
                            nombre_comercial VARCHAR(255),
                            razon_social VARCHAR(255),
                            calle VARCHAR(255),
                            numero_exterior VARCHAR(255),
                            numero_interior VARCHAR(255),
                            codigo_postal VARCHAR(255),
                            asentamiento VARCHAR(255),
                            telefono_1 VARCHAR(255),
                            telefono_2 VARCHAR(255),
                            nombre_contacto VARCHAR(255)
                        )
                    """)
                except utils.OperationalError as e:
                    self.stdout.write(
                        self.style.ERROR('An error occurred while creating the temporary table: {}'.format(e)))

    @staticmethod
    def create_cliente_table_if_not_exists():
        with connection.cursor() as cursor:
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS data_cliente (
                    id INT AUTO_INCREMENT PRIMARY KEY,
                    nombre_comercial VARCHAR(255),
                    razon_social VARCHAR(255),
                    # Add other fields here...
                )
            """)

    @staticmethod
    def load_data_into_temp_table(file_path):
        df = pd.read_csv(file_path)
        with connection.cursor() as cursor:
            for index, row in df.iterrows():
                cursor.execute("""
                    INSERT INTO temp_cliente (
                        nombre_comercial, 
                        razon_social, 
                        calle, 
                        numero_exterior, 
                        numero_interior, 
                        codigo_postal, 
                        asentamiento, 
                        telefono_1, 
                        telefono_2, 
                        nombre_contacto
                    )
                    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                """, [
                    row['Nombre Comercial'],
                    row['NombreFiscal'],
                    row['CALLE'],
                    row['NUMERO EXTERIOR'],
                    row['NUMERO INTERIOR'],
                    row['C.P.'],
                    row['COLONIA'],
                    row['NO. DE TELEFONO'],
                    row['NO. DE TELEFONO2'],
                    row['CONTACTO']
                ])

    @staticmethod
    def compare_data():
        with connection.cursor() as cursor:
            cursor.execute("""
                SELECT 
                    temp_cliente.nombre_comercial,
                    temp_cliente.razon_social,
                    temp_cliente.calle,
                    temp_cliente.numero_exterior,
                    temp_cliente.numero_interior,
                    temp_cliente.codigo_postal,
                    temp_cliente.asentamiento,
                    temp_cliente.telefono_1,
                    temp_cliente.telefono_2,
                    temp_cliente.nombre_contacto
                FROM temp_cliente
                LEFT JOIN data_cliente ON temp_cliente.nombre_comercial = data_cliente.nombre_comercial
                LEFT JOIN data_carpetaclientegenerales ON data_cliente.id = data_carpetaclientegenerales.cliente_id
                LEFT JOIN data_domicilio ON data_carpetaclientegenerales.domicilio_id = data_domicilio.id
                LEFT JOIN data_codigopostal ON data_domicilio.codigo_postal_id = data_codigopostal.id
                LEFT JOIN data_carpetaclientecontactos ON data_cliente.id = data_carpetaclientecontactos.cliente_id
                WHERE 
                    temp_cliente.nombre_comercial != data_cliente.nombre_comercial OR
                    temp_cliente.razon_social != data_cliente.razon_social OR
                    temp_cliente.calle != data_domicilio.calle OR
                    temp_cliente.numero_exterior != data_domicilio.numero_exterior OR
                    temp_cliente.numero_interior != data_domicilio.numero_interior OR
                    temp_cliente.codigo_postal != data_codigopostal.codigo_postal OR
                    temp_cliente.asentamiento != data_codigopostal.asentamiento OR
                    temp_cliente.telefono_1 != data_carpetaclientecontactos.telefono_1 OR
                    temp_cliente.telefono_2 != data_carpetaclientecontactos.telefono_2 OR
                    temp_cliente.nombre_contacto != data_carpetaclientecontactos.nombre_contacto
            """)
            return cursor.fetchall()

    @staticmethod
    def import_data_to_db(results):
        df = pd.DataFrame(results, columns=['nombre_comercial', 'razon_social', 'calle', 'numero_exterior', 'numero_interior', 'codigo_postal', 'asentamiento', 'telefono_1', 'telefono_2', 'nombre_contacto'])
        for i, row in df.iterrows():
            codigo_postal, created = CodigoPostal.objects.get_or_create(codigo_postal=row['codigo_postal'], asentamiento=row['asentamiento'])
            domicilio = Domicilio(calle=row['calle'], numero_exterior=row['numero_exterior'], numero_interior=row['numero_interior'], codigo_postal=codigo_postal,)
            domicilio.save()
            cliente_input = Cliente(nombre_comercial=row['nombre_comercial'], razon_social=row['razon_social'])
            cliente_input.save()
            carpetaclientegenerales = CarpetaClienteGenerales(cliente=cliente_input, domicilio=domicilio)
            carpetaclientegenerales.save()
            carpetaclientecontactos=CarpetaClienteContactos(telefono_1=row['telefono_1'], telefono_2=row['telefono_2'], nombre_contacto=row['nombre_contacto'])
            carpetaclientecontactos.save()
