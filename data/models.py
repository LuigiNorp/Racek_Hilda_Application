from django.db import models
from .choices import *
from django.core.validators import RegexValidator
from django.core.validators import  MinValueValidator, MaxValueValidator
from datetime import datetime
from dateutil.relativedelta import relativedelta

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

    def obtener_total():
        pass

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
    total_ingresos = models.DecimalField(max_digits=10, decimal_places=2, blank=True, default=obtener_total)
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
    total_egresos = models.DecimalField(max_digits=10, decimal_places=2, blank=True, default=obtener_total)
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

class Curp(models.Model):
    
    # TODO: Make a connection with a CURP_DB
    # TODO: Make a Consult function to save third person APIs Info (Signals)
    
    def check_curp_info():
        pass
    
    # TODO: Function to transform Str to Date data type (Signals)
    
    def transform_api_str_to_date():
        pass

    # TODO: Function to verify CURP by regex 
    def verify_curp_syntax():
        pass

    # TODO: Function to transform gender str into options
    def api_str_to_option():
        pass

    # TODO: Function to calculate age
    def calculate_age():
        pass

    # TODO: Function to transform year str into integer
    def transform_str_year_to_integer():
        pass

    curp = models.CharField(max_length=18, default=verify_curp_syntax)
    nombre = models.CharField(max_length=100, blank=True)
    apellido_paterno = models.CharField(max_length=100, blank=True)
    apellido_materno = models.CharField(max_length=100, blank=True)
    iniciales = models.CharField(max_length=30, default=check_curp_info, blank=True)
    fecha_nacimiento = models.DateField(blank=True, default=transform_api_str_to_date)
    edad = models.PositiveIntegerField(validators=[MinValueValidator(18), MaxValueValidator(99)], blank=True, default=calculate_age)
    anio_registro = models.PositiveIntegerField(validators=[MinValueValidator(1850), MaxValueValidator(2200)], blank=True, default=transform_str_year_to_integer)
    numero_acta = models.CharField(max_length=6, blank=True)
    validacion_renapo = models.CharField(max_length=3,blank=True)
    sexo = models.PositiveSmallIntegerField(choices=SEXO_OPCIONES, default=api_str_to_option, blank=True)
    estatus_curp = models.CharField(max_length=20, blank=True)
    empleado = models.OneToOneField(Empleado, on_delete=models.CASCADE)


    def __str__(self):
        return f'{self.curp}: {self.nombre} {self.apellido_paterno} {self.apellido_materno} ({self.empleado})'
    
    class Meta:
        verbose_name_plural = 'CURP'

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