import requests
from datetime import datetime
from .choices import *
from django.db import models
from django.core.validators import RegexValidator
from django.core.validators import  MinValueValidator, MaxValueValidator

# Create your models here.
class Cliente(models.Model):
    nombre_comercial = models.CharField(max_length=200, blank=True)
    razon_social = models.CharField(max_length=200, blank=True)
    activo = models.BooleanField(default=False, blank=True)

    def __str__(self):
        return f'{self.nombre_comercial}'
    
    class Meta:
        verbose_name_plural = 'Clientes'

class Sede(models.Model):
    clave_sede = models.PositiveIntegerField(validators=[MinValueValidator(1), MaxValueValidator(99999)], blank=True)
    nombre_sede = models.CharField(max_length=100, blank=True)
    cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.clave_sede}: {self.nombre_sede}'
    
    class Meta:
        verbose_name_plural = 'Sedes'

class ClienteGenerales(models.Model):
    reg_estatal = models.CharField(max_length=30, blank=True)
    reg_federal = models.CharField(max_length=30, blank=True)
    rfc = models.CharField(max_length=13, blank=True)
    validador_num_telefono = RegexValidator(regex=r'^\+?1?\d{9,10}$', message='El número telefónico debe ser ingresado de la siguiente manera: "5512345678". Limitado a 10 dígitos.')
    telefono_1 = models.CharField(validators=[validador_num_telefono], max_length=17, blank=True, help_text='Ingrese número telefónico a 10 dígitos')
    telefono_2 = models.CharField(validators=[validador_num_telefono], max_length=17, blank=True, help_text='Ingrese número telefónico a 10 dígitos')
    telefono_3 = models.CharField(validators=[validador_num_telefono], max_length=17, blank=True, help_text='Ingrese número telefónico a 10 dígitos')    
    representante_legal = models.CharField(max_length=300, blank=True)
    encargado_operativo = models.CharField(max_length=300, blank=True)
    encargado_rh = models.CharField(max_length=300, blank=True)
    coordinador = models.CharField(max_length=300, blank=True)
    registro_patronal = models.CharField(max_length=30, blank=True)
    cliente = models.OneToOneField(Cliente, on_delete=models.CASCADE)
    
    def __str__(self):
        return f'{self.rfc}: {self.cliente}'
    
    class Meta:
        verbose_name_plural = 'Clientes Generales'

class ClientePagos(models.Model):
    encargado_pagos = models.CharField(max_length=150, blank=True)
    validador_num_telefono = RegexValidator(regex=r'^\+?1?\d{9,10}$', message='El número telefónico debe ser ingresado de la siguiente manera: "5512345678". Limitado a 10 dígitos.')
    telefono_oficina = models.CharField(validators=[validador_num_telefono], max_length=17, blank=True, help_text='Ingrese número telefónico a 10 dígitos')
    telefono_celular = models.CharField(validators=[validador_num_telefono], max_length=17, blank=True, help_text='Ingrese número telefónico a 10 dígitos')
    email = models.CharField(max_length=200, blank=True)
    rfc = models.CharField(max_length=13, blank=True)
    facturacion_tipo = models.PositiveSmallIntegerField(choices=FACTURACION_TIPO, blank=True)
    revision = models.CharField(max_length=50, blank=True)
    pagos = models.CharField(max_length=50, blank=True)
    factura_subtotal = models.DecimalField(max_digits=10, decimal_places=2, blank=True)
    factura_iva = models.DecimalField(max_digits=10, decimal_places=2, blank=True)
    factura_total = models.DecimalField(max_digits=10, decimal_places=2, blank=True)
    cliente = models.OneToOneField(Cliente, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.cliente}: {self.encargado_pagos}'
    
    class Meta:
        verbose_name_plural = 'Clientes Pagos'

