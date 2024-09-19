from fastapi import FastAPI
from app.routes import todo  # Import the routes

# Initialize the FastAPI app
app = FastAPI()

# Include the ToDo routes
app.include_router(todo.router)
