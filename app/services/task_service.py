from app.models.task import HomeTask, HomeTaskCreate, HomeTaskUpdate
from app.services.json_store import read_collection, write_collection
from app.utils.dates import now_iso
from app.utils.ids import new_id

COLLECTION = "tasks"


def list_tasks(home_id: str, status: str | None = None, priority: str | None = None, room_id: str | None = None) -> list[dict]:
    items = [t for t in read_collection(COLLECTION) if t.get("home_id") == home_id]
    if status:
        items = [t for t in items if t.get("status") == status]
    if priority:
        items = [t for t in items if t.get("priority") == priority]
    if room_id:
        items = [t for t in items if t.get("room_id") == room_id]
    return items


def get_task(task_id: str) -> dict | None:
    for task in read_collection(COLLECTION):
        if task.get("id") == task_id:
            return task
    return None


def create_task(home_id: str, data: HomeTaskCreate) -> dict:
    items = read_collection(COLLECTION)
    now = now_iso()
    record = HomeTask(id=new_id("task"), home_id=home_id, created_at=now, updated_at=now, **data.model_dump()).model_dump()
    items.append(record)
    write_collection(COLLECTION, items)
    return record


def update_task(task_id: str, data: HomeTaskUpdate) -> dict | None:
    items = read_collection(COLLECTION)
    for idx, task in enumerate(items):
        if task.get("id") == task_id:
            task.update(data.model_dump(exclude_unset=True))
            task["updated_at"] = now_iso()
            validated = HomeTask(**task).model_dump()
            items[idx] = validated
            write_collection(COLLECTION, items)
            return validated
    return None


def delete_task(task_id: str) -> bool:
    items = read_collection(COLLECTION)
    filtered = [t for t in items if t.get("id") != task_id]
    if len(filtered) == len(items):
        return False
    write_collection(COLLECTION, filtered)
    return True
