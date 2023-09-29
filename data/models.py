from .choices import *
from django.db import models
from django.core.validators import RegexValidator
from django.core.validators import MinValueValidator, MaxValueValidator
from django.utils import timezone
import os

def get_upload_path(instance, filename):
    cliente_nombre = instance.personal.cliente.nombre_comercial
    modelo = instance.__class__.__name__
    return os.path.join('Documentos', cliente_nombre, modelo, filename)



# Create your models here.
class Curp(models.Model):
    # Implementar Curp Api desde Frontend
    curp_regex = r'^[A-Z]{1}[AEIOU]{1}[A-Z]{2}[0-9]{2}(0[1-9]|1[0-2])(0[1-9]|[1-2][0-9]|3[0-1])[HM]{1}(AS|BC|BS|CC|CS|CH|CL|CM|DF|DG|GT|GR|HG|JC|MC|MN|MS|NT|NL|OC|PL|QT|QR|SP|SL|SR|TC|TS|TL|VZ|YN|ZS|NE)[B-DF-HJ-NP-TV-Z]{3}[0-9A-Z]{1}[0-9]{1}$'
    curp = models.CharField(max_length=18, blank=True, unique=True,
                            validators=[RegexValidator(curp_regex, 'La CURP no es válida')])
    nombre = models.CharField(max_length=100)
    apellido_paterno = models.CharField(max_length=100)
    apellido_materno = models.CharField(max_length=100)
    iniciales = models.CharField(max_length=20, blank=True, null=True)
    fecha_nacimiento = models.DateField(blank=True)
    edad = models.PositiveIntegerField(blank=True, null=True)
    anio_registro = models.PositiveIntegerField(blank=True, null=True)
    numero_acta = models.CharField(max_length=20, blank=True, null=True)
    validacion_renapo = models.BooleanField(default=False, blank=True, null=True)
    sexo = models.CharField(max_length=10)
    estatus_curp = models.CharField(max_length=20, choices=ESTATUS_CURP, blank=True, null=True)
    clave_municipio_registro = models.CharField(max_length=5, blank=True, null=True)
    municipio_registro = models.CharField(max_length=100, blank=True, null=True)
    clave_entidad_registro = models.CharField(max_length=5, blank=True, null=True)
    entidad_registro = models.CharField(max_length=100, blank=True, null=True)
    transaction_id = models.CharField(max_length=100, blank=True, null=True)

    def obtener_iniciales(self):
        """Obtiene las iniciales del nombre y apellidos de la persona.

        Returns:
            str: Iniciales del nombre y apellidos de la persona.
        """
        # Obtenemos las iniciales de cada palabra en el nombre y apellidos
        iniciales_nombre = ''.join([nombre[0] for nombre in self.nombre.split()])
        iniciales_apellido_paterno = ''.join([apellido[0] for apellido in self.apellido_paterno.split()])
        iniciales_apellido_materno = ''.join([apellido[0] for apellido in self.apellido_materno.split()])
        # Concatenamos las iniciales
        iniciales = f"{iniciales_nombre}{iniciales_apellido_paterno}{iniciales_apellido_materno}"
        return iniciales

    def calcular_edad(self):
        """
        Calcula la edad de la persona a partir de su fecha de nacimiento.
        """
        today = timezone.now().date()
        age = today.year - self.fecha_nacimiento.year
        if (today.month, today.day) < (self.fecha_nacimiento.month, self.fecha_nacimiento.day):
            age -= 1
        return age

    def sexo_en_un_caracter(self):
        if self.sexo.upper() in ["HOMBRE", "MASCULINO", "H", "h"]:
            sexo = "H"
        elif self.sexo.upper() in ["MUJER", "FEMENINO", "M", "m"]:
            sexo = "M"
        elif self.sexo.upper() in ["NO BINARIO", "X", "x"]:
            sexo = "X"
        else:
            sexo = "UNKNOWN"
        return sexo

    def save(self, *args, **kwargs):
        self.iniciales = self.obtener_iniciales()
        self.edad = self.calcular_edad()
        self.sexo = self.sexo_en_un_caracter()

        # Llamamos al método save() original del modelo
        super().save(*args, **kwargs)

    def __str__(self):
        return f'{self.curp}: {self.nombre} {self.apellido_paterno} {self.apellido_materno})'

    class Meta:
        verbose_name_plural = 'CURP'


class Rfc(models.Model):
    # Hacer conexiones con API RFC desde FrontEnd

    rfc_regex = r'^[A-Za-z]{3,4}(\d{6})([A-Za-z]\d{2}|(\D|\d){3})?$'
    rfc = models.CharField(max_length=13, validators=[RegexValidator(rfc_regex, 'El RFC ingresado no es válido')])
    rfc_digital = models.FileField(upload_to=get_upload_path, blank=True, unique=True)
    razon_social = models.CharField(max_length=255, blank=True, null=True)
    estatus = models.CharField(max_length=20, blank=True, null=True)
    fecha_efectiva = models.DateField(blank=True, null=True)
    correo_contacto = models.CharField(max_length=200, blank=True, null=True)
    validez = models.CharField(max_length=20, blank=True, null=True)
    tipo = models.CharField(max_length=20, blank=True, null=True)

    def __str__(self):
        return f'{self.rfc}'

    class Meta:
        verbose_name_plural = 'RFC'


class Pais(models.Model):
    pais = models.CharField(max_length=100, default='México')
    clave_pais_racek = models.CharField(max_length=4, blank=True, null=True)

    def __str__(self):
        return f'{self.pais}'

    class Meta:
        verbose_name_plural = 'Paises'


class Estado(models.Model):
    estado = models.CharField(max_length=100)
    clave_estado_racek = models.CharField(max_length=2, blank=True, null=True)
    pais = models.OneToOneField(Pais, on_delete=models.RESTRICT)

    def __str__(self):
        return f'{self.estado}'

    class Meta:
        verbose_name_plural = 'Estados'


class Municipio(models.Model):
    municipio = models.CharField(max_length=100)
    clave_municipio_racek = models.CharField(max_length=4, blank=True, null=True)
    estado = models.OneToOneField(Estado, on_delete=models.RESTRICT, null=True)

    def __str__(self):
        return f'{self.municipio}'

    class Meta:
        verbose_name_plural = 'Municipios'


class Colonia(models.Model):
    colonia = models.CharField(max_length=100)
    municipio = models.ForeignKey(Municipio, on_delete=models.RESTRICT)

    def __str__(self):
        return f'{self.colonia}'

    class Meta:
        verbose_name_plural = 'Colonias'


class CodigoPostal(models.Model):
    codigo_postal = models.CharField(max_length=5, blank=True, null=True)
    colonia = models.OneToOneField(Colonia, on_delete=models.RESTRICT)

    def __str__(self):
        return f'{self.codigo_postal}'

    class Meta:
        verbose_name_plural = 'Codigos Postales'


class Domicilio(models.Model):
    calle = models.CharField(max_length=100)
    numero_exterior = models.CharField(max_length=20)
    numero_interior = models.CharField(max_length=20, blank=True, null=True)
    entre_calle = models.CharField(max_length=100, null=True, blank=True)
    y_calle = models.CharField(max_length=100, null=True, blank=True)
    ciudad = models.CharField(max_length=50)
    colonia = models.OneToOneField(Colonia, on_delete=models.RESTRICT)
    municipio = models.OneToOneField(Municipio, on_delete=models.RESTRICT)
    estado = models.OneToOneField(Estado, on_delete=models.RESTRICT, null=True)
    codigo_postal = models.OneToOneField(CodigoPostal, on_delete=models.RESTRICT)
    pais = models.OneToOneField(Pais, on_delete=models.RESTRICT)

    class Meta:
        verbose_name_plural = 'Domicilios'


class Cliente(models.Model):
    nombre_comercial = models.CharField(max_length=200)
    razon_social = models.CharField(max_length=200, blank=True)
    activo = models.BooleanField(default=False, blank=True)

    def __str__(self):
        return f'{self.nombre_comercial}'

    class Meta:
        verbose_name_plural = 'Clientes'


