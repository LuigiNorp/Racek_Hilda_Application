SEXO_OPCIONES = (
    (1, 'FEMENINO'),
    (2, 'MASCULINO'),
    (3, 'NO BINARIO'),
)

PROCESO_RACEK = (
    (1, "CONTRATADO"),
    (2,"APTO CON RESERVA"),
    (3,"NO CONCLUYÓ"),
    (4,"CANCELADO"),
    (5,"EN EVALUACIÓN"),
    (6,"APTO"),
    (7,"NO APTO"),
    (8,"BAJA"),
)

MODALIDAD = (
    (1,"ADMINISTRATIVO"),
    (2,"EN LOS BIENES"),
    (3,"EN EL TRASLADO DE BIENES"),
    (4,"A PERSONAS"),
    (5,"MANTENIMIENTO"),
)

ESTATUS_EMPLEADO = (
    (1,"ACTIVO"),
    (2,"BAJA SIN ENTREGAR UNIFORME"),
    (3,"BAJA PROCESO COMPLETO"),
    (4,"BAJA DEMANDÓ"),
    (5,"BAJA DEMANDADO"),
)

NIVEL_MANDO = (
    (1,"MEDIO"),
    (2,"NINGUNO"),
    (3,"ALTO"),
)

ESTADO_REGISTROS = (
    (1,"NO REQUERIDO"),
    (2,"EN TRÁMITE"),
    (3,"ACEPTADO"),
    (4,"RECHAZADO"),
)

EDO_CIVIL = (
    (1,"SOLTERO(A)"),
    (2,"CASADO(A)"),
    (3,"VIUDO(A)"),
    (4,"DIVORCIADO(A)"),
    (5,"UNIÓN LIBRE O CONCUBINATO"),
)

ESTADO_CARTILLA = (
    (1,"PRE-CARTILLA"),
    (2,"LIBERADA"),
    (3,"NO APLICA"),
    (4,"PRESENTÓ"),
)

ESCOLARIDAD = (
    (1,"SIN ESCOLARIDAD"),
    (2,"PRIMARIA INCOMPLETA"),
    (3,"PRIMARIA COMPLETA"),
    (4,"SECUNDARIA INCOMPLETA"),
    (5,"SECUNDARIA COMPLETA"),
    (6,"CARRERA TÉCNICA INCOMPLETA"),
    (7,"CARRERA TÉCNICA COMPLETA"),
    (8,"BACHILLERATO INCOMPLETA"),
    (9,"BACHILLERATO COMPLETA"),
    (10,"LICENCIATURA INCOMPLETA"),
    (11,"LICENCIATURA COMPLETA"),
    (12,"ESPECIALIDAD INCOMPLETA"),
    (13,"ESPECIALIDAD COMPLETA"),
    (14,"MAESTRÍA INCOMPLETA"),
    (15,"MAESTRÍA COMPLETA"),
    (16,"DOCTORADO INCOMPLETA"),
    (17,"DOCTORADO COMPLETA"),
    (18,"ANALFABETO(A)"),
)

COMPROBANTE_ESTUDIOS = (
    (1,"NINGUNO"),
    (2,"BOLETA"),
    (3,"DIPLOMA"),
    (4,"CONSTANCIA"),
    (5,"CERTIFICADO"),
    (6,"TÍTULO"),    
)

ANTECEDENTES = (
    (1,"1ER EMPLEO"),
    (2,"SIN EXPERIENCIA EN SEGURIDAD PRIVADA"),
    (3,"EXPERIENCIA EN SEGURIDAD PRIVADA"),
    (4,"MILITAR CON BAJA"),
    (5,"MILITAR RETIRADO"),
    (6,"EX-POLICÍA"),       
)

COMPLEXION = (
    (1,"DELGADA"),
    (2,"REGULAR"),
    (3,"ROBUSTA"),
    (4,"ATLÉTICA"),
    (5,"OBESA"),    
)

COLOR_PIEL = (
    (1,"ALBINO"),
    (2,"BLANCO"),
    (3,"AMARILLO"),
    (4,"MORENO CLARO"),
    (5,"MORENO"),
    (6,"MORENO OSCURO"),
    (7,"NEGRO"),
    (8,"OTRO"),
)

CARA = (
    (1,"ALARGADA"),
    (2,"CUADRADA"),
    (3,"OVALADA"),
    (4,"REDONDA"),    
)

SANGRE = (
    (1,"NO SABE"),
    (2,"A"),
    (3,"B"),
    (4,"O"),
    (5,"AB"),
)

RH = (
    (1,"-"),
    (2,"+"),
)

FACTURACION_TIPO = (
    (1,"QUINCENAL"),
    (2,"MENSUAL"),
    (3,"POR EVENTO"),    
)

TIPO_REFERENCIA = (
    (1,"FAMILIAR CERCANO"),
    (2,"PARIENTE CERCANO"),
    (3,"PERSONAL"),
    (4,"VECINAL"),
    (5,"LABORAL"),    
)

