from .choices import *
from django.db import models
from django.core.validators import RegexValidator
from django.core.validators import MinValueValidator, MaxValueValidator
# from django.utils import timezone
from django.core.files.storage import default_storage
import os
from uuid import uuid4


def get_upload_path(instance, filename):
	# Generate a unique filename using a UUID
	_, ext = os.path.splitext(filename)
	unique_filename = f"{uuid4().hex}{ext}"

	directory = ""
	if isinstance(instance, DocumentosCliente):
		# When it's a DocumentosCliente, use the cliente.nombre_comercial directly
		cliente_nombre = instance.cliente.nombre_comercial
		directory = os.path.join('Documentos', cliente_nombre, cliente_nombre)
	elif isinstance(instance, DocumentosDigitales):
		if instance.personal.curp:
			# When it's a DocumentosDigitales with a valid curp, access personal.cliente.nombre_comercial
			personal_nombre = instance.personal.curp.get_nombre_completo()
			cliente_nombre = instance.personal.cliente.nombre_comercial
			directory = os.path.join('Documentos', cliente_nombre, personal_nombre)
		else:
			# When it's a DocumentosDigitales with no curp, use a default value or directory
			cliente_nombre = instance.personal.cliente.nombre_comercial
			directory = os.path.join('Documentos', cliente_nombre, 'No Personal Name')

	# Construct the full file path
	full_path = os.path.join(directory, unique_filename)

	return full_path


# Create your models here.
class CodigoPostal(models.Model):
	codigo_postal = models.CharField(max_length=5, blank=True, null=True)
	tipo_asentamiento = models.CharField(max_length=50, blank=True, null=True)
	asentamiento = models.CharField(max_length=100, blank=True, null=True)
	municipio = models.CharField(max_length=100, blank=True, null=True)
	estado = models.CharField(max_length=50, blank=True, null=True)
	ciudad = models.CharField(max_length=100, blank=True, null=True)
	pais = models.CharField(max_length=50, default='México', blank=True, null=True)

	def __str__(self):
		return f'{self.codigo_postal}: {self.tipo_asentamiento} {self.asentamiento}, {self.municipio}, {self.estado}, {self.pais}'

	class Meta:
		verbose_name_plural = 'Codigos Postales'


class Cliente(models.Model):
	nombre_comercial = models.CharField(max_length=200)
	razon_social = models.CharField(max_length=200, null=True, blank=True)
	activo = models.BooleanField(default=False, null=True, blank=True)

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


class DocumentosCliente(models.Model):
	cliente = models.OneToOneField(Cliente, on_delete=models.CASCADE)
	qr_code = models.ImageField(upload_to=get_upload_path, blank=True, null=True)
	logotipo = models.ImageField(upload_to=get_upload_path, blank=True, null=True)


class CarpetaClienteGenerales(models.Model):
	cliente = models.OneToOneField(Cliente, on_delete=models.CASCADE)
	reg_estatal = models.CharField(max_length=30, null=True, blank=True)
	reg_federal = models.CharField(max_length=30, null=True, blank=True)
	rfc = models.CharField(max_length=13, null=True, blank=True)
	validador_num_telefono = RegexValidator(regex=r'^\+?1?\d{9,10}$', message='El número telefónico debe ser ingresado de la siguiente manera: "5512345678". Limitado a 10 dígitos.')
	telefono_1 = models.CharField(validators=[validador_num_telefono], max_length=17, blank=True, help_text='Ingrese número telefónico a 10 dígitos')
	telefono_2 = models.CharField(validators=[validador_num_telefono], max_length=17, blank=True, help_text='Ingrese número telefónico a 10 dígitos')
	telefono_3 = models.CharField(validators=[validador_num_telefono], max_length=17, blank=True, help_text='Ingrese número telefónico a 10 dígitos')
	representante_legal = models.CharField(max_length=300, null=True, blank=True)
	encargado_operativo = models.CharField(max_length=300, null=True, blank=True)
	encargado_rh = models.CharField(max_length=300, null=True, blank=True)
	coordinador = models.CharField(max_length=300, null=True, blank=True)
	registro_patronal = models.CharField(max_length=30, null=True, blank=True)

	def __str__(self):
		return f'{self.rfc}: {self.cliente}'

	class Meta:
		verbose_name_plural = 'Clientes Generales'


class CarpetaClientePagos(models.Model):
	cliente = models.OneToOneField(Cliente, on_delete=models.CASCADE)
	encargado_pagos = models.CharField(max_length=150, blank=True, null=True)
	validador_num_telefono = RegexValidator(regex=r'^\+?1?\d{9,10}$', message='El número telefónico debe ser ingresado de la siguiente manera: "5512345678". Limitado a 10 dígitos.')
	telefono_oficina = models.CharField(validators=[validador_num_telefono], max_length=17, blank=True, null=True, help_text='Ingrese número telefónico a 10 dígitos')
	telefono_celular = models.CharField(validators=[validador_num_telefono], max_length=17, blank=True, null=True, help_text='Ingrese número telefónico a 10 dígitos')
	email = models.CharField(max_length=200, blank=True, null=True)
	rfc = models.CharField(max_length=13, blank=True, null=True)
	facturacion_tipo = models.PositiveSmallIntegerField(choices=FACTURACION_TIPO, null=True, blank=True)
	revision = models.CharField(max_length=50, blank=True, null=True)
	pagos = models.CharField(max_length=50, blank=True, null=True)
	factura_subtotal = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
	factura_iva = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
	factura_total = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)

	def __str__(self):
		return f'{self.cliente}: {self.encargado_pagos}'

	class Meta:
		verbose_name_plural = 'Clientes Pagos'