class ClienteContactos(models.Model):
    nombre_contacto = models.CharField(max_length=300, blank=True)
    validador_num_telefono = RegexValidator(regex=r'^\+?1?\d{9,10}$', message='El número telefónico debe ser ingresado de la siguiente manera: "5512345678". Limitado a 10 dígitos.')
    telefono_1 = models.CharField(validators=[validador_num_telefono], max_length=17, blank=True, help_text='Ingrese número telefónico a 10 dígitos')
    telefono_2 = models.CharField(validators=[validador_num_telefono], max_length=17, blank=True, help_text='Ingrese número telefónico a 10 dígitos')
    telefono_3 = models.CharField(validators=[validador_num_telefono], max_length=17, blank=True, help_text='Ingrese número telefónico a 10 dígitos')    
    puesto = models.CharField(max_length=30, blank=True)
    email_1 = models.CharField(max_length=200, blank=True)
    email_2 = models.CharField(max_length=200, blank=True)
    cliente = models.OneToOneField(Cliente, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.cliente}: {self.nombre_contacto}'
    
    class Meta:
        verbose_name_plural = 'Clientes Contactos'

class Empleado(models.Model):
    cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.cliente}'
    
    class Meta:
        verbose_name_plural = 'Empleados'

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
    comentarios = models.TextField(blank=True)
    empleado = models.OneToOneField(Empleado, on_delete=models.CASCADE)
    
    def __str__(self):
        return f'{self.empleado}: {self.proceso_racek}'
    
    class Meta:
        verbose_name_plural = 'Carpetas Laborales'

class Puesto(models.Model):
    nombre_puesto = models.CharField(max_length=30)
    carpeta_laboral = models.OneToOneField(CarpetaLaboral, on_delete=models.RESTRICT)

    def __str__(self):
        return f'{self.carpeta_laboral}: {self.nombre_puesto}'
    
    class Meta:
        verbose_name_plural = 'Puestos'

class CarpetaGenerales(models.Model):
    empleado = models.OneToOneField(Empleado, on_delete=models.CASCADE)
    email_empleado = models.CharField(max_length=200, blank=True)
    validador_num_telefono = RegexValidator(regex=r'^\+?1?\d{9,10}$', message='El número telefónico debe ser ingresado de la siguiente manera: "5512345678". Limitado a 10 dígitos.')
    telefono_domicilio = models.CharField(validators=[validador_num_telefono], max_length=17, blank=True, help_text='Ingrese número telefónico a 10 dígitos')
    telefono_celular = models.CharField(validators=[validador_num_telefono], max_length=17, blank=True, help_text='Ingrese número telefónico a 10 dígitos')
    telefono_recados = models.CharField(validators=[validador_num_telefono], max_length=17, blank=True, help_text='Ingrese número telefónico a 10 dígitos')
    numero_elemento = models.PositiveIntegerField(blank=True)
    transporte = models.CharField(max_length=50, blank=True)
    tiempo_trayecto = models.PositiveIntegerField(validators=[MinValueValidator(1), MaxValueValidator(1440)], blank=True, help_text="Ingrese el tiempo en minutos")
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
    complexion = models.PositiveSmallIntegerField(choices=COMPLEXION, blank=True)
    color_piel = models.PositiveSmallIntegerField(choices=COLOR_PIEL, blank=True)
    cara = models.PositiveSmallIntegerField(choices=CARA, blank=True)
    sangre = models.PositiveSmallIntegerField(choices=SANGRE, blank=True)
    rh = models.PositiveSmallIntegerField(choices=RH, blank=True)
    peso = models.DecimalField(max_digits=3, decimal_places=2, blank=True)
    estatura = models.PositiveIntegerField(validators=[MinValueValidator(0), MaxValueValidator(400)], blank=True, default=0)
    alergias = models.CharField(max_length=30, blank=True)
    inicio_trabajo = models.DateField(blank=True)
    fin_trabajo = models.DateField(blank=True)

    def __str__(self):
        return f'{self.empleado}'
    
    class Meta:
        verbose_name_plural = 'Carpetas Generales'

