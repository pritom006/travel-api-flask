# Travel-API Management

## Table of Contents
1. [Project Overview](#project-overview)
2. [Features](#features)
3. [Project Structure](#project-structure)
4. [Getting Started](#getting-started)
    - [Installation](#installation)
    - [Environment Setup](#environment-setup)
    - [Running the Services](#running-the-services)
5. [API Endpoints](#api-endpoints)
    - [Authentication Service](#authentication-service)
    - [User Service](#user-service)
    - [Destination Service](#destination-service)
6. [Testing](#testing)
7. [Useful Links](#useful-links)
8. [License](#license)

---

## Project Overview

The **Travel-API Management** project is a microservice-based application designed to manage user authentication, destination information, and role-based access control. This system leverages Flask for the backend and organizes services for scalability and maintainability.

---

## Features

- **Authentication Service:** Handles user registration, login, and token-based authentication.
- **User Service:** Manages user profiles and roles.
- **Destination Service:** Provides APIs for viewing and managing travel destinations.
- **Role-Based Access Control:** Secure endpoints based on user roles (e.g., Admin).
- **Swagger Integration:** API documentation for each service.

---

# Project Structure

```plaintext
travel-api/
├── destination_service/
│   ├── src/
│   │   ├── controllers/
│   │   │   └── destination_controller.py
│   │   ├── models/
│   │   │   └── destination_model.py
│   │   ├── routes/
│   │   │   └── destination_routes.py
│   │   └── app.py
│   ├── static/
│   │   └── swagger.json
│   ├── tests/
│   │   └── test_destination_service.py
│   └── requirements.txt
├── user_service/
│   ├── src/
│   │   ├── controllers/
│   │   │   └── user_controller.py
│   │   ├── models/
│   │   │   └── user_model.py
│   │   ├── routes/
│   │   │   └── user_routes.py
│   │   └── app.py
│   ├── static/
│   │   └── swagger.json
│   ├── tests/
│   │   └── test_user_service.py
│   └── requirements.txt
├── auth_service/
│   ├── src/
│   │   ├── controllers/
│   │   │   └── auth_controller.py
│   │   ├── models/
│   │   │   └── token_model.py
│   │   ├── routes/
│   │   │   └── auth_routes.py
│   │   └── app.py
│   ├── static/
│   │   └── swagger.json
│   ├── tests/
│   │   └── test_auth_service.py
│   └── requirements.txt
├── common/
│   ├── utils.py
│   └── constants.py
├── README.md
├── run_services.sh
└── .gitignore
```



---

## Getting Started

### Installation

1. Clone the repository:
    ```bash
    git clone https://github.com/your-repo/travel-api.git
    cd travel-api
    ```

2. Install dependencies for each service:
    ```bash
    cd auth_service
    pip install -r requirements.txt
    cd ../user_service
    pip install -r requirements.txt
    cd ../destination_service
    pip install -r requirements.txt
    ```

### Environment Setup

1. Set the `PYTHONPATH` for each service:
    ```bash
    export PYTHONPATH=$PYTHONPATH:/path/to/travel-api
    ```

2. Use the provided shell script to automate this:
    ```bash
    chmod +x run_services.sh
    ./run_services.sh
    ```

---

### Running the Services

1. Run each service manually:
    - **Authentication Service**:
        ```bash
        python auth_service/src/app.py
        ```
    - **User Service**:
        ```bash
        python user_service/src/app.py
        ```
    - **Destination Service**:
        ```bash
        python destination_service/src/app.py
        ```

2. Alternatively, run all services using:
    ```bash
    ./run_services.sh
    ```

---

## API Endpoints

### Authentication Service

- **POST /admin_access**: If user is Admin then available for manage destinaitons.
-
Example:
```bash
curl -X 'POST' \
  'http://localhost:5003/admin-access' \
  -H 'Authorization: Bearer <access_token>'
```

### User Service

- **POST /register**: Register a new user.
- **POST /login**: Authenticate user and get a token.

Example:
```bash
curl -X 'POST' \
  'http://localhost:5002/register' \
  -H 'Content-Type: application/json' \
  -d '{"name": "lorem",  "password": "lorem006"}'
```

Example:
```bash
curl -X 'POST' \
  'http://localhost:5002/login' \
  -H 'Content-Type: application/json' \
  -d '{"username": "lorem", "password": "lorem006", "role": "Admin"}'
```

**GET /profile**: Fetch user profile details.  
Example:

```bash
curl -X 'GET' \
  'http://localhost:5002/profile' \
  -H 'Authorization: Bearer <access_token>'
 
``` 

## Destination Service
**GET /destinations**: view all destinations.  
Example:

```bash
curl -X 'GET' \
  'http://127.0.0.1:5001/destinations' \
  -H 'Authorization: Bearer <access_token>'
```

**DElETE /destinations/<destination_id>**: Delete specific destinations.  
Example:

```bash
curl -X 'GET' \
  'http://127.0.0.1:5001/destinations/1' \
  -H 'Authorization: Bearer <access_token>'
```

**POST /destinations**: Add destinations.  
Example:

```bash
curl -X 'GET' \
  'http://127.0.0.1:5001/destinations' \
  -H 'Authorization: Bearer <access_token>'
```

## Testing
** For each directory activate virtual env and ensure pytest is installed
** pytest --cov=src --maxfail=5 --disable-warnings -v (run this command)
 
## Useful Links

- **API Documentation**:
  - [Authentication Service Swagger](http://localhost:5003/swagger/)
  - [User Service API Docs](http://localhost:5002/api/docs)
  - [Destination Service Swagger](http://127.0.0.1:5001/api/docs/#/default/get_destinations)


