# OSINT Web Domain Scanner Microservice
This project is a microservice designed to gather Open Source Intelligence (OSINT) on a specific web domain. It acts as a RESTful API that accepts a domain name and returns a public data set, including WHOIS information and a list of known subdomains.
The project is built following the principles of Clean Architecture and Domain-Driven Design (DDD), ensuring a clear separation of concerns across Domain, Application, Infrastructure, and Presentation layers.
# ✨ Key Features
RESTful API: Exposes an endpoint to programmatically initiate domain scans.
WHOIS Data Collection: Retrieves WHOIS records for the requested domain.
Subdomain Enumeration: Identifies associated subdomains (mock implementation).
Database Persistence: Stores the results of each scan in a SQL Server database.
Clean Architecture: A decoupled design that promotes maintainability and extensibility.
Dockerized Environment: Ready to run in any environment that supports Docker and Docker Compose.
# 🏗️ Architecture
The project is structured into the following layers, ensuring dependencies point inwards toward the domain:
domain/: Contains the core business logic and entities, completely independent of any technology or framework.
application/: Orchestrates the use cases (application logic) and defines the interfaces (contracts) that the infrastructure layer must implement.
infrastructure/: Holds the concrete implementations of the interfaces, such as external data providers (WHOIS) and the database repository (SQLAlchemy for SQL Server).
presentation/: The outermost layer, which exposes the functionality through a RESTful API built with FastAPI.
# 🚀 Getting Started
Follow these steps to set up and run the development environment locally.
Prerequisites
Docker
Docker Compose
A SQL Server instance accessible from the machine running Docker.
Configuration
Clone the repository:
git clone <YOUR_REPOSITORY_URL>
cd osint_domain_scanner

Set up environment variables:
Create a file named .env in the project root. You can copy the example file if you create one (.env.example).
# Create and edit the .env file

Add your SQL Server connection details to the .env file. Use host.docker.internal as the server address to allow the Docker container to connect to a service running on your host machine.
.env
# For SQL Server Authentication
DB_CONNECTION_STRING="mssql+pyodbc://YOUR_SQL_USER:YOUR_SECURE_PASSWORD@host.docker.internal/ScannerDB?driver=ODBC+Driver+17+for+SQL+Server&TrustServerCertificate=yes"

# For Windows Authentication (Note: This is complex from a Linux container and not recommended)
DB_CONNECTION_STRING="mssql+pyodbc://host.docker.internal/ScannerDB?driver=ODBC+Driver+17+for+SQL+Server&Trusted_Connection=yes&TrustServerCertificate=yes"

# Important: Ensure your SQL Server is configured to:
Allow remote connections (TCP/IP protocol enabled).
Accept connections on its port (default is 1433), and a firewall rule is in place on the host machine to allow incoming traffic on this port.
Use "SQL Server and Windows Authentication mode" if you are using a SQL login.
Running with Docker Compose (Recommended)
This is the simplest method to run the application.
Build and start the service:
From the project root directory, run:
docker-compose up --build

The --build flag forces a rebuild of the Docker image, which is useful after changing dependencies (requirements.txt) or the Dockerfile. For subsequent runs, docker-compose up is sufficient.
The application will be available at:
API Base URL: http://localhost:8000
Interactive API Docs (Swagger UI): http://localhost:8000/docs
Running Locally (Without Docker)
Create a virtual environment and install dependencies:
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt

Run the application:
Ensure your config.json is correctly configured if you are not using environment variables.
uvicorn main:app --reload


🔌 API Usage
Scan a Domain
Make a POST request to the /api/v1/scan endpoint.
URL: http://localhost:8000/api/v1/scan
Method: POST
Body (JSON):
{
  "domain_name": "github.com"
}

Success Response (200 OK):
The API will return a JSON object containing the collected information.
{
  "domain_name": "github.com",
  "whois_data": {
    "domain_name": "GITHUB.COM",
    "registrar": "MarkMonitor, Inc.",
    "creation_date": "2007-10-09T18:20:50",
    "expiration_date": "2024-10-09T18:20:50",
    "updated_date": "2023-09-08T10:04:47",
    "...": "..."
  },
  "subdomains": [
    "www.github.com",
    "api.github.com",
    "dev.github.com"
  ],
  "id": 1,
  "scanned_at": "2023-10-27T18:55:00.123456"
}