*Leer en otros idiomas: [English](README.md), [Español](README.es.md)*

# Sistema de Gestión de Biblioteca

Una aplicación Django REST Framework para gestionar libros y autores con una relación muchos-a-muchos.

## Características

- **Modelos de Datos**: Modelos de Libro y Autor con relación muchos-a-muchos
- **Django Admin**: Interfaz de administración completa para gestionar libros y autores
- **API REST**: Operaciones CRUD completas para ambas entidades
- **Consultas Avanzadas**: Incluye agregaciones, anotaciones y filtrado complejo
- **Pruebas**: Pruebas unitarias e de integración exhaustivas
- **Docker**: Completamente containerizado con base de datos PostgreSQL
- **Datos Iniciales**: Datos de muestra precargados para pruebas

## Stack Tecnológico

- **Backend**: Django 4.2.9
- **API**: Django REST Framework 3.14.0
- **Base de Datos**: PostgreSQL 15
- **Containerización**: Docker & Docker Compose
- **Python**: 3.11

## Estructura del Proyecto

```
drf-library-tech-challenge/
├── core/                      # Configuración del proyecto Django
│   ├── settings.py           # Archivo de configuración principal
│   ├── urls.py               # Configuración de URLs raíz
│   └── wsgi.py               # Configuración WSGI
├── library/                   # Aplicación principal
│   ├── models.py             # Modelos Author y Book
│   ├── serializers.py        # Serializadores DRF
│   ├── views.py              # Viewsets de API con consultas avanzadas
│   ├── admin.py              # Configuración de Django admin
│   ├── tests.py              # Pruebas unitarias e de integración
│   └── management/
│       └── commands/
│           └── load_initial_data.py  # Cargador de datos iniciales
├── Dockerfile                 # Configuración de imagen Docker
├── docker-compose.yml         # Servicios de Docker Compose
├── deploy.sh                  # Script de despliegue
├── requirements.txt           # Dependencias de Python
└── README.md                  # Este archivo
```

## Inicio Rápido

### Prerequisitos

- Docker
- Docker Compose

### Instalación y Despliegue

1. **Clonar el repositorio**
   ```bash
   git clone <repository-url>
   cd drf-library-tech-challenge
   ```

2. **Ejecutar el script de despliegue**
   ```bash
   ./deploy.sh
   ```

3. **Seguir las instrucciones interactivas**
   - Elegir opción 1 para despliegue nuevo
   - Crear un superusuario cuando se solicite
   - Opcionalmente ejecutar las pruebas

El script de despliegue hará:
- Construir imágenes Docker
- Iniciar contenedores PostgreSQL y Django
- Ejecutar migraciones de base de datos
- Cargar datos de muestra iniciales
- Opcionalmente crear un superusuario y ejecutar pruebas

### Despliegue Manual

Si prefieres el despliegue manual:

```bash
# Construir e iniciar contenedores
docker-compose up -d --build

# Esperar a que la base de datos esté lista
sleep 10

# Ejecutar migraciones
docker exec library_web python manage.py migrate

# Cargar datos iniciales
docker exec library_web python manage.py load_initial_data

# Crear superusuario (opcional)
docker exec -it library_web python manage.py createsuperuser

# Ejecutar pruebas (opcional)
docker exec library_web python manage.py test
```

## Endpoints de la API

### URL Base
```
http://localhost:8000/api/
```

### Autores

| Método | Endpoint | Descripción |
|--------|----------|-------------|
| GET | `/api/authors/` | Listar todos los autores |
| POST | `/api/authors/` | Crear nuevo autor |
| GET | `/api/authors/{id}/` | Obtener detalles de autor |
| PUT | `/api/authors/{id}/` | Actualizar autor |
| PATCH | `/api/authors/{id}/` | Actualización parcial de autor |
| DELETE | `/api/authors/{id}/` | Eliminar autor |
| GET | `/api/authors/{id}/books/` | Obtener todos los libros de un autor |
| GET | `/api/authors/statistics/` | **Consulta avanzada**: Estadísticas de autores |

### Libros

