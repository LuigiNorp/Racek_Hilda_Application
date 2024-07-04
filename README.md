# Racek_Hilda_Application

## Descripción

Racek_Hilda_Application es una aplicación web desarrollada con Django Rest Framework que le pertenece a Racek, la cual permite registrar y disponer información de manera sencilla de los trámites para Empresas de Seguridad Privada que Racek tiene como clientes. Permite registrar usuarios de Racek (Gestores) y empleados de la empresa cliente, guardar sus documentos en una base de datos MariaDB; la aplicación utiliza dos bases de datos: una para almacenar todos los usuarios y datos de la aplicación, y otra para almacenar la información ingresada a través del sitio web.

Permite la generación reportes en formato PDF a partir de plantillas hechas en archivos DOCX y XLSX. Igualmente permite la exportación e importación de la base de datos. La importación se puede hacer por medio de un archivo CSV


### Tipos de Usuarios

#### 1) Gestor (Operative)

Permisos limitados a **ingresar información a la base de datos**, estos cambios deben ser autorizados por el usuario Supervisor.

#### 2) Supervisor

Con permisos para **validar la información capturada por** el usuario **Operative**, **autorizar movimientos** en los rubros **de** **los equipos**, puede modificar la información ingresada por el usuario Operative. Solo puede acceder a las empresas que tiene asignadas.

#### 3) Gerente (Manager)

**Con permiso para crear usuarios** (Supervisor y Operative), validar la información capturada por los usuarios Administrativos.  autorizar movimientos en los rubros de los equipos, solo puede acceder y modificar la información de los proyectos que tiene asignados.

#### 4) Superboss (SuperUser)

**Con acceso completo** a modificar la base de datos (SuperUser), crear usuarios (Manager, Supervisor, Operative, Employee y Admin), autorizar movimientos de equipos, ****define quien puede tener acceso a información y privilegios**, ver la información completa, descargar la base de datos completa**. Con acceso al panel de control de pendientes.

#### 5) Empleado (Employee)

Permisos limitados a **ingresar información a la base de datos**, estos cambios deben ser autorizados por el usuario Supervisor. Solo puede acceder a los formularios del empleado.

#### 6) Mantenimiento (Admin)

**Con** casi **todos** los **permisos** para **modificar** la **base** de **datos** **excepto** para **crear** nuevos **usuarios** ni **borrar** la **base** de **datos**. Solicita permisos de modificación a SuperBoss

## Requisitos

Asegúrate de tener las siguientes dependencias instaladas en tu entorno:

asgiref==3.6.0
beautifulsoup4==4.12.2
charset-normalizer==3.0.1
darkdetect==0.5.1
defusedxml==0.7.1
diff-match-patch==20200713
Django==4.1.7
django-cors-headers==3.13.0
django-db-multitenant==0.3.2
django-environ==0.9.0
django-extensions==3.2.1
django-import-export==3.0.2
django-nested-admin==4.0.2
django-toggle-switch-widget==0.1.1
djangorestframework==3.13.1
et-xmlfile==1.1.0
exceptiongroup==1.0.0rc5
flake8==6.0.0
gaphas==3.6.0
gaphor==2.9.2
generic==1.1.0
gunicorn==21.2.0
html2text==2020.1.16
idna==3.4
jedi==0.18.1
MarkupPy==1.14
mccabe==0.7.0
mysqlclient==2.1.1
numpy==1.23.4
odfpy==1.4.1
openpyxl==3.0.10
ordered-set==4.1.0
pandas==1.4.2
parso==0.8.3
Pillow==9.2.0
psycopg2-binary==2.9.4
pycairo==1.21.0
pycodestyle==2.10.0
pyflakes==3.0.1
PyGObject==3.42.2
pygraphviz==1.10
python-dateutil==2.8.2
python-monkey-business==1.0.0
pytz==2022.6
PyYAML==6.0
requests==2.28.2
six==1.16.0
soupsieve==2.4.1
sqlparse==0.4.2
style==1.1.0
tablib==3.3.0
tinycss2==1.1.1
update==0.0.1
urllib3==1.26.14
webencodings==0.5.1
whitenoise==6.2.0
xlrd==2.0.1
xlwt==1.3.0


## Configuración del entorno

Para configurar el entorno de desarrollo, sigue estos pasos:

1️⃣ Clona el repositorio: `https://github.com/LuigiNorp/Racek_Hilda_Application.git`
2️⃣ Navega al directorio del proyecto: `cd repo`
3️⃣ Instala las dependencias: `pip install -r requirements.txt`

## Despliegue con Docker Compose

La aplicación se desplegó en un Synology NAS utilizando Docker Compose y se sirve utilizando Nginx y Gunicorn.

```yaml
version: "3.9"
services:
    web:
        image: nginx:stable
        restart: always
        ports:
            - 8080:80
            - 4343:443
        environment:
            - DJANGO_HOST=app
        volumes:
            - ./default.conf.template:/etc/nginx/templates/default.conf.template
            - ./conf/:/etc/nginx/conf.d/:ro
        networks:
            - backend
    app:
        build:
            context: .
            dockerfile: Dockerfile
        restart: always
        ports:
            - 20001:20001
        command: python manage.py runserver 0.0.0.0:20001
        environment:
            NAME: ${NAME}
            USER: ${USER}
            PASSWORD: ${PASSWORD}
            HOST: ${HOST}
            PORT: ${PORT}
        volumes:
            - .:/app
            - ./conf/:/etc/nginx/conf.d/:ro
        networks:
            - backend

networks:
    backend:   
```
Para desplegar la aplicación, sigue estos pasos:

1️⃣ Construye la imagen Docker: docker-compose build 2️⃣ Inicia los servicios: docker-compose up

Visita localhost:20001 en tu navegador para ver la aplicación en funcionamiento.

## Migrations

### Make migrations
``` python
python manage.py makemigrations
```

### Migrate app database

```python
python manage.py migrate
```

### Migrate data database

```python
python manage.py migrate data --database=hilda_data
```

## Create SuperUser

```python
python manage.py createsuperuser
```

# Licencia
Este proyecto está licenciado bajo los términos de la licencia MIT.
