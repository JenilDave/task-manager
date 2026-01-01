from fastapi import APIRouter, HTTPException, Depends, BackgroundTasks
from src.utils.db import get_db_session
from src.service.task_service import create_task, update_task_status, get_task_by_id
from src.schema.task import CreateTaskPayload, TaskResponse, UpdateTaskStatusPayload
from src.api.deps import CurrentUser

router = APIRouter(
    prefix="/tasks",
    tags=["tasks"],
    responses={404: {"description": "Not found"}},
)

@router.get("/{task_id}")
async def read_task(task_id: int, current_user: CurrentUser, session=Depends(get_db_session)) -> TaskResponse:

    task = await get_task_by_id(session, task_id)
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")

    return TaskResponse(
        task_id=task.id,
        title=task.title,
        description=task.description,
        status=task.status,
    )

@router.post("/create")
async def create_new_task(request: CreateTaskPayload, current_user: CurrentUser, session=Depends(get_db_session)) -> TaskResponse:

    task = await create_task(
        session,
        request.title,
        request.description,
        request.status,
    )

    if task is None:
        raise HTTPException(
            status_code=400,
            detail="Invalid task data or status",
        )

    return TaskResponse(
        task_id=task.id,
        title=task.title,
        description=task.description,
        status=task.status,
    )

@router.put("/{task_id}/status")
async def update_task(
    request: UpdateTaskStatusPayload,
    current_user: CurrentUser,
    background_tasks: BackgroundTasks = None,
    session=Depends(get_db_session),
) -> TaskResponse:

    task = await update_task_status(
        session,
        request.task_id,
        request.new_status,
        background_tasks,
    )

    if task is None:
        raise HTTPException(
            status_code=400,
            detail="Task not found or invalid status transition",
        )

    return TaskResponse(
        task_id=task.id,
        title=task.title,
        description=task.description,
        status=task.status,
    )