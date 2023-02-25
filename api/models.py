import requests
from dateutil.relativedelta import relativedelta
from django.core.validators import RegexValidator
from datetime import datetime
from django.db import models
from data.models import *

"""
El problema con este código es que todavía no verifica y almacena el municipio 
ni la entidad, ni las claves, las cuales quiero que primero se verifique en Municipio, Estado.
También falta en anio_registro
"""

class Curp(models.Model):
    curp_regex = '^[A-Z]{1}[AEIOU]{1}[A-Z]{2}[0-9]{2}(0[1-9]|1[0-2])(0[1-9]|[1-2][0-9]|3[0-1])[HM]{1}(AS|BC|BS|CC|CS|CH|CL|CM|DF|DG|GT|GR|HG|JC|MC|MN|MS|NT|NL|OC|PL|QT|QR|SP|SL|SR|TC|TS|TL|VZ|YN|ZS|NE)[B-DF-HJ-NP-TV-Z]{3}[0-9A-Z]{1}[0-9]{1}$'
    curp = models.CharField(max_length=18, blank=True, validators=[RegexValidator(curp_regex, 'La CURP no es válida')])
    nombre = models.CharField(max_length=100, blank=True)
    apellido_paterno = models.CharField(max_length=100, blank=True)
    apellido_materno = models.CharField(max_length=100, blank=True)
    iniciales = models.CharField(max_length=20, blank=True)
    fecha_nacimiento = models.DateField(blank=True, null=True)
    edad = models.PositiveIntegerField(validators=[MinValueValidator(18), MaxValueValidator(99)], blank=True)
    anio_registro = models.PositiveIntegerField(blank=True, null=True)
    numero_acta = models.CharField(max_length=20, blank=True)
    validacion_renapo = models.BooleanField(default=False, blank=True)
    sexo = models.CharField(max_length=1, blank=True, choices=SEXO_OPCIONES)
    estatus_curp = models.CharField(max_length=20, blank=True, choices=(('emitida', 'Emitida'), ('vigente', 'Vigente'), ('desconocido', 'Desconocido')))
    empleado = models.OneToOneField(Empleado, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.empleado} - {self.curp}'

    def obtener_iniciales(nombre, apellido_paterno, apellido_materno)->str:
        """List of words to exclude from initials. Obtener las palabras en el nombre 
        y eliminar las excluidas. Obtain the words in the name and eliminate the excluded ones.
        Combine initials and return them

        Args:
            nombre (str): Is the name of the person in question, can be more than one name.
            apellido_paterno (str): It is the last name of the person in question, it can be more than one last name.
            apellido_materno (str): It is the second last name of the person in question, it can be more than one second last name.

        Returns:
            _type_: Returns the initials excluding words like ['y', 'de', 'la', 'el', 'las', 'los'] from the result
        """
        # List of words to exclude from initials
        excluidas = ['y', 'de', 'la', 'el', 'las', 'los']

        # Obtener las palabras en el nombre y eliminar las excluidas
        palabras_nombre = [word for word in nombre.split() if word.lower() not in excluidas]
        iniciales_nombre = ''.join([word[0] for word in palabras_nombre])
        
        # Obtain the words in the name and eliminate the excluded ones.
        palabras_apellidos = [apellido.split() for apellido in [apellido_paterno, apellido_materno]]
        palabras_apellidos = [word for apellido in palabras_apellidos for word in apellido if word.lower() not in excluidas]
        iniciales_apellidos = ''.join([word[0] for word in palabras_apellidos])
        
        # Combine initials and return them
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
                    self.estatus_curp = data['status_curp']
                else:
                    # Si la consulta a la API falló, se puede manejar el error adecuadamente
                    print(f'Error al consultar la CURP en la API: {response.status_code}')
                
                # Guardar el objeto
                super().save(*args, **kwargs)
        else:
            super().save(*args, **kwargs)


class CodigoPostal(models.Model):
    codigo_postal = models.PositiveIntegerField(validators=[MinValueValidator(1), MaxValueValidator(99999)])
    domicilio = models.OneToOneField(Domicilio, on_delete=models.RESTRICT)

    def __str__(self):
        return f'{self.codigo_postal}'
    
    class Meta:
        verbose_name_plural = 'Codigos Postales'

class Colonia(models.Model):
    colonia = models.CharField(max_length=100)
    codigo_postal = models.ForeignKey(CodigoPostal, on_delete=models.RESTRICT)

    def __str__(self):
        return f'{self.colonia}'
    
    class Meta:
        verbose_name_plural = 'Colonias'

class Municipio(models.Model):
    municipio = models.CharField(max_length=100)
    clave_municipio_racek = models.PositiveIntegerField(validators=[MinValueValidator(1), MaxValueValidator(9999)])
    clave_municipio_api_curp = models.CharField(max_length=3)
    colonia = models.OneToOneField(Colonia, on_delete=models.RESTRICT, null=True)
    curp = models.OneToOneField(Curp, on_delete=models.RESTRICT, null=True)

    def __str__(self):
        return f'{self.municipio}'
    
    class Meta:
        verbose_name_plural = 'Municipios'

class Estado(models.Model):
    estado = models.CharField(max_length=100)
    clave_estado_racek = models.PositiveIntegerField(validators=[MinValueValidator(1), MaxValueValidator(99)])
    clave_num_estado_api_curp = models.PositiveIntegerField(validators=[MinValueValidator(1), MaxValueValidator(99)])
    clave_txt_estado_api_curp = models.CharField(max_length=11)
    municipio = models.OneToOneField(Municipio, on_delete=models.RESTRICT)

    def __str__(self):
        return f'{self.estado}'
    
    class Meta:
        verbose_name_plural = 'Estados'

class Pais(models.Model):
    pais = models.CharField(max_length=100, default='México')
    clave_pais_racek = models.PositiveIntegerField(validators=[MinValueValidator(1), MaxValueValidator(999)])
    clave_pais_api_curp = models.PositiveIntegerField(validators=[MinValueValidator(1), MaxValueValidator(999)])
    estado = models.OneToOneField(Estado, on_delete=models.RESTRICT)

    def __str__(self):
        return f'{self.pais}'
    
    class Meta:
        verbose_name_plural = 'Paises'