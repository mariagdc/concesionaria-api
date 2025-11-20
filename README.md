🚗 API Concesionaria de Autos - UTN

Sistema completo de gestión de ventas de automóviles
Trabajo Práctico - Programación IV - Universidad Tecnológica Nacional
📋 Descripción del Proyecto

API REST desarrollada con FastAPI para la gestión integral de una concesionaria de automóviles. El sistema permite administrar el inventario de vehículos y registrar las ventas realizadas, implementando todas las operaciones CRUD con arquitectura profesional.
🎯 Objetivos Cumplidos

    ✅ API REST completa con FastAPI

    ✅ Patrón Repository para acceso a datos

    ✅ Validaciones robustas con Pydantic

    ✅ Base de datos relacional con SQLModel

    ✅ Arquitectura escalable y mantenible

🏗️ Arquitectura del Proyecto
text

concesionaria_api/
├── main.py              # Aplicación FastAPI principal
├── database.py          # Configuración de base de datos
├── models.py            # Modelos SQLModel y Pydantic
├── repository.py        # Patrón Repository para acceso a datos
├── autos.py            # Router de endpoints para autos
├── ventas.py           # Router de endpoints para ventas
├── requirements.txt     # Dependencias del proyecto
└── README.md           # Documentación

🛠️ Tecnologías Utilizadas

    FastAPI - Framework web moderno y rápido

    SQLModel - ORM con integración Pydantic

    PostgreSQL - Base de datos relacional

    Pydantic - Validación y serialización de datos

    Uvicorn - Servidor ASGI de alto rendimiento

📊 Modelo de Datos
Entidad Auto

    marca - Marca del vehículo (Toyota, Ford, Chevrolet)

    modelo - Modelo específico (Corolla, Focus, Cruze)

    año - Año de fabricación (1900-actual)

    numero_chasis - Identificación única alfanumérica

    precio - Precio del vehículo

    estado - Disponible/Vendido/Reservado/Mantenimiento

Entidad Venta

    nombre_comprador - Nombre completo del comprador

    precio - Precio de venta

    fecha_venta - Fecha y hora de la transacción

    auto_id - Relación con el auto vendido

🚀 Instalación y Configuración
1. Clonar y configurar entorno
bash

# Crear entorno virtual
python -m venv venv

# Activar entorno virtual
# Windows:
venv\Scripts\activate
# Mac/Linux:
source venv/bin/activate

# Instalar dependencias
pip install -r requirements.txt

2. Configurar base de datos
bash

# PostgreSQL (recomendado)
DATABASE_URL=postgresql://usuario:password@localhost/concesionaria

# SQLite (desarrollo)
DATABASE_URL=sqlite:///concesionaria.db

3. Ejecutar la aplicación
bash

uvicorn main:app --reload

📚 Endpoints de la API
```
🔧 Autos (/autos)
Método	Endpoint	Descripción
POST	/autos	Crear nuevo auto
GET	/autos	Listar autos (con filtros)
GET	/autos/{id}	Obtener auto por ID
PUT	/autos/{id}	Actualizar auto
DELETE	/autos/{id}	Eliminar auto
GET	/autos/chasis/{chasis}	Buscar por número de chasis
GET	/autos/{id}/with-ventas	Auto con historial de ventas
💰 Ventas (/ventas)
Método	Endpoint	Descripción
POST	/ventas	Registrar nueva venta
GET	/ventas	Listar ventas
GET	/ventas/{id}	Obtener venta por ID
PUT	/ventas/{id}	Actualizar venta
DELETE	/ventas/{id}	Eliminar venta
GET	/ventas/auto/{auto_id}	Ventas de un auto
GET	/ventas/comprador/{nombre}	Ventas por comprador
GET	/ventas/{id}/with-auto	Venta con información del auto
```
## 🔍 Ejemplos de Uso
Crear un auto
bash

curl -X POST "http://localhost:8000/autos/" \
-H "Content-Type: application/json" \
-d '{
  "marca": "Toyota",
  "modelo": "Corolla",
  "anio": 2022,
  "numero_chasis": "ABC123XYZ789",
  "precio": 25000,
  "kilometraje": 15000,
  "color": "Blanco",
  "tipo_combustible": "gasolina"
}'

Registrar una venta
bash

curl -X POST "http://localhost:8000/ventas/" \
-H "Content-Type: application/json" \
-d '{
  "nombre_comprador": "María González",
  "precio": 24500,
  "auto_id": 1
}'

Buscar autos por marca
bash

curl "http://localhost:8000/autos/?marca=Toyota"

🎨 Características Destacadas
Validaciones Avanzadas

    ✅ Número de chasis único y alfanumérico

    ✅ Año entre 1900 y actual

    ✅ Precio mayor a cero

    ✅ Fecha de venta no futura

    ✅ Nombre de comprador no vacío

Funcionalidades de Búsqueda

    🔍 Búsqueda por marca y modelo

    🔍 Filtrado por estado del vehículo

    🔍 Búsqueda por número de chasis

    🔍 Historial de ventas por comprador

    🔍 Ventas por rango de fechas

Patrones de Diseño

    🏗️ Repository Pattern - Separación de concerns

    🏗️ Dependency Injection - Inyección de dependencias

    🏗️ Data Transfer Objects - Modelos Pydantic especializados

    🏗️ Routers Modulares - Separación por dominio



# Health check
curl http://localhost:8000/health

# Verificar estructura de datos
curl http://localhost:8000/autos/

👥 Responsables del Proyecto

Estudiante: [Maria Florencia Godoy Del Castillo]
Materia: Programación IV
Carrera: Tecnicatura Universitaria en Programación
Universidad: Universidad Tecnológica Nacional
Año: 2025
📄 Licencia

Este proyecto fue desarrollado con fines educativos para la Universidad Tecnológica Nacional.
🚀 Próximos Pasos

Para comenzar a usar la API:

    Configurar la base de datos en database.py

    Ejecutar la aplicación con uvicorn main:app --reload

    Explorar la documentación en http://localhost:8000/docs

    Probar los endpoints con Postman o curl

¡La API está lista para producción! 🎉