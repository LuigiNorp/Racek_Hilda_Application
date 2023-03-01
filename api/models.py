import requests
from django.core.validators import RegexValidator
from datetime import datetime
from django.db import models
from api.choices import *
from data.models import *

class Curp(models.Model):
    empleado = models.ForeignKey(Empleado, on_delete=models.CASCADE)
    curp_regex = '^[A-Z]{1}[AEIOU]{1}[A-Z]{2}[0-9]{2}(0[1-9]|1[0-2])(0[1-9]|[1-2][0-9]|3[0-1])[HM]{1}(AS|BC|BS|CC|CS|CH|CL|CM|DF|DG|GT|GR|HG|JC|MC|MN|MS|NT|NL|OC|PL|QT|QR|SP|SL|SR|TC|TS|TL|VZ|YN|ZS|NE)[B-DF-HJ-NP-TV-Z]{3}[0-9A-Z]{1}[0-9]{1}$'
    curp = models.CharField(max_length=18, blank=True, validators=[RegexValidator(curp_regex, 'La CURP no es válida')])
    nombre = models.CharField(max_length=100, blank=True, null=True)
    apellido_paterno = models.CharField(max_length=100, blank=True, null=True)
    apellido_materno = models.CharField(max_length=100, blank=True, null=True)
    iniciales = models.CharField(max_length=20, blank=True)
    fecha_nacimiento = models.DateField(blank=True, null=True)
    edad = models.PositiveIntegerField(blank=True, null=True)
    anio_registro = models.PositiveIntegerField(blank=True, null=True)
    numero_acta = models.CharField(max_length=20, blank=True, null=True)
    validacion_renapo = models.BooleanField(default=False, blank=True, null=True)
    sexo = models.CharField(max_length=1, blank=True, null=True)
    estatus_curp = models.CharField(max_length=20, blank=True, null=True)
    clave_municipio_registro = models.CharField(max_length=5, blank=True, null=True)
    municipio_registro = models.CharField(max_length=100, blank=True, null=True)
    clave_entidad_registro = models.CharField(max_length=5, blank=True, null=True)
    entidad_registro = models.CharField(max_length=100, blank=True, null=True)
    transaction_id = models.CharField(max_length=100, blank=True, null=True)

    def __str__(self):
        return f'{self.empleado} - {self.curp}: {self.nombre} {self.apellido_paterno} {self.apellido_materno} ({self.empleado})'

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

    def calcular_edad(fecha_nacimiento, fecha_referencia=None):
        if not fecha_referencia:
            fecha_referencia = datetime.now().date()
        edad = fecha_referencia.year - fecha_nacimiento.year - ((fecha_referencia.month, fecha_referencia.day) < (fecha_nacimiento.month, fecha_nacimiento.day))
        return edad
    
    def save(self, *args, **kwargs):
        if not self.id:
            # Consultar si la CURP ya existe en la base de datos
            curp_existente = Curp.objects.filter(curp=self.curp).first()
            if curp_existente:
                # Si la CURP ya existe, mostrar un mensaje y no hacer nada
                print('La CURP ya se encuentra registrada')
                return
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
                    self.fecha_nacimiento = datetime.strptime(data['birthdate'], '%d/%m/%Y')
                    self.edad = self.calcular_edad(self.fecha_nacimiento)
                    self.anio_registro = data['anioReg']
                    self.numero_acta = data['probation_document_data']['numActa']
                    self.validacion_renapo = data['renapo_valid']
                    self.sexo = data['sex']
                    estatus_curp_clave = data['status_curp']
                    estatus_curp_completo = dict(ESTATUS_CURP).get(estatus_curp_clave)
                    self.estatus_curp = estatus_curp_completo
                    self.municipio_registro = data['probation_document_data']['municipioRegistro']
                    self.clave_municipio_registro = data['probation_document_data']['claveMunicipioRegistro']
                    self.entidad_registro = data['probation_document_data']['entidadRegistro']
                    self.clave_entidad_registro = data['probation_document_data']['claveEntidadRegistro']
                    self.transaction_id = data ['transaction_id']
                else:
                    # Si la consulta a la API falló, se puede manejar el error adecuadamente
                    print(f'Error al consultar la CURP en la API: {response.status_code}')
                
                # Guardar el objeto
                super().save(*args, **kwargs)
        else:
            super().save(*args, **kwargs)

class Rfc(models.Model):
    #TODO: Make a connection with a RFC_DB
    #TODO: Function to transform Str to Date data type (Signals)
    
    def transform_api_str_to_date():
        pass

    #TODO: Function to verify RFC syntax by regex 
    def verify_rfc_syntax():
        pass

    rfc = models.CharField(max_length=13, default=verify_rfc_syntax)
    rfc_digital = models.FileField(upload_to="temp/documentos", blank=True)
    razon_social  = models.CharField(max_length=255, blank=True)
    estatus = models.CharField(max_length=20, blank=True)
    fecha_efectiva = models.DateField(blank=True, default=transform_api_str_to_date)
    correo_contacto = models.CharField(max_length=200, blank=True)
    validez = models.CharField(max_length=20, blank=True)
    tipo = models.CharField(max_length=20, blank=True)
    empleado = models.OneToOneField(Empleado, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.rfc}: {self.empleado}'
    
    class Meta:
        verbose_name_plural = 'RFC'

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
    colonia = models.OneToOneField(Colonia, on_delete=models.RESTRICT, null=True)

    def __str__(self):
        return f'{self.municipio}'
    
    class Meta:
        verbose_name_plural = 'Municipios'

class Estado(models.Model):
    estado = models.CharField(max_length=100)
    clave_estado_racek = models.PositiveIntegerField(validators=[MinValueValidator(1), MaxValueValidator(99)])
    municipio = models.OneToOneField(Municipio, on_delete=models.RESTRICT)

    def __str__(self):
        return f'{self.estado}'
    
    class Meta:
        verbose_name_plural = 'Estados'

class Pais(models.Model):
    pais = models.CharField(max_length=100, default='México')
    clave_pais_racek = models.PositiveIntegerField(validators=[MinValueValidator(1), MaxValueValidator(999)])
    estado = models.OneToOneField(Estado, on_delete=models.RESTRICT)

    def __str__(self):
        return f'{self.pais}'
    
    class Meta:
        verbose_name_plural = 'Paises'