class CarpetaReferencias(models.Model):
    empleado = models.OneToOneField(Empleado, on_delete=models.CASCADE)
    
    class Meta:
        verbose_name_plural = 'Carpeta Referencias'

class Referencia(models.Model):
    tipo_referencia = models.PositiveSmallIntegerField(choices=TIPO_REFERENCIA, blank=True)
    nombre = models.CharField(max_length=100, blank=True)
    apellido_paterno = models.CharField(max_length=100, blank=True)
    apellido_materno = models.CharField(max_length=100, blank=True)
    sexo = models.PositiveSmallIntegerField(choices=SEXO_OPCIONES, blank=True)
    ocupacion = models.PositiveSmallIntegerField(choices=OCUPACION, blank=True)
    parentesco = models.PositiveSmallIntegerField(choices=PARENTESCO, blank=True)
    tiempo_de_conocerse = models.CharField(max_length=30, blank=True)
    direccion = models.CharField(max_length=100, blank=True)
    codigo_postal = models.PositiveIntegerField(validators=[MinValueValidator(1), MaxValueValidator(99999)], blank=True)
    validador_num_telefono = RegexValidator(regex=r'^\+?1?\d{9,10}$', message='El número telefónico debe ser ingresado de la siguiente manera: "5512345678". Limitado a 10 dígitos.')
    telefono_contacto = models.CharField(validators=[validador_num_telefono], max_length=17, blank=True, help_text='Ingrese número telefónico a 10 dígitos')
    opinion = models.TextField(blank=True)
    carpeta_referencia = models.ForeignKey(CarpetaReferencias, on_delete=models.CASCADE)

    class Meta:
        verbose_name_plural = 'Referencias'

class CarpetasDependientes(models.Model):
    vive_con_familia = models.BooleanField(default=False, blank=True)
    cantidad_dependientes_economicos = models.PositiveIntegerField(validators=[MinValueValidator(0), MaxValueValidator(999)], blank=True, default=0)
    cantidad_hijos = models.PositiveIntegerField(validators=[MinValueValidator(0), MaxValueValidator(999)], blank=True, default=0)
    empleado = models.OneToOneField(Empleado, on_delete=models.CASCADE)

    class Meta:
        verbose_name_plural = 'Carpeta Dependientes'

class Dependiente(models.Model):
    nombre = models.CharField(max_length=100, blank=True)
    apellido_paterno = models.CharField(max_length=100, blank=True)
    apellido_materno = models.CharField(max_length=100, blank=True)
    sexo = models.PositiveSmallIntegerField(choices=SEXO_OPCIONES, blank=True)
    fecha_nacimiento = models.DateField(blank=True)
    parentesco = models.PositiveSmallIntegerField(choices=PARENTESCO, blank=True)
    actividad =  models.PositiveSmallIntegerField(choices=ACTIVIDAD, blank=True)
    comentarios = models.TextField(blank=True)
    carpeta_dependiente = models.ForeignKey(CarpetasDependientes, on_delete=models.CASCADE)

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
    observacion = models.TextField(blank=True)
    empleado = models.OneToOneField(Empleado, on_delete=models.CASCADE)
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
    observacion = models.TextField(blank=True)
    empleado = models.OneToOneField(Empleado, on_delete=models.CASCADE)
    class Meta:
        verbose_name_plural = 'Carpeta Examen Toxicológico'

