from app.models.maintenance import MaintenanceItem, MaintenanceItemCreate
from app.services.json_store import read_collection, write_collection
from app.utils.dates import now_iso
from app.utils.ids import new_id

COLLECTION = "maintenance_items"


def list_items(home_id: str) -> list[dict]:
    return [m for m in read_collection(COLLECTION) if m.get("home_id") == home_id]


def create_item(home_id: str, data: MaintenanceItemCreate) -> dict:
    items = read_collection(COLLECTION)
    now = now_iso()
    record = MaintenanceItem(
        id=new_id("maint"), home_id=home_id, created_at=now, updated_at=now, **data.model_dump()
    ).model_dump()
    items.append(record)
    write_collection(COLLECTION, items)
    return record


def update_item(item_id: str, data: MaintenanceItemCreate) -> dict | None:
    items = read_collection(COLLECTION)
    for idx, item in enumerate(items):
        if item.get("id") == item_id:
            updated = MaintenanceItem(
                id=item_id, home_id=item.get("home_id"), created_at=item.get("created_at"),
                updated_at=now_iso(), **data.model_dump(),
            ).model_dump()
            items[idx] = updated
            write_collection(COLLECTION, items)
            return updated
    return None


def delete_item(item_id: str) -> bool:
    items = read_collection(COLLECTION)
    filtered = [m for m in items if m.get("id") != item_id]
    if len(filtered) == len(items):
        return False
    write_collection(COLLECTION, filtered)
    return True
