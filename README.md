<p align="center">
  <img src="unnamed.png" width="200" alt="MediaAmp Logo"/>
</p>

<h1 align="center">MediaAmp Backend Task Submission</h1>

<p align="center">
  A scalable, production-ready backend system built with Flask, PostgreSQL, Redis, Celery, and Docker.<br/>
  Designed for real-world applications with secure architecture, background task handling, and modular design.
</p>

---

## 🚀 Project Overview

This project is a **role-based backend system** that supports:

- **JWT Authentication & RBAC**
- **PostgreSQL** for persistent storage
- **Celery + Redis** for background tasks
- **Dockerized setup** for seamless deployment
- **Swagger API documentation**
- **Caching & task scheduling**

> It is designed to scale, secure, and perform — tailored for the MediaAmp selection round.

---

## 🧠 System Architecture

Client ↔️ API (Flask) ↕️ ↕️ PostgreSQL Redis (cache + queue) ↕️ ↕️ Celery (background jobs) ↕️ Dockerized Microservices


### 🔧 Core Components

| Component         | Description                                      |
|------------------|--------------------------------------------------|
| `app/`            | Main application logic                          |
| `models/`         | SQLAlchemy ORM models                           |
| `auth/`           | JWT-based authentication                        |
| `routes.py`       | All API route definitions                       |
| `tasks/`          | Celery workers for async jobs                   |
| `migrations/`     | Alembic database versioning                     |
| `docker-compose`  | Full orchestration of all services              |
| `config.py`       | Environment-specific settings                   |
| `utils/`          | Helper functions                                |

---

## 🛠️ Technology Stack

- **Backend**: Flask
- **Database**: PostgreSQL
- **Async Queue**: Redis + Celery
- **Auth**: JWT (PyJWT)
- **Migrations**: Alembic
- **Docs**: Swagger (Flasgger)
- **Deployment**: Docker + Docker Compose

---
## Complete Project Structure

Here’s a brief overview of the directory structure:

```
mediaamp-backend/
├── Dockerfile                                # Docker configuration for the Flask web app
├── README.md                                # Project documentation
├── __pycache__                              # Python bytecode files
├── app/                                      # Flask application code
│   ├── __init__.py                          # Flask app initialization
│   ├── api/                                 # API-related code
│   ├── auth/                                # Authentication-related code
│   ├── celery_worker.py                     # Celery worker for background tasks
│   ├── config.py                            # Configuration file (DB, Redis, etc.)
│   ├── extensions.py                        # Additional app extensions
│   ├── models/                              # Database models (User, Task, etc.)
│   ├── models.py                            # Main model definitions
│   ├── repositories/                       # Data repositories
│   ├── routes.py                            # API routes
│   ├── services/                            # Business logic and services
│   └── utils/                               # Utility functions
├── create_admin.py                          # Script for creating an admin user
├── credential.txt                          # File containing credentials
├── docker-compose.yml                      # Docker Compose configuration file
├── manage.py                               # Script to manage the Flask app
├── migrations/                             # Database migration files
│   ├── README                               # Migration instructions
│   ├── alembic.ini                         # Alembic configuration for DB migrations
│   └── versions/                            # Individual migration scripts
├── requirements.txt                        # Python dependencies for the project
├── run.py                                   # Entry point for running the Flask app
└── tasks/                                   # Celery tasks (background jobs)
    ├── daily_loader.py                     # Example background task for loading data
    └── __init__.py                          # Task initialization
```
## Project Setup

### Prerequisites

Before setting up and running the project, ensure that you have the following software installed on your machine:

1. **Docker** – Required for containerizing the application.
2. **Docker Compose** – For managing multi-container Docker applications.
3. **Git** – For version control and managing the repository.
4. **Python 3.x** – Needed for running the application and its dependencies if you're not using Docker.

### Installation

#### Clone the Repository

To get started, clone the repository from GitHub:

```bash
git clone https://github.com/your-username/mediaamp-backend.git
cd mediaamp-backend
```

#### Install Dependencies (Optional)

If you choose to run the project locally without Docker, install the required Python packages:

```bash
pip install -r requirements.txt
```

This will install all the necessary dependencies to run the project.

## Running the Project

### Development Setup

For local development, it is recommended to use Docker to easily set up and run the application.

1. **Build and Start the Application Using Docker Compose**

To set up the application, run the following command:

```bash
docker-compose up --build
```

This command will:

- Build the Docker images for Flask, Celery, PostgreSQL, and Redis.
- Start the containers and link them together.

2. **Access the Application**

After the containers are up and running, you can access the application via the following URLs:

- **Flask App**: http://localhost:5000
- **Swagger UI (API Documentation)**: http://localhost:5000/apidocs

## API Documentation

You can explore and test the API through Swagger UI. The Swagger documentation is available at:

- **Swagger UI URL**: http://localhost:5000/apidocs

### Key Endpoints

- **POST /register**: Register a new user.
- **POST /login**: Login and receive a JWT token.
- **GET /tasks**: Fetch all tasks, with an optional date filter.
- **POST /task**: Create a new task.
- **GET /task/{id}**: Retrieve a task by ID.
- **PUT /task/{id}**: Update an existing task.
- **DELETE /task/{id}**: Delete a task.


### 🔐 Authentication & Roles
JWT Authentication for secure login

User roles: admin, moderator, user

Protected routes based on role (RBAC)
The system uses JWT for authentication which will generate when you first register then login with the same username and password you will get the token which will be enternd in the authorized button. To make API requests, include the JWT token in the Authorization header, like so:

```bash
Authorization: Bearer <your_token>

GET /admin/dashboard   → accessible only to admin
```
### ⚙️ Background Task Scheduler
Uses Celery to load daily tasks automatically

Redis acts as the broker for Celery

Auto-skips already-logged tasks
```bash
celery -A app.celery_worker.celery worker --loglevel=info
```
### ✅ Features Implemented
 *JWT-based Auth System*

 *Role-Based Access Control (RBAC)*

 *Celery Tasks with Redis*

 *PostgreSQL with secure connection*

 *Redis caching*

 *Swagger API Docs*

 *Dockerized for Production*
 ## 🤝 Contributing
Pull requests are welcome! For major changes, please open an issue first to discuss.
**💬 A Note from the Developer**
This backend project was built with scalability, security, and performance in mind — ensuring that every component is production-ready and follows best practices. I sincerely hope it showcases my backend engineering capabilities and aligns with the standards of MediaAmp.

Thank you for reviewing my submission! 🙏