class CarpetaExamenMedico(models.Model):
    fecha_examen = models.DateField(blank=True)
    medico_agudeza_visual = models.CharField(max_length=100, blank=True)
    medico_agudeza_auditiva = models.CharField(max_length=100, blank=True)
    medico_agudeza_motriz = models.CharField(max_length=100, blank=True)
    medico_estado_nutricional = models.CharField(max_length=100, blank=True)
    medico_diagnostico_musculo_esqueletico = models.CharField(max_length=100, blank=True)
    medico_cardiologico = models.CharField(max_length=100, blank=True)
    medico_pulmonar = models.CharField(max_length=100, blank=True)
    medico_odontologico = models.CharField(max_length=100, blank=True)
    medico_resultado = models.CharField(max_length=100, blank=True)
    ishihara_visual_oi = models.CharField(max_length=10, blank=True)
    ishihara_visual_od = models.CharField(max_length=10, blank=True)
    ishihara_visual_ao = models.CharField(max_length=10, blank=True)
    ishihara_lentes = models.CharField(max_length=10, blank=True)
    ishihara_deuteranopia = models.CharField(max_length=30, blank=True)
    ishihara_protanopia = models.CharField(max_length=30, blank=True)
    ishihara_tritanopia = models.CharField(max_length=30, blank=True)
    ishihara_acromatopsia = models.CharField(max_length=30, blank=True)
    ishihara_resultado = models.CharField(max_length=100, blank=True)
    observacion = models.TextField(blank=True)
    empleado = models.OneToOneField(Empleado, on_delete=models.CASCADE)
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
    elasticidad = models.PositiveIntegerField(validators=[MinValueValidator(0), MaxValueValidator(10)], blank=True, default=0)
    velocidad = models.PositiveIntegerField(validators=[MinValueValidator(0), MaxValueValidator(10)], blank=True, default=0)
    resistencia = models.PositiveIntegerField(validators=[MinValueValidator(0), MaxValueValidator(10)], blank=True, default=0)
    condicion_fisica = models.PositiveIntegerField(validators=[MinValueValidator(0), MaxValueValidator(10)], blank=True, default=0)
    reflejos = models.PositiveIntegerField(validators=[MinValueValidator(0), MaxValueValidator(10)], blank=True, default=0)
    locomocion = models.PositiveIntegerField(validators=[MinValueValidator(0), MaxValueValidator(10)], blank=True, default=0)
    prueba_esfuerzo = models.PositiveIntegerField(validators=[MinValueValidator(0), MaxValueValidator(10)], blank=True, default=0)
    resultado = models.CharField(max_length=100)
    observacion = models.TextField(blank=True)
    empleado = models.OneToOneField(Empleado, on_delete=models.CASCADE)
    class Meta:
        verbose_name_plural = 'Carpeta Examen Físico'

