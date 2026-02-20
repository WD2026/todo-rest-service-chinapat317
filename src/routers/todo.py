import logging
from fastapi import APIRouter, HTTPException, Request, Response
from models import TodoCreate, Todo
from persistence import TodoDao

router = APIRouter(tags=["Todo"])

# Data Access Object (dao) provides persistence operations for todo.
dao = TodoDao("todo_data.json")

logger = router.logger    # logging.getLogger(__name__)

### REST service URLs and request handlers ###
@router.get("/todos/", response_model=list[Todo])
def get_todos():
    """Get all todos."""
    return dao.get_all()


@router.post("/todos/", response_model=Todo, status_code=201)
def create_todo(todo: TodoCreate, request: Request, response: Response):
    """Create and save a new todo. A unique ID is assigned."""
    logger.info(f'Saving todo "{todo.text}"')
    created = dao.save(todo)
    logger.info(f"Saved todo with id {todo.id}")
    # Return the location of the new todo.
    location = f"/todos/{created.id}"
    # A cleaner way to get the location URL is reverse mapping.
    # location = request.url_for("get_todo", todo_id=str(created.id))
    response.headers["Location"] = location
    return created


@router.get("/todos/{todo_id}", response_model=Todo)
def get_todo(todo_id: int):
    """Get a specific todo by id.

    :param todo_id: identifier of the todo to get.
    """
    todo = dao.get(todo_id)
    if not todo:
        raise HTTPException(status_code=404, detail="Todo not found")
    return todo


@router.put("/todos/{todo_id}", response_model=Todo)
def update_todo(todo_id: int, todo: TodoCreate):
    """Update an existing Todo.

    :param todo_id: identifier of the todo to update
    :param todo: revised data for the todo
    """
    existing = dao.get(todo_id)
    if not existing:
        raise HTTPException(status_code=404, detail="Todo not found")

    updated = Todo(
        id=todo_id,
        text=todo.text,
        done=todo.done,
    )
    return dao.update(updated)


@router.delete("/todos/{todo_id}", status_code=204)
def delete_todo(todo_id: int):
    """Delete a Todo.

    :param todo_id: identifier of the todo to delete

    Return 204 (or 200 + message) if todo is deleted.
    Return {what?} if todo is not found.
    """
    # TODO implement this method
    try:
        dao.delete(todo_id=todo_id)
    
    except ValueError:
        raise HTTPException(status_code=404, detail="Id not found")

@router.options("/todos/")
def todos_options(response: Response):
    """Return the allowed HTTP methods for this URL."""
    response.headers["Allow"] = "GET,POST,OPTIONS"
    return


@router.options("/todos/{todo_id}")
def todo_options(todo_id: int, response: Response):
    """Return the allowed HTTP methods for this URL."""
    todo = dao.get(todo_id)
    if not todo:
        raise HTTPException(status_code=404, detail="Todo not found")
    response.headers["Allow"] = "GET,PUT,DELETE,OPTIONS"
    return