class Sede(models.Model):
    clave_sede = models.CharField(max_length=6, blank=True, null=True)
    nombre_sede = models.CharField(max_length=100, blank=True, null=True)
    cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.clave_sede}: {self.nombre_sede}'

    class Meta:
        verbose_name_plural = 'Sedes'


class CarpetaClienteGenerales(models.Model):
    reg_estatal = models.CharField(max_length=30, blank=True)
    reg_federal = models.CharField(max_length=30, blank=True)
    rfc = models.CharField(max_length=13, blank=True)
    validador_num_telefono = RegexValidator(regex=r'^\+?1?\d{9,10}$',
                                            message='El número telefónico debe ser ingresado de la siguiente manera: "5512345678". Limitado a 10 dígitos.')
    telefono_1 = models.CharField(validators=[validador_num_telefono], max_length=17, blank=True,
                                  help_text='Ingrese número telefónico a 10 dígitos')
    telefono_2 = models.CharField(validators=[validador_num_telefono], max_length=17, blank=True,
                                  help_text='Ingrese número telefónico a 10 dígitos')
    telefono_3 = models.CharField(validators=[validador_num_telefono], max_length=17, blank=True,
                                  help_text='Ingrese número telefónico a 10 dígitos')
    representante_legal = models.CharField(max_length=300, blank=True)
    encargado_operativo = models.CharField(max_length=300, blank=True)
    encargado_rh = models.CharField(max_length=300, blank=True)
    coordinador = models.CharField(max_length=300, blank=True)
    registro_patronal = models.CharField(max_length=30, blank=True)
    cliente = models.OneToOneField(Cliente, on_delete=models.CASCADE)
    domicilio = models.OneToOneField(Domicilio, on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return f'{self.rfc}: {self.cliente}'

    class Meta:
        verbose_name_plural = 'Clientes Generales'


class CarpetaClientePagos(models.Model):
    encargado_pagos = models.CharField(max_length=150, blank=True)
    validador_num_telefono = RegexValidator(regex=r'^\+?1?\d{9,10}$',
                                            message='El número telefónico debe ser ingresado de la siguiente manera: "5512345678". Limitado a 10 dígitos.')
    telefono_oficina = models.CharField(validators=[validador_num_telefono], max_length=17, blank=True,
                                        help_text='Ingrese número telefónico a 10 dígitos')
    telefono_celular = models.CharField(validators=[validador_num_telefono], max_length=17, blank=True,
                                        help_text='Ingrese número telefónico a 10 dígitos')
    email = models.CharField(max_length=200, blank=True)
    rfc = models.CharField(max_length=13, blank=True)
    facturacion_tipo = models.PositiveSmallIntegerField(choices=FACTURACION_TIPO, blank=True)
    revision = models.CharField(max_length=50, blank=True)
    pagos = models.CharField(max_length=50, blank=True)
    factura_subtotal = models.DecimalField(max_digits=10, decimal_places=2, blank=True)
    factura_iva = models.DecimalField(max_digits=10, decimal_places=2, blank=True)
    factura_total = models.DecimalField(max_digits=10, decimal_places=2, blank=True)
    cliente = models.OneToOneField(Cliente, on_delete=models.CASCADE)
    domicilio = models.OneToOneField(Domicilio, on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return f'{self.cliente}: {self.encargado_pagos}'

    class Meta:
        verbose_name_plural = 'Clientes Pagos'


class CarpetaClienteContactos(models.Model):
    nombre_contacto = models.CharField(max_length=300)
    validador_num_telefono = RegexValidator(regex=r'^\+?1?\d{9,10}$',
                                            message='El número telefónico debe ser ingresado de la siguiente manera: "5512345678". Limitado a 10 dígitos.')
    telefono_1 = models.CharField(validators=[validador_num_telefono], max_length=17, blank=True,
                                  help_text='Ingrese número telefónico a 10 dígitos')
    telefono_2 = models.CharField(validators=[validador_num_telefono], max_length=17, blank=True,
                                  help_text='Ingrese número telefónico a 10 dígitos')
    telefono_3 = models.CharField(validators=[validador_num_telefono], max_length=17, blank=True,
                                  help_text='Ingrese número telefónico a 10 dígitos')
    puesto = models.CharField(max_length=30)
    email_1 = models.CharField(max_length=200, blank=True)
    email_2 = models.CharField(max_length=200, blank=True)
    cliente = models.OneToOneField(Cliente, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.cliente}: {self.nombre_contacto}'

    class Meta:
        verbose_name_plural = 'Clientes Contactos'


class Evaluador(models.Model):
    evaluador = models.CharField(max_length=300)

    class Meta:
        verbose_name_plural = 'Evaluadores'


class Personal(models.Model):
    folio = models.CharField(max_length=10, default='SIN FOLIO', blank=True, null=True)
    cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE)
    curp = models.OneToOneField(Curp, on_delete=models.RESTRICT, null=True)
    rfc = models.OneToOneField(Rfc, on_delete=models.RESTRICT, null=True, blank=True)
    domicilio = models.OneToOneField(Domicilio, on_delete=models.CASCADE, null=True, blank=True)
    origen = models.PositiveSmallIntegerField(choices=ORIGEN_ASPIRANTE, blank=True, null=True)
    fecha = models.DateField(auto_now=True)
    es_empleado = models.BooleanField(default=False, blank=True)
    observaciones = models.TextField(blank=True, null=True)
    resultado = models.PositiveSmallIntegerField(choices=RESULTADOS_COMPLETOS_ASPIRANTES, blank=True, null=True)
    evaluador = models.OneToOneField(Evaluador, on_delete=models.RESTRICT, null=True, blank=True, )

    def __str__(self):
        return f'{self.curp.nombre if self.curp else ""} {self.curp.apellido_materno if self.curp else ""} {self.curp.apellido_paterno if self.curp else ""}'

    class Meta:
        verbose_name_plural = 'Personal'


class Puesto(models.Model):
    nombre_puesto = models.CharField(max_length=30)

    def __str__(self):
        return f'{self.carpeta_laboral}: {self.nombre_puesto}'

    class Meta:
        verbose_name_plural = 'Puestos'


class CarpetaLaboral(models.Model):
    modalidad = models.PositiveSmallIntegerField(choices=MODALIDAD, blank=True)
    estatus_empleado = models.PositiveSmallIntegerField(choices=ESTATUS_EMPLEADO, blank=True)
    proceso_racek = models.PositiveSmallIntegerField(choices=PROCESO_RACEK, blank=True)
    fecha_atencion = models.DateField(blank=True)
    reingreso = models.BooleanField(default=False, blank=True)
    inicio_labores = models.DateField(blank=True)
    visita_domiciliaria = models.BooleanField(default=False, blank=True)
    cedula = models.DateField(blank=True)
    nivel_mando = models.PositiveSmallIntegerField(choices=NIVEL_MANDO, blank=True)
    oficina = models.CharField(max_length=30, blank=True)
    especialidad_empleo = models.CharField(max_length=35, blank=True)
    servicio = models.CharField(max_length=30, blank=True)
    rango = models.CharField(max_length=30, blank=True)
    turno = models.CharField(max_length=30, blank=True)
    division = models.CharField(max_length=35, blank=True)
    sueldo = models.DecimalField(max_digits=7, decimal_places=2, blank=True)
    funciones = models.CharField(max_length=35, blank=True)
    evaluacion = models.BooleanField(default=False, blank=True)
    integracion = models.DateField(auto_now=True)
    vigencia = models.DateField(auto_now=True)
    capacitacion = models.BooleanField(default=False, blank=True)
    ultima_actualizacion = models.DateField(auto_now=True)
    impresion = models.BooleanField(default=False, blank=True)
    # TODO: Trigger that saves TODAY DATE when you send the info to print
    fecha_impresion = models.DateField(blank=True)
    expediente = models.CharField(max_length=25, blank=True)
    cedula_federal = models.BooleanField(default=False, blank=True)
    fecha_cedula_federal = models.DateField(blank=True)
    cedula_cdmx = models.BooleanField(default=False, blank=True)
    fecha_cedula_cdmx = models.DateField(blank=True)
    evaluacion_federal = models.BooleanField(default=False, blank=True)
    fecha_evaluacion_federal = models.DateField(blank=True)
    evaluacion_cdmx = models.BooleanField(default=False, blank=True)
    fecha_evaluacion_cdmx = models.DateField(blank=True)
    evaluacion_sedena = models.BooleanField(default=False, blank=True)
    fecha_evaluacion_sedena = models.DateField(blank=True)
    registro_estatal = models.PositiveSmallIntegerField(choices=ESTADO_REGISTROS, blank=True)
    fecha_registro_estatal = models.DateField(blank=True)
    oficio_registro_estatal = models.CharField(max_length=25, blank=True)
    verificacion = models.PositiveSmallIntegerField(choices=ESTADO_REGISTROS, blank=True)
    fecha_verificacion = models.DateField(blank=True)
    registro_dgsp = models.PositiveSmallIntegerField(choices=ESTADO_REGISTROS, blank=True)
    fecha_registro_dgsp = models.DateField(blank=True)
    oficio_registro_dgsp = models.CharField(max_length=25, blank=True)
    registro_sedena = models.PositiveSmallIntegerField(choices=ESTADO_REGISTROS, blank=True)
    fecha_registro_sedena = models.DateField(blank=True)
    oficio_registro_sedena = models.CharField(max_length=25, blank=True)
    lic_part_col = models.CharField(max_length=25, blank=True)
    comentarios = models.TextField(blank=True, null=True)
    personal = models.OneToOneField(Personal, on_delete=models.CASCADE)
    puesto = models.OneToOneField(Puesto, on_delete=models.RESTRICT)

    def __str__(self):
        return f'{self.personal}: {self.proceso_racek}'

    class Meta:
        verbose_name_plural = 'Carpetas Laborales'


class CarpetaGenerales(models.Model):
    personal = models.OneToOneField(Personal, on_delete=models.CASCADE)
    email_empleado = models.CharField(max_length=200, blank=True)
    validador_num_telefono = RegexValidator(regex=r'^\+?1?\d{9,10}$',
                                            message='El número telefónico debe ser ingresado de la siguiente manera: "5512345678". Limitado a 10 dígitos.')
    telefono_domicilio = models.CharField(validators=[validador_num_telefono], max_length=17, blank=True,
                                          help_text='Ingrese número telefónico a 10 dígitos')
    telefono_celular = models.CharField(validators=[validador_num_telefono], max_length=17, blank=True,
                                        help_text='Ingrese número telefónico a 10 dígitos')
    telefono_recados = models.CharField(validators=[validador_num_telefono], max_length=17, blank=True,
                                        help_text='Ingrese número telefónico a 10 dígitos')
    numero_elemento = models.PositiveIntegerField(blank=True)
    transporte = models.CharField(max_length=50, blank=True)
    tiempo_trayecto = models.CharField(max_length=15, blank=True, null=True)
    estado_civil = models.PositiveSmallIntegerField(choices=EDO_CIVIL, blank=True)
    estado_cartilla = models.PositiveSmallIntegerField(choices=ESTADO_CARTILLA, blank=True)
    clave_cartilla = models.CharField(max_length=18, blank=True)
    cuip = models.CharField(max_length=20, blank=True)
    clave_ine = models.CharField(max_length=20, blank=True)
    folio = models.CharField(max_length=20, blank=True)
    nss = models.CharField(max_length=15, blank=True)
    pasaporte = models.CharField(max_length=20, blank=True)
    escolaridad = models.PositiveSmallIntegerField(choices=ESCOLARIDAD, blank=True)
    escuela = models.CharField(max_length=200, blank=True)
    especialidad_escuela = models.CharField(max_length=50, blank=True)
    cedula_profesional = models.CharField(max_length=20, blank=True)
    registro_sep = models.BooleanField(default=False, blank=True)
    anio_inicio_escolaridad = models.DateField(blank=True)
    anio_termino_escolaridad = models.DateField(blank=True)
    comprobante_estudios = models.PositiveSmallIntegerField(choices=COMPROBANTE_ESTUDIOS, blank=True)
    folio_certificado = models.CharField(max_length=20, blank=True)
    promedio = models.DecimalField(max_digits=3, decimal_places=2, blank=True)
    antecedentes = models.PositiveSmallIntegerField(choices=ANTECEDENTES, blank=True)
    sabe_conducir = models.BooleanField(default=False, blank=True)
    licencia_conducir = models.CharField(max_length=20, blank=True)
    alergias = models.CharField(max_length=30, blank=True)
    inicio_trabajo = models.DateField(blank=True)
    fin_trabajo = models.DateField(blank=True)

    def __str__(self):
        return f'{self.personal.curp.nombre} {self.personal.curp.apellido_paterno} {self.personal.curp.apellido_materno}'

    class Meta:
        verbose_name_plural = 'Carpetas Generales'


class CarpetaReferencias(models.Model):
    personal = models.OneToOneField(Personal, on_delete=models.CASCADE)

    class Meta:
        verbose_name_plural = 'Carpeta Referencias'


class Referencia(models.Model):
    tipo_referencia = models.PositiveSmallIntegerField(choices=TIPO_REFERENCIA, blank=True)
    nombre = models.CharField(max_length=100)
    apellido_paterno = models.CharField(max_length=100)
    apellido_materno = models.CharField(max_length=100)
    sexo = models.PositiveSmallIntegerField(choices=SEXO_OPCIONES, blank=True)
    ocupacion = models.PositiveSmallIntegerField(choices=OCUPACION, blank=True)
    parentesco = models.PositiveSmallIntegerField(choices=PARENTESCO, blank=True)
    tiempo_de_conocerse = models.CharField(max_length=30, blank=True)
    direccion = models.CharField(max_length=100, blank=True)
    codigo_postal = models.CharField(max_length=5, blank=True, null=True)
    validador_num_telefono = RegexValidator(regex=r'^\+?1?\d{9,10}$',
                                            message='El número telefónico debe ser ingresado de la siguiente manera: "5512345678". Limitado a 10 dígitos.')
    telefono_contacto = models.CharField(validators=[validador_num_telefono], max_length=17, blank=True,
                                         help_text='Ingrese número telefónico a 10 dígitos')
    opinion = models.TextField(blank=True, null=True)
    carpeta_referencia = models.ForeignKey(CarpetaReferencias, on_delete=models.CASCADE)
    domicilio = models.OneToOneField(Domicilio, on_delete=models.CASCADE, null=True, blank=True)

    class Meta:
        verbose_name_plural = 'Referencias'


class CarpetaDependientes(models.Model):
    vive_con_familia = models.BooleanField(default=False, blank=True)
    cantidad_dependientes_economicos = models.CharField(max_length=3, blank=True, null=True)
    cantidad_hijos = models.CharField(max_length=3, blank=True, null=True)
    personal = models.OneToOneField(Personal, on_delete=models.CASCADE)

    class Meta:
        verbose_name_plural = 'Carpeta Dependientes'


class Dependiente(models.Model):
    nombre = models.CharField(max_length=100, blank=True)
    apellido_paterno = models.CharField(max_length=100, blank=True)
    apellido_materno = models.CharField(max_length=100, blank=True)
    sexo = models.PositiveSmallIntegerField(choices=SEXO_OPCIONES, blank=True)
    fecha_nacimiento = models.DateField(blank=True)
    parentesco = models.PositiveSmallIntegerField(choices=PARENTESCO, blank=True)
    actividad = models.PositiveSmallIntegerField(choices=ACTIVIDAD, blank=True)
    comentarios = models.TextField(blank=True, null=True)
    carpeta_dependientes = models.ForeignKey(CarpetaDependientes, on_delete=models.CASCADE)

    class Meta:
        verbose_name_plural = 'Dependientes'


class CarpetaExamenPsicologico(models.Model):
    fecha_examen = models.DateField(auto_now=True, blank=True)
    actitud = models.PositiveSmallIntegerField(choices=OPCIONES_PSICOLOGICO, blank=True)
    inteligencia = models.PositiveSmallIntegerField(choices=OPCIONES_PSICOLOGICO, blank=True)
    personalidad = models.PositiveSmallIntegerField(choices=OPCIONES_PSICOLOGICO, blank=True)
    impulsividad = models.PositiveSmallIntegerField(choices=OPCIONES_PSICOLOGICO, blank=True)
    organizacion = models.PositiveSmallIntegerField(choices=OPCIONES_PSICOLOGICO, blank=True)
    valores = models.PositiveSmallIntegerField(choices=OPCIONES_PSICOLOGICO, blank=True)
    temperamento = models.PositiveSmallIntegerField(choices=OPCIONES_PSICOLOGICO, blank=True)
    confiabilidad = models.PositiveSmallIntegerField(choices=OPCIONES_PSICOLOGICO, blank=True)
    compromiso = models.PositiveSmallIntegerField(choices=OPCIONES_PSICOLOGICO, blank=True)
    habilidades_laborales = models.PositiveSmallIntegerField(choices=OPCIONES_PSICOLOGICO, blank=True)
    resultado_psicologico = models.PositiveSmallIntegerField(choices=RESULTADO_PSICOLOGICO, blank=True)
    resultado_aspirante = models.PositiveSmallIntegerField(choices=RESULTADOS_COMPLETOS_ASPIRANTES, blank=True,
                                                           null=True)
    observacion = models.TextField(blank=True, null=True)
    personal = models.OneToOneField(Personal, on_delete=models.CASCADE)

    class Meta:
        verbose_name_plural = 'Carpeta Examen Psicológico'


class CarpetaExamenToxicologico(models.Model):
    fecha_examen = models.DateField(auto_now=True, blank=True)
    cocaina = models.BooleanField(blank=True, default=False)
    marihuana = models.BooleanField(blank=True, default=False)
    opiaceos = models.BooleanField(blank=True, default=False)
    anfetaminas = models.BooleanField(blank=True, default=False)
    metanfetaminas = models.BooleanField(blank=True, default=False)
    barbituricos = models.BooleanField(blank=True, default=False)
    benzodiacepinas = models.BooleanField(blank=True, default=False)
    resultado_toxicologico = models.BooleanField(blank=True, default=False)
    resultado_aspirante = models.PositiveSmallIntegerField(choices=RESULTADO_TOXICOLOGICO_ASPIRANTE, blank=True,
                                                           null=True)
    observacion = models.TextField(blank=True, null=True)
    personal = models.OneToOneField(Personal, on_delete=models.CASCADE)

    class Meta:
        verbose_name_plural = 'Carpeta Examen Toxicológico'


class CarpetaExamenMedico(models.Model):
    fecha_examen = models.DateField(blank=True, null=True)
    medico_agudeza_visual = models.CharField(max_length=100, blank=True, null=True)
    medico_agudeza_auditiva = models.CharField(max_length=100, blank=True, null=True)
    medico_agudeza_motriz = models.CharField(max_length=100, blank=True, null=True)
    medico_estado_nutricional = models.CharField(max_length=100, blank=True, null=True)
    medico_diagnostico_musculo_esqueletico = models.CharField(max_length=100, blank=True, null=True)
    medico_cardiologico = models.CharField(max_length=100, blank=True, null=True)
    medico_pulmonar = models.CharField(max_length=100, blank=True, null=True)
    medico_odontologico = models.CharField(max_length=100, blank=True, null=True)
    medico_resultado = models.CharField(max_length=100, blank=True, null=True)
    ishihara_visual_oi = models.CharField(max_length=10, blank=True, null=True)
    ishihara_visual_od = models.CharField(max_length=10, blank=True, null=True)
    ishihara_visual_ao = models.CharField(max_length=10, blank=True, null=True)
    ishihara_lentes = models.CharField(max_length=10, blank=True, null=True)
    ishihara_deuteranopia = models.CharField(max_length=30, blank=True, null=True)
    ishihara_protanopia = models.CharField(max_length=30, blank=True, null=True)
    ishihara_tritanopia = models.CharField(max_length=30, blank=True, null=True)
    ishihara_acromatopsia = models.CharField(max_length=30, blank=True, null=True)
    ishihara_resultado = models.CharField(max_length=100, blank=True, null=True)
    resultado_aspirante = models.PositiveSmallIntegerField(choices=RESULTADOS_COMPLETOS_ASPIRANTES, blank=True,
                                                           null=True)
    observacion = models.TextField(blank=True, null=True)
    personal = models.OneToOneField(Personal, on_delete=models.CASCADE)

    class Meta:
        verbose_name_plural = 'Carpeta Examen Médico'


class CarpetaExamenFisico(models.Model):
    """
    Todas las evaluaciones dentro del examen físico usan la escala:
        Baja: 1-3
        Media: 4-6
        Alta: 7-10
    """
    fecha_examen = models.DateField(blank=True)
    elasticidad = models.PositiveIntegerField(validators=[MinValueValidator(0), MaxValueValidator(10)], blank=True,
                                              default=0)
    velocidad = models.PositiveIntegerField(validators=[MinValueValidator(0), MaxValueValidator(10)], blank=True,
                                            default=0)
    resistencia = models.PositiveIntegerField(validators=[MinValueValidator(0), MaxValueValidator(10)], blank=True,
                                              default=0)
    condicion_fisica = models.PositiveIntegerField(validators=[MinValueValidator(0), MaxValueValidator(10)], blank=True,
                                                   default=0)
    reflejos = models.PositiveIntegerField(validators=[MinValueValidator(0), MaxValueValidator(10)], blank=True,
                                           default=0)
    locomocion = models.PositiveIntegerField(validators=[MinValueValidator(0), MaxValueValidator(10)], blank=True,
                                             default=0)
    prueba_esfuerzo = models.PositiveIntegerField(validators=[MinValueValidator(0), MaxValueValidator(10)], blank=True,
                                                  default=0)
    resultado = models.CharField(max_length=100, blank=True, null=True)
    resultado_aspirante = models.PositiveSmallIntegerField(choices=RESULTADOS_COMPLETOS_ASPIRANTES, blank=True,
                                                           null=True)
    observacion = models.TextField(blank=True, null=True)
    personal = models.OneToOneField(Personal, on_delete=models.CASCADE)

    class Meta:
        verbose_name_plural = 'Carpeta Examen Físico'


class CarpetaExamenSocioeconomico(models.Model):
    propiedades = models.CharField(max_length=200, blank=True, null=True)
    inversiones = models.CharField(max_length=200, blank=True, null=True)
    vehiculo = models.CharField(max_length=200, blank=True, null=True)
    tarjetas_credito_departamental = models.CharField(max_length=200, blank=True, null=True)
    adeudos_importantes = models.CharField(max_length=200, blank=True, null=True)
    tipo_domicilio = models.PositiveSmallIntegerField(choices=TIPO_DOMICILIO, blank=True, null=True)
    titular_domicilio = models.CharField(max_length=300, blank=True, null=True)
    tipo_vivienda = models.PositiveSmallIntegerField(choices=TIPO_VIVIENDA, blank=True, null=True)
    anios_residencia = models.CharField(max_length=10, blank=True, null=True)
    niveles = models.CharField(max_length=4, blank=True, null=True)
    cuartos = models.CharField(max_length=5, blank=True, null=True)
    banos = models.CharField(max_length=3, blank=True, null=True)
    patios = models.CharField(max_length=3, blank=True, null=True)
    material_paredes = models.PositiveSmallIntegerField(choices=MATERIAL_PAREDES, blank=True, null=True)
    material_pisos = models.PositiveSmallIntegerField(choices=MATERIAL_PISOS, blank=True, null=True)
    material_techos = models.PositiveSmallIntegerField(choices=MATERIAL_TECHOS, blank=True, null=True)
    mobiliario_vivienda = models.PositiveSmallIntegerField(choices=MOBILIARIO_VIVIENDA, blank=True, null=True)
    television = models.BooleanField(blank=True, default=False)
    estereo = models.BooleanField(blank=True, default=False)
    dvd = models.BooleanField(blank=True, default=False)
    estufa = models.BooleanField(blank=True, default=False)
    horno_microondas = models.BooleanField(blank=True, default=False)
    lavadora = models.BooleanField(blank=True, default=False)
    refrigerador = models.BooleanField(blank=True, default=False)
    computadora = models.BooleanField(blank=True, default=False)
    internet = models.BooleanField(blank=True, default=False)
    tv_paga = models.BooleanField(blank=True, default=False)
    personal = models.OneToOneField(Personal, on_delete=models.CASCADE)
    gasto_diario = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    familiar_adicional = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True, default=0)
    importe_interesado = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True, default=0)
    parentesco_familiar_1 = models.CharField(max_length=35, null=True, blank=True)
    importe_familiar_1 = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True, default=0)
    parentesco_familiar_2 = models.CharField(max_length=35, null=True, blank=True)
    importe_familiar_2 = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True, default=0)
    parentesco_familiar_3 = models.CharField(max_length=35, null=True, blank=True)
    importe_familiar_3 = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True, default=0)
    parentesco_familiar_4 = models.CharField(max_length=35, null=True, blank=True)
    importe_familiar_4 = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True, default=0)
    # La suma del total de ingresos se hará desde frontend
    total_ingresos = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    egresos_alimentacion = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True, default=0)
    egresos_renta = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True, default=0)
    egresos_agua = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True, default=0)
    egresos_electricidad = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True, default=0)
    egresos_gas = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True, default=0)
    egresos_telefono = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True, default=0)
    egresos_transporte = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True, default=0)
    egresos_educacion = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True, default=0)
    egresos_adeudos = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True, default=0)
    egresos_otros = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True, default=0)
    # La suma del total de egresos se hará desde frontend
    total_egresos = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    salud_alergias = models.CharField(max_length=100, blank=True, null=True)
    salud_visual_auditiva_fisica = models.CharField(max_length=100, blank=True, null=True)
    salud_cirugias = models.CharField(max_length=100, blank=True, null=True)
    salud_enfermedad_cronica = models.CharField(max_length=100, blank=True, null=True)
    cigarro = models.BooleanField(blank=True, default=False, null=True)
    cantidad_frecuencia_ciqarro = models.CharField(max_length=100, blank=True, null=True)
    alcohol = models.BooleanField(blank=True, default=False, null=True)
    cantidad_frecuencia_alcohol = models.CharField(max_length=100, blank=True, null=True)
    vicios = models.CharField(max_length=100, blank=True, null=True)
    atencion_medica_familiares = models.BooleanField(blank=True, default=False, null=True)
    at_medica_observaciones = models.CharField(max_length=100, blank=True, null=True)
    estado_salud_propio = models.CharField(max_length=100, blank=True, null=True)
    ultima_vez_enfermo = models.CharField(max_length=100, blank=True, null=True)
    embarazada = models.CharField(max_length=100, blank=True, null=True)
    contacto_emergencia = models.CharField(max_length=100, blank=True, null=True)
    validador_num_telefono = RegexValidator(regex=r'^\+?1?\d{9,10}$',
                                            message='El número telefónico debe ser ingresado de la siguiente manera: "5512345678". Limitado a 10 dígitos.')
    telefono_emergencia = models.CharField(validators=[validador_num_telefono], max_length=17, blank=True, null=True,
                                           help_text='Ingrese número telefónico a 10 dígitos')
    parentesco_contacto = models.CharField(max_length=100, blank=True, null=True)
    actividates_fin_semana = models.PositiveSmallIntegerField(choices=ACTIVIDADES_FIN_SEMANA, blank=True, null=True)
    actividades_culturales_deportes = models.CharField(max_length=100, blank=True, null=True)
    estudia = models.BooleanField(blank=True, default=False)
    que_estudia = models.CharField(max_length=100, blank=True, null=True)
    organizacion_familia = models.CharField(max_length=100, blank=True, null=True)
    comunicacion = models.CharField(max_length=100, blank=True, null=True)
    roles = models.CharField(max_length=100, blank=True, null=True)
    autoridad = models.CharField(max_length=100, blank=True, null=True)
    limites = models.CharField(max_length=100, blank=True, null=True)
    calidad_vida = models.CharField(max_length=100, blank=True, null=True)
    imagen_publica = models.CharField(max_length=100, blank=True, null=True)
    comportamiento_social = models.CharField(max_length=100, blank=True, null=True)
    demanda_laboral = models.CharField(max_length=100, blank=True, null=True)
    antecedentes_penales = models.CharField(max_length=100, blank=True, null=True)
    porque_este_empleo = models.CharField(max_length=200, blank=True, null=True)
    puesto_deseado = models.CharField(max_length=100, blank=True, null=True)
    area_deseada = models.CharField(max_length=100, blank=True, null=True)
    tiempo_ascenso = models.CharField(max_length=100, blank=True, null=True)
    obtencion_reconocimiento = models.CharField(max_length=100, blank=True, null=True)
    obtencion_ascenso = models.CharField(max_length=100, blank=True, null=True)
    capacitacion_deseada = models.CharField(max_length=100, blank=True, null=True)
    fecha_entrevista = models.DateField(blank=True, null=True)
    visitador = models.CharField(max_length=300, null=True, blank=True)
    cedula_profesional_visitador = models.CharField(max_length=30, null=True, blank=True)
    supervisor = models.CharField(max_length=300, null=True, blank=True)
    cedula_profesional_supervisor = models.CharField(max_length=30, null=True, blank=True)
    recomendable = models.PositiveSmallIntegerField(choices=RECOMENDABLE, blank=True, null=True)
    entorno_social = models.PositiveSmallIntegerField(choices=CALIF_BUENO_MALO, blank=True, null=True)
    entorno_familiar = models.PositiveSmallIntegerField(choices=CALIF_BUENO_MALO, blank=True, null=True)
    situacion_economica = models.PositiveSmallIntegerField(choices=CALIF_BUENO_MALO, blank=True, null=True)
    experiencia_laboral = models.PositiveSmallIntegerField(choices=CALIF_BUENO_MALO, blank=True, null=True)
    resultado_aspirante = models.PositiveSmallIntegerField(choices=RESULTADOS_COMPLETOS_ASPIRANTES, blank=True,
                                                           null=True)
    comentarios_generales = models.TextField(blank=True, null=True)
    ruta_acceso = models.CharField(max_length=200, blank=True, null=True)
    color_vivienda_porton = models.CharField(max_length=150, blank=True, null=True)
    referencias = models.CharField(max_length=150, blank=True, null=True)
    tiempo_traslado = models.CharField(max_length=20, blank=True, null=True)
    gasto = models.CharField(max_length=20, blank=True, null=True)
    nombre_recados = models.CharField(max_length=300, blank=True, null=True)
    parentesco = models.CharField(max_length=30, blank=True, null=True)
    nombre_recados = models.CharField(max_length=300, blank=True, null=True)
    telefono_recados = models.CharField(validators=[validador_num_telefono], max_length=17, blank=True, null=True,
                                        help_text='Ingrese número telefónico a 10 dígitos')
    comentario = models.CharField(max_length=300, blank=True, null=True)

    class Meta:
        verbose_name_plural = 'Carpeta Examen Socioeconómico'