class CarpetaExamenSocioeconomico(models.Model):
    
    # TODO: make a function that sums up all the amounts and returns the total amount
    def obtener_total_ingresos(self):
        total = sum(self.ingreso_familiar_1, self.ingreso_familiar_2, self.ingreso_familiar_3, self.ingreso_familiar_4)
        return total

    def obtener_total_egresos(self):
        total = sum(self.egresos_adeudos, self.egresos_agua, self.egresos_alimentacion, self.egresos_educacion, self.egresos_electricidad, self.egresos_gas, self.egresos_otros, self.egresos_renta, self.egresos_telefono, self.egresos_transporte)
        return total

    propiedades = models.CharField(max_length=200, blank=True)
    inversiones = models.CharField(max_length=200, blank=True)
    vehiculo = models.CharField(max_length=200, blank=True)
    tarjetas_credito_departamental = models.CharField(max_length=200, blank=True)
    adeudos_importantes = models.CharField(max_length=200, blank=True)
    tipo_domicilio = models.PositiveSmallIntegerField(choices=TIPO_DOMICILIO, blank=True)
    titular_domicilio = models.CharField(max_length=300, blank=True)
    tipo_vivienda = models.PositiveSmallIntegerField(choices=TIPO_VIVIENDA, blank=True)
    anios_residencia =  models.CharField(max_length=10, blank=True)
    niveles = models.PositiveIntegerField(validators=[MinValueValidator(-99), MaxValueValidator(999)], blank=True, default=0)
    cuartos = models.PositiveIntegerField(validators=[MinValueValidator(0), MaxValueValidator(99999)], blank=True, default=0)
    banos = models.PositiveIntegerField(validators=[MinValueValidator(0), MaxValueValidator(999)], blank=True, default=0)
    patios = models.PositiveIntegerField(validators=[MinValueValidator(0), MaxValueValidator(999)], blank=True, default=0)
    material_paredes = models.PositiveSmallIntegerField(choices=MATERIAL_PAREDES, blank=True)
    material_pisos = models.PositiveSmallIntegerField(choices=MATERIAL_PISOS, blank=True)
    material_techos = models.PositiveSmallIntegerField(choices=MATERIAL_TECHOS, blank=True)
    mobiliario_vivienda = models.PositiveSmallIntegerField(choices=MOBILIARIO_VIVIENDA, blank=True)
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
    empleado = models.OneToOneField(Empleado, on_delete=models.CASCADE)
    gasto_diario = models.DecimalField(max_digits=10, decimal_places=2, blank=True)
    ingreso_familiar_adicional = models.DecimalField(max_digits=10, decimal_places=2, blank=True, default=0)
    importe_ingreso_interesado = models.DecimalField(max_digits=10, decimal_places=2, blank=True, default=0)
    familiar_1 = models.CharField(max_length=35)
    ingreso_familiar_1 = models.DecimalField(max_digits=10, decimal_places=2, blank=True, default=0)
    familiar_2 = models.CharField(max_length=35)
    ingreso_familiar_2 = models.DecimalField(max_digits=10, decimal_places=2, blank=True, default=0)
    familiar_3 = models.CharField(max_length=35)
    ingreso_familiar_3 = models.DecimalField(max_digits=10, decimal_places=2, blank=True, default=0)
    familiar_4 = models.CharField(max_length=35)
    ingreso_familiar_4 = models.DecimalField(max_digits=10, decimal_places=2, blank=True, default=0)
    total_ingresos = models.DecimalField(max_digits=10, decimal_places=2, blank=True, default=obtener_total_ingresos)
    egresos_alimentacion = models.DecimalField(max_digits=10, decimal_places=2, blank=True, default=0)
    egresos_renta = models.DecimalField(max_digits=10, decimal_places=2, blank=True, default=0)
    egresos_agua = models.DecimalField(max_digits=10, decimal_places=2, blank=True, default=0)
    egresos_electricidad = models.DecimalField(max_digits=10, decimal_places=2, blank=True, default=0)
    egresos_gas = models.DecimalField(max_digits=10, decimal_places=2, blank=True, default=0)
    egresos_telefono = models.DecimalField(max_digits=10, decimal_places=2, blank=True, default=0)
    egresos_transporte = models.DecimalField(max_digits=10, decimal_places=2, blank=True, default=0)
    egresos_educacion = models.DecimalField(max_digits=10, decimal_places=2, blank=True, default=0)
    egresos_adeudos = models.DecimalField(max_digits=10, decimal_places=2, blank=True, default=0)
    egresos_otros = models.DecimalField(max_digits=10, decimal_places=2, blank=True, default=0)
    total_egresos = models.DecimalField(max_digits=10, decimal_places=2, blank=True, default=obtener_total_egresos)
    salud_alergias = models.CharField(max_length=100, blank=True)
    salud_visual_auditiva_fisica = models.CharField(max_length=100, blank=True)
    salud_cirugias = models.CharField(max_length=100, blank=True)
    salud_enfermedad_cronica = models.CharField(max_length=100, blank=True)
    cigarro = models.BooleanField(blank=True, default=False)
    cantidad_frecuencia_ciqarro = models.CharField(max_length=100, blank=True)
    alcohol = models.BooleanField(blank=True, default=False)
    cantidad_frecuencia_alcohol = models.CharField(max_length=100, blank=True)
    vicios = models.CharField(max_length=100, blank=True)
    atencion_medica_familiares = models.BooleanField(blank=True, default=False)
    at_medica_observaciones = models.CharField(max_length=100, blank=True)
    estado_salud_propio = models.CharField(max_length=100, blank=True)
    ultima_vez_enfermo = models.CharField(max_length=100, blank=True)
    embarazada = models.CharField(max_length=100, blank=True)
    contacto_emergencia = models.CharField(max_length=100, blank=True)
    validador_num_telefono = RegexValidator(regex=r'^\+?1?\d{9,10}$', message='El número telefónico debe ser ingresado de la siguiente manera: "5512345678". Limitado a 10 dígitos.')
    telefono_emergencia = models.CharField(validators=[validador_num_telefono], max_length=17, blank=True, help_text='Ingrese número telefónico a 10 dígitos')
    parentesco_contacto = models.CharField(max_length=100, blank=True)
    actividates_fin_semana = models.PositiveSmallIntegerField(choices=ACTIVIDADES_FIN_SEMANA, blank=True)
    actividades_culturales_deportes = models.CharField(max_length=100, blank=True)
    estudia = models.BooleanField(blank=True, default=False)
    que_estudia = models.CharField(max_length=100, blank=True)
    organizacion_familia = models.CharField(max_length=100, blank=True)
    comunicacion = models.CharField(max_length=100, blank=True)
    roles = models.CharField(max_length=100, blank=True)
    autoridad = models.CharField(max_length=100, blank=True)
    limites = models.CharField(max_length=100, blank=True)
    calidad_vida = models.CharField(max_length=100, blank=True)
    imagen_publica = models.CharField(max_length=100, blank=True)
    comportamiento_social = models.CharField(max_length=100, blank=True)
    demanda_laboral = models.CharField(max_length=100, blank=True)
    antecedentes_penales = models.CharField(max_length=100, blank=True)
    porque_este_empleo = models.CharField(max_length=200, blank=True)
    puesto_deseado = models.CharField(max_length=100, blank=True)
    area_deseada = models.CharField(max_length=100, blank=True)
    tiempo_ascenso = models.CharField(max_length=100, blank=True)
    obtencion_reconocimiento = models.CharField(max_length=100, blank=True)
    obtencion_ascenso = models.CharField(max_length=100, blank=True)
    capacitacion_deseada = models.CharField(max_length=100, blank=True)
    fecha_entrevista = models.DateField(blank=True)

    class Meta:
        verbose_name_plural = 'Carpeta Examen Socioeconómico'

