from fastapi import FastAPI
from .database import engine, Base
from .routers import todos, reminders, calendar

app = FastAPI()

# Create tables
Base.metadata.create_all(bind=engine)

# Include your routers with original paths
app.include_router(todos.router)
app.include_router(reminders.router)
app.include_router(calendar.router)