class CarpetaExamenPoligrafo(models.Model):
    resultado_aspirante = models.PositiveSmallIntegerField(choices=RESULTADO_POLIGRAFO_ASPIRANTE, blank=True, null=True)
    observaciones = models.TextField(blank=True, null=True)
    personal = models.OneToOneField(Personal, on_delete=models.CASCADE)

    class Meta:
        verbose_name_plural = 'Carpeta Examen Polígrafo'


# Consultar con Hilda si es así
class CarpetaEmpleoAnteriorSeguridadPublica(models.Model):
    personal = models.OneToOneField(Personal, on_delete=models.CASCADE)
    domicilio = models.OneToOneField(Domicilio, on_delete=models.CASCADE, null=True, blank=True)

    class Meta:
        verbose_name_plural = 'Carpeta Empresas Anteriores Seguridad Publica'


class MotivoSeparacion(models.Model):
    motivo = models.CharField(max_length=50, blank=True, null=True)

    class Meta:
        verbose_name_plural = 'Motivos Separacion'


class PuestoFuncional(models.Model):
    nombre_puesto = models.CharField(max_length=50, blank=True, null=True)

    class Meta:
        verbose_name_plural = 'Puestos Funcionales'


class TipoBaja(models.Model):
    motivo = models.CharField(max_length=50, blank=True, null=True)

    class Meta:
        verbose_name_plural = 'Tipos Baja'


