from src.db.task_status import TaskStatus
from src.db.task_status_history import TaskStatusHistory
from src.db.task_result import TaskResult
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, and_
from src.service.status import is_new_status_valid, is_final_status
from fastapi import BackgroundTasks

async def get_task_by_id(session: AsyncSession, task_id: int) -> TaskStatus:
    return await session.get(TaskStatus, task_id)

async def create_task(
    session: AsyncSession,
    title: str,
    description: str,
    status: str,
) -> TaskStatus:

    result = await session.execute(
        select(TaskStatus).where(
            and_(
                TaskStatus.title == title,
                TaskStatus.description == description,
            )
        )
    )
    existing_task = result.scalar_one_or_none()

    if existing_task:
        return existing_task

    new_task = TaskStatus(
        title=title,
        description=description,
        status=status,
    )

    session.add(new_task)

    try:
        await session.commit()
    except Exception:
        await session.rollback()
        raise

    await session.refresh(new_task)
    return new_task


async def update_task_status(
    session: AsyncSession,
    task_id: int,
    new_status: str,
    background_tasks: BackgroundTasks = None,
) -> TaskStatus | None:

    task = await session.get(TaskStatus, task_id)
    if not task:
        return None

    old_status = task.status
    if not is_new_status_valid(task.status, new_status):
        return None

    task.status = new_status

    status_history = TaskStatusHistory(
        task_id=task.id,
        from_state=old_status,
        to_state=new_status,
    )
    session.add(status_history)

    if is_final_status(new_status) and background_tasks:
        background_tasks.add_task(update_task_result, session, task.id, "COMPLETED", "Task has been completed successfully.")

    try:
        await session.commit()
    except Exception:
        await session.rollback()
        raise

    await session.refresh(task)
    return task

async def update_task_result(session, task_id: int, status: str, message: str = None):
    task_result = TaskResult(
        task_id=task_id,
        status=status,
        message=message,
    )
    session.add(task_result)
    try:
        await session.commit()
    except Exception:
        await session.rollback()
        raise

    await session.refresh(task_result)
    return task_result