| Método | Endpoint | Descripción |
|--------|----------|-------------|
| GET | `/api/books/` | Listar todos los libros |
| POST | `/api/books/` | Crear nuevo libro |
| GET | `/api/books/{id}/` | Obtener detalles de libro |
| PUT | `/api/books/{id}/` | Actualizar libro |
| PATCH | `/api/books/{id}/` | Actualización parcial de libro |
| DELETE | `/api/books/{id}/` | Eliminar libro |
| GET | `/api/books/statistics/` | **Consulta avanzada**: Estadísticas de libros con agregaciones |
| GET | `/api/books/top_rated/` | **Consulta avanzada**: Libros mejor valorados (rating >= 4.0) |
| GET | `/api/books/recent_releases/` | **Consulta avanzada**: Lanzamientos recientes con filtrado complejo |
| GET | `/api/books/by_author/` | **Consulta avanzada**: Libros agrupados por cantidad de autores |

### Ejemplos de Consultas Avanzadas

La aplicación incluye varias consultas avanzadas de base de datos utilizando `annotate`, `aggregate` y objetos `Q` complejos del ORM de Django:

#### 1. Estadísticas de Libros (Agregación)
```bash
GET /api/books/statistics/
```
Devuelve:
- Cantidad total de libros
- Precios promedio, máximo y mínimo
- Valoración promedio
- Cantidad total de stock
- Cantidad promedio de páginas
- Estadísticas agrupadas por género
- Cantidad de libros con múltiples autores

**Características ORM**: `aggregate()`, `annotate()`, `Count()`, `Avg()`, `Sum()`, `Max()`, `Min()`

#### 2. Estadísticas de Autores (Agregación con Filtros)
```bash
GET /api/authors/statistics/
```
Devuelve:
- Total de autores
- Autores con libros
- Promedio de libros por autor
- Autores más prolíficos

**Características ORM**: `aggregate()`, `annotate()`, `Count()`, `Avg()`, objetos `Q()` con filtros

#### 3. Libros Mejor Valorados (Anotación + Filtrado)
```bash
GET /api/books/top_rated/
```
Devuelve libros con valoración >= 4.0, anotados con cantidad de autores.

**Características ORM**: `annotate()`, `Count()`, `filter()`, `order_by()`

#### 4. Lanzamientos Recientes (Objetos Q Complejos)
```bash
GET /api/books/recent_releases/
```
Devuelve libros del último año que están en stock O tienen alta valoración.

**Características ORM**: Objetos `Q()`, filtrado complejo con operadores `&` y `|`

### Parámetros de Consulta

#### Autores
- `search`: Buscar por nombre, nacionalidad o email
- `nationality`: Filtrar por nacionalidad
- `ordering`: Ordenar por campos (ej., `last_name`, `-created_at`)

Ejemplo:
```bash
GET /api/authors/?search=George&nationality=British&ordering=last_name
```

#### Libros
- `search`: Buscar por título, ISBN, editorial o nombre de autor
- `genre`: Filtrar por género (FICTION, MYSTERY, etc.)
- `in_stock`: Filtrar por disponibilidad en stock (true/false)
- `min_price`: Filtro de precio mínimo
- `max_price`: Filtro de precio máximo
- `min_rating`: Filtro de valoración mínima
- `ordering`: Ordenar por campos (ej., `title`, `-publication_date`)

Ejemplo:
```bash
GET /api/books/?genre=FICTION&in_stock=true&min_rating=4.0&ordering=-rating
```

## Django Admin

Acceder al panel de administración en: `http://localhost:8000/admin/`

Características:
- Crear, editar y eliminar libros y autores
- Filtrado y búsqueda avanzados
- Edición en línea de relaciones muchos-a-muchos
- Visualizaciones de lista personalizadas con campos calculados

## Modelos de Datos

### Modelo Author
```python
- first_name: CharField
- last_name: CharField
- birth_date: DateField (opcional)
- nationality: CharField
- biography: TextField
- email: EmailField (único)
- created_at: DateTimeField (automático)
- updated_at: DateTimeField (automático)
```

### Modelo Book
```python
- title: CharField
- isbn: CharField (único, validado)
- authors: ManyToManyField(Author)
- genre: CharField (opciones)
- publication_date: DateField
- publisher: CharField
- page_count: PositiveIntegerField
- language: CharField
- description: TextField
- price: DecimalField
- stock_quantity: PositiveIntegerField
- rating: DecimalField (0-5)
- created_at: DateTimeField (automático)
- updated_at: DateTimeField (automático)
```

## Pruebas

Ejecutar la suite de pruebas:

```bash
# Ejecutar todas las pruebas
docker exec library_web python manage.py test

# Ejecutar clase de prueba específica
docker exec library_web python manage.py test library.tests.BookAPITest

# Ejecutar con salida detallada
docker exec library_web python manage.py test --verbosity=2
```

