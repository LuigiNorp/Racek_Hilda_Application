import pandas as pd
from django.db import transaction
from data.models import (
    Cliente, Sede, DocumentosCliente, CarpetaClienteGenerales, CarpetaClientePagos, CarpetaClienteContactos, PaqueteCapacitacion, Personal, CodigoPostal, Curp, Rfc, Evaluador, Ocupacion, CarpetaLaboral, CarpetaGenerales, CarpetaDependientes,
    Dependiente, CarpetaExamenPsicologico, CarpetaExamenToxicologico, JefeMedico, MedicoOdontologico, CarpetaExamenMedico, CarpetaExamenFisico, CarpetaExamenSocioeconomico, EstructuraFamiliar, DatosFamiliar, Referencia, CarpetaExamenPoligrafo,
    MotivoSeparacion, PuestoFuncional, TipoBaja, EmpleoAnteriorSeguridadPublica, EmpleoAnterior, Instructor, Capacitacion, RepresentanteTrabajadores, Domicilio, Idioma, CarpetaMediaFiliacion, Resultado, DocumentosDigitales
)


class ModelNode:
    def __init__(self, model, parent=None):
        self.model = model
        self.parent = parent
        self.children = []

    def add_child(self, child):
        self.children.append(child)


class DataImporter:
    def __init__(self, csv_fields):
        self.csv_fields = csv_fields
        self.model_tree = {}

    def update_or_create(self, model, data):
        return model.objects.update_or_create(defaults=data, **data)

    def get_parent_model_name(self, model_name):
        # Esta función debe definirse para determinar el modelo padre basándose en el nombre del modelo
        parent_models = {
            'CarpetaClienteContactos': 'Cliente',
            'RepresentanteTrabajadores': 'Cliente',
            'CarpetaClienteGenerales': 'Cliente',
            'Domicilio': 'CarpetaClienteGenerales',
            'CodigoPostal': 'Domicilio',
            'Personal': 'Cliente',
            'Curp': 'Personal',
            'Rfc': 'Personal',
            'CarpetaLaboral': 'Personal',
            'Ocupacion': 'CarpetaLaboral',
            'CarpetaGenerales': 'Personal',
            'Evaluador': 'Personal',
            'Resultado': 'Personal',
        }
        return parent_models.get(model_name)

    def import_data_from_csv(self, file):
        try:
            for chunk in pd.read_csv(file.path, chunksize=5000):
                data = chunk.itertuples()
                with transaction.atomic():
                    for row in data:
                        created_objects = {}
                        for csv_field in self.csv_fields:
                            model_name, field_name = csv_field.split('_', 1)
                            model = globals()[model_name]
                            if model_name not in self.model_tree:
                                parent_model_name = self.get_parent_model_name(model_name)
                                parent_model_node = self.model_tree.get(parent_model_name) if parent_model_name else None
                                self.model_tree[model_name] = ModelNode(model, parent=parent_model_node)
                            model_node = self.model_tree[model_name]
                            data = {field_name: getattr(row, csv_field)}
                            if model_node.parent:
                                # Si el modelo tiene un modelo padre, incluimos el objeto padre en los datos
                                data[model_node.parent.model.__name__.lower()] = created_objects[model_node.parent.model.__name__]
                            created_objects[model_name] = self.update_or_create(model, data)

        except pd.errors.EmptyDataError:
            print("The CSV file is empty")
        except pd.errors.ParserError:
            print("There was an error reading the CSV file")
        except FileNotFoundError:
            print("The file was not found")
        except Exception as e:
            print(f"An unexpected error occurred: {e}")
