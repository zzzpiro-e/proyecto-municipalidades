# proyecto-municipalidades
Proyecto desarrollo web equipo 4 - Proyecto web que permite ordenar la información de incidencias dentro de las municipalidades.

## Instalación y Configuración

### Prerrequisitos
- Python
- VSCode
- PostgreSQL
- Git

### Dependencias
- Django 5.2.4
- Psycopg2-binary 2.9.10

### 1. Crear entorno e instalar dependencias

### 2. Crear base de datos
Crear base de datos llamada proyecto_municipalidad

### 3. Clonar repositorio
```bash
git clone https://github.com/zzzpiro-e/proyecto-municipalidades.git

cd proyecto-municipalidades
```

### 4. Crear y Configurar Archivo de Settings Local
En la carpeta proyecto_municipalidades crear settings.py y pegar:
```bash
"""
CONFIGURACIÓN LOCAL - NO SE SUBE A GITHUB
"""

from .settings_base import *

DATABASES = {
    "default": {
        'HOST': "localhost",
        "ENGINE": "django.db.backends.postgresql",
        "NAME": "proyecto_municipalidad",
        "USER": "postgres",
        "PASSWORD": "12345678",
        "PORT": "5432",
    }
}
```

### 5. Migraciones y Ejecución
```bash
# Aplicar migraciones
python manage.py makemigrations
python manage.py migrate

# Ejecutar servidor de desarrollo
python manage.py runserver
```

## Flujo de Trabajo Git

### 1. Actualizar tu develop local
```bash
git checkout develop

git pull origin develop
```

### 2. Crear una rama nueva para tu feature
```bash
git checkout -b feature/nombre-de-la-feature
```

### 3. Trabajar y hacer commits
```bash
git add .

git commit -m "Descripción clara del cambio"
```

### 4. Subir la rama y crear pull request
```bash
git push -u origin feature/nombre-de-la-feature
```