class CarpetaClienteContactos(models.Model):
	cliente = models.OneToOneField(Cliente, on_delete=models.CASCADE)
	nombre_contacto = models.CharField(max_length=300)
	validador_num_telefono = RegexValidator(regex=r'^\+?1?\d{9,10}$', message='El número telefónico debe ser ingresado de la siguiente manera: "5512345678". Limitado a 10 dígitos.')
	telefono_1 = models.CharField(validators=[validador_num_telefono], max_length=17, blank=True, help_text='Ingrese número telefónico a 10 dígitos')
	telefono_2 = models.CharField(validators=[validador_num_telefono], max_length=17, blank=True, help_text='Ingrese número telefónico a 10 dígitos')
	telefono_3 = models.CharField(validators=[validador_num_telefono], max_length=17, blank=True, help_text='Ingrese número telefónico a 10 dígitos')
	puesto = models.CharField(max_length=30, null=True, blank=True)
	email_1 = models.CharField(max_length=200, null=True, blank=True)
	email_2 = models.CharField(max_length=200, null=True, blank=True)

	def __str__(self):
		return f'{self.cliente}: {self.nombre_contacto}'

	class Meta:
		verbose_name_plural = 'Clientes Contactos'


class Curp(models.Model):
	# Implementar Curp Api desde Frontend
	curp_regex = r'^[A-Z]{1}[AEIOU]{1}[A-Z]{2}[0-9]{2}(0[1-9]|1[0-2])(0[1-9]|[1-2][0-9]|3[0-1])[HM]{1}(AS|BC|BS|CC|CS|CH|CL|CM|DF|DG|GT|GR|HG|JC|MC|MN|MS|NT|NL|OC|PL|QT|QR|SP|SL|SR|TC|TS|TL|VZ|YN|ZS|NE)[B-DF-HJ-NP-TV-Z]{3}[0-9A-Z]{1}[0-9]{1}$'
	curp = models.CharField(max_length=18, unique=True, validators=[RegexValidator(curp_regex, 'La CURP no es válida')])
	nombre = models.CharField(max_length=100)
	apellido_paterno = models.CharField(max_length=100)
	apellido_materno = models.CharField(max_length=100)
	iniciales = models.CharField(max_length=20, blank=True, null=True)
	fecha_nacimiento = models.DateField(blank=True, null=True)
	edad = models.PositiveIntegerField(blank=True, null=True)
	anio_registro = models.PositiveIntegerField(blank=True, null=True, verbose_name="Año registro")
	numero_acta = models.CharField(max_length=20, blank=True, null=True)
	validacion_renapo = models.PositiveSmallIntegerField(choices=VALIDACION_RENAPO, blank=True, null=True)
	sexo = models.PositiveSmallIntegerField(choices=SEXO_CURP_OPCIONES, blank=True, null=True)
	estatus_curp = models.CharField(max_length=20, choices=ESTATUS_CURP, blank=True, null=True)
	clave_municipio_registro = models.CharField(max_length=5, blank=True, null=True)
	municipio_registro = models.CharField(max_length=100, blank=True, null=True)
	clave_entidad_registro = models.CharField(max_length=5, blank=True, null=True)
	entidad_registro = models.CharField(max_length=100, blank=True, null=True)
	transaction_id = models.CharField(max_length=100, blank=True, null=True)

	def get_nombre_completo(self):
		return f'{self.nombre} {self.apellido_paterno} {self.apellido_materno}'

	def __str__(self):
		return f'{self.curp}: {self.get_nombre_completo()}'

	class Meta:
		verbose_name_plural = 'CURP'


class CurpPrevio(Curp):
	class Meta:
		proxy = True
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


class RfcPrevio(Rfc):
	class Meta:
		proxy = True
		verbose_name_plural = 'RFC'


class Personal(models.Model):
	folio = models.CharField(max_length=10, default='SIN FOLIO', blank=True, null=True)
	cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE)
	origen = models.PositiveSmallIntegerField(choices=ORIGEN_ASPIRANTE, blank=True, null=True)
	fecha = models.DateField(auto_now=True)
	es_empleado = models.BooleanField(default=False, null=True, blank=True)
	observaciones = models.TextField(blank=True, null=True)
	resultado = models.PositiveSmallIntegerField(choices=RESULTADOS_COMPLETOS_ASPIRANTES, blank=True, null=True)
	curp = models.OneToOneField(Curp, on_delete=models.RESTRICT)
	rfc = models.OneToOneField(Rfc, on_delete=models.RESTRICT)

	def __str__(self):
		try:
			return f'{self.curp.get_nombre_completo()}: {self.cliente}'
		except AttributeError:
			return 'SIN CURP'

	class Meta:
		verbose_name_plural = 'Personal'


class PersonalPrevio(Personal):
	class Meta:
		proxy = True
		verbose_name_plural = 'Personal'


class Evaluador(models.Model):
	solicitante = models.CharField(max_length=300)
	personal = models.OneToOneField(Personal, on_delete=models.RESTRICT, blank=True, null=True)

	def __str__(self):
		return f'{self.solicitante}'

	class Meta:
		verbose_name_plural = 'Evaluadores'