class EmpleoAnteriorSeguridadPublica(models.Model):
    dependencia = models.CharField(max_length=100, blank=True, null=True)
    corporacion = models.CharField(max_length=100, blank=True, null=True)
    direccion = models.CharField(max_length=150, blank=True, null=True)
    numero_exterior = models.CharField(max_length=20, blank=True, null=True)
    numero_interior = models.CharField(max_length=20, blank=True, null=True)
    validador_num_telefono = RegexValidator(regex=r'^\+?1?\d{9,10}$',
                                            message='El número telefónico debe ser ingresado de la siguiente manera: "5512345678". Limitado a 10 dígitos.')
    telefono = models.CharField(validators=[validador_num_telefono], max_length=17, blank=True,
                                help_text='Ingrese número telefónico a 10 dígitos')
    fecha_ingreso = models.DateField(blank=True, null=True)
    fecha_separacion = models.DateField(blank=True, null=True)
    funciones = models.CharField(max_length=100, blank=True, null=True)
    especialidad = models.CharField(max_length=50, blank=True, null=True)
    rango_categoria = models.CharField(max_length=50, blank=True, null=True)
    sueldo_base = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True, default=0)
    numero_placa = models.CharField(max_length=15, blank=True, null=True)
    numero_emp = models.CharField(max_length=15, blank=True, null=True)
    area = models.CharField(max_length=50, blank=True, null=True)
    division = models.CharField(max_length=50, blank=True, null=True)
    tipo_separacion = models.PositiveSmallIntegerField(choices=TIPO_SEPARACION, blank=True, null=True)
    jefe_inmediato = models.CharField(max_length=300, blank=True, null=True)
    cuip_jefe_inmediato = models.CharField(max_length=20, blank=True, null=True)
    comentarios = models.CharField(max_length=150, blank=True, null=True)
    carp_emp_ant_seg_pub = models.ForeignKey(CarpetaEmpleoAnteriorSeguridadPublica, on_delete=models.CASCADE)
    puesto_funcional = models.OneToOneField(PuestoFuncional, on_delete=models.RESTRICT, null=True, blank=True)
    tipo_baja = models.OneToOneField(TipoBaja, on_delete=models.RESTRICT, null=True, blank=True)
    motivo_separacion = models.OneToOneField(MotivoSeparacion, on_delete=models.RESTRICT, null=True, blank=True)

    class Meta:
        verbose_name_plural = 'Empresas Anteriores Seguridad Publica'