La cobertura de pruebas incluye:
- Validación de modelos y métodos
- Operaciones CRUD de la API
- Filtrado por parámetros de consulta
- Endpoints de consultas avanzadas
- Validación de serializadores
- Casos extremos y manejo de errores

## Datos de Muestra

La aplicación viene con datos de muestra precargados incluyendo:

**Autores** (8 total):
- George Orwell
- Jane Austen
- F. Scott Fitzgerald
- Harper Lee
- J.K. Rowling
- Stephen King
- Agatha Christie
- Isaac Asimov

**Libros** (10 total):
- Ficción clásica, misterio, romance, ciencia ficción y fantasía
- Varias valoraciones, precios y niveles de stock
- Demostrando relaciones muchos-a-muchos

Recargar datos de muestra:
```bash
docker exec library_web python manage.py load_initial_data
```

## Ejemplos de Uso de la API

### Crear un Autor
```bash
curl -X POST http://localhost:8000/api/authors/ \
  -H "Content-Type: application/json" \
  -d '{
    "first_name": "Ernest",
    "last_name": "Hemingway",
    "birth_date": "1899-07-21",
    "nationality": "American",
    "email": "ernest@example.com"
  }'
```

### Crear un Libro
```bash
curl -X POST http://localhost:8000/api/books/ \
  -H "Content-Type: application/json" \
  -d '{
    "title": "The Old Man and the Sea",
    "isbn": "0684801221",
    "author_ids": [1],
    "genre": "FICTION",
    "publication_date": "1952-09-01",
    "publisher": "Charles Scribner",
    "page_count": 127,
    "price": "14.99",
    "stock_quantity": 20,
    "rating": "4.5"
  }'
```

### Obtener Estadísticas de Libros
```bash
curl http://localhost:8000/api/books/statistics/
```

### Buscar Libros
```bash
curl "http://localhost:8000/api/books/?search=Harry&in_stock=true"
```

## Comandos de Docker

```bash
# Iniciar servicios
docker-compose up -d

# Detener servicios
docker-compose down

# Ver logs
docker-compose logs -f

# Reiniciar servicios
docker-compose restart

# Acceder al shell de Django
docker exec -it library_web python manage.py shell

# Acceder a la base de datos
docker exec -it library_db psql -U library_user -d library_db

# Ejecutar migraciones
docker exec library_web python manage.py migrate

# Crear nueva migración
docker exec library_web python manage.py makemigrations
```

## Variables de Entorno

Crear un archivo `.env` basado en `.env.example`:

```bash
SECRET_KEY=your-secret-key-here
DEBUG=True
DATABASE_NAME=library_db
DATABASE_USER=library_user
DATABASE_PASSWORD=library_password
DATABASE_HOST=db
DATABASE_PORT=5432
```

## Desarrollo

### Agregar Nuevas Dependencias

1. Agregar el paquete a `requirements.txt`
2. Reconstruir la imagen Docker:
   ```bash
   docker-compose up -d --build
   ```

### Realizar Cambios en los Modelos

1. Actualizar modelos en `library/models.py`
2. Crear migraciones:
   ```bash
   docker exec library_web python manage.py makemigrations
   ```
3. Aplicar migraciones:
   ```bash
   docker exec library_web python manage.py migrate
   ```

## Resolución de Problemas

### Problemas de Conexión a la Base de Datos
```bash
# Verificar si la base de datos está ejecutándose
docker-compose ps

# Ver logs de la base de datos
docker-compose logs db

# Reiniciar base de datos
docker-compose restart db
```

### Permiso Denegado en deploy.sh
```bash
chmod +x deploy.sh
```

### Puerto Ya en Uso
Si el puerto 8000 o 5432 ya está en uso, modificar `docker-compose.yml`:
```yaml
ports:
  - "8001:8000"  # Cambiar 8000 a otro puerto
```

## Documentación de la API

Para documentación interactiva de la API, puedes integrar la API navegable de Django REST Framework:

Visitar: `http://localhost:8000/api/`

La API navegable proporciona:
- Formularios interactivos para probar endpoints
- Documentación automática de endpoints disponibles
- Ejemplos de solicitudes/respuestas

## Licencia

Este proyecto fue creado como demostración de un desafío técnico.

## Contacto

Para preguntas o problemas, consultar el issue tracker del repositorio.
