from import_export import resources
from .models import (
    Cliente,
    Sede,
    DocumentosCliente,
    CarpetaClienteGenerales,
    CarpetaClientePagos,
    CarpetaClienteContactos,
    PaqueteCapacitacion,
    RepresentanteTrabajadores
)


class ClienteResource(resources.ModelResource):
    class Meta:
        model = Cliente
        fields = ('nombre_comercial', 'razon_social', 'activo', 'updated_at', 'update_by')


class SedeResource(resources.ModelResource):
    class Meta:
        model = Sede
        fields = ('clave_sede', 'nombre_sede', 'cliente', 'updated_at', 'update_by')


class DocumentosClienteResource(resources.ModelResource):
    class Meta:
        model = DocumentosCliente
        fields = ('qr_code', 'logotipo', 'updated_at', 'update_by')


class CarpetaClienteGeneralesResource(resources.ModelResource):
    class Meta:
        model = CarpetaClienteGenerales
        fields = (
            'reg_estatal', 'reg_federal', 'rfc', 'telefono_1', 'telefono_2', 'telefono_3',
            'representante_legal', 'encargado_operativo', 'encargado_rh', 'coordinador',
            'registro_patronal',  'updated_at', 'update_by'
        )


class CarpetaClientePagosResource(resources.ModelResource):
    class Meta:
        model = CarpetaClientePagos
        fields = (
            'encargado_pagos', 'telefono_oficina', 'telefono_celular', 'email', 'rfc', 'facturacion_tipo',
            'revision', 'pagos', 'factura_subtotal', 'factura_iva', 'factura_total', 'updated_at', 'update_by'
        )


class CarpetaClienteContactosResource(resources.ModelResource):
    class Meta:
        model = CarpetaClienteContactos
        fields = (
            'nombre_contacto', 'telefono_1', 'telefono_2', 'telefono_3',
            'puesto', 'email_1', 'email_2', 'updated_at', 'update_by'
        )


class PaqueteCapacitacionResource(resources.ModelResource):
    class Meta:
        model = PaqueteCapacitacion
        fields = (
            'estatus_capacitacion', 'fecha_solicitud', 'detalle_solicitud', 'fecha_realizacion',
            'detalle_realizacion', 'fecha_entrega', 'detalle_entrega', 'fecha_facturado', 'no_factura',
            'fecha_pagado', 'detalle_pagado', 'comentarios', 'updated_at', 'update_by'
        )


class RepresentanteTrabajadoresResource(resources.ModelResource):
    class Meta:
        model = RepresentanteTrabajadores
        fields = ('cliente', 'personal', 'nombre_completo', 'firma', 'reglamento_interno', 'updated_at', 'update_by')
