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
      python create_db.py
      ```

4. Start the User Service:
    - Run the following command to start the User Service:
      ```sh
      uvicorn main:app --reload --port 8001
      ```

5. Access the User Service API documentation:
    - Open your web browser and go to `http://localhost:8001/docs` to access the Swagger UI documentation for the User Service API.

## Testing Descriptions

This project includes unit tests at various levels to ensure the correctness of the application.

### Router Level Tests

- **Purpose:** These tests focus on ensuring the API endpoints behave as expected.
- **Scope:** They test the routing logic, including request validation, response status codes, and response data.
- **Example:** Testing the `/users` endpoint to create a new user and verify that it returns a 201 status code with the correct user data.

### Service Level Tests

- **Purpose:** These tests validate the business logic implemented in the service layer.
- **Scope:** They ensure that the service methods correctly process data and handle different scenarios, such as successful operations and exceptions.
- **Example:** Testing the `create_user` service method to ensure it correctly creates a user and raises appropriate exceptions for invalid data.

### Repository Level Tests

- **Purpose:** These tests focus on the database interactions and ensure the repository methods work as intended.
- **Scope:** They verify that the database operations, such as CRUD operations, are correctly implemented and handle edge cases.
- **Example:** Testing the `add_user` repository method to ensure it correctly inserts a new user record into the database and retrieves it.

## Running Tests

To run the tests for this project, use the following commands:

```sh
python -m unittest routers/test_routes.py
python -m unittest services/test_services.py
python -m unittest repositories/test_repository.py
