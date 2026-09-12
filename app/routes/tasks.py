from fastapi import APIRouter, Response

from app.models.task import HomeTask, HomeTaskCreate, HomeTaskUpdate
from app.services import task_service
from app.utils.validation import not_found

router = APIRouter(prefix="/api/tasks", tags=["tasks"])


class TaskCreateBody(HomeTaskCreate):
    home_id: str


@router.get("", response_model=list[HomeTask])
def list_tasks(home_id: str, status: str | None = None, priority: str | None = None, room_id: str | None = None):
    return task_service.list_tasks(home_id, status, priority, room_id)


@router.post("", response_model=HomeTask, status_code=201)
def create_task(data: TaskCreateBody):
    home_id = data.home_id
    task_data = HomeTaskCreate(**data.model_dump(exclude={"home_id"}))
    return task_service.create_task(home_id, task_data)


@router.put("/{task_id}", response_model=HomeTask)
def update_task(task_id: str, data: HomeTaskUpdate):
    task = task_service.update_task(task_id, data)
    if task is None:
        raise not_found("Task", task_id)
    return task


@router.delete("/{task_id}", status_code=204)
def delete_task(task_id: str):
    if not task_service.delete_task(task_id):
        raise not_found("Task", task_id)
    return Response(status_code=204)
