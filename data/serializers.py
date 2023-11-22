from rest_framework import serializers
from data.models import *
from main.models import *
from django.contrib.auth import authenticate


class CustomUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = (
            'id',
            'username',
            'email',
            'password',
            'nombre',
            'apellido_paterno',
            'apellido_materno',
            'departamento'
        )
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        return CustomUser.objects.create_user(**validated_data)

    def update(self, instance, validated_data):
        password = validated_data.pop('password', None)
        user = super().update(instance, validated_data)

        if password:
            user.set_password(password)
            user.save()

        return user


class AuthTokenSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField(style={'input_type': 'password'})

    def validate(self, data):
        username = data.get('username')
        password = data.get('password')
        user = authenticate(
            request=self.context.get('request'),
            username=username,
            password=password
        )

        if not user:
            raise serializers.ValidationError(
                'No se pudo realizar la autenticación satisfactoriamente',
                code='authorization')

        data['user'] = user
        return data


class EditProfileSerializer(serializers.ModelSerializer):
    nombre = serializers.CharField(max_length=100)
    apellido_paterno = serializers.CharField(max_length=100)
    apellido_materno = serializers.CharField(max_length=100)

    class Meta:
        model = CustomUser
        fields = (
            'nombre',
            'apellido_paterno',
            'apellido_materno'
        )


def create_serializer(model, fields=None):
    """
    Creates a serializer for the given model.
    Args:
        model: The Django model for which the serializer is being created.
        fields: A list or tuple of fields to be included in the serializer. If not provided, all fields will be included.
    Returns:
        A Django Rest Framework serializer for the given model.
    """

    class_name = f"{model.__name__}Serializer"
    fields = fields if fields else "__all__"
    meta_class = type('Meta', (object,), {'model': model, 'fields': fields})
    return type(class_name, (serializers.ModelSerializer,), {'Meta': meta_class})


CurpEmpleadoSerializer = create_serializer(Curp)
CurpPrevioSerializer = create_serializer(
    CurpPrevio,
    [
        'curp',
        'nombre',
        'apellido_paterno',
        'apellido_materno',
        'sexo']
)
RfcEmpleadoSerializer = create_serializer(Rfc)
RfcPrevioSerializer = create_serializer(
    RfcPrevio,
    [
        'rfc',
        'rfc_digital'
    ]
)
ClienteEmpleadoSerializer = create_serializer(Cliente)
ClientePrevioSerializer = create_serializer(
    Cliente,
    [
        'id',
        'nombre_comercial'
    ]
)
DocumentosClienteSerializer = create_serializer(DocumentosCliente)
SedeEmpleadoSerializer = create_serializer(Sede)
SedePrevioSerializer = create_serializer(
    Sede,
    ['nombre_sede'])