class CarpetaEmpleoAnterior(models.Model):
    personal = models.ForeignKey(Personal, on_delete=models.CASCADE)
    domicilio = models.OneToOneField(Domicilio, on_delete=models.CASCADE, null=True, blank=True)

    class Meta:
        verbose_name_plural = 'Carpeta Empleos Anteriores'


class EmpleoAnterior(models.Model):
    empresa = models.CharField(max_length=100, blank=True, null=True)
    validador_num_telefono = RegexValidator(regex=r'^\+?1?\d{9,10}$',
                                            message='El número telefónico debe ser ingresado de la siguiente manera: "5512345678". Limitado a 10 dígitos.')
    telefono = models.CharField(validators=[validador_num_telefono], max_length=17, blank=True,
                                help_text='Ingrese número telefónico a 10 dígitos')
    fecha_ingreso = models.DateField(blank=True, null=True)
    fecha_separacion = models.DateField(blank=True, null=True)
    salario = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True, default=0)
    area_puesto = models.CharField(max_length=50, blank=True, null=True)
    funciones = models.CharField(max_length=100, blank=True, null=True)
    tipo_separacion = models.PositiveSmallIntegerField(choices=TIPO_SEPARACION, blank=True, null=True)
    jefe_inmediato = models.CharField(max_length=300, blank=True, null=True)
    puesto_jefe_inmediato = models.CharField(max_length=50, blank=True, null=True)
    informante = models.CharField(max_length=300, blank=True, null=True)
    puesto_informante = models.CharField(max_length=50, blank=True, null=True)
    desempenio = models.PositiveSmallIntegerField(choices=CALIF_BUENO_MALO, blank=True, null=True)
    observaciones = models.TextField(blank=True, null=True)
    carp_emp_ant = models.OneToOneField(CarpetaEmpleoAnterior, on_delete=models.CASCADE)
    motivo_separacion = models.OneToOneField(MotivoSeparacion, on_delete=models.RESTRICT, null=True, blank=True)

    class Meta:
        verbose_name_plural = 'Empleos Anteriores'


