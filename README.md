### Microservice for the International Delivery Service

[![Lang: RU](https://img.shields.io/badge/lang-RU-blue)](README_RU.md)
[![Python](https://img.shields.io/badge/python-3.12%2B-blue)](#installation-guide)
[![License](https://img.shields.io/badge/license-MIT-green)](LICENSE)
[![Tests](https://img.shields.io/badge/tests-pytest-blue)](#testing)
[![Architecture](https://img.shields.io/badge/architecture-DDD%20&%20Clean%20architecture-orange)](#architecture)

#### Task description:

- [EN](/TASK_EN.md)
- [RU](/TASK_RU.md)

---

### Contents:

* [Description](#description)
* [Installation Guide](#installation-guide)
* [Testing](#testing)
* [Architecture](#architecture)
* [License](#license)

---

### Description

A microservice for registering and calculating the delivery cost of international parcels.
Built according to the principles of **Domain-Driven Design (DDD)** and **Clean Architecture** using the following technologies:

* FastAPI and Pydantic — for building REST API and data validation
* RabbitMQ — for asynchronous parcel registration with cost calculation
* Redis — for caching the USD to RUB exchange rate
* MySQL — main database
* Swagger (OpenAPI) — for automatic API documentation
* Docker and docker-compose — for deployment and dependency management

##### REST API:

* `POST /parcels`
  Register a new parcel.
  Input: JSON with name, weight, type, and content value in USD.
  The parcel is sent to the RabbitMQ queue, where a worker calculates the delivery cost and saves the data to the database.

* `GET /parcels/types`
  Get the list of available parcel types: clothing, electronics, other.
  The data is retrieved from a separate database table.

* `GET /parcels`
  Get a list of all parcels for the current user (tracked via cookie).
  Supports:

  * Pagination: `limit`, `offset`
  * Filter by type: `type_id`
  * Filter by delivery cost status: `has_price=true|false`

* `GET /parcels/{id}`
  Get information about a specific parcel.
  Includes name, weight, type, content value, and calculated delivery cost.

---

### Installation Guide

Clone the repository:

```bash
git clone https://github.com/artemy-sh/delivery-service.git
cd delivery-service
```

Create an environment file based on the example:

```bash
cp .env.example .env
```

#### 1. Run via `docker-compose`

```bash
docker-compose up --build
```

After building and starting the services, the FastAPI app will be available at:

```
http://localhost:8000
```

Swagger documentation:

```
http://localhost:8000/docs
```

Migrations are automatically applied at startup, and necessary data is initialized (including parcel types).

To stop and clean up containers:

```bash
docker-compose down -v
```

#### 2. Run via `make`

You can use the following `make` commands:

```bash
make up         # Start the project with build (docker-compose up --build)
make down       # Stop all services (docker-compose down)
make run        # Run in background (docker-compose up -d)
make rebuild    # Rebuild and restart the project
make scale      # Start multiple workers: WORKERS=3 make scale
make migrate    # Apply migrations manually via Alembic
make nuke       # Full cleanup and removal of volumes and orphans

make install    # Install dependencies via Poetry
make mypy       # Run mypy type checks
make ruff       # Run ruff linter
```

#### 3. Run locally without Docker

System dependencies:

* Python 3.12+
* MySQL
* Redis
* RabbitMQ

#### Install dependencies

```bash
poetry install
```

Create a `.env` file and configure environment variables for your system (hosts and ports of MySQL, Redis, RabbitMQ).

---

#### Apply migrations

Before running the project, create tables in the database:

```bash
alembic upgrade head
```

Or via Makefile:

```bash
make migrations
```

---

#### Run the application

To run the app locally, set the environment variable `PYTHONPATH=src`.

---

#### Start FastAPI application

```bash
PYTHONPATH=src python3 src/main.py
```

The application will be available at:
`http://localhost:8000`
Swagger docs:
`http://localhost:8000/docs`

#### Start RabbitMQ worker

```bash
PYTHONPATH=src python3 src/worker.py
```

---

### Testing

The project includes unit tests using `pytest`.

#### Run tests

```bash
pytest
```

You can also use `make`:

```bash
make test
```

---

### Architecture

The project is built using **Domain-Driven Design (DDD)** and **Clean Architecture**.
All dependencies flow inward — from outer layers toward the business logic.

#### Project structure

```
src/
├── delivery_service/
│   ├── domain/     
│   ├── application/    
│   ├── infrastructure/  
│   ├── presentation/   
│   └── entrypoints/     
│── main.py           
└── worker.py         
```

#### Layer descriptions

* **domain**
  The core of the domain: entities (`Parcel`, `ParcelType`), value objects, and interfaces. Also contains base delivery cost logic.

* **application**
  Use-cases implementing business logic, using abstract repositories and external services.

* **infrastructure**
  Concrete implementations of external interfaces: message brokers, SQLAlchemy database access, exchange rate APIs, loggers, and Redis caching.

* **presentation**
  The app interface: FastAPI routes, validation schemas, DTO-to-entity mappers, error handling.

* **entrypoints**
  Application entry points: FastAPI app launcher, RabbitMQ consumer, CLI.

---

#### Features

* The architecture allows:

  * Replacing FastAPI with any other framework without affecting business logic
  * Using a different message broker instead of RabbitMQ
  * Connecting alternative exchange rate providers
  * Extending and modifying behavior without changing core logic

* All dependencies are inverted:

  * Use-cases rely on abstractions (interfaces), not concrete implementations
  * Infrastructure is plugged in only at the outermost level

---

### Contacts

* **Author**: Artemiy Shalygin
* **Email**: [artemy.sh@gmail.com](mailto:artemy.sh@gmail.com)
* **Telegram**: [@artemy\_sh](https://t.me/artemy_sh)

---

#### Bug reporting

If you find a bug or want to suggest improvements — please create an issue in the repository.

---

#### License

[MIT License](/LICENSE)