class CarpetaLaboral(models.Model):
	personal = models.OneToOneField(Personal, on_delete=models.CASCADE, null=True, blank=True)
	modalidad = models.PositiveSmallIntegerField(choices=MODALIDAD, null=True, blank=True)
	estatus_empleado = models.PositiveSmallIntegerField(choices=ESTATUS_EMPLEADO, null=True, blank=True)
	proceso_racek = models.PositiveSmallIntegerField(choices=PROCESO_RACEK, null=True, blank=True)
	fecha_atencion = models.DateField(null=True, blank=True)
	reingreso = models.BooleanField(default=False, null=True, blank=True)
	inicio_labores = models.DateField(null=True, blank=True)
	visita_domiciliaria = models.BooleanField(default=False, null=True, blank=True)
	cedula = models.DateField(null=True, blank=True)
	nivel_mando = models.PositiveSmallIntegerField(choices=NIVEL_MANDO, null=True, blank=True)
	oficina = models.CharField(max_length=30, null=True, blank=True)
	especialidad_empleo = models.CharField(max_length=35, null=True, blank=True)
	servicio = models.CharField(max_length=30, null=True, blank=True)
	rango = models.CharField(max_length=30, null=True, blank=True)
	turno = models.CharField(max_length=30, null=True, blank=True)
	division = models.CharField(max_length=35, null=True, blank=True)
	sueldo = models.DecimalField(max_digits=7, decimal_places=2, null=True, blank=True)
	funciones = models.CharField(max_length=35, null=True, blank=True)
	evaluacion = models.BooleanField(default=False, null=True, blank=True)
	integracion = models.DateField(auto_now=True)
	vigencia = models.DateField(auto_now=True)
	capacitacion = models.BooleanField(default=False, null=True, blank=True)
	ultima_actualizacion = models.DateField(auto_now=True)
	impresion = models.BooleanField(default=False, null=True, blank=True)
	# TODO: Trigger that saves TODAY DATE when you send the info to print
	fecha_impresion = models.DateField(null=True, blank=True)
	expediente = models.CharField(max_length=25, null=True, blank=True)
	cedula_federal = models.BooleanField(default=False, null=True, blank=True)
	fecha_cedula_federal = models.DateField(null=True, blank=True)
	cedula_cdmx = models.BooleanField(default=False, null=True, blank=True)
	fecha_cedula_cdmx = models.DateField(null=True, blank=True)
	evaluacion_federal = models.BooleanField(default=False, null=True, blank=True)
	fecha_evaluacion_federal = models.DateField(null=True, blank=True)
	evaluacion_cdmx = models.BooleanField(default=False, null=True, blank=True)
	fecha_evaluacion_cdmx = models.DateField(null=True, blank=True)
	evaluacion_sedena = models.BooleanField(default=False, null=True, blank=True)
	fecha_evaluacion_sedena = models.DateField(null=True, blank=True)
	registro_estatal = models.PositiveSmallIntegerField(choices=ESTADO_REGISTROS, null=True, blank=True)
	fecha_registro_estatal = models.DateField(null=True, blank=True)
	oficio_registro_estatal = models.CharField(max_length=25, null=True, blank=True)
	verificacion = models.PositiveSmallIntegerField(choices=ESTADO_REGISTROS, null=True, blank=True)
	fecha_verificacion = models.DateField(null=True, blank=True)
	registro_dgsp = models.PositiveSmallIntegerField(choices=ESTADO_REGISTROS, null=True, blank=True)
	fecha_registro_dgsp = models.DateField(null=True, blank=True)
	oficio_registro_dgsp = models.CharField(max_length=25, null=True, blank=True)
	registro_sedena = models.PositiveSmallIntegerField(choices=ESTADO_REGISTROS, null=True, blank=True)
	fecha_registro_sedena = models.DateField(null=True, blank=True)
	oficio_registro_sedena = models.CharField(max_length=25, null=True, blank=True)
	lic_part_col = models.CharField(max_length=25, null=True, blank=True)
	comentarios = models.TextField(blank=True, null=True)

	def __str__(self):
		return f'{self.personal}: {self.proceso_racek}'

	class Meta:
		verbose_name_plural = 'Carpetas Laborales'


class Ocupacion(models.Model):
	nombre_ocupacion = models.CharField(max_length=100, blank=True, null=True)
	carpeta_laboral = models.OneToOneField(CarpetaLaboral, on_delete=models.RESTRICT, blank=True, null=True)

	def __str__(self):
		return f'{self.nombre_ocupacion}'

	class Meta:
		verbose_name_plural = 'Ocupaciones'


class Puesto(models.Model):
	nombre_puesto = models.CharField(max_length=30)
	carpeta_laboral = models.OneToOneField(CarpetaLaboral, on_delete=models.RESTRICT, blank=True, null=True)

	def __str__(self):
		return f'{self.nombre_puesto}'

	class Meta:
		verbose_name_plural = 'Puestos'


class CarpetaGenerales(models.Model):
	personal = models.OneToOneField(Personal, on_delete=models.CASCADE)
	email_empleado = models.CharField(max_length=200, null=True, blank=True)
	validador_num_telefono = RegexValidator(regex=r'^\+?1?\d{9,10}$', message='El número telefónico debe ser ingresado de la siguiente manera: "5512345678". Limitado a 10 dígitos.')
	telefono_domicilio = models.CharField(validators=[validador_num_telefono], max_length=17, blank=True, help_text='Ingrese número telefónico a 10 dígitos')
	telefono_celular = models.CharField(validators=[validador_num_telefono], max_length=17, blank=True, help_text='Ingrese número telefónico a 10 dígitos')
	telefono_recados = models.CharField(validators=[validador_num_telefono], max_length=17, blank=True, help_text='Ingrese número telefónico a 10 dígitos')
	numero_elemento = models.PositiveIntegerField(null=True, blank=True)
	transporte = models.CharField(max_length=50, null=True, blank=True)
	tiempo_trayecto = models.CharField(max_length=15, blank=True, null=True)
	estado_civil = models.PositiveSmallIntegerField(choices=EDO_CIVIL, null=True, blank=True)
	estado_cartilla = models.PositiveSmallIntegerField(choices=ESTADO_CARTILLA, null=True, blank=True)
	clave_cartilla = models.CharField(max_length=18, null=True, blank=True)
	cuip = models.CharField(max_length=20, null=True, blank=True)
	clave_ine = models.CharField(max_length=20, null=True, blank=True)
	folio = models.CharField(max_length=20, null=True, blank=True)
	nss = models.CharField(max_length=15, null=True, blank=True)
	pasaporte = models.CharField(max_length=20, null=True, blank=True)
	escolaridad = models.PositiveSmallIntegerField(choices=ESCOLARIDAD, null=True, blank=True)
	escuela = models.CharField(max_length=200, null=True, blank=True)
	especialidad_escuela = models.CharField(max_length=50, null=True, blank=True)
	cedula_profesional = models.CharField(max_length=20, null=True, blank=True)
	registro_sep = models.BooleanField(default=False, null=True, blank=True)
	anio_inicio_escolaridad = models.DateField(blank=True, verbose_name='Año inicio escolaridad')
	anio_termino_escolaridad = models.DateField(blank=True, verbose_name='Año término escolaridad')
	comprobante_estudios = models.PositiveSmallIntegerField(choices=COMPROBANTE_ESTUDIOS, null=True, blank=True)
	folio_certificado = models.CharField(max_length=20, null=True, blank=True)
	promedio = models.DecimalField(max_digits=3, decimal_places=2, null=True, blank=True)
	antecedentes = models.PositiveSmallIntegerField(choices=ANTECEDENTES, null=True, blank=True)
	sabe_conducir = models.BooleanField(default=False, null=True, blank=True)
	licencia_conducir = models.CharField(max_length=20, null=True, blank=True)
	alergias = models.CharField(max_length=30, null=True, blank=True)
	inicio_trabajo = models.DateField(null=True, blank=True)
	fin_trabajo = models.DateField(null=True, blank=True)

	def __str__(self):
		return f'{self.personal}'

	class Meta:
		verbose_name_plural = 'Carpetas Generales'


