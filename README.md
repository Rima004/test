# Django Project

This is a Django-based web application.

## Technologies Used

*   **Backend:** Django, Django REST Framework
*   **Database:** PostgreSQL
*   **Asynchronous Tasks:** Celery
*   **Message Broker:** RabbitMQ / Redis
*   **Authentication:** JWT (JSON Web Token)
*   **Containerization:** Docker, Docker Compose
*   **API Schema:** OpenAPI 3 (via drf-spectacular)

## Setup and Installation

1.  **Clone the repository:**
    ```bash
    git clone <repository-url>
    cd <repository-name>
    ```

2.  **Create a `.env` file** for environment variables. You can use `.env.example` as a template.

3.  **Build and run the Docker containers:**
    ```bash
    docker-compose up --build
    ```

## Running the Application

The application will be available at `http://localhost:8000`.

### API Documentation

The auto-generated API documentation (Swagger UI) can be accessed at `http://localhost:8000/api/docs/`.
