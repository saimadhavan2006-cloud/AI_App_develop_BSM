# REST APIs & FastAPI — VS Code Practice Project

A beginner-friendly Python project for learning REST API development with FastAPI. It covers routing, request validation, CRUD operations, HTTP status codes, dependencies, headers, response models, automated testing, and interactive API documentation.

## Learning Objectives

- Build REST endpoints using FastAPI.
- Work with path and query parameters.
- Validate request data using Pydantic models.
- Implement Create, Read, Update, and Delete (CRUD) operations.
- Understand HTTP methods and status codes.
- Handle missing resources and invalid requests.
- Use request headers and dependency injection.
- Filter API responses using response models.
- Write automated tests with FastAPI TestClient.
- Explore generated OpenAPI documentation.

## Technology Stack

| Technology | Purpose |
|---|---|
| Python | Application programming language |
| FastAPI | REST API framework |
| Pydantic | Request validation and response models |
| Uvicorn | ASGI development server |
| pytest | Automated testing |
| FastAPI TestClient | In-process API testing |

## Project Structure

```text
rest_fastapi_vscode/
├── main.py
├── requirements.txt
├── README.md
├── PRACTICE.md
├── .gitignore
└── tests/
    └── test_api.py
```

## Features and Endpoints

| Method | Endpoint | Purpose |
|---|---|---|
| GET | `/` | Check that the API is responding |
| GET | `/numbers/{number}` | Validate a number and return its double |
| GET | `/greet` | Generate a greeting using query parameters |
| POST | `/tasks` | Create a task |
| GET | `/tasks` | List tasks, optionally filtered by completion status |
| GET | `/tasks/{task_id}` | Retrieve a task by ID |
| PUT | `/tasks/{task_id}` | Replace a task |
| PATCH | `/tasks/{task_id}` | Update selected task fields |
| DELETE | `/tasks/{task_id}` | Delete a task |
| GET | `/profile-demo` | Demonstrate response-model filtering |
| GET | `/header-demo` | Read an `X-Request-ID` header |
| GET | `/protected-demo` | Demonstrate dependency-based header checking |
| GET | `/wait-demo` | Demonstrate an asynchronous endpoint |

## Getting Started

### Prerequisites

- Python 3
- Visual Studio Code
- The Microsoft Python extension for VS Code

### 1. Clone the repository

```powershell
git clone https://github.com/saimadhavan2006-cloud/AI_App_develop_BSM.git
cd AI_App_develop_BSM/rest_fastapi_vscode/rest_fastapi_vscode
```

### 2. Create a virtual environment

```powershell
py -3 -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
```

If `py -3` is unavailable, try:

```powershell
python -m venv .venv
```

If PowerShell blocks virtual-environment activation, use this for the current terminal only:

```powershell
Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
.\.venv\Scripts\Activate.ps1
```

### 3. Install dependencies

```powershell
python -m pip install -r requirements.txt
```

### 4. Start the development server

```powershell
uvicorn main:app --reload
```

Open the following URLs:

- **API root:** http://127.0.0.1:8000/
- **Swagger UI:** http://127.0.0.1:8000/docs
- **ReDoc:** http://127.0.0.1:8000/redoc

Swagger UI lets you send requests and inspect responses interactively.

Stop the server with `Ctrl+C`.

## Example Requests

### Greeting

```http
GET /greet?name=Asha&loud=true
```

Example response:

```json
{
  "message": "HELLO, ASHA"
}
```

### Create a task

Send a `POST` request to `/tasks`:

```json
{
  "title": "Learn FastAPI",
  "done": false
}
```

The API returns HTTP `201 Created` with the newly created task.

### Filter tasks

```http
GET /tasks?done=true&limit=5
```

This retrieves up to five completed tasks.

### Demonstrate request headers

Send a request to `/header-demo` with the header:

```text
X-Request-ID: practice-01
```

### Run the protected demo

Send a request to `/protected-demo` with:

```text
X-API-Key: practice-key
```

The hardcoded key is for learning dependency injection only. It is not suitable for production authentication or security.

## Data Storage

Tasks are currently stored in a Python dictionary in application memory.

- Data is lost when the application restarts.
- The ID counter resets when the application restarts.
- This project does not currently use a database.

Replacing the in-memory dictionary with SQLite is a useful future extension.

## Validation and Error Handling

The API demonstrates several common HTTP responses:

- **200 OK:** A successful read or update.
- **201 Created:** A task was created.
- **204 No Content:** A task was deleted successfully.
- **403 Forbidden:** The protected demo key was missing or incorrect.
- **404 Not Found:** The requested task does not exist.
- **422 Unprocessable Content:** Input validation failed.

Pydantic models validate request bodies, while FastAPI validates path and query parameters.

## Automated Testing

Run the test suite from the project directory:

```powershell
python -m pytest tests/ -v
```

The current tests cover:

- Home and number endpoints
- Greeting query parameters
- Task CRUD operations
- Input validation and error responses
- Headers, dependencies, and response-model filtering

The tests use FastAPI TestClient to exercise the application in-process without requiring a separate Uvicorn server.

## Practice Exercises

Use `PRACTICE.md` to work through the learning exercises, including:

- Adding routes and query parameters
- Improving validation
- Extending task models with a priority field
- Testing invalid input
- Understanding `PUT` versus `PATCH`
- Exploring database-backed persistence

## Future Improvements

- Add task priority and priority-based filtering.
- Replace in-memory storage with SQLite.
- Add pagination and more comprehensive tests.
- Replace the demo API key with a proper authentication mechanism.
- Add API configuration and structured logging.

## Author

**B. Sai Madhavan**

Python | FastAPI | REST API Development