class CarpetaGeneralesPrevio(CarpetaGenerales):
	class Meta:
		proxy = True
		verbose_name_plural = 'Carpeta Generales'


class CarpetaReferencias(models.Model):
	personal = models.OneToOneField(Personal, on_delete=models.CASCADE)

	def __str__(self):
		return f'{self.personal}'

	class Meta:
		verbose_name_plural = 'Carpeta Referencias'


class Referencia(models.Model):
	tipo_referencia = models.PositiveSmallIntegerField(choices=TIPO_REFERENCIA, null=True, blank=True)
	nombre = models.CharField(max_length=100)
	apellido_paterno = models.CharField(max_length=100)
	apellido_materno = models.CharField(max_length=100)
	sexo = models.PositiveSmallIntegerField(choices=SEXO_OPCIONES, null=True, blank=True)
	ocupacion = models.PositiveSmallIntegerField(choices=OCUPACION, null=True, blank=True)
	parentesco = models.PositiveSmallIntegerField(choices=PARENTESCO, null=True, blank=True)
	tiempo_de_conocerse = models.CharField(max_length=30, null=True, blank=True)
	direccion = models.CharField(max_length=100, null=True, blank=True)
	codigo_postal = models.CharField(max_length=5, blank=True, null=True)
	validador_num_telefono = RegexValidator(regex=r'^\+?1?\d{9,10}$', message='El número telefónico debe ser ingresado de la siguiente manera: "5512345678". Limitado a 10 dígitos.')
	telefono_contacto = models.CharField(validators=[validador_num_telefono], max_length=17, blank=True, help_text='Ingrese número telefónico a 10 dígitos')
	opinion = models.TextField(blank=True, null=True)
	carpeta_referencia = models.ForeignKey(CarpetaReferencias, on_delete=models.CASCADE)

	class Meta:
		verbose_name_plural = 'Referencias'


class CarpetaDependientes(models.Model):
	personal = models.OneToOneField(Personal, on_delete=models.CASCADE)
	vive_con_familia = models.BooleanField(default=False, null=True, blank=True)
	cantidad_dependientes_economicos = models.CharField(max_length=3, blank=True, null=True)
	cantidad_hijos = models.CharField(max_length=3, blank=True, null=True)

	def __str__(self):
		return f'{self.personal}'

	class Meta:
		verbose_name_plural = 'Carpeta Dependientes'


class Dependiente(models.Model):
	nombre = models.CharField(max_length=100, null=True, blank=True)
	apellido_paterno = models.CharField(max_length=100, null=True, blank=True)
	apellido_materno = models.CharField(max_length=100, null=True, blank=True)
	sexo = models.PositiveSmallIntegerField(choices=SEXO_OPCIONES, null=True, blank=True)
	fecha_nacimiento = models.DateField(null=True, blank=True)
	parentesco = models.PositiveSmallIntegerField(choices=PARENTESCO, null=True, blank=True)
	actividad = models.PositiveSmallIntegerField(choices=ACTIVIDAD, null=True, blank=True)
	comentarios = models.TextField(blank=True, null=True)
	carpeta_dependientes = models.ForeignKey(CarpetaDependientes, on_delete=models.CASCADE)

	class Meta:
		verbose_name_plural = 'Dependientes'


class CarpetaExamenPsicologico(models.Model):
	personal = models.OneToOneField(Personal, on_delete=models.CASCADE)
	fecha_examen = models.DateField(auto_now=True, null=True, blank=True)
	actitud = models.PositiveSmallIntegerField(choices=OPCIONES_PSICOLOGICO, null=True, blank=True)
	inteligencia = models.PositiveSmallIntegerField(choices=OPCIONES_PSICOLOGICO, null=True, blank=True)
	personalidad = models.PositiveSmallIntegerField(choices=OPCIONES_PSICOLOGICO, null=True, blank=True)
	impulsividad = models.PositiveSmallIntegerField(choices=OPCIONES_PSICOLOGICO, null=True, blank=True)
	organizacion = models.PositiveSmallIntegerField(choices=OPCIONES_PSICOLOGICO, null=True, blank=True)
	valores = models.PositiveSmallIntegerField(choices=OPCIONES_PSICOLOGICO, null=True, blank=True)
	temperamento = models.PositiveSmallIntegerField(choices=OPCIONES_PSICOLOGICO, null=True, blank=True)
	confiabilidad = models.PositiveSmallIntegerField(choices=OPCIONES_PSICOLOGICO, null=True, blank=True)
	compromiso = models.PositiveSmallIntegerField(choices=OPCIONES_PSICOLOGICO, null=True, blank=True)
	habilidades_laborales = models.PositiveSmallIntegerField(choices=OPCIONES_PSICOLOGICO, null=True, blank=True)
	resultado_psicologico = models.PositiveSmallIntegerField(choices=RESULTADO_PSICOLOGICO, null=True, blank=True)
	resultado_aspirante = models.PositiveSmallIntegerField(choices=RESULTADOS_COMPLETOS_ASPIRANTES, blank=True, null=True)
	observacion = models.TextField(blank=True, null=True)

	def __str__(self):
		return f'{self.personal}'

	class Meta:
		verbose_name_plural = 'Carpeta Examen Psicológico'


