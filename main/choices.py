DEPARTAMENTO = (
    (1, 'César'),
    (2, 'Karla'),
    (3,'Ramiro'),
)

PERMISOS = (
    (1, 'employee'),
    (2, 'supervisor'),
    (3, 'manager'),
    (4, 'superboss'),
    (5, 'dbadmin'),
)

# Group names with special permissions
REGISTER_ENABLED_GROUPS = ['Admin', 'Superboss', 'Manager']
DB_DELETE_ENABLED_GROUPS = ['Admin','Superboss']
SUPERUSER_GROUPS = ['Superboss']