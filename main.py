from fastapi import FastAPI
from src.api import task

app = FastAPI()

app.include_router(task.router)

@app.get("/")
async def root():
    return {"message": "Welcome to the Task Manager API"}