class CarpetaExamenPsicologicoPrevio(CarpetaExamenPsicologico):
	class Meta:
		proxy = True
		verbose_name_plural = 'Carpeta Examen Psicológico'


class CarpetaExamenToxicologico(models.Model):
	fecha_examen = models.DateField(auto_now=True, null=True, blank=True)
	cocaina = models.BooleanField(blank=True, default=False)
	marihuana = models.BooleanField(blank=True, default=False)
	opiaceos = models.BooleanField(blank=True, default=False)
	anfetaminas = models.BooleanField(blank=True, default=False)
	metanfetaminas = models.BooleanField(blank=True, default=False)
	barbituricos = models.BooleanField(blank=True, default=False)
	benzodiacepinas = models.BooleanField(blank=True, default=False)
	resultado_toxicologico = models.BooleanField(blank=True, default=False)
	resultado_aspirante = models.PositiveSmallIntegerField(choices=RESULTADO_TOXICOLOGICO_ASPIRANTE, blank=True, null=True)
	observacion = models.TextField(blank=True, null=True)
	personal = models.OneToOneField(Personal, on_delete=models.CASCADE)

	class Meta:
		verbose_name_plural = 'Carpeta Examen Toxicológico'


class CarpetaExamenToxicologicoPrevio(CarpetaExamenToxicologico):
	class Meta:
		proxy = True
		verbose_name_plural = 'Carpeta Examen Toxicológico'


class CarpetaExamenMedico(models.Model):
	personal = models.OneToOneField(Personal, on_delete=models.CASCADE)
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
	resultado_aspirante = models.PositiveSmallIntegerField(choices=RESULTADOS_COMPLETOS_ASPIRANTES, blank=True, null=True)
	observacion = models.TextField(blank=True, null=True)

	def __str__(self):
		return f'{self.personal}'

	class Meta:
		verbose_name_plural = 'Carpeta Examen Médico'


class CarpetaExamenMedicoPrevio(CarpetaExamenMedico):
	class Meta:
		proxy = True
		verbose_name_plural = 'Carpeta Examen Médico'


class CarpetaExamenFisico(models.Model):
	"""
    Todas las evaluaciones dentro del examen físico usan la escala:
    Baja: 1-3
    Media: 4-6
    Alta: 7-10
    """
	personal = models.OneToOneField(Personal, on_delete=models.CASCADE)
	fecha_examen = models.DateField(null=True, blank=True)
	elasticidad = models.PositiveIntegerField(validators=[MinValueValidator(0), MaxValueValidator(10)], blank=True, default=0)
	velocidad = models.PositiveIntegerField(validators=[MinValueValidator(0), MaxValueValidator(10)], blank=True, default=0)
	resistencia = models.PositiveIntegerField(validators=[MinValueValidator(0), MaxValueValidator(10)], blank=True, default=0)
	condicion_fisica = models.PositiveIntegerField(validators=[MinValueValidator(0), MaxValueValidator(10)], blank=True, default=0)
	reflejos = models.PositiveIntegerField(validators=[MinValueValidator(0), MaxValueValidator(10)], blank=True, default=0)
	locomocion = models.PositiveIntegerField(validators=[MinValueValidator(0), MaxValueValidator(10)], blank=True, default=0)
	prueba_esfuerzo = models.PositiveIntegerField(validators=[MinValueValidator(0), MaxValueValidator(10)], blank=True, default=0)
	resultado = models.CharField(max_length=100, blank=True, null=True)
	resultado_aspirante = models.PositiveSmallIntegerField(choices=RESULTADOS_COMPLETOS_ASPIRANTES, blank=True, null=True)
	observacion = models.TextField(blank=True, null=True)

	def __str__(self):
		return f'{self.personal}'

	class Meta:
		verbose_name_plural = 'Carpeta Examen Físico'


class CarpetaExamenFisicoPrevio(CarpetaExamenFisico):
	class Meta:
		proxy = True
		verbose_name_plural = 'Carpeta Examen Físico'


