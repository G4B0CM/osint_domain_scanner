# Microservicio de Escaneo OSINT para Dominios Web

Este proyecto es un microservicio diseñado para recopilar información de fuentes abiertas (OSINT) sobre un dominio web específico. Actúa como una API que recibe un nombre de dominio y devuelve un conjunto de datos públicos, como información de WHOIS y una lista de subdominios conocidos.

El proyecto está construido siguiendo los principios de **Clean Architecture** y **Domain-Driven Design (DDD)**, separando claramente las responsabilidades en capas de Dominio, Aplicación, Infraestructura y Presentación.

## ✨ Características Principales

- **API RESTful:** Expone un endpoint para iniciar escaneos de manera programática.
- **Recopilación de WHOIS:** Obtiene registros de WHOIS para el dominio solicitado.
- **Búsqueda de Subdominios:** Identifica subdominios asociados (implementación de ejemplo).
- **Persistencia en Base de Datos:** Almacena los resultados de cada escaneo en una base de datos SQL Server.
- **Arquitectura Limpia:** Diseño desacoplado que facilita el mantenimiento y la extensibilidad.
- **Contenerizado con Docker:** Listo para ser ejecutado en cualquier entorno con Docker y Docker Compose.

## 🏗️ Arquitectura

El proyecto está estructurado en las siguientes capas:

-   `domain/`: Contiene las entidades y la lógica de negocio central, independiente de cualquier tecnología.
-   `application/`: Orquesta los casos de uso y define las interfaces (contratos) que la infraestructura debe implementar.
-   `infrastructure/`: Contiene las implementaciones concretas de las interfaces, como proveedores de datos externos (WHOIS) y el repositorio de la base de datos (SQLAlchemy para SQL Server).
-   `presentation/`: La capa más externa, que expone la funcionalidad a través de una API RESTful (FastAPI).

## 🚀 Cómo Empezar

Sigue estos pasos para levantar el entorno de desarrollo localmente.

### Prerrequisitos

-   [Docker](https://www.docker.com/get-started)
-   [Docker Compose](https://docs.docker.com/compose/install/)
-   Una instancia de SQL Server accesible desde el entorno donde se ejecute Docker.
-   Tener instalado el [Controlador ODBC 17 para SQL Server](https://docs.microsoft.com/en-us/sql/connect/odbc/download-odbc-driver-for-sql-server) en la máquina host si se ejecuta sin Docker.

### Configuración

1.  **Clona el repositorio:**
    ```bash
    git clone <URL_DEL_REPOSITORIO>
    cd osint_domain_scanner
    ```

2.  **Configura las variables de entorno:**
    Crea un archivo llamado `.env` en la raíz del proyecto, copiando el ejemplo de `.env.example` (que deberías crear).
    ```bash
    cp .env.example .env
    ```
    Edita el archivo `.env` y añade tus credenciales de la base de datos SQL Server:
    ```
    # .env
    DB_CONNECTION_STRING="mssql+pyodbc://TU_USUARIO:TU_CONTRASEÑA@IP_O_HOST_DEL_SERVIDOR/NOMBRE_DB?driver=ODBC+Driver+17+for+SQL+Server"
    ```

### Ejecución con Docker Compose (Recomendado)

Este es el método más sencillo para ejecutar la aplicación.

1.  **Construir y levantar el servicio:**
    ```bash
    docker-compose up --build
    ```
    El flag `--build` fuerza la reconstrucción de la imagen si has hecho cambios en el `Dockerfile` o en los `requirements.txt`. Para ejecuciones posteriores, `docker-compose up` es suficiente.

2.  **La aplicación estará disponible en:**
    -   **API:** `http://localhost:8000`
    -   **Documentación Interactiva (Swagger UI):** `http://localhost:8000/docs`

### Ejecución Local (Sin Docker)

1.  **Crea un entorno virtual e instala las dependencias:**
    ```bash
    python -m venv venv
    source venv/bin/activate  # En Windows: venv\Scripts\activate
    pip install -r requirements.txt
    ```

2.  **Ejecuta la aplicación:**
    Asegúrate de que tu archivo `config.json` esté configurado correctamente si no usas variables de entorno.
    ```bash
    uvicorn main:app --reload
    ```

## 🔌 Uso de la API

### Escanear un Dominio

Realiza una petición `POST` al endpoint `/api/v1/scan`.

-   **URL:** `http://localhost:8000/api/v1/scan`
-   **Método:** `POST`
-   **Cuerpo (Body) - JSON:**
    ```json
    {
      "domain_name": "github.com"
    }
    ```

-   **Respuesta Exitosa (200 OK):**
    ```json
    {
      "domain_name": "github.com",
      "whois_data": {
        "domain_name": "GITHUB.COM",
        "registrar": "MarkMonitor, Inc.",
        "creation_date": "2007-10-09T18:20:50",
        "...": "..."
      },
      "subdomains": [
        "www.github.com",
        "api.github.com",
        "dev.github.com"
      ],
      "id": 1,
      "scanned_at": "2023-10-27T10:30:00.123456"
    }
    ```

## 🛠️ Próximos Pasos

-   [ ] Implementar un proveedor real para la búsqueda de subdominios (ej. usando APIs de VirusTotal, SecurityTrails, etc.).
-   [ ] Añadir más recolectores de información (certificados SSL, tecnologías web, etc.).
-   [ ] Implementar un sistema de caché (ej. Redis) para evitar escaneos repetitivos.
-   [ ] Mejorar el manejo de errores y el logging.