# Cloud Microservices Project

This project is a Docker-based microservices architecture deployed on an EC2 instance. It consists of multiple Python microservices, an API Gateway, and a PostgreSQL database, all orchestrated using Docker Compose.

---

## Architecture Overview

Services included:

* **API Gateway** – entry point for all client requests
* **User Service** – handles user-related operations
* **Task Service** – manages tasks
* **Notification Service** – handles notifications
* **PostgreSQL** – shared relational database

All services communicate over a private Docker network. PostgreSQL can optionally be accessed externally via port 5432.

---

## Project Structure

```
cloud-microservices-project/
│
├── api-gateway/
│   ├── Dockerfile
│   └── main.py
│
├── user-service/
│   ├── Dockerfile
│   └── main.py
│
├── task-service/
│   ├── Dockerfile
│   └── main.py
│
├── notification-service/
│   ├── Dockerfile
│   └── main.py
│
├── docker-compose.yml
└── README.md
```

---

## Prerequisites

Make sure the following are installed on your EC2 instance or local machine:

* Docker
* Docker Compose (v2+ recommended)
* An AWS EC2 instance (Amazon Linux or Ubuntu)
* Security Group allowing required ports

### Required Open Ports (EC2 Security Group)

|      Port | Purpose                                  |
| --------: | ---------------------------------------- |
|        22 | SSH access                               |
| 8000–8003 | Microservices (optional external access) |
|      5432 | PostgreSQL (optional external access)    |

---

## Environment Variables

Each microservice uses the following database connection string:

```
DATABASE_URL=postgresql://postgres:postgres@postgres:5432/microservices
```

This is automatically injected via `docker-compose.yml`.

---

## How the Project Is Built

1. Each microservice has its own **Dockerfile**
2. The Dockerfile:

   * Uses Python as the base image
   * Copies the service source code
   * Installs dependencies
   * Starts the app using `main.py`
3. Docker Compose:

   * Builds images for all services
   * Creates a shared Docker network
   * Starts PostgreSQL before application services

---

## How to Build the Project

From the project root directory:

```bash
docker-compose build
```

This command:

* Builds all microservice images
* Pulls the PostgreSQL image

---

## How to Run the Project

Start all services:

```bash
docker-compose up -d
```

Check running containers:

```bash
docker-compose ps
```

View logs:

```bash
docker-compose logs -f
```

---

## How to Stop and Reset Everything

Stop containers:

```bash
docker-compose down
```

Stop containers **and delete volumes (fresh start)**:

```bash
docker-compose down -v
```

Remove unused images and networks (optional):

```bash
docker system prune -a
```

---

## Accessing PostgreSQL

### From another container:

```bash
psql -h postgres -U postgres -d microservices
```

### From outside EC2:

```bash
psql -h <EC2_PUBLIC_IP> -U postgres -d microservices -p 5432
```

Make sure port **5432** is allowed in the EC2 security group.

---

## Common Issues & Fixes

### Container exits with `app.py not found`

**Cause:** Application file is named `main.py`

**Fix:** Ensure Dockerfile command matches:

```
CMD ["python", "main.py"]
```

---

### Database connection fails

* Ensure PostgreSQL container is running
* Use hostname `postgres`, not `localhost`
* Verify `DATABASE_URL` inside container

```bash
docker exec -it <container_name> env | grep DATABASE
```

---

## Useful Docker Commands

```bash
docker-compose ps
docker-compose restart
docker exec -it <container> bash
```

---

## Notes

* Docker Compose `version` warning can be safely ignored
* PostgreSQL data persists using Docker volumes
* Services auto-restart unless stopped manually

---

## Author

Cloud Microservices Project
