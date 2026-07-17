# Librarium API

Librarium API es el backend para una plataforma de gestion y tracking de lecturas personales, disenada con una logica similar a Letterboxd o Goodreads. Este sistema permite a los usuarios catalogar sus libros, organizar estantes personalizados mediante relaciones Muchos a Muchos y calificar sus lecturas con resenas detalladas.

El proyecto esta construido bajo una arquitectura robusta, escalable y completamente contenedorizada, lista para entornos de produccion.

---

## Tecnologias Utilizadas

* **Framework Principal:** Django 5.x y Django REST Framework (DRF)
* **Base de Datos:** PostgreSQL
* **Autenticacion:** JWT (JSON Web Tokens) via djangorestframework-simplejwt
* **Entorno de Desarrollo y Produccion:** Docker y Docker Compose
* **Servidor de Produccion:** Gunicorn
* **Despliegue Orientado a:** Render (Configuracion por codigo mediante render.yaml)

---

## Caracteristicas Principales y Arquitectura

1. **Autenticacion Segura (JWT):** Flujo completo de registro y login con emision de tokens de acceso y refresco.
2. **Aislamiento de Datos por Usuario:** Los usuarios solo pueden visualizar, editar o borrar sus propios libros y estantes personales (get_queryset dinamico).
3. **Relaciones Complejas (Many-to-Many):** Implementacion de estantes virtuales donde un estante puede contener multiples libros y un libro pertenecer a varios estantes.
4. **Sistema de Resenas Colectivo:** Sistema de feedback con puntuaciones validadas del 1 al 5 y comentarios abiertos, visibles para toda la comunidad.
5. **Seguridad Avanzada:** Permisos personalizados (IsOwnerOrReadOnly) que bloquean acciones de escritura a usuarios que no sean los legitimos duenos del recurso.

---

## Mapa de Endpoints de la API

### Autenticacion (/api/auth/)
| Metodo | Endpoint | Descripcion | Requiere Token |
| :--- | :--- | :--- | :---: |
| POST | /api/auth/register/ | Registrar un nuevo usuario | No |
| POST | /api/auth/login/ | Login de usuario (Devuelve Access y Refresh Token) | No |
| POST | /api/auth/token/refresh/ | Renovar el Access Token usando el Refresh Token | No |

### Libros (/api/books/)
| Metodo | Endpoint | Descripcion | Requiere Token |
| :--- | :--- | :--- | :---: |
| GET | /api/books/ | Listar solo los libros del usuario logueado | Si |
| POST | /api/books/ | Registrar un nuevo libro | Si |
| PUT/PATCH | /api/books/{id}/ | Modificar un libro (Solo el dueno) | Si |
| DELETE | /api/books/{id}/ | Eliminar un libro (Solo el dueno) | Si |

### Estantes (/api/shelves/)
| Metodo | Endpoint | Descripcion | Requiere Token |
| :--- | :--- | :--- | :---: |
| GET | /api/shelves/ | Listar estantes del usuario logueado | Si |
| POST | /api/shelves/ | Crear un estante vacio | Si |
| POST | /api/shelves/{id}/books/ | Agregar un libro especifico a un estante | Si |
| DELETE | /api/shelves/{id}/ | Eliminar un estante (Solo el dueno) | Si |

### Resenas (/api/reviews/)
| Metodo | Endpoint | Descripcion | Requiere Token |
| :--- | :--- | :--- | :---: |
| GET | /api/reviews/ | Listar todas las resenas de la plataforma | Si |
| POST | /api/reviews/ | Crear una resena de 1 a 5 estrellas para un libro | Si |
| DELETE | /api/reviews/{id}/ | Eliminar una resena (Solo el dueno) | Si |

---

## Instalacion y Ejecucion Local (Desarrollo)

El proyecto esta completamente automatizado con Docker. No es necesario instalar Python ni PostgreSQL en el sistema local.

### Paso 1: Clonar el repositorio

    git clone https://github.com/EmiDelgadoV/Librarium.git
    cd Librarium

### Paso 2: Configurar las variables de entorno
Crear un archivo llamado .env en la raiz del proyecto con la siguiente estructura base:

    DEBUG=True
    SECRET_KEY=django-insecure-desarrollo-local-12345
    DB_NAME=librarium_db
    DB_USER=librarium_user
    DB_PASSWORD=librarium_pass
    DB_HOST=db
    DB_PORT=5432

### Paso 3: Levantar los contenedores

    docker compose up --build

### Paso 4: Ejecutar las migraciones iniciales
En una terminal secundaria ejecutar el siguiente comando para impactar las tablas:

    docker compose run --rm web python manage.py migrate

El servidor estara disponible en el entorno local en http://localhost:8000/.

---

## Configuracion de Produccion

El proyecto incluye un Dockerfile.prod optimizado de multiples etapas y un plano de infraestructura como codigo render.yaml. Esto permite que plataformas como Render detecten automaticamente la arquitectura, levanten la base de datos PostgreSQL gestionada y sirvan la aplicacion utilizando Gunicorn como servidor HTTP WSGI de nivel de produccion.


## Deploy

API disponible en producción: https://librarium-qacs.onrender.com

Documentación navegable: https://librarium-qacs.onrender.com/api/
---
## Autor

Victor Emiliano Delgado
[github.com/EmiDelgadoV](https://github.com/EmiDelgadoV) · [linkedin.com/in/emiliano-delgado-212b042b5](https://linkedin.com/in/emiliano-delgado-212b042b5)