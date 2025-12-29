from src.db.task_status import TaskStatus
from src.db.task_status_history import TaskStatusHistory
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, and_
from src.service.verify_status import is_new_status_valid

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

    try:
        await session.commit()
    except Exception:
        await session.rollback()
        raise

    await session.refresh(task)
    return task
