import requests
from dateutil.relativedelta import relativedelta
from django.core.validators import RegexValidator
from datetime import datetime
from django.db import models
from .models import *

class Curp(models.Model):
    empleado = models.ForeignKey(Empleado, on_delete=models.CASCADE)
    nombre = models.CharField(max_length=50, blank=True)
    apellido_paterno = models.CharField(max_length=50, blank=True)
    apellido_materno = models.CharField(max_length=50, blank=True)
    iniciales = models.CharField(max_length=15, blank=True)
    fecha_nacimiento = models.DateField(blank=True, null=True)
    edad = models.PositiveIntegerField(blank=True, null=True)
    anio_registro = models.PositiveIntegerField(blank=True, null=True)
    numero_acta = models.CharField(max_length=20, blank=True)
    validacion_renapo = models.BooleanField(default=False, blank=True)
    sexo = models.CharField(max_length=1, blank=True, choices=(('H', 'Hombre'), ('M', 'Mujer')))
    estatus_curp = models.CharField(max_length=20, blank=True, choices=(('emitida', 'Emitida'), ('vigente', 'Vigente'), ('desconocido', 'Desconocido')))
    curp_regex = '^[A-Z]{1}[AEIOU]{1}[A-Z]{2}[0-9]{2}(0[1-9]|1[0-2])(0[1-9]|[1-2][0-9]|3[0-1])[HM]{1}(AS|BC|BS|CC|CS|CH|CL|CM|DF|DG|GT|GR|HG|JC|MC|MN|MS|NT|NL|OC|PL|QT|QR|SP|SL|SR|TC|TS|TL|VZ|YN|ZS|NE)[B-DF-HJ-NP-TV-Z]{3}[0-9A-Z]{1}[0-9]{1}$'
    curp = models.CharField(max_length=18, blank=True, validators=[RegexValidator(curp_regex, 'La CURP no es válida')])

    def __str__(self):
        return f'{self.empleado} - {self.curp}'

    def obtener_iniciales(nombre, apellido_paterno, apellido_materno):
        # Lista de palabras a excluir de las iniciales
        excluidas = ['y', 'de', 'la', 'el', 'las', 'los']

        # Obtener las palabras en el nombre y eliminar las excluidas
        palabras_nombre = [word for word in nombre.split() if word.lower() not in excluidas]
        iniciales_nombre = ''.join([word[0] for word in palabras_nombre])
        
        # Obtener las palabras en los apellidos y eliminar las excluidas
        palabras_apellidos = [apellido.split() for apellido in [apellido_paterno, apellido_materno]]
        palabras_apellidos = [word for apellido in palabras_apellidos for word in apellido if word.lower() not in excluidas]
        iniciales_apellidos = ''.join([word[0] for word in palabras_apellidos])
        
        # Combinar las iniciales y retornarlas
        return iniciales_nombre + iniciales_apellidos

    def calcular_edad(fecha_nacimiento):
        hoy = datetime.now().date()
        edad = relativedelta(hoy, fecha_nacimiento).years
        return edad

    def save(self, *args, **kwargs):
        if not self.id:
            # Consultar si la CURP ya existe en la base de datos
            curp_existente = Curp.objects.filter(curp=self.curp).first()
            if curp_existente:
                # Si la CURP ya existe, llenar los campos correspondientes con los datos de la CURP existente
                self.nombre = curp_existente.nombre
                self.apellido_paterno = curp_existente.apellido_paterno
                self.apellido_materno = curp_existente.apellido_materno
                self.iniciales = curp_existente.iniciales
                self.fecha_nacimiento = curp_existente.fecha_nacimiento
                self.edad = curp_existente.edad
                self.anio_registro = curp_existente.anio_registro
                self.numero_acta = curp_existente.numero_acta
                self.validacion_renapo = curp_existente.validacion_renapo
                self.sexo = curp_existente.sexo
                self.estatus_curp = curp_existente.estatus_curp
            else:
                # Si la CURP no existe en la base de datos, buscar en la API                
                url = "https://www.curpapi.mx/api/v1/curp"
                payload = {
                    "curp": self.curp
                }
                headers = {
                    "Content-Type": "application/json",
                    "Authorization": f"TU_API_KEY" # Reemplazar TU_API_KEY por tu clave de API
                }
                response = requests.post(url, json=payload, headers=headers)

                if response.status_code == 200:
                    # Si la consulta a la API fue exitosa, llenar los campos correspondientes
                    data = response.json()
                    self.nombre = data['names']
                    self.apellido_paterno = data['paternal_surname']
                    self.apellido_materno = data['mothers_maiden_name']
                    self.iniciales = self.obtener_iniciales(data['names'], data['paternal_surname'], data['mothers_maiden_name'])
                    self.fecha_nacimiento = datetime.strptime(data['birthdate'], '%m/%d/%Y')
                    self.edad = self.calcular_edad(self.fecha_nacimiento)
                    self.anio_registro = self.fecha_nacimiento.year
                    self.numero_acta = data['probation_document_data']['numActa']
                    self.validacion_renapo = data['renapo_valid']
                    self.sexo = data['sex']
                    self.estatus_curp = 'emitida'
                else:
                    # Si la consulta a la API falló, se puede manejar el error adecuadamente
                    print(f'Error al consultar la CURP en la API: {response.status_code}')
                
                # Guardar el objeto
                super().save(*args, **kwargs)
        else:
            super().save(*args, **kwargs)