class CarpetaCapacitacion(models.Model):
    personal = models.OneToOneField(Personal, on_delete=models.CASCADE)

    class Meta:
        verbose_name_plural = 'Carpeta Capacitaciones'


class Capacitacion(models.Model):
    institucion_empresa = models.CharField(max_length=100, blank=True, null=True)
    curso = models.CharField(max_length=100, blank=True, null=True)
    impartido_recibido = models.PositiveSmallIntegerField(choices=IMPARTIDO_RECIBIDO, blank=True, null=True)
    eficiencia_terminal = models.PositiveSmallIntegerField(choices=EFICIENCIA_TERMINAL, blank=True, null=True)
    inicio = models.DateField(blank=True, null=True)
    conclusion = models.DateField(blank=True, null=True)
    duracion = models.CharField(max_length=10, blank=True, null=True)
    carpeta_capacitacion = models.ForeignKey(CarpetaCapacitacion, on_delete=models.CASCADE)

    class Meta:
        verbose_name_plural = 'Capacitaciones'


class TipoCurso(models.Model):
    tipo_curso = models.CharField(max_length=100, blank=True, null=True)
    capacitacion_previa = models.OneToOneField(Capacitacion, on_delete=models.RESTRICT)

    class Meta:
        verbose_name_plural = 'Tipo Cursos'


# class CapacitacionEnCurso(models.Model):
#     estudio_curso = models.CharField(max_length=100, blank=True, null=True)
#     inicio = models.DateField(blank=True, null=True)
#     conclusion = models.DateField(blank=True, null=True)
#     duracion = models.CharField(max_length=10, blank=True, null=True)
#     carpeta_capacitacion = models.ForeignKey(CarpetaCapacitacion, on_delete=models.RESTRICT)

#     class Meta:
#         verbose_name_plural = 'Capacitaciones en Curso'

class Idioma(models.Model):
    idioma = models.CharField(max_length=50, blank=True, null=True)
    lectura = models.CharField(max_length=3, blank=True, null=True)
    escritura = models.CharField(max_length=3, blank=True, null=True)
    conversacion = models.CharField(max_length=3, blank=True, null=True)
    carpeta_capacitacion = models.ForeignKey(CarpetaCapacitacion, on_delete=models.CASCADE)


