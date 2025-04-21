# Flask Container Details App

This application displays container details and a to-do list using Flask and Docker Compose.

## Setup

1. Install Docker and Docker Compose.
2. Clone the repository.
3. Run `docker-compose up` to start the application and database.

## Docker Compose Services

- `web`: Flask application container
- `db`: PostgreSQL database container

The Flask app displays container details on the main page and a to-do list on the `/todos` route. The to-do items are stored in the PostgreSQL database.

The application now supports adding new to-do items, removing existing to-do items, and persisting the data in the PostgreSQL database. The data will be persisted even if the containers are stopped and restarted.
