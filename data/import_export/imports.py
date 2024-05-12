from django.apps import apps
from django.db import transaction
from django.db.models import Q
import pandas as pd
from dateutil import parser
from data.choices import (
    MODALIDAD, ORIGEN_ASPIRANTE, EDO_CIVIL
)
from data.models import (
    Cliente, CarpetaClienteContactos, RepresentanteTrabajadores, CarpetaClienteGenerales,
    Domicilio, CodigoPostal, Personal, Curp, Rfc, CarpetaLaboral, Ocupacion, CarpetaGenerales,
    Evaluador, Resultado
)
import logging

logger = logging.getLogger(__name__)


class CSVImporter:
    def __init__(self, csv_file_path: str):
        self.__csv_file_path = csv_file_path
        self.__models_data = {}
        self.__settlement = None
        self.__modalidad_dict = {texto.upper(): numero for numero, texto in MODALIDAD}
        self.__origen_dict = {texto.upper(): numero for numero, texto in ORIGEN_ASPIRANTE}
        self.__edo_civil_dict = {texto.upper(): numero for numero, texto in EDO_CIVIL}

    def import_data_from_csv(self):
        self.__extract_csv_data_in_a_dictionary()
        self.__populate_dictionary_in_database()

    @staticmethod
    def __get_models_and_fields_from_csv(header: str) -> tuple:
        model_name, field_name = header.split('_', 1)
        return model_name, field_name.lower()

    @staticmethod
    def __handle_remaining_fields(row_dict: dict, header: str, field_name: str) -> dict:
        return {field_name: row_dict[header]}

    def __handle_zip_code(self, row_dict: dict, header: str, field_name: str) -> dict:
        model_data = {field_name: row_dict[header]}
        if field_name == 'asentamiento':
            self.__settlement = model_data['asentamiento']
            # It's __self.asentamiento because is needed to save the data until the
            # next csv_field (codigo_postal) is reached and could be used in the query
        if field_name == 'codigo_postal':
            zip_code = model_data['codigo_postal']
            try:
                zip_code_object = CodigoPostal.objects.get(Q(codigo_postal=zip_code) & Q(asentamiento__icontains=self.__settlement))
                model_data[field_name] = zip_code_object
                zip_code, self.__settlement = None, None
                return model_data
            except CodigoPostal.DoesNotExist:
                return None

    @staticmethod
    def __handle_employment(row_dict: dict, header: str) -> dict:
        employment_text = row_dict[header]
        try:
            employment_object = Ocupacion.objects.get(subarea__icontains=employment_text)
            return {'ocupacion': employment_object}
        except Ocupacion.DoesNotExist:
            return None

    @staticmethod
    def __handle_choices(row_dict: dict, header: str, choice_dict: dict, field_name: str) -> dict:
        choice_text = row_dict[header].upper()
        choice_number = choice_dict.get(choice_text)
        return {field_name: choice_number} if choice_number is not None else None

    def __handle_dates(self, row_dict: dict, header: str) -> dict:
        date_str = row_dict[header]
        model_name, field_name = self.__get_models_and_fields_from_csv(header)
        try:
            date = parser.parse(date_str, dayfirst=True)
            return {field_name: date.strftime('%Y-%m-%d')}
        except ValueError:
            print("La fecha ingresada no tiene un formato reconocible.")
            return None

    def __get_model_data(self, row_content: pd.DataFrame, header: str, field_name: str) -> dict:
        row_dict = row_content.to_dict()
        if field_name == 'codigo_postal' or field_name == 'asentamiento':
            model_data = self.__handle_zip_code(row_dict, header, field_name)
        elif field_name == 'ocupacion':
            model_data = self.__handle_employment(row_dict, header)
        elif field_name == 'modalidad':
            model_data = self.__handle_choices(row_dict, header, self.__modalidad_dict, field_name)
        elif field_name == 'origen':
            model_data = self.__handle_choices(row_dict, header, self.__origen_dict, field_name)
        elif field_name == 'estado_civil':
            model_data = self.__handle_choices(row_dict, header, self.__edo_civil_dict, field_name)
        elif field_name.__contains__('fecha'):
            model_data = self.__handle_dates(row_dict, header)
        else:
            model_data = self.__handle_remaining_fields(row_dict, header, field_name)
        return model_data

    @staticmethod
    def __add_model_data_to_row_data_dict(model_data: dict, model_name: str, row_data_dict: dict):
        if model_data is not None:
            if model_name not in row_data_dict:
                row_data_dict[model_name] = []
            row_data_dict[model_name].append(model_data)

    def __store_row_data_in_models_data_dict(self, row_num: any, row_data_dict: dict):
        self.__models_data[row_num] = row_data_dict

    def __extract_data_from_row(self, row_content: any, headers: str, row_num: any) -> None:
        row_data_dict = {}
        for header in headers:
            model_name, field_name = self.__get_models_and_fields_from_csv(header)
            model_data = self.__get_model_data(row_content, header, field_name)
            self.__add_model_data_to_row_data_dict(model_data, model_name, row_data_dict)
        self.__store_row_data_in_models_data_dict(row_num, row_data_dict)

    def __extract_csv_data_in_a_dictionary(self) -> None:
        df = pd.read_csv(self.__csv_file_path)
        headers = df.columns.tolist()
        for row_num, row_content in df.iterrows():
            self.__extract_data_from_row(row_content, headers, row_num)

    @staticmethod
    def __convert_model_data_to_dict(data: list) -> dict:
        return {k: v for d in data for k, v in d.items()}

    def __populate_dictionary_in_database(self):
        parent_models = ['CarpetaClienteContactos', 'CarpetaClienteGenerales', 'Personal']
        for row, data in self.__models_data.items():
            grandparent_instance = self.__create_grandparent_model_instances(data)
            for model in parent_models:
                parent_instance = self.__create_parent_model_instance(data, model, grandparent_instance)
                if not isinstance(parent_instance, CarpetaClienteContactos):
                    self.__create_child_models_instances(data, grandparent_instance, parent_instance)

    def __create_grandparent_model_instances(self, data: any) -> object:
        client_data = data.get('Cliente')
        if client_data:
            client_data_dict = self.__convert_model_data_to_dict(client_data)
            client = self.__get_or_create_client(client_data_dict)
            return client
        return None

    def __get_or_create_client(self, data_dict: dict) -> object:
        client, created = Cliente.objects.get_or_create(nombre_comercial=data_dict.get('nombre_comercial'), defaults=data_dict)
        if not created:
            self.__update_client_fields(client, data_dict)
        return client

    @staticmethod
    def __update_client_fields(client: object, data_dict: dict) -> None:
        for field, value in data_dict.items():
            setattr(client, field, value)
        client.save()

    def __create_parent_model_instance(self, data, model_name, grandparent_instance):
        model_data = data.get(model_name)
        if model_data:
            model_data_dict = self.__convert_model_data_to_dict(model_data)
            model_data_dict['cliente'] = grandparent_instance
            ModelClass = apps.get_model('data', model_name)
            return self.__get_or_create_model_instance(ModelClass, model_data_dict)
        
    def __create_child_models_instances(self, data, grandparent_instance, parent_instance):
        child_instances = {}
        parent_to_child_models = {
            CarpetaClienteGenerales: ['Domicilio'],
            Personal: ['Curp', 'Rfc', 'Ocupacion', 'CarpetaGenerales', 'Evaluador', 'Resultado'],
            Cliente: ['RepresentanteTrabajadores']
        }
        for model_class, child_models in parent_to_child_models.items():
            if isinstance(parent_instance, model_class):
                for model in child_models:
                    model_data = data.get(model)
                    if model_data:
                        model_data_dict = self.__convert_model_data_to_dict(model_data)
                        if isinstance(parent_instance, CarpetaClienteGenerales):
                            model_data_dict['carpeta_cliente_generales'] = parent_instance
                        elif isinstance(parent_instance, Personal):
                            model_data_dict['personal'] = parent_instance
                        elif isinstance(parent_instance, Cliente):
                            model_data_dict['cliente'] = grandparent_instance
                        model_class = apps.get_model('data', model)
                        child_instances[model] = self.__get_or_create_model_instance(model_class, model_data_dict)
            return child_instances

    @staticmethod
    def __get_or_create_model_instance(model_class, model_data_dict):
        instance, created = model_class.objects.get_or_create(**model_data_dict)
        if not created:
            for field, value in model_data_dict.items():
                setattr(instance, field, value)
            instance.save()
        return instance