# class Habilidad(models.Model):
#     computacion = models.PositiveSmallIntegerField(choices=CALIF_BUENO_MALO, blank=True, null=True)
#     investigacion = models.PositiveSmallIntegerField(choices=CALIF_BUENO_MALO, blank=True, null=True)
#     manejo_armas = models.PositiveSmallIntegerField(choices=CALIF_BUENO_MALO, blank=True, null=True)
#     manejo_grupos = models.PositiveSmallIntegerField(choices=CALIF_BUENO_MALO, blank=True, null=True)
#     mecanica = models.PositiveSmallIntegerField(choices=CALIF_BUENO_MALO, blank=True, null=True)
#     carpinteria = models.PositiveSmallIntegerField(choices=CALIF_BUENO_MALO, blank=True, null=True)
#     conduccion_medios = models.PositiveSmallIntegerField(choices=CALIF_BUENO_MALO, blank=True, null=True)
#     carpeta_capacitacion = models.OneToOneField(CarpetaCapacitacion, on_delete=models.CASCADE)

#     class Meta:
#         verbose_name_plural = 'Habilidades'

# class HabilidadPersonalizada(models.Model):
#     nombre_habilidad = models.CharField(max_length=50, blank=True, null=True)
#     calificacion = models.PositiveSmallIntegerField(choices=CALIF_BUENO_MALO, blank=True, null=True)
#     habilidad = models.ForeignKey(Habilidad, on_delete=models.CASCADE)

#     class Meta:
#         verbose_name_plural = 'Habilidades Personalizadas'

class CarpetaMediaFiliacion(models.Model):
    tension_arterial = models.CharField(max_length=10, null=True, blank=True)
    temperatura = models.CharField(max_length=5, null=True, blank=True)
    indice_masa_corporal = models.CharField(max_length=6, null=True, blank=True)
    clasificacion_imc = models.PositiveSmallIntegerField(choices=CLASIFICACION_IMC, blank=True, null=True)
    sat02 = models.CharField(max_length=10, null=True, blank=True)
    frecuencia_cardiaca = models.CharField(max_length=6, null=True, blank=True)
    cronica_degenerativa = models.CharField(max_length=100, null=True, blank=True)
    complexion = models.PositiveSmallIntegerField(choices=COMPLEXION, blank=True)
    color_piel = models.PositiveSmallIntegerField(choices=COLOR_PIEL, blank=True)
    cara = models.PositiveSmallIntegerField(choices=CARA, blank=True)
    cabello_cantidad = models.PositiveSmallIntegerField(choices=CABELLO_CANTIDAD, blank=True)
    cabello_color = models.PositiveSmallIntegerField(choices=CABELLO_COLOR, blank=True)
    cabello_forma = models.PositiveSmallIntegerField(choices=CABELLO_FORMA, blank=True)
    cabello_calvicie = models.PositiveSmallIntegerField(choices=CABELLO_CALVICIE, blank=True)
    cabello_implantacion = models.PositiveSmallIntegerField(choices=CABELLO_IMPLANTACION, blank=True)
    frente_altura = models.PositiveSmallIntegerField(choices=TAMANIOS_GMP, blank=True)
    frente_indicacion = models.PositiveSmallIntegerField(choices=FRENTE_INCLINACION, blank=True)
    frente_ancho = models.PositiveSmallIntegerField(choices=TAMANIOS_GMP, blank=True)
    cejas_direccion = models.PositiveSmallIntegerField(choices=CEJAS_DIRECCION, blank=True)
    cejas_implantacion = models.PositiveSmallIntegerField(choices=CEJAS_IMPLANTACION, blank=True)
    cejas_forma = models.PositiveSmallIntegerField(choices=CEJAS_FORMA, blank=True)
    cejas_tamanio = models.PositiveSmallIntegerField(choices=CEJAS_TAMANIO, blank=True)
    ojos_color = models.PositiveSmallIntegerField(choices=OJOS_COLOR, blank=True)
    ojos_forma = models.PositiveSmallIntegerField(choices=OJOS_FORMA, blank=True)
    ojos_tamanio = models.PositiveSmallIntegerField(choices=OJOS_TAMANIO, blank=True)
    ojos_raiz = models.PositiveSmallIntegerField(choices=TAMANIOS_GMP, blank=True)
    nariz_dorso = models.PositiveSmallIntegerField(choices=NARIZ_DORSO, blank=True)
    nariz_ancho = models.PositiveSmallIntegerField(choices=TAMANIOS_GMP, blank=True)
    nariz_base = models.PositiveSmallIntegerField(choices=NARIZ_BASE, blank=True)
    nariz_altura = models.PositiveSmallIntegerField(choices=TAMANIOS_GMP, blank=True)
    boca_tamanio = models.PositiveSmallIntegerField(choices=TAMANIOS_GMP, blank=True)
    boca_comisuras = models.PositiveSmallIntegerField(choices=BOCA_COMISURAS, blank=True)
    labios_espesor = models.PositiveSmallIntegerField(choices=LABIOS_ESPESOR, blank=True)
    altura_nasolabial = models.PositiveSmallIntegerField(choices=TAMANIOS_GMP, blank=True)
    labios_prominencia = models.PositiveSmallIntegerField(choices=LABIOS_PROMINENCIA, blank=True)
    menton_tipo = models.PositiveSmallIntegerField(choices=MENTON_TIPO, blank=True)
    menton_forma = models.PositiveSmallIntegerField(choices=MENTON_FORMA, blank=True)
    menton_inclinacion = models.PositiveSmallIntegerField(choices=MENTON_INCLINACION, blank=True)
    oreja_derecha_forma = models.PositiveSmallIntegerField(choices=OREJA_DERECHA_FORMA, blank=True)
    oreja_derecha_original = models.PositiveSmallIntegerField(choices=TAMANIOS_GMP, blank=True)
    oreja_derecha_helix_superior = models.PositiveSmallIntegerField(choices=TAMANIOS_GMP, blank=True)
    oreja_derecha_helix_posterior = models.PositiveSmallIntegerField(choices=TAMANIOS_GMP, blank=True)
    oreja_derecha_helix_adherencia = models.PositiveSmallIntegerField(choices=OREJA_DERECHA_ADHERENCIA, blank=True)
    oreja_derecha_helix_contorno = models.PositiveSmallIntegerField(choices=OREJA_DERECHA_HELIX_CONTORNO, blank=True)
    oreja_derecha_lobulo_adherencia = models.PositiveSmallIntegerField(choices=OREJA_DERECHA_ADHERENCIA, blank=True)
    oreja_derecha_lobulo_particularidad = models.PositiveSmallIntegerField(choices=OREJA_DERECHA_LOBULO_PARTICULARIDAD,
                                                                           blank=True)
    oreja_derecha_lobulo_dimension = models.PositiveSmallIntegerField(choices=TAMANIOS_GMP, blank=True)
    sangre = models.PositiveSmallIntegerField(choices=SANGRE, blank=True)
    rh = models.PositiveSmallIntegerField(choices=RH, blank=True)
    anteojos = models.BooleanField(default=False, null=True, blank=True)
    estatura = models.CharField(max_length=15, blank=True, null=True)
    peso = models.DecimalField(max_digits=3, decimal_places=2, blank=True)
    personal = models.OneToOneField(Personal, on_delete=models.CASCADE)

    class Meta:
        verbose_name_plural = 'Carpetas Media Filiación'


