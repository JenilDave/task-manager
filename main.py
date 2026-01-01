from fastapi import FastAPI
from src.api import task, user

app = FastAPI()

app.include_router(task.router)
app.include_router(user.router)

@app.get("/")
async def root():
    return {"message": "Welcome to the Task Manager API"}