from typing import Annotated
from fastapi.responses import Response

from fastapi import FastAPI, HTTPException, Query, Path as ApiPath, Header, Depends, Response
from pydantic import BaseModel, Field, ConfigDict

app = FastAPI(title="My Task API", version="1.0.0")

tasks: dict[int, dict] = {}
next_id = 1


class TaskCreate(BaseModel):
    model_config = ConfigDict(extra="forbid")
    title: str = Field(min_length=1, max_length=100)
    done: bool = False


class TaskReplace(BaseModel):
    model_config = ConfigDict(extra="forbid")
    title: str = Field(min_length=1, max_length=100)
    done: bool


class TaskPatch(BaseModel):
    model_config = ConfigDict(extra="forbid")
    title: str | None = Field(default=None, min_length=1, max_length=100)
    done: bool | None = None


class TaskOut(BaseModel):
    id: int
    title: str
    done: bool


class PublicProfile(BaseModel):
    username: str


@app.get("/")
def home():
    return {"message": "My Task API is working"}


@app.get("/numbers/{number}")
def describe_number(number: Annotated[int, ApiPath(ge=1)]):
    return {"number": number, "double": number * 2}


@app.get("/greet")
def greeting(
    name: Annotated[str, Query(min_length=1)] = "friend",
    loud: bool = False,
):
    message = f"Hello, {name}"
    return {"message": message.upper() if loud else message}


def find_task(task_id: int):
    if task_id not in tasks:
        raise HTTPException(status_code=404, detail="Task not found")
    return tasks[task_id]


@app.post("/tasks", response_model=TaskOut, status_code=201)
def create_task(task: TaskCreate):
    global next_id
    saved = {"id": next_id, **task.model_dump()}
    tasks[next_id] = saved
    next_id += 1
    return saved


@app.get("/tasks", response_model=list[TaskOut])
def list_tasks(
    done: bool | None = None,
    limit: Annotated[int, Query(ge=1, le=100)] = 10,
):
    selected = list(tasks.values())
    if done is not None:
        selected = [task for task in selected if task["done"] == done]
    return selected[:limit]


@app.get("/tasks/{task_id}", response_model=TaskOut)
def read_task(task_id: Annotated[int, ApiPath(ge=1)]):
    return find_task(task_id)


@app.put("/tasks/{task_id}", response_model=TaskOut)
def replace_task(
    task_id: Annotated[int, ApiPath(ge=1)],
    task: TaskReplace,
):
    find_task(task_id)
    tasks[task_id] = {"id": task_id, **task.model_dump()}
    return tasks[task_id]


@app.patch("/tasks/{task_id}", response_model=TaskOut)
def patch_task(
    task_id: Annotated[int, ApiPath(ge=1)],
    patch: TaskPatch,
):
    saved = find_task(task_id)
    changes = patch.model_dump(exclude_unset=True)
    if any(value is None for value in changes.values()):
        raise HTTPException(status_code=422, detail="Fields cannot be null")
    saved.update(changes)
    return saved


@app.delete("/tasks/{task_id}", status_code=204)
def delete_task(task_id: Annotated[int, ApiPath(ge=1)]):
    find_task(task_id)
    del tasks[task_id]
    return Response(status_code=204)


@app.get("/profile-demo", response_model=PublicProfile)
def profile_demo():
    return {"username": "learner", "internal_note": "this field is filtered out"}


@app.get("/header-demo")
def header_demo(x_request_id: Annotated[str | None, Header()] = None):
    return {"request_id": x_request_id}


def require_demo_key(x_api_key: Annotated[str | None, Header()] = None):
    if x_api_key != "practice-key":
        raise HTTPException(status_code=403, detail="Demo access denied")
    return x_api_key


@app.get("/protected-demo")
def protected_demo(key: Annotated[str, Depends(require_demo_key)]):
    return {"message": "You passed the demo check"}


@app.get("/wait-demo")
async def wait_demo():
    import asyncio
    await asyncio.sleep(0.01)
    return {"message": "Finished waiting"}

@app.get("/favicon.ico", include_in_schema=False)
def favicon():
    return Response(status_code=204)