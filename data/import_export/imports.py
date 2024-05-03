from django.apps import apps
from django.db import transaction
from django.db.models import Q
import pandas as pd
from data.choices import MODALIDAD
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
        self.__asentamiento = None
        self.__modalidad_dict = {texto.upper(): numero for numero, texto in MODALIDAD}

    @staticmethod
    def __get_models_and_fields_from_csv(header: str) -> tuple:
        model_name, field_name = header.split('_', 1)
        return model_name, field_name.lower()

    @staticmethod
    def __handle_remaining_fields(row_dict: dict, header: str, field_name: str) -> dict:
        model_data = {}
        if field_name:
            model_data[field_name] = row_dict[header]
        return model_data

    def __handle_codigo_postal(self, row_dict: dict, header: str, field_name: str) -> dict:
        model_data = {field_name: row_dict[header]}
        if field_name == 'asentamiento':
            self.__asentamiento = model_data['asentamiento']
            # It's __self.asentamiento because is needed to save the data until the
            # next csv_field (codigo_postal) is reached and could be used in the query
        if field_name == 'codigo_postal':
            codigo_postal = model_data['codigo_postal']
            try:
                codigo_postal_object = CodigoPostal.objects.get(Q(codigo_postal=codigo_postal) & Q(asentamiento__icontains=self.__asentamiento))
                model_data[field_name] = codigo_postal_object
                codigo_postal, self.__asentamiento = None, None
                return model_data
            except CodigoPostal.DoesNotExist:
                return None

    @staticmethod
    def __handle_ocupacion(row_dict: dict, header: str) -> dict:
        ocupacion_text = row_dict[header]
        try:
            ocupacion_object = Ocupacion.objects.get(subarea__icontains=ocupacion_text)
            return {'ocupacion': ocupacion_object}
        except Ocupacion.DoesNotExist:
            return None

    def __handle_modalidad(self, row_dict: dict, header: str) -> dict:
        modalidad_text = row_dict[header].upper()
        modalidad_numero = self.__modalidad_dict.get(modalidad_text)
        return {'modalidad': modalidad_numero} if modalidad_numero is not None else None

    def __get_model_data(self, row_content: pd.DataFrame, header: str, field_name: str) -> dict:
        row_dict = row_content.to_dict()
        if field_name == 'codigo_postal' or field_name == 'asentamiento':
            model_data = self.__handle_codigo_postal(row_dict, header, field_name)
        elif field_name == 'ocupacion':
            model_data = self.__handle_ocupacion(row_dict, header)
        elif field_name == 'modalidad':
            model_data = self.__handle_modalidad(row_dict, header)
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
        # Convertir la lista de diccionarios en un solo diccionario
        return {k: v for d in data for k, v in d.items()}

    def __get_or_create_client(self, data_dict: dict) -> object:
        # Obtener o crear la instancia de Cliente
        client, created = Cliente.objects.get_or_create(nombre_comercial=data_dict.get('nombre_comercial'), defaults=data_dict)
        if not created:
            # Si la instancia ya existía, actualizar los campos
            self.__update_client_fields(client, data_dict)
        return client

    @staticmethod
    def __update_client_fields(client: object, data_dict: dict) -> None:
        for field, value in data_dict.items():
            setattr(client, field, value)
        client.save()

    def __create_grandparent_model_instances(self, data: any) -> object:
        client_data = data.get('Cliente')
        if client_data:
            client_data_dict = self.__convert_model_data_to_dict(client_data)
            client = self.__get_or_create_client(client_data_dict)
            return client
        return None

    def __create_parent_models_instances(self, model_data, grandparent_instance):
        # Aquí es donde crearías las instancias que dependen de Cliente
        pass

    def __create_child_models_instances(self, model_data, parent_instance):
        # Aquí es donde crearías las instancias que dependen de las instancias padre
        pass

    def __populate_dictionary_in_database(self):
        for row, data in self.__models_data.items():
            grandparent_instance = self.__create_grandparent_model_instances(data)
            parent_instance = self.__create_parent_models_instances(data, grandparent_instance)
            self.__create_child_models_instances(data, parent_instance)

    def import_data_from_csv(self):
        self.__extract_csv_data_in_a_dictionary()
        self.__populate_dictionary_in_database()
