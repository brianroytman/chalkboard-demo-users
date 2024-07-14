# Chalkboard Demo Users Microservice

This repository contains the code for the chalkboard_demo_users project, which consists of two interconnected microservices: User Service and Todo Service. The User Service is responsible for managing user-related operations.

## Technologies Used

The following technologies were used in this project:

- FastAPI
- PostgreSQL
- SQLAlchemy
- Docker
- OpenAPI/Swagger

## Directory Structure

The directory structure of this project is as follows:

### User Service

- `repositories/user_repository.py`: This file implements database operations using SQLAlchemy.
- `routers/user_routes.py`: This file defines API routes and endpoints using FastAPI. It depends on services for handling requests.
- `services/users_service.py`: This file implements the business logic and coordinates with repositories.
- `create_db.py`: This script is used for database creation.
- `database.py`: This file contains the setup for the database connection.
- `main.py`: This file initializes the FastAPI app.
- `models.py`: This file defines the SQLAlchemy model for User.
- `schemas.py`: This file defines the Pydantic schemas for input/output validation.

## API Endpoints

- Create a User: POST /users/
- Read Users: GET /users/
- Read a User by ID: GET /users/{user_id}/
- Update a User: PUT /users/{user_id}/
- Delete a User: DELETE /users/{user_id}/

## Setup Instructions

To set up and run this project, follow these instructions:

1. Clone the repository:
    ```sh
    git clone <repository_url>
    ```

2. Install the required dependencies:
    ```sh
    pip install -r requirements.txt
    ```

3. Set up the database:
    - Run the following command to create the database:
    ```sh
    py create_db.py
    ```

4. Start the User Service:
    - Run the following command to start the User Service:
    ```sh
    uvicorn main:app --reload --port 8001
    ```

5. Access the User Service API documentation:
    - Open your web browser and go to `http://localhost:8001/docs` to access the Swagger UI documentation for the User Service API.

## cURL Request Examples
- GET /users/
```sh
curl -X 'GET' \
  'http://127.0.0.1:8001/users' \
  -H 'accept: application/json'
```

- POST /users/
```sh
curl -X 'POST' \
  'http://127.0.0.1:8001/users' \
  -H 'accept: application/json' \
  -H 'Content-Type: application/json' \
  -d '{
  "email": "testing@gmail.com",
  "first_name": "Test",
  "last_name": "Me",
  "username": "TestMeAgain"
}'
```

-GET /users/{user_id}
```sh
curl -X 'GET' \
  'http://127.0.0.1:8001/users/1' \
  -H 'accept: application/json'
```

- PUT /users/{user_id}/
```sh
curl -X 'PUT' \
  'http://127.0.0.1:8001/users/1' \
  -H 'accept: application/json' \
  -H 'Content-Type: application/json' \
  -d '{
  "email": "johnnydoe@gmail.com",
  "first_name": "Johnny",
  "last_name": "Doe",
  "username": "jd"
}'
```

- DELETE /users/{user_id}/
```sh
curl -X 'DELETE' \
  'http://127.0.0.1:8001/users/6' \
  -H 'accept: */*'
```

## Running Tests

To run the tests for this project, use the following commands:

```sh
python -m unittest -v routers/test_routes.py
python -m unittest -v services/test_services.py
python -m unittest -v repositories/test_repository.py