# TODO: Preguntar a Hilda Por las opciones completas
OCUPACION = (
    (1,"ADMINISTRATIVO"),
    (2,"AGRÍCOLA-GANADERO, SILVICULTURA Y PESCA"),
    (3,"COMERCIANTE Y AGENTE DE VENTAS"),
    (4,"DE LA EDUCACIÓN"),
    (5,"DE SERVICIOS DOMÉSTICOS REMUNERADOS"),
    (6,"DE SERVICIOS PERSONALES"),
    (7,"DEL ARTE, ESPECTÁCULOS Y DEPORTES"),
    (8,"EMPLEADO"),
    (9,"ESTUDIANTE"),
    (10,"FUNCIONARIO DEL SECTOR PRIVADO"),
    (11,"FUNCIONARIO DEL SECTOR PÚBLICO"),
    (12,"HOGAR"),
    (13,"JEFES DE ACTIVIDADES ADMINISTRATIVAS"),
    (14,"JUBILADO"),
    (15,"NO TRABAJA"),
    (16,"OBRERO"),
    (17,"OPERADOR DE MÁQUINAS DE PRODUCCIÓN"),
    (18,"OPERADOR DE TRANSPORTES"),
    (19,"PERSONA CONTRATADA EN ACTIVIDADES INDUSTRIALES"),
    (20,"PERSONA DE APOYO EN LA INDUSTRIA ARTESANAL"),
    (21,"PROFESIONISTA"),
    (22,"REPRESENTANTE LEGAL"),
    (23,"SECRETARIA"),
    (24,"SERVIDOR DE PROTECCIÓN Y VIGILANCIA"),
    (25,"TÉCNICO"),
    (26,"VENDEDOR AMBULANTE"),
)

PARENTESCO = (
    (1,"ABUELO(A)"),
    (2,"AHIJADO(A)"),
    (3,"AMISTAD"),
    (4,"AMOROSA"),
    (5,"CÓNYUGE"),
    (6,"CUÑADO(A)"),    
    (7,"ENTENADO(A)"),
    (8,"HERMANO(A)"),
    (9,"HIJO(A)"),
    (10,"LABORAL"),
    (11,"MADRE"),
    (12,"MADRINA"),
    (13,"NIETO(A)"),
    (14,"PADRE"),
    (15,"PADRINO"),
    (16,"PRIMO(A)"),
    (17,"SOBRINO(A)"),
    (18,"SUEGRO(A)"),
    (19,"TÍO(A)"),
    (20,"YERNO O NUERA"),
)    

ACTIVIDAD = (
    (1,"HOGAR"),
    (2,"ESTUDIANTE"),
    (3,"INCAPACITADO"),
    (4,"PENSIONADO"),
    (5,"DESEMPLEADO"),        
)

OPCIONES_PSICOLOGICO = (
    (1,"DEFICIENTE"),
    (2,"BUENO"),
    (3,"EXCELENTE"),    
)

RESULTADO_PSICOLOGICO = (
    (1,"NO APTO"),
    (2,"APTO BAJO RESERVA"),
    (3,"APTO"),
)

TIPO_DOMICILIO  = (
    (1,"PROPIO"),
    (2,"RENTADO"),
    (3,"HIPOTECADO"),
    (4,"PRESTADO"),
    (5,"FAMILIAR"),            
)

TIPO_VIVIENDA = (
    (1,"CASA SOLA"),
    (2,"DEPARTAMENTO"),
    (3,"VECINDAD"),
    (4,"CAMPAMENTO"),
    (5,"ALBERGUE"),      
)

MATERIAL_PAREDES = (
    (1,"TABIQUE"),
    (2,"MADERA"),
    (3,"CARTÓN"),
    (4,"OTROS"),
)

MATERIAL_PISOS = (
    (1,"MOZAICO"),
    (2,"LOSETA"),    
    (3,"CEMENTO"),
    (4,"TIERRA APISONADA"),
)

MATERIAL_TECHOS = (
    (1,"CONCRETO"),
    (2,"LÁMINA DE ASBESTO"),
    (3,"CARTÓN"),
    (4,"LÁMINA METÁLICA"),    
)

MOBILIARIO_VIVIENDA = (
    (1,"SENCILLO"),
    (2,"RUSTICO"),    
    (3,"MODERNO"),    
)

ACTIVIDADES_FIN_SEMANA = (
    (1,"PRACTICAR DEPORTE"),
    (2,"VER TELEVISIÓN"),
    (3,"IR AL CINE"),
    (4,"VISITAR FAMILIARES"),
    (5,"ACTIVIDAD AL AIRE LIBRE"),
    (6,"REALIZAR QUEHACERES DEL HOGAR"),    
)

ESTATUS_CURP = (
    ('AN','Alta Normal'),
    ('AH','Alta con Homonimia'),
    ('RCC','Registro de cambio afectando a CURP'),
    ('RCN','Registro de cambio no afectando a CURP'),
    ('BD','Baja por defunción'),
    ('BSU','Baja sin uso'),
    ('BJD','Baja Judicial'),
    ('BDM','Baja administrativa'),
    ('BAP','Baja por documento apócrifo'),
    ('BDP','Baja por adopción'),
)

RECOMENDABLE = (
    (1,"SI"),
    (2,"NO"),
    (3,"BAJO RESERVA"),
)

CALIF_BUENO_MALO = (
    (1,"DEFICIENTE"),
    (2,"REGULAR"),
    (3,"BUENO"),
    (4,"EXCELENTE"),
)

TIPO_SEPARACION = (
    (1,"RENUNCIA"),
    (2,"CAUSA ADMINISTRATIVA"),
    (3,"COMETER DELITO"),
    (4,"PENSIONADO(A)"),
    (5,"DEFUNCIÓN"),      
)

IMPARTIDO_RECIBIDO = (
    (1,"IMPARTIDO"),
    (2,"RECIBIDO"),    
)

EFICIENCIA_TERMINAL = (
    (1,"INCONCLUSO"),
    (2,"CONCLUIDO"),
    (3,"CURSANDO"),
    (4,"SOLICITUD"),    
)