class CarpetaExamenSocioeconomico(models.Model):
	personal = models.OneToOneField(Personal, on_delete=models.CASCADE)
	propiedades = models.CharField(max_length=200, blank=True, null=True)
	inversiones = models.CharField(max_length=200, blank=True, null=True)
	vehiculo = models.CharField(max_length=200, blank=True, null=True)
	tarjetas_credito_departamental = models.CharField(max_length=200, blank=True, null=True)
	adeudos_importantes = models.CharField(max_length=200, blank=True, null=True)
	tipo_domicilio = models.PositiveSmallIntegerField(choices=TIPO_DOMICILIO, blank=True, null=True)
	titular_domicilio = models.CharField(max_length=300, blank=True, null=True)
	tipo_vivienda = models.PositiveSmallIntegerField(choices=TIPO_VIVIENDA, blank=True, null=True)
	anios_residencia = models.CharField(max_length=10, blank=True, null=True, verbose_name='Años residencia')
	niveles = models.CharField(max_length=4, blank=True, null=True)
	cuartos = models.CharField(max_length=5, blank=True, null=True)
	banos = models.CharField(max_length=3, blank=True, null=True, verbose_name='Baños')
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
	validador_num_telefono = RegexValidator(regex=r'^\+?1?\d{9,10}$', message='El número telefónico debe ser ingresado de la siguiente manera: "5512345678". Limitado a 10 dígitos.')
	telefono_emergencia = models.CharField(validators=[validador_num_telefono], max_length=17, blank=True, null=True, help_text='Ingrese número telefónico a 10 dígitos')
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
	resultado_aspirante = models.PositiveSmallIntegerField(choices=RESULTADOS_COMPLETOS_ASPIRANTES, blank=True, null=True)
	comentarios_generales = models.TextField(blank=True, null=True)
	ruta_acceso = models.CharField(max_length=200, blank=True, null=True)
	color_vivienda_porton = models.CharField(max_length=150, blank=True, null=True)
	referencias = models.CharField(max_length=150, blank=True, null=True)
	tiempo_traslado = models.CharField(max_length=20, blank=True, null=True)
	gasto = models.CharField(max_length=20, blank=True, null=True)
	nombre_recados = models.CharField(max_length=300, blank=True, null=True)
	parentesco = models.CharField(max_length=30, blank=True, null=True)
	telefono_recados = models.CharField(validators=[validador_num_telefono], max_length=17, blank=True, null=True, help_text='Ingrese número telefónico a 10 dígitos')
	comentario = models.CharField(max_length=300, blank=True, null=True)

	def __str__(self):
		return f'{self.personal}'

	class Meta:
		verbose_name_plural = 'Carpeta Examen Socioeconómico'


class CarpetaExamenSocioeconomicoPrevio(CarpetaExamenSocioeconomico):
	class Meta:
		proxy = True
		verbose_name_plural = 'Carpeta Examen Fisico'


class CarpetaExamenPoligrafo(models.Model):
	personal = models.OneToOneField(Personal, on_delete=models.CASCADE)
	resultado_aspirante = models.PositiveSmallIntegerField(choices=RESULTADO_POLIGRAFO_ASPIRANTE, blank=True, null=True)
	observacion = models.TextField(blank=True, null=True)

	def __str__(self):
		return f'{self.personal}'

	class Meta:
		verbose_name_plural = 'Carpeta Examen Polígrafo'


class CarpetaExamenPoligrafoPrevio(CarpetaExamenPoligrafo):
	class Meta:
		proxy = True
		verbose_name_plural = 'Carpeta Examen Polígrafo'


class CarpetaEmpleoAnteriorSeguridadPublica(models.Model):
	personal = models.OneToOneField(Personal, on_delete=models.CASCADE)

	def __str__(self):
		return f'{self.personal}'

	class Meta:
		verbose_name_plural = 'Carpeta Empleos Anteriores Seguridad Publica'


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
	validador_num_telefono = RegexValidator(regex=r'^\+?1?\d{9,10}$', message='El número telefónico debe ser ingresado de la siguiente manera: "5512345678". Limitado a 10 dígitos.')
	telefono = models.CharField(validators=[validador_num_telefono], max_length=17, blank=True, help_text='Ingrese número telefónico a 10 dígitos')
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
		verbose_name_plural = 'Empleos Anteriores Seguridad Publica'


class CarpetaEmpleoAnterior(models.Model):
	personal = models.ForeignKey(Personal, on_delete=models.CASCADE)

	def __str__(self):
		return f'{self.personal}'

	class Meta:
		verbose_name_plural = 'Carpeta Empleos Anteriores'


class EmpleoAnterior(models.Model):
	empresa = models.CharField(max_length=100, blank=True, null=True)
	validador_num_telefono = RegexValidator(regex=r'^\+?1?\d{9,10}$', message='El número telefónico debe ser ingresado de la siguiente manera: "5512345678". Limitado a 10 dígitos.')
	telefono = models.CharField(validators=[validador_num_telefono], max_length=17, blank=True, help_text='Ingrese número telefónico a 10 dígitos')
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
	desempenio = models.PositiveSmallIntegerField(choices=CALIF_BUENO_MALO, blank=True, null=True, verbose_name='desempeño')
	observaciones = models.TextField(blank=True, null=True)
	carp_emp_ant = models.OneToOneField(CarpetaEmpleoAnterior, on_delete=models.CASCADE)
	motivo_separacion = models.OneToOneField(MotivoSeparacion, on_delete=models.RESTRICT, null=True, blank=True)

	class Meta:
		verbose_name_plural = 'Empleos Anteriores'


class CarpetaCapacitacion(models.Model):
	personal = models.OneToOneField(Personal, on_delete=models.CASCADE)

	def __str__(self):
		return f'{self.personal}'

	class Meta:
		verbose_name_plural = 'Carpeta Capacitaciones'


class Capacitacion(models.Model):
	carpeta_capacitacion = models.ForeignKey(CarpetaCapacitacion, on_delete=models.CASCADE)
	institucion_empresa = models.CharField(max_length=100, blank=True, null=True)
	curso = models.CharField(max_length=100, blank=True, null=True)
	tipo_curso = models.CharField(max_length=100, blank=True, null=True)
	area_curso = models.CharField(max_length=100, blank=True, null=True)
	impartido_recibido = models.PositiveSmallIntegerField(choices=IMPARTIDO_RECIBIDO, blank=True, null=True)
	eficiencia_terminal = models.PositiveSmallIntegerField(choices=EFICIENCIA_TERMINAL, blank=True, null=True)
	inicio = models.DateField(blank=True, null=True)
	conclusion = models.DateField(blank=True, null=True)
	duracion = models.CharField(max_length=10, blank=True, null=True)

	def __str__(self):
		return f'{self.curso}'

	class Meta:
		verbose_name_plural = 'Capacitaciones'


class Instructor(models.Model):
	capacitacion = models.OneToOneField(Capacitacion, on_delete=models.RESTRICT, blank=True, null=True)
	nombre_instructor = models.CharField(max_length=300, blank=True, null=True)
	numero_registro = models.CharField(max_length=14, blank=True, null=True)

	def __str__(self):
		return f'{self.nombre_instructor}'

	class Meta:
		verbose_name_plural = 'Instructores'