class DocumentosDigitales(models.Model):
    hoja_datos = models.FileField(upload_to="temp/documentos", blank=True)
    solicitud = models.ImageField(upload_to="temp/documentos", blank=True)
    ine = models.ImageField(upload_to="temp/documentos", blank=True)
    acta_nacimiento = models.ImageField(upload_to="temp/documentos", blank=True)
    folio_acta_nacimiento = models.CharField(max_length=20, blank=True)
    curp = models.FileField(upload_to="temp/documentos", blank=True)
    comprobante_domicilio = models.ImageField(upload_to="temp/documentos", blank=True)
    fecha_comprobante_domicilio = models.DateField(blank=True)
    antecedentes_no_penales = models.ImageField(upload_to="temp/documentos", blank=True)
    fecha_antecedentes_no_penales = models.DateField(blank=True)
    comprobante_estudios = models.ImageField(upload_to="temp/documentos", blank=True)
    cartilla_smn = models.ImageField(upload_to="temp/documentos", blank=True)
    nss = models.FileField(upload_to="temp/documentos", blank=True)
    carta_recomendacion = models.FileField(upload_to="temp/documentos", blank=True)
    contrato = models.FileField(upload_to="temp/documentos", blank=True)
    socioeconomico = models.FileField(upload_to="temp/documentos", blank=True)
    fecha_socioeconomico = models.DateField(blank=True)
    foto_socioeconomico = models.ImageField(upload_to="temp/documentos", blank=True)
    psicologico = models.FileField(upload_to="temp/documentos", blank=True)
    fecha_psicologico = models.DateField(blank=True)
    medico = models.FileField(upload_to="temp/documentos", blank=True)
    fecha_medico = models.DateField(blank=True)
    toxicologico = models.FileField(upload_to="temp/documentos", blank=True)
    fecha_toxicologico = models.DateField(blank=True)
    fisico = models.FileField(upload_to="temp/documentos", blank=True)
    fecha_fisico = models.DateField(blank=True)
    croquis = models.ImageField(upload_to="temp/documentos", blank=True)
    curriculum = models.FileField(upload_to="temp/documentos", blank=True)
    empleado = models.OneToOneField(Empleado, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.empleado}'
    
    class Meta:
        verbose_name_plural = 'Documentos Personales'

