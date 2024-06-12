from django.db import transaction
from unidecode import unidecode
from django.db.models import Q
import re
import pandas as pd
from dateutil import parser
from data.choices import (
    MODALIDAD, ORIGEN_ASPIRANTE, EDO_CIVIL, ESCOLARIDAD, ESTADO_CARTILLA,
    PROCESO_RACEK, TIPO_PUESTO, RESULTADOS_PREVIO
)
from data.models import (
    Cliente, CarpetaClienteContactos, RepresentanteTrabajadores, CarpetaClienteGenerales,
    Domicilio, CodigoPostal, Personal, Curp, Rfc, CarpetaLaboral, Ocupacion, CarpetaGenerales,
    Evaluador, Resultado, Sede
)
import logging

logger = logging.getLogger(__name__)


class CSVImporter:
    def __init__(self, csv_file_path: str):
        self.created_instances = {}
        self.clientes = {}
        self.__csv_file_path = csv_file_path
        self.__models_data = {}
        self.__settlement = None
        self.__modalidad_dict = {texto.upper(): numero for numero, texto in MODALIDAD}
        self.__origen_dict = {texto.upper(): numero for numero, texto in ORIGEN_ASPIRANTE}
        self.__edo_civil_dict = {texto.upper(): numero for numero, texto in EDO_CIVIL}
        self.__escolaridad_dict = {texto.upper(): numero for numero, texto in ESCOLARIDAD}
        self.__estado_cartilla_dict = {texto.upper(): numero for numero, texto in ESTADO_CARTILLA}
        self.__proceso_racek_dict = {texto.upper(): numero for numero, texto in PROCESO_RACEK}
        self.__tipo_puesto_dict = {texto.upper(): numero for numero, texto in TIPO_PUESTO}
        self.__resultados_completos_aspirantes_dict = {texto.upper(): numero for numero, texto in RESULTADOS_PREVIO}

    def import_data_from_csv(self):
        self.__extract_csv_data_in_a_dictionary()
        self.__populate_dictionary_in_database()

    def __extract_csv_data_in_a_dictionary(self) -> None:
        df = pd.read_csv(self.__csv_file_path, dtype=str, encoding='utf-8')
        headers = df.columns.tolist()
        for row_num, row_content in df.iterrows():
            self.__extract_data_from_row(row_content, headers, row_num)

    def __extract_data_from_row(self, row_content: any, headers: str, row_num: any) -> None:
        row_data_dict = {}
        for header in headers:
            model_name, field_name = self.__get_models_and_fields_from_csv(header)
            model_data = self.__get_model_data(row_content, header, field_name)
            self.__add_model_data_to_row_data_dict(model_data, model_name, row_data_dict)
        self.__store_row_data_in_models_data_dict(row_num, row_data_dict)

    @staticmethod
    def __get_models_and_fields_from_csv(header: str) -> tuple:
        model_name, field_name = header.split('_', 1)
        return model_name, field_name.lower()

    def __get_model_data(self, row_content: pd.DataFrame, header: str, field_name: str) -> dict:
        row_dict = row_content.to_dict()

        field_handlers = {
            'codigo_postal': lambda: self.__handle_zip_code(row_dict, header, field_name),
            'asentamiento': lambda: self.__handle_zip_code(row_dict, header, field_name),
            'ocupacion': lambda: self.__handle_employment(row_dict, header),
            'modalidad': lambda: self.__handle_choices(row_dict, header, self.__modalidad_dict, field_name),
            'origen': lambda: self.__handle_choices(row_dict, header, self.__origen_dict, field_name),
            'escolaridad': lambda: self.__handle_choices(row_dict, header, self.__escolaridad_dict, field_name),
            'estado_cartilla': lambda: self.__handle_choices(row_dict, header, self.__estado_cartilla_dict, field_name),
            'estado_civil': lambda: self.__handle_choices(row_dict, header, self.__edo_civil_dict, field_name),
            'proceso_racek': lambda: self.__handle_choices(row_dict, header, self.__proceso_racek_dict, field_name),
            'puesto': lambda: self.__handle_choices(row_dict, header, self.__tipo_puesto_dict, field_name),
            'resultado': lambda: self.__handle_choices(row_dict, header, self.__resultados_completos_aspirantes_dict, field_name)
        }
        # It's outside mapping because it's looking for a field that contains 'fecha'
        # not an excact match like the mapped ones
        if 'fecha' in field_name:
            return self.__handle_dates(row_dict, header)

        # It triggers the corresponding handling function or handle the remaining field
        return field_handlers.get(field_name, lambda: self.__handle_remaining_fields(row_dict, header, field_name))()

    @staticmethod
    def __handle_remaining_fields(row_dict: dict, header: str, field_name: str) -> dict:
        if pd.isnull(row_dict[header]):
            return {field_name: ""}
        else:
            return {field_name: row_dict[header]}

    def __handle_zip_code(self, row_dict: dict, header: str, field_name: str) -> dict:
        WORDS_TO_DELETE = [
            'COLONIA', 'COL', 'COL.', 'C.', 'C', 'CL', 'PUEBLO', 'PUEB', 'PUEB.', 'PBL', 'PBL.', 'P.', 'P', 'PB', 'PB.', 'BARRIO', 'BARR', 'BARR.', 'BAR.', 'BAR', 'B.', 'B', 'EQUIPAMIENTO', 'EQUIP.', 'EQUIP', 'E.', 'E',
            'CAMPAMENTO', 'CAMP.', 'CAMP', 'AEROPUERTO', 'AEROP.', 'AEROP', 'AEROPTO', 'AEROPTO.', 'A', 'FRACCIONAMIENTO', 'FRAC', 'FRAC.', 'FRACC', 'CONDOMINIO', 'COND.', 'COND', 'UNIDAD HABITACIONAL', 'UNIDAD HAB', 'UNIDAD HAB.',
            'U.H.', 'U H', 'U. HABITACIONAL', 'U HABITACIONAL', 'ZONA COMERCIAL', 'Z.C.', 'Z C', 'ZONA C.', 'ZONA C', 'Z. COMERCIAL', 'Z COMERCIAL', 'Z COM.', 'ZONA COM.', 'ZC', 'ZC.', 'ZN. COM.', 'ZN COM', 'RANCHO', 'RCHO',
            'RCHO.', 'RANCHERÍA', 'RCHIA', 'RCHÍA', 'RCHIA.', 'RCHÍA.', 'RNCHIA', 'RNCHÍA.', 'RNCHIA.', 'RNCHÍA', 'ZONA INDUSTRIAL', 'Z. INDUSTRIAL', 'Z INDUSTRIAL', 'Z. IND.', 'Z IND', 'Z. INDUST.', 'Z. INDUST', 'ZI.', 'ZN. IND.',
            'ZN INDUST.', 'GRANJA', 'GJA', 'GJA.', 'ZONA FEDERAL', 'Z. FED.', 'Z. FED', 'Z.F.', 'ZF', 'EJIDO', 'EJDO.', 'EJDO', 'PARAJE', 'PAR', 'PAR.', 'PJE', 'PJE.', 'HACIENDA', 'HAC.', 'HAC', 'HDA', 'HDA.', 'CONJUNTO HABITACIONAL',
            'CONJ HAB', 'CONJ. HAB.', 'CONJ. HAB', 'CONJ HAB.', 'CTO. HAB.', 'CTO. HAB', 'C. HAB', 'C. HAB.', 'C.H.', 'CH', 'C H', 'ZONA MILITAR', 'Z. MIL.', 'Z MIL.', 'ZN. MIL.', 'Z. MILITAR', 'Z. COMERCIAL', 'PUERTO', 'PTO.',
            'PTO', 'CONGREGACIÓN', 'CONGREG.', 'EXHACIENDA', 'EXHDA', 'EXHDA.', 'EXHAC', 'ZONA NAVAL', 'ZN. NAVAL', 'Z. N.', 'ZN NAVAL', 'ZN. NAV.', 'FINCA', 'FCA.', 'PARQUE INDUSTRIAL', 'PAR. IND.', 'PAR IND', 'PARQ. INDUST.',
            'PARQ INDUST', 'POBLADO COMUNAL', 'POB. COMUNAL', 'PB COM', 'PB. COM.', 'P. COMUNAL']

        if pd.isnull(row_dict[header]):
            return ""
        else:
            model_data = {field_name: row_dict[header]}
            if field_name == 'asentamiento':
                self.__settlement = model_data['asentamiento']
                pattern = r'\b(?:' + '|'.join(re.escape(word) for word in WORDS_TO_DELETE) + r')\b'
                self.__settlement = re.sub(pattern, '', self.__settlement, flags=re.IGNORECASE).strip()
            if field_name == 'codigo_postal':
                normalized_settlement = unidecode(self.__settlement)
                zip_code = model_data['codigo_postal']
                zip_code_object = CodigoPostal.objects.filter(Q(codigo_postal=zip_code) & Q(asentamiento_normalizado__icontains=normalized_settlement)).first()
                if zip_code_object:
                    model_data[field_name] = zip_code_object
                    zip_code, self.__settlement = None, None
                    return model_data
                else:
                    return ""
            return model_data

    @staticmethod
    def __handle_employment(row_dict: dict, header: str) -> dict:
        if pd.isnull(row_dict[header]):
            return ""
        else:
            employment_text = row_dict[header]
            if Ocupacion.objects.filter(subarea__icontains=employment_text).exists():
                employment_object = Ocupacion.objects.get(subarea__icontains=employment_text)
                return {'ocupacion': employment_object}
            else:
                return ""

    @staticmethod
    def __handle_choices(row_dict: dict, header: str, choice_dict: dict, field_name: str) -> dict:
        if pd.isnull(row_dict[header]):
            return ""
        else:
            choice_text = row_dict[header].upper()
            choice_number = choice_dict.get(choice_text)
            return {field_name: choice_number} if choice_number is not None else ""

    def __handle_dates(self, row_dict: dict, header: str) -> dict:
        if pd.isnull(row_dict[header]):
            return ""
        else:
            date_str = row_dict[header]
            model_name, field_name = self.__get_models_and_fields_from_csv(header)
            try:
                date = parser.parse(date_str, dayfirst=True)
                return {field_name: date.strftime('%Y-%m-%d')}
            except ValueError:
                print("La fecha ingresada no tiene un formato reconocible.")
                return ""

    @staticmethod
    def __add_model_data_to_row_data_dict(model_data: dict, model_name: str, row_data_dict: dict):
        if model_data is not None:
            if model_name not in row_data_dict:
                row_data_dict[model_name] = []
            row_data_dict[model_name].append(model_data)

    def __store_row_data_in_models_data_dict(self, row_num: any, row_data_dict: dict):
        self.__models_data[row_num] = row_data_dict

    def __populate_dictionary_in_database(self):
        self.__populate_client_data_in_database()
        self.__populate_employee_data_in_database()

    @transaction.atomic
    def __populate_client_data_in_database(self):
        for row_num, row_data in self.__models_data.items():
            try:
                cliente_data_list = row_data.get('Cliente', [{}])
                cliente_data = self.merge_dicts(cliente_data_list)
                cliente_hash = hash(frozenset(cliente_data.items()))
                if cliente_hash not in self.created_instances:
                    cliente, created = Cliente.objects.update_or_create(**cliente_data)
                    self.created_instances[cliente_hash] = cliente

                    sede_data_list = row_data.get('Sede', [{}])
                    sede_data = self.merge_dicts(sede_data_list)
                    sede_data['cliente'] = cliente
                    sede_hash = hash(frozenset(sede_data.items()))
                    if sede_hash not in self.created_instances:
                        sede, created = Sede.objects.update_or_create(**sede_data)
                        self.created_instances[sede_hash] = sede

                    carpeta_cliente_contactos_data_list = row_data.get('CarpetaClienteContactos', [{}])
                    carpeta_cliente_contactos_data = self.merge_dicts(carpeta_cliente_contactos_data_list)
                    carpeta_cliente_contactos_data['cliente'] = cliente
                    carpeta_cliente_contactos_hash = hash(frozenset(carpeta_cliente_contactos_data.items()))
                    if carpeta_cliente_contactos_hash not in self.created_instances:
                        carpeta_cliente_contactos, created = CarpetaClienteContactos.objects.update_or_create(**carpeta_cliente_contactos_data)
                        self.created_instances[carpeta_cliente_contactos_hash] = carpeta_cliente_contactos

                    carpeta_cliente_generales_data_list = row_data.get('CarpetaClienteGenerales', [{}])
                    carpeta_cliente_generales_data = self.merge_dicts(carpeta_cliente_generales_data_list)
                    carpeta_cliente_generales_data['cliente'] = cliente
                    carpeta_cliente_generales_hash = hash(frozenset(carpeta_cliente_generales_data.items()))
                    if carpeta_cliente_generales_hash not in self.created_instances:
                        carpeta_cliente_generales, created = CarpetaClienteGenerales.objects.update_or_create(**carpeta_cliente_generales_data)
                        self.created_instances[carpeta_cliente_generales_hash] = carpeta_cliente_generales

                        domicilio_data_list = row_data.get('Domicilio', [{}])
                        domicilio_data = self.merge_dicts(domicilio_data_list)
                        domicilio_data['carpeta_cliente_generales'] = carpeta_cliente_generales
                        domicilio_hash = hash(frozenset(domicilio_data.items()))
                        if domicilio_hash not in self.created_instances:
                            domicilio, created = Domicilio.objects.update_or_create(**domicilio_data)
                            self.created_instances[domicilio_hash] = domicilio

                self.clientes[row_num] = cliente

            except Exception as e:
                logger.error(f"Error al importar los datos de la fila {row_num}: {e}")
                continue

    @transaction.atomic
    def __populate_employee_data_in_database(self):
        for row_num, row_data in self.__models_data.items():
            try:
                personal_data_list = row_data.get('Personal', [{}])
                personal_data = self.merge_dicts(personal_data_list)
                personal_data['cliente'] = self.clientes[row_num]
                personal_hash = hash(frozenset(personal_data.items()))
                if personal_hash not in self.created_instances:
                    personal, created = Personal.objects.update_or_create(**personal_data)
                    self.created_instances[personal_hash] = personal

                    curp_data_list = row_data.get('Curp', [{}])
                    curp_data = self.merge_dicts(curp_data_list)
                    curp_data['personal'] = personal
                    curp_hash = hash(frozenset(curp_data.items()))
                    if curp_hash not in self.created_instances:
                        curp, created = Curp.objects.update_or_create(**curp_data)
                        self.created_instances[curp_hash] = curp

                    rfc_data_list = row_data.get('Rfc', [{}])
                    rfc_data = self.merge_dicts(rfc_data_list)
                    rfc_data['personal'] = personal
                    rfc_hash = hash(frozenset(rfc_data.items()))
                    if rfc_hash not in self.created_instances:
                        rfc, created = Rfc.objects.update_or_create(**rfc_data)
                        self.created_instances[rfc_hash] = rfc

                    carpeta_generales_data_list = row_data.get('CarpetaGenerales', [{}])
                    carpeta_generales_data = self.merge_dicts(carpeta_generales_data_list)
                    carpeta_generales_data['personal'] = personal
                    carpeta_generales_hash = hash(frozenset(carpeta_generales_data.items()))
                    if carpeta_generales_hash not in self.created_instances:
                        carpeta_generales, created = CarpetaGenerales.objects.update_or_create(**carpeta_generales_data)
                        self.created_instances[carpeta_generales_hash] = carpeta_generales

                    carpeta_laboral_data_list = row_data.get('CarpetaLaboral', [{}])
                    carpeta_laboral_data = self.merge_dicts(carpeta_laboral_data_list)
                    carpeta_laboral_data['personal'] = personal
                    carpeta_laboral_hash = hash(frozenset(carpeta_laboral_data.items()))
                    if carpeta_laboral_hash not in self.created_instances:
                        # Intenta obtener la instancia existente de CarpetaLaboral
                        try:
                            carpeta_laboral = CarpetaLaboral.objects.get(**carpeta_laboral_data)
                        except CarpetaLaboral.DoesNotExist:
                            # Si no existe, crea una nueva instancia
                            carpeta_laboral, created = CarpetaLaboral.objects.get_or_create(**carpeta_laboral_data)
                        else:
                            # Si ya existe una instancia, verifica si los campos relevantes necesitan actualizarse
                            if carpeta_laboral.ocupacion != carpeta_laboral_data['ocupacion']:
                                carpeta_laboral.ocupacion = carpeta_laboral_data['ocupacion']
                                carpeta_laboral.save()

                        # Agrega la instancia a self.created_instances
                        self.created_instances[carpeta_laboral_hash] = carpeta_laboral

                    representante_trabajadores_data_list = row_data.get('RepresentanteTrabajadores', [{}])
                    representante_trabajadores_data = self.merge_dicts(representante_trabajadores_data_list)
                    representante_trabajadores_data['cliente'] = self.clientes[row_num]
                    representante_trabajadores_hash = hash(frozenset(representante_trabajadores_data.items()))
                    representante_trabajadores_data['personal'] = personal
                    if representante_trabajadores_hash not in self.created_instances:
                        # Intenta obtener la instancia existente de CarpetaLaboral
                        try:
                            representante_trabajadores = RepresentanteTrabajadores.objects.get(**representante_trabajadores_data)
                        except RepresentanteTrabajadores.DoesNotExist:
                            # Si no existe, crea una nueva instancia
                            representante_trabajadores, created = RepresentanteTrabajadores.objects.get_or_create(**representante_trabajadores_data)
                        else:
                            # Si ya existe una instancia, verifica si los campos relevantes necesitan actualizarse
                            if representante_trabajadores.nombre_completo != representante_trabajadores_data['nombre_completo']:
                                representante_trabajadores.nombre_completo = representante_trabajadores_data['nombre_completo']
                                representante_trabajadores.save()
                        # Agrega la instancia a self.created_instances
                        self.created_instances[representante_trabajadores_hash] = representante_trabajadores

                    evaluador_data_list = row_data.get('Evaluador', [{}])
                    evaluador_data = self.merge_dicts(evaluador_data_list)
                    evaluador_data['personal'] = personal
                    evaluador_hash = hash(frozenset(evaluador_data.items()))
                    if evaluador_hash not in self.created_instances:
                        evaluador, created = Evaluador.objects.update_or_create(**evaluador_data)
                        self.created_instances[evaluador_hash] = evaluador

                    resultado_data_list = row_data.get('Resultado', [{}])
                    resultado_data = self.merge_dicts(resultado_data_list)
                    resultado_data['personal'] = personal
                    resultado_hash = hash(frozenset(resultado_data.items()))
                    if resultado_hash not in self.created_instances:
                        resultado, created = Resultado.objects.update_or_create(**resultado_data)
                        self.created_instances[resultado_hash] = resultado

            except Exception as e:
                logger.error(f"Error al importar los datos de la fila {row_num}: {e}")
                continue

    @staticmethod
    def merge_dicts(dict_list):
        merged_dict = {}
        for dictionary in dict_list:
            merged_dict.update(dictionary)
        return merged_dict