class RepresentanteTrabajadores(models.Model):
	cliente = models.OneToOneField(Cliente, on_delete=models.CASCADE, blank=True, null=True, editable=False)
	personal = models.OneToOneField(Personal, on_delete=models.CASCADE, blank=True, null=True, editable=False)
	nombre_completo = models.CharField(max_length=300, blank=True, null=True)
	firma = models.FileField(upload_to='firma-representantes', blank=True, null=True)
	reglamento_interno = models.FileField(upload_to='reglamentos-trabajo', blank=True, null=True)

	def __str__(self):
		return self.nombre_completo

	class Meta:
		verbose_name_plural = 'Representantes Trabajadores'


class Domicilio(models.Model):
	calle = models.CharField(max_length=100, blank=True, null=True)
	numero_exterior = models.CharField(max_length=20, default='S/N', blank=True, null=True)
	numero_interior = models.CharField(max_length=20, blank=True, null=True)
	entre_calle = models.CharField(max_length=100, null=True, blank=True)
	y_calle = models.CharField(max_length=100, null=True, blank=True)
	codigo_postal = models.OneToOneField(CodigoPostal, on_delete=models.RESTRICT)
	carpeta_cliente_generales = models.OneToOneField(CarpetaClienteGenerales, on_delete=models.CASCADE, blank=True, null=True, editable=False)
	carpeta_cliente_pagos = models.OneToOneField(CarpetaClientePagos, on_delete=models.CASCADE, blank=True, null=True, editable=False)
	personal = models.OneToOneField(Personal, on_delete=models.CASCADE, blank=True, null=True, editable=False)
	referencia = models.OneToOneField(Referencia, on_delete=models.CASCADE, blank=True, null=True, editable=False)
	empleo_anterior_sp = models.OneToOneField(EmpleoAnteriorSeguridadPublica, on_delete=models.CASCADE, blank=True, null=True, editable=False)
	empleo_anterior = models.OneToOneField(EmpleoAnterior, on_delete=models.CASCADE, blank=True, null=True, editable=False)

	def __str__(self):
		return (
			f'{self.calle} No.{self.numero_exterior} '
			f'{self.numero_interior}, '
			f'{self.codigo_postal.tipo_asentamiento} {self.codigo_postal.asentamiento}, '
			f'{self.codigo_postal.municipio}, '
			f'{self.codigo_postal.estado}, '
			f'{self.codigo_postal.pais}'
		)

	class Meta:
		verbose_name_plural = 'Domicilios'


class Idioma(models.Model):
	idioma = models.CharField(max_length=50, blank=True, null=True)
	lectura = models.CharField(max_length=3, blank=True, null=True)
	escritura = models.CharField(max_length=3, blank=True, null=True)
	conversacion = models.CharField(max_length=3, blank=True, null=True)
	carpeta_capacitacion = models.ForeignKey(CarpetaCapacitacion, on_delete=models.CASCADE)


