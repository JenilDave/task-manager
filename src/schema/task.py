from pydantic import BaseModel, Field

class CreateTaskPayload(BaseModel):
    title: str = Field(..., max_length=100)
    description: str = Field(..., max_length=500)
    status: str = Field(..., max_length=20)

class TaskResponse(BaseModel):
    task_id: int
    title: str
    description: str
    status: str