CarpetaClienteGeneralesSerializer = create_serializer(CarpetaClienteGenerales)
CarpetaClientePagosSerializer = create_serializer(CarpetaClientePagos)
CarpetaClienteContactosSerializer = create_serializer(CarpetaClienteContactos)
PersonalEmpleadoSerializer = create_serializer(Personal)
PersonalPrevioSerializer = create_serializer(
    Personal,
    [
        'folio',
        'origen',
        'fecha',
        'observaciones',
        'resultado'
    ]
)
EvaluadorEmpleadoSerializer = create_serializer(Evaluador)
EvaluadorPrevioSerializer = create_serializer(
    Evaluador,
    ['solicitante']
)
OcupacionSerializer = create_serializer(Ocupacion)
InstructorSerializer = create_serializer(Instructor)
CarpetaLaboralSerializer = create_serializer(CarpetaLaboral)
CarpetaGeneralesEmpleadoSerializer = create_serializer(CarpetaGenerales)
CarpetaGeneralesPrevioSerializer = create_serializer(
    CarpetaGeneralesPrevio,
    [
        'estado_civil',
        'escolaridad',
        'telefono_domicilio',
        'telefono_celular',
        'telefono_recados',
        'email_empleado'
    ]
)
ReferenciaSerializer = create_serializer(Referencia)
CarpetaDependientesSerializer = create_serializer(CarpetaDependientes)
DependienteSerializer = create_serializer(Dependiente)
CarpetaExamenPsicologicoEmpleadoSerializer = create_serializer(CarpetaExamenPsicologico)
CarpetaExamenPsicologicoPrevioSerializer = create_serializer(
    CarpetaExamenPsicologicoPrevio,
    [
        'resultado_aspirante',
        'observacion'
    ]
)
CarpetaExamenToxicologicoEmpleadoSerializer = create_serializer(CarpetaExamenToxicologico)
CarpetaExamenToxicologicoPrevioSerializer = create_serializer(
    CarpetaExamenToxicologicoPrevio,
    [
        'resultado_aspirante',
        'observacion'
    ]
)
CarpetaExamenMedicoEmpleadoSerializer = create_serializer(CarpetaExamenMedico)
CarpetaExamenMedicoPrevioSerializer = create_serializer(
    CarpetaExamenMedicoPrevio,
    [
        'resultado_aspirante',
        'observacion'
    ]
)
CarpetaExamenFisicoEmpleadoSerializer = create_serializer(CarpetaExamenFisico)
CarpetaExamenFisicoPrevioSerializer = create_serializer(
    CarpetaExamenFisicoPrevio,
    [
        'resultado_aspirante',
        'observacion'
    ]
)
CarpetaExamenSocioeconomicoEmpleadoSerializer = create_serializer(CarpetaExamenSocioeconomico)
CarpetaExamenSocioeconomicoPrevioSerializer = create_serializer(
    CarpetaExamenSocioeconomicoPrevio,
    [
        'resultado_aspirante',
        'observacion'
    ]
)
CarpetaExamenPoligrafoEmpleadoSerializer = create_serializer(CarpetaExamenPoligrafo)
CarpetaExamenPoligrafoPrevioSerializer = create_serializer(
    CarpetaExamenPoligrafoPrevio,
    [
        'resultado_aspirante',
        'observacion'
    ]
)
EmpleoAnteriorSeguridadPublicaSerializer = create_serializer(EmpleoAnteriorSeguridadPublica)
PuestoFuncionalSerializer = create_serializer(PuestoFuncional)
TipoBajaSerializer = create_serializer(TipoBaja)
EmpleoAnteriorSerializer = create_serializer(EmpleoAnterior)
MotivoSeparacionSerializer = create_serializer(MotivoSeparacion)
CapacitacionSerializer = create_serializer(Capacitacion)
IdiomaSerializer = create_serializer(Idioma)
CarpetaMediaFiliacionEmpleadoSerializer = create_serializer(CarpetaMediaFiliacion)
CarpetaMediaFiliacionPrevioSerializer = create_serializer(
    CarpetaMediaFiliacionPrevio,
    [
        'peso',
        'estatura',
        'tension_arterial',
        'temperatura',
        'indice_masa_corporal',
        'clasificacion_imc',
        'sat02',
        'frecuencia_cardiaca',
        'cronica_degenerativa',
        'sangre',
        'rh'
    ]
)
DocumentosDigitalesEmpleadoSerializer = create_serializer(DocumentosDigitales)
DocumentosDigitalesPrevioSerializer = create_serializer(
    DocumentosDigitalesPrevio,
    [
        'acta_nacimiento',
        'ine',
        'comprobante_domicilio',
        'comprobante_estudios',
        'curp',
        'cartilla_smn',
        'nss',
        'huellas_digitales'
    ]
)
RepresentanteTrabajadoresSerializer = create_serializer(RepresentanteTrabajadores)
CapacitacionClienteSerializer = create_serializer(PaqueteCapacitacion)
DomicilioSerializer = create_serializer(Domicilio)
CodigoPostalSerializer = create_serializer(CodigoPostal)
