# FastAPI Authentication App with PostgreSQL

This is a FastAPI application that provides user authentication and user creation functionality, using PostgreSQL as the database. The application is containerized with Docker for easy setup and deployment.

## Features
- User registration
- User authentication (OAuth2 with JWT)
- PostgreSQL database integration
- Dockerized for easy deployment

## Project Structure

```bash
fastapi_app/
│
├── app/
│   ├── __init__.py          # Package initializer
│   ├── main.py              # FastAPI entry point
│   ├── auth.py              # Authentication routes and logic
│   ├── models.py            # SQLAlchemy models
│   ├── database.py          # Database connection and session handling
│   ├── schemas.py           # Pydantic schemas for validation
│   ├── utils.py             # Utility functions (hashing, token creation)
│
├── alembic.ini              # Alembic configuration for migrations
├── Dockerfile               # Dockerfile for the FastAPI app
├── docker-compose.yml       # Docker Compose file to run app and PostgreSQL
├── requirements.txt         # Python dependencies
├── .env                     # Environment variables (Database URL, secrets, etc.)
└── README.md                # Project instructions
```

Prerequisites
Ensure that you have the following installed on your machine:

Docker
Docker Compose
Git

Getting Started

Build and start the Docker containers
Run the following command to build the Docker images and start the FastAPI app along with the PostgreSQL database:

```bash
docker-compose up --build
```

This will pull the necessary Docker images, build the FastAPI app image, and start the PostgreSQL database.

Access the API
Once the containers are up and running, you can access the FastAPI application at:

API URL: http://localhost:8000
API Docs: http://localhost:8000/docs (Swagger UI)
You can use the /docs endpoint to test the API endpoints with FastAPI's Swagger interface.

Database Migrations (Optional)
If you want to use Alembic for database migrations, initialize Alembic and generate migrations:

```bash
# Initialize Alembic (Run once)
alembic init alembic

# Create a migration after changing models
alembic revision --autogenerate -m "Initial migration"

# Apply migrations
alembic upgrade head
```

API Endpoints
1. Create User
Endpoint: POST /users

Request Body:

```json
{
  "username": "your_username",
  "password": "your_password"
}
```
Response:

```json
{
  "id": 1,
  "username": "your_username"
}
```
2. Login
Endpoint: POST /token

Request Body (using OAuth2PasswordRequestForm):

username: your username
password: your password
Response:

```json
{
  "access_token": "your_jwt_token",
  "token_type": "bearer"
}
```
Running the Application in Development
While the Docker setup is recommended for deployment, you can also run the application locally for development:

Install dependencies:

```bash
pip install -r requirements.txt
```

Start the FastAPI server:

```bash
uvicorn app.main:app --reload
```

Stopping the Application
To stop the running Docker containers, run:

```bash
docker-compose down
```