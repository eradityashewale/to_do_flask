# Flask Todo API

This is a simple RESTful Todo API built with Flask and MongoDB. The API allows you to create, retrieve, update, and delete todo items.

## Features

- Create a todo item
- Retrieve all todo items
- Retrieve a specific todo item by ID
- Update a todo item
- Delete a todo item
- Filtering and sorting
- Basic rate limiting
- Pagination

## Requirements

- Python 3.x
- MongoDB
- Docker (optional, for containerized setup)

## Setup Instructions

### 1. Clone the Repository

git clone https://github.com/eradityashewale/to_do_flask.git
cd flask-todo-api

### 2. Set up a Virtual Environment

python -m venv venv
source venv/bin/activate 

### 3. Install Dependencies

pip install -r requirements.txt

### 4. Set Up MongoDB

Make sure you have MongoDB running locally or modify the connection URI in the app.py file.

### 5. Run the Application

flask run

The API will be available at http://127.0.0.1:5000.

### 6. Run with Docker

To run the application with Docker:
docker build -t flask-todo-api .
docker run -d -p 5000:5000 flask-todo-api

## API Endpoints

| Method | Endpoint          | Description                          | Request Body               | Response Body                      | Status Codes                 |
|--------|-------------------|--------------------------------------|----------------------------|-------------------------------------|------------------------------|
| GET    | `/todos`          | Retrieve all todos                   | None                       | Array of Todo objects               | 200                          |
| POST   | `/todos`          | Create a new todo                    | `{"title": "string", "description": "string", "status": "string"}` | Todo object                      | 201                          |
| GET    | `/todos/{id}`     | Retrieve a specific todo by ID       | None                       | Todo object                        | 200, 404                     |
| PUT    | `/todos/{id}`     | Update an existing todo              | `{"title": "string", "description": "string", "status": "string"}` | Todo object                      | 200, 404                     |
| DELETE | `/todos/{id}`     | Delete a todo                        | None                       | None                                | 204, 404                     |

## Todo Object Schema

{
  "id": "integer",
  "title": "string",
  "description": "string",
  "status": "enum: [pending, in_progress, completed]",
  "created_at": "datetime",
  "updated_at": "datetime"
}

## API Documentation

The API documentation is provided using Swagger (OpenAPI).

1. Install Flask-Swagger-UI
pip install flask-swagger-ui

2. Access Swagger Documentation
Navigate to http://127.0.0.1:5000/swagger-ui to view the interactive API documentation.


## Testing

To run unit tests for the API:
python -m unittest discover