class DocumentosDigitales(models.Model):
    hoja_datos = models.FileField(upload_to=get_upload_path, blank=True, null=True)
    solicitud = models.ImageField(upload_to=get_upload_path, blank=True, null=True)
    ine = models.ImageField(upload_to=get_upload_path, blank=True, null=True)
    acta_nacimiento = models.ImageField(upload_to=get_upload_path, blank=True, null=True)
    folio_acta_nacimiento = models.CharField(max_length=20, blank=True, null=True)
    huellas_digitales = models.FileField(upload_to=get_upload_path, blank=True, null=True)
    curp = models.FileField(upload_to=get_upload_path, blank=True, null=True)
    comprobante_domicilio = models.ImageField(upload_to=get_upload_path, blank=True, null=True)
    fecha_comprobante_domicilio = models.DateField(blank=True, null=True)
    antecedentes_no_penales = models.ImageField(upload_to=get_upload_path, blank=True, null=True)
    fecha_antecedentes_no_penales = models.DateField(blank=True, null=True)
    comprobante_estudios = models.ImageField(upload_to=get_upload_path, blank=True, null=True)
    cartilla_smn = models.ImageField(upload_to=get_upload_path, blank=True, null=True)
    nss = models.FileField(upload_to=get_upload_path, blank=True, null=True)
    carta_recomendacion = models.FileField(upload_to=get_upload_path, blank=True, null=True)
    contrato = models.FileField(upload_to=get_upload_path, blank=True, null=True)
    socioeconomico = models.FileField(upload_to=get_upload_path, blank=True, null=True)
    fecha_socioeconomico = models.DateField(blank=True, null=True)
    foto_socioeconomico = models.ImageField(upload_to=get_upload_path, blank=True, null=True)
    psicologico = models.FileField(upload_to=get_upload_path, blank=True, null=True)
    fecha_psicologico = models.DateField(blank=True, null=True)
    medico = models.FileField(upload_to=get_upload_path, blank=True, null=True)
    fecha_medico = models.DateField(blank=True, null=True)
    toxicologico = models.FileField(upload_to=get_upload_path, blank=True, null=True)
    fecha_toxicologico = models.DateField(blank=True, null=True)
    fisico = models.FileField(upload_to=get_upload_path, blank=True, null=True)
    fecha_fisico = models.DateField(blank=True, null=True)
    croquis = models.ImageField(upload_to=get_upload_path, blank=True, null=True)
    curriculum = models.FileField(upload_to=get_upload_path, blank=True, null=True)
    check_acta_nacimiento = models.BooleanField(default=False, blank=True)
    check_ine = models.BooleanField(default=False, blank=True)
    check_comprobante_domicilio = models.BooleanField(default=False, blank=True)
    check_comprobante_estudios = models.BooleanField(default=False, blank=True)
    check_curp = models.BooleanField(default=False, blank=True)
    check_rfc = models.BooleanField(default=False, blank=True)
    check_cartilla = models.BooleanField(default=False, blank=True)
    check_nss = models.BooleanField(default=False, blank=True)
    check_huellas_digitales = models.BooleanField(default=False, blank=True)
    check_fotografias = models.BooleanField(default=False, blank=True)
    personal = models.OneToOneField(Personal, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.personal}'

    
    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        campos_documentos = {
            'hoja_datos': self.hoja_datos,
            'solicitud': self.solicitud,
            'ine': self.ine,
            'acta_nacimiento': self.acta_nacimiento,
            'folio_acta_nacimiento': self.folio_acta_nacimiento,
            'huellas_digitales': self.huellas_digitales,
            'curp': self.curp,
            'comprobante_domicilio': self.comprobante_domicilio,
            'fecha_comprobante_domicilio': self.fecha_comprobante_domicilio,
            'antecedentes_no_penales': self.antecedentes_no_penales,
            'fecha_antecedentes_no_penales': self.fecha_antecedentes_no_penales,
            'comprobante_estudios': self.comprobante_estudios,
            'cartilla_smn': self.cartilla_smn,
            'nss': self.nss,
            'carta_recomendacion': self.carta_recomendacion,
            'contrato': self.contrato,
            'socioeconomico': self.socioeconomico,
            'fecha_socioeconomico': self.fecha_socioeconomico,
            'foto_socioeconomico': self.foto_socioeconomico,
            'psicologico': self.psicologico,
            'fecha_psicologico': self.fecha_psicologico,
            'medico': self.medico,
            'fecha_medico': self.fecha_medico,
            'toxicologico': self.toxicologico,
            'fecha_toxicologico': self.fecha_toxicologico,
            'fisico': self.fisico,
            'fecha_fisico': self.fecha_fisico,
            'croquis': self.croquis,
            'curriculum': self.curriculum,
            'check_acta_nacimiento': self.check_acta_nacimiento,
            'check_ine': self.check_ine,
            'check_comprobante_domicilio': self.check_comprobante_domicilio,
            'check_comprobante_estudios': self.check_comprobante_estudios,
            'check_curp': self.check_curp,
            'check_rfc': self.check_rfc,
            'check_cartilla': self.check_cartilla,
            'check_nss': self.check_nss,
            'check_huellas_digitales': self.check_huellas_digitales,
            'check_fotografias': self.check_fotografias,
        }

        for campo, archivo in campos_documentos.items():
            if isinstance(archivo, (models.FileField, models.ImageField)) and archivo:
                archivo.name = get_upload_path(self, archivo.name)
                super().save(update_fields=[campo])

    class Meta:
        verbose_name_plural = 'Documentos Personales'


class CapacitacionCliente(models.Model):
    estatus_capacitacion = models.PositiveSmallIntegerField(choices=ESTATUS_CAPACITACION, blank=True, null=True)
    '''
    no_elementos = models.PositiveIntegerField(validators=[MinValueValidator(0), MaxValueValidator(999999)],default=0, null=True, blank=True)
                                    checa abajo en el siguiente modelo
    '''
    fecha_solicitud = models.DateField(blank=True, null=True)
    detalle_solicitud = models.CharField(max_length=200, blank=True, null=True)
    fecha_realizacion = models.DateField(blank=True, null=True)
    detalle_realizacion = models.CharField(max_length=200, blank=True, null=True)
    fecha_entrega = models.DateField(blank=True, null=True)
    detalle_entrega = models.CharField(max_length=200, blank=True, null=True)
    fecha_facturado = models.DateField(blank=True, null=True)
    no_factura = models.CharField(max_length=200, blank=True, null=True)
    fecha_pagado = models.DateField(blank=True, null=True)
    detalle_pagado = models.CharField(max_length=200, blank=True, null=True)
    comentarios = models.TextField(blank=True, null=True)
    capacitacion = models.ManyToManyField(Capacitacion, related_name='capacitacionesencurso', blank=True)
    cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE, null=True)

    def __str__(self):
        return f'{self.pk} {self.cliente}'

    class Meta:
        verbose_name_plural = 'Capacitaciones Cliente'


class PersonalPorCapacitar(models.Model):
    # TODO: Contar numero de elementos por recibir capacitación desde FRONT-END
    resultado_capacitacion = models.PositiveSmallIntegerField(choices=RESULTADO_CAPACITACION, blank=True, null=True)
    personal = models.OneToOneField(Personal, on_delete=models.CASCADE)
    capacitacion_cliente = models.ForeignKey(CapacitacionCliente, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.personal.curp.nombre} {self.personal.curp.apellido_paterno} {self.personal.curp.apellido_materno}: {self.resultado_capacitacion}'

    class Meta:
        verbose_name_plural = 'Personal Por Capacitar'


class Capacitador(models.Model):
    nombre_capacitador = models.CharField(max_length=300, blank=True, null=True)
    numero_registro = models.CharField(max_length=14, blank=True, null=True)
    
    def __str__(self):
        return f'{self.nombre_capacitador}'
    
    class Meta:
        verbose_name_plural = 'Capacitadores'


class AreaCurso(models.Model):
    nombre_area = models.CharField(max_length=100, blank=True, null=True)
    
    def __str__(self):
        return f'{self.nombre_area}'
    
    class Meta:
        verbose_name_plural = 'Areas Curso'
        
        
class Ocupacion(models.Model):
    nombre_ocupacion = models.CharField(max_length=100, blank=True, null=True)
    
    def __str__(self):
        return f'{self.nombre_area}'
    
    class Meta:
        verbose_name_plural = 'Ocupaciones'       