class Domicilio(models.Model):
    calle = models.CharField(max_length=100, blank=True)
    numero_exterior = models.PositiveIntegerField(validators=[MinValueValidator(1), MaxValueValidator(99999)], blank=True)
    numero_interior = models.IntegerField(validators=[MinValueValidator(-99), MaxValueValidator(99999)], blank=True)
    entre_calle = models.CharField(max_length=100, null=True, blank=True)
    y_calle = models.CharField(max_length=100, null=True, blank=True)
    ciudad = models.CharField(max_length=50, blank=True)
    empleado = models.OneToOneField(Empleado, on_delete=models.CASCADE, null=True)
    cliente_generales = models.OneToOneField(ClienteGenerales, on_delete=models.CASCADE, null=True)
    cliente_pagos = models.OneToOneField(ClientePagos, on_delete=models.CASCADE, null=True)
    referencia = models.OneToOneField(Referencia, on_delete=models.CASCADE, null=True)

    def __str__(self):
        if self.empleado is not None:
            return f'{self.empleado}'
        if self.cliente_generales is not None:
            return f'{self.cliente_generales}'
        if self.cliente_pagos is not None:
            return f'{self.cliente_pagos}'

    class Meta:
        verbose_name_plural = 'Domicilios'

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

class Curp(models.Model):
    empleado = models.OneToOneField(Empleado, on_delete=models.CASCADE)
    curp_regex = r'^[A-Z]{1}[AEIOU]{1}[A-Z]{2}[0-9]{2}(0[1-9]|1[0-2])(0[1-9]|[1-2][0-9]|3[0-1])[HM]{1}(AS|BC|BS|CC|CS|CH|CL|CM|DF|DG|GT|GR|HG|JC|MC|MN|MS|NT|NL|OC|PL|QT|QR|SP|SL|SR|TC|TS|TL|VZ|YN|ZS|NE)[B-DF-HJ-NP-TV-Z]{3}[0-9A-Z]{1}[0-9]{1}$'
    curp = models.CharField(max_length=18, blank=True, unique=True,validators=[RegexValidator(curp_regex, 'La CURP no es válida')])
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
    estatus_curp = models.CharField(max_length=20, choices=ESTATUS_CURP, blank=True, null=True)
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
                    estatus_curp_completo = dict(ESTATUS_CURP).get(estatus_curp_clave, "Opción no existe" )
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
    class Meta:
        verbose_name_plural = 'CURP'

class Rfc(models.Model):
    #TODO: Make a connection with a RFC_DB
    #TODO: Function to transform Str to Date data type (Signals)
    

    rfc_regex = r'/^([A-ZÑ&]{3,4}) ?(?:- ?)?(\d{2}(?:0[1-9]|1[0-2])(?:0[1-9]|[12]\d|3[01])) ?(?:- ?)?([A-Z\d]{2})([A\d])$/'
    rfc = models.CharField(max_length=18, blank=True, validators=[RegexValidator(rfc_regex, 'La CURP no es válida')])
    rfc_digital = models.FileField(upload_to="temp/documentos", blank=True, unique=True)
    razon_social  = models.CharField(max_length=255, blank=True, null=True)
    estatus = models.CharField(max_length=20, blank=True, null=True)
    fecha_efectiva = models.DateField(blank=True, null=True)
    correo_contacto = models.CharField(max_length=200, blank=True, null=True)
    validez = models.CharField(max_length=20, blank=True, null=True)
    tipo = models.CharField(max_length=20, blank=True, null=True)
    empleado = models.OneToOneField(Empleado, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.rfc}: {self.empleado}'
    
    class Meta:
        verbose_name_plural = 'RFC'