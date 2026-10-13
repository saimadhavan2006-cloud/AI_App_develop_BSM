# REST APIs & FastAPI — VS Code Practice Project

This is a VS Code version of the supplied Google Colab guide. It keeps the guide's beginner task API and its main ideas: routes, path/query parameters, Pydantic models, CRUD, status codes, headers, dependencies, async handlers, tests, and OpenAPI docs.

## 1. Open in VS Code

1. Extract this ZIP.
2. In VS Code choose **File → Open Folder** and select `rest_fastapi_vscode`.
3. Install the Microsoft **Python** extension if needed.
4. Open **Terminal → New Terminal**.

## 2. Create a virtual environment (Windows PowerShell)

```powershell
py -3 -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
pip install -r requirements.txt
```

If PowerShell blocks activation, run this only for the current terminal:
```powershell
Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
.\.venv\Scripts\Activate.ps1
```

If `py -3` is unavailable, try `python -m venv .venv`.

## 3. Run the API

```powershell
uvicorn main:app --reload
```

Open these URLs in your browser:
- http://127.0.0.1:8000 — home endpoint
- http://127.0.0.1:8000/docs — interactive Swagger UI (try requests here)
- http://127.0.0.1:8000/redoc — alternate API documentation

Stop the server with `Ctrl+C`.

## 4. Run automated tests

Open a second terminal, activate `.venv` if needed, then run:
```powershell
pytest -q
```
Expected: all tests pass.

## 5. Practice in this order

1. Change the message in `home()` and refresh `/`.
2. Try `/numbers/7`, `/numbers/abc`, `/numbers/0`.
3. Try `/greet?name=Asha&loud=true`.
4. In `/docs`, create a task with `POST /tasks`.
5. List tasks with `GET /tasks`, then filter with `?done=true` or `?done=false`.
6. Replace all editable fields with `PUT /tasks/{task_id}`.
7. Change one field with `PATCH /tasks/{task_id}`.
8. Delete a task with `DELETE /tasks/{task_id}`. A `204` response has no body.
9. Try an invalid title, unknown ID, and `limit=0`; inspect the status and error.
10. Try `/header-demo` with `X-Request-ID: practice-01`.
11. Try `/protected-demo` with `X-API-Key: practice-key`. This is a demo key only, not real security.
12. Run `pytest -q` after edits.

## Important learning notes

- The tasks are stored in a Python dictionary, so they disappear when the app restarts. This is not a database.
- `TestClient` tests the app in-process; Uvicorn serves real HTTP requests.
- `GET` reads, `POST` creates, `PUT` replaces, `PATCH` updates selected fields, and `DELETE` removes.
- `422` usually means validation failed; `404` means the requested task was not found.
- Restarting the app resets the in-memory task list and ID counter.

## Next challenge

Add an integer `priority` field restricted to 1–3. Update `TaskCreate`, `TaskReplace`, `TaskPatch`, and `TaskOut` consistently. Choose a default, add a filter to `GET /tasks`, and add a test proving priority 4 is rejected.
