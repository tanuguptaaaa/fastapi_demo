from fastapi import FastAPI

from app.routes import todo, users  # Import the routes

# Initialize the FastAPI app
app = FastAPI()

# Include the ToDo routes
app.include_router(todo.router)
app.include_router(users.router)
