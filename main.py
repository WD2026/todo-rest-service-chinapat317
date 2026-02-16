"""FastAPI implementation of the Todo REST API."""
from fastapi import FastAPI
from routers import todo


# 'app' is refers to FastAPI
# use param: redirect_slashes=False to disable automatic
# redirection of paths without trailing slash.
app = FastAPI(title="Todo REST API")
app.include_router(todo.router)