class CarpetaMediaFiliacion(models.Model):
	personal = models.OneToOneField(Personal, on_delete=models.CASCADE)
	tension_arterial = models.CharField(max_length=10, null=True, blank=True)
	temperatura = models.CharField(max_length=5, null=True, blank=True)
	indice_masa_corporal = models.CharField(max_length=6, null=True, blank=True)
	clasificacion_imc = models.PositiveSmallIntegerField(choices=CLASIFICACION_IMC, blank=True, null=True)
	sat02 = models.CharField(max_length=10, null=True, blank=True)
	frecuencia_cardiaca = models.CharField(max_length=6, null=True, blank=True)
	cronica_degenerativa = models.CharField(max_length=100, null=True, blank=True)
	complexion = models.PositiveSmallIntegerField(choices=COMPLEXION, null=True, blank=True)
	color_piel = models.PositiveSmallIntegerField(choices=COLOR_PIEL, null=True, blank=True)
	cara = models.PositiveSmallIntegerField(choices=CARA, null=True, blank=True)
	cabello_cantidad = models.PositiveSmallIntegerField(choices=CABELLO_CANTIDAD, null=True, blank=True)
	cabello_color = models.PositiveSmallIntegerField(choices=CABELLO_COLOR, null=True, blank=True)
	cabello_forma = models.PositiveSmallIntegerField(choices=CABELLO_FORMA, null=True, blank=True)
	cabello_calvicie = models.PositiveSmallIntegerField(choices=CABELLO_CALVICIE, null=True, blank=True)
	cabello_implantacion = models.PositiveSmallIntegerField(choices=CABELLO_IMPLANTACION, null=True, blank=True)
	frente_altura = models.PositiveSmallIntegerField(choices=TAMANIOS_GMP, null=True, blank=True)
	frente_indicacion = models.PositiveSmallIntegerField(choices=FRENTE_INCLINACION, null=True, blank=True)
	frente_ancho = models.PositiveSmallIntegerField(choices=TAMANIOS_GMP, null=True, blank=True)
	cejas_direccion = models.PositiveSmallIntegerField(choices=CEJAS_DIRECCION, null=True, blank=True)
	cejas_implantacion = models.PositiveSmallIntegerField(choices=CEJAS_IMPLANTACION, null=True, blank=True)
	cejas_forma = models.PositiveSmallIntegerField(choices=CEJAS_FORMA, null=True, blank=True)
	cejas_tamanio = models.PositiveSmallIntegerField(choices=CEJAS_TAMANIO, blank=True, verbose_name='Cejas tamaño')
	ojos_color = models.PositiveSmallIntegerField(choices=OJOS_COLOR, null=True, blank=True)
	ojos_forma = models.PositiveSmallIntegerField(choices=OJOS_FORMA, null=True, blank=True)
	ojos_tamanio = models.PositiveSmallIntegerField(choices=OJOS_TAMANIO, blank=True, verbose_name='Ojos tamaño')
	ojos_raiz = models.PositiveSmallIntegerField(choices=TAMANIOS_GMP, null=True, blank=True)
	nariz_dorso = models.PositiveSmallIntegerField(choices=NARIZ_DORSO, null=True, blank=True)
	nariz_ancho = models.PositiveSmallIntegerField(choices=TAMANIOS_GMP, null=True, blank=True)
	nariz_base = models.PositiveSmallIntegerField(choices=NARIZ_BASE, null=True, blank=True)
	nariz_altura = models.PositiveSmallIntegerField(choices=TAMANIOS_GMP, null=True, blank=True)
	boca_tamanio = models.PositiveSmallIntegerField(choices=TAMANIOS_GMP, null=True, blank=True,
	                                                verbose_name='Boca tamaño')
	boca_comisuras = models.PositiveSmallIntegerField(choices=BOCA_COMISURAS, null=True, blank=True)
	labios_espesor = models.PositiveSmallIntegerField(choices=LABIOS_ESPESOR, null=True, blank=True)
	altura_nasolabial = models.PositiveSmallIntegerField(choices=TAMANIOS_GMP, null=True, blank=True)
	labios_prominencia = models.PositiveSmallIntegerField(choices=LABIOS_PROMINENCIA, null=True, blank=True)
	menton_tipo = models.PositiveSmallIntegerField(choices=MENTON_TIPO, null=True, blank=True)
	menton_forma = models.PositiveSmallIntegerField(choices=MENTON_FORMA, null=True, blank=True)
	menton_inclinacion = models.PositiveSmallIntegerField(choices=MENTON_INCLINACION, null=True, blank=True)
	oreja_derecha_forma = models.PositiveSmallIntegerField(choices=OREJA_DERECHA_FORMA, null=True, blank=True)
	oreja_derecha_original = models.PositiveSmallIntegerField(choices=TAMANIOS_GMP, null=True, blank=True)
	oreja_derecha_helix_superior = models.PositiveSmallIntegerField(choices=TAMANIOS_GMP, null=True, blank=True)
	oreja_derecha_helix_posterior = models.PositiveSmallIntegerField(choices=TAMANIOS_GMP, null=True, blank=True)
	oreja_derecha_helix_adherencia = models.PositiveSmallIntegerField(choices=OREJA_DERECHA_ADHERENCIA, null=True,
	                                                                  blank=True)
	oreja_derecha_helix_contorno = models.PositiveSmallIntegerField(choices=OREJA_DERECHA_HELIX_CONTORNO, null=True,
	                                                                blank=True)
	oreja_derecha_lobulo_adherencia = models.PositiveSmallIntegerField(choices=OREJA_DERECHA_ADHERENCIA, null=True,
	                                                                   blank=True)
	oreja_derecha_lobulo_particularidad = models.PositiveSmallIntegerField(choices=OREJA_DERECHA_LOBULO_PARTICULARIDAD,
	                                                                       null=True, blank=True)
	oreja_derecha_lobulo_dimension = models.PositiveSmallIntegerField(choices=TAMANIOS_GMP, null=True, blank=True)
	sangre = models.PositiveSmallIntegerField(choices=SANGRE, null=True, blank=True)
	rh = models.PositiveSmallIntegerField(choices=RH, null=True, blank=True)
	anteojos = models.BooleanField(default=False, null=True, blank=True)
	estatura = models.CharField(max_length=15, blank=True, null=True)
	peso = models.DecimalField(max_digits=3, decimal_places=2, null=True, blank=True)

	def __str__(self):
		return f'{self.personal}'

	class Meta:
		verbose_name_plural = 'Carpeta Media Filiación'


class CarpetaMediaFiliacionPrevio(CarpetaMediaFiliacion):
	class Meta:
		proxy = True
		verbose_name_plural = 'Carpeta Media Filiación'


class DocumentosDigitales(models.Model):
	personal = models.OneToOneField(Personal, on_delete=models.CASCADE)
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

	def __str__(self):
		return f'{self.personal}'

	def save(self, *args, **kwargs):
		# Check if the instance already exists in the database
		if self.pk:
			# Get the existing instance to access old field values
			existing_instance = DocumentosDigitales.objects.get(pk=self.pk)

			# Iterate through each file field
			for field_name in [f.name for f in DocumentosDigitales._meta.get_fields() if
			                   isinstance(f, (models.FileField, models.ImageField))]:
				old_file = getattr(existing_instance, field_name)
				new_file = getattr(self, field_name)

				if new_file and old_file != new_file:
					# If the new file is different from the old file, delete the old file
					if old_file:
						# Use the storage's delete method to remove the file
						default_storage.delete(old_file.name)
				elif not new_file:
					# If the new file is empty, delete the old file
					if old_file:
						default_storage.delete(old_file.name)

		super().save(*args, **kwargs)

	class Meta:
		verbose_name_plural = 'Documentos Digitales'


class DocumentosDigitalesPrevio(DocumentosDigitales):
	class Meta:
		proxy = True
		verbose_name_plural = 'Documentos Digitales'


class CapacitacionCliente(models.Model):
	estatus_capacitacion = models.PositiveSmallIntegerField(choices=ESTATUS_CAPACITACION, blank=True, null=True)
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
	resultado_capacitacion = models.PositiveSmallIntegerField(choices=RESULTADO_CAPACITACION, blank=True, null=True)
	personal = models.OneToOneField(Personal, on_delete=models.CASCADE)
	capacitacion_cliente = models.ForeignKey(CapacitacionCliente, on_delete=models.CASCADE)

	def __str__(self):
		try:
			return f'{self.personal.curp.nombre} {self.personal.curp.apellido_paterno} {self.personal.curp.apellido_materno}: {self.resultado_capacitacion}'
		except AttributeError:
			return f'SIN CURP'

	class Meta:
		verbose_name_plural = 'Personal Por Capacitar'
