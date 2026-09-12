from app.models.appliance import Appliance, ApplianceCreate
from app.models.furniture import FurnitureItem, FurnitureCreate
from app.models.home import HomeProfile
from app.models.room import Room, RoomCreate, RoomUpdate
from app.services.json_store import read_collection, write_collection
from app.utils.dates import now_iso
from app.utils.ids import new_id

COLLECTION = "homes"


def _load_homes() -> list[dict]:
    return read_collection(COLLECTION)


def _save_homes(homes: list[dict]) -> None:
    write_collection(COLLECTION, homes)


def _find_home_index(homes: list[dict], home_id: str) -> int | None:
    for idx, home in enumerate(homes):
        if home.get("id") == home_id:
            return idx
    return None


def _find_home_containing_room(homes: list[dict], room_id: str) -> tuple[int, int] | None:
    for h_idx, home in enumerate(homes):
        for r_idx, room in enumerate(home.get("rooms") or []):
            if room.get("id") == room_id:
                return h_idx, r_idx
    return None


def list_rooms(home_id: str) -> list[dict]:
    for home in _load_homes():
        if home.get("id") == home_id:
            return home.get("rooms") or []
    return []


def get_room(room_id: str) -> dict | None:
    homes = _load_homes()
    location = _find_home_containing_room(homes, room_id)
    if location is None:
        return None
    h_idx, r_idx = location
    return homes[h_idx]["rooms"][r_idx]


def add_room(home_id: str, data: RoomCreate) -> dict | None:
    homes = _load_homes()
    h_idx = _find_home_index(homes, home_id)
    if h_idx is None:
        return None
    now = now_iso()
    order = len(homes[h_idx].get("rooms") or [])
    room = Room(
        id=new_id("room"),
        home_id=home_id,
        order=order,
        furniture=[],
        appliances=[],
        created_at=now,
        updated_at=now,
        **data.model_dump(),
    )
    record = room.model_dump()
    homes[h_idx].setdefault("rooms", []).append(record)
    homes[h_idx]["updated_at"] = now
    HomeProfile(**homes[h_idx])
    _save_homes(homes)
    return record


def update_room(room_id: str, data: RoomUpdate) -> dict | None:
    homes = _load_homes()
    location = _find_home_containing_room(homes, room_id)
    if location is None:
        return None
    h_idx, r_idx = location
    room = homes[h_idx]["rooms"][r_idx]
    room.update(data.model_dump(exclude_unset=True))
    room["updated_at"] = now_iso()
    validated = Room(**room).model_dump()
    homes[h_idx]["rooms"][r_idx] = validated
    homes[h_idx]["updated_at"] = now_iso()
    _save_homes(homes)
    return validated


def delete_room(room_id: str) -> bool:
    homes = _load_homes()
    location = _find_home_containing_room(homes, room_id)
    if location is None:
        return False
    h_idx, r_idx = location
    del homes[h_idx]["rooms"][r_idx]
    homes[h_idx]["updated_at"] = now_iso()
    _save_homes(homes)
    return True


def duplicate_room(room_id: str) -> dict | None:
    homes = _load_homes()
    location = _find_home_containing_room(homes, room_id)
    if location is None:
        return None
    h_idx, r_idx = location
    original = homes[h_idx]["rooms"][r_idx]
    now = now_iso()
    copy = dict(original)
    copy["id"] = new_id("room")
    copy["name"] = f"{original.get('name', 'Room')} (Copy)"
    copy["order"] = len(homes[h_idx]["rooms"])
    copy["created_at"] = now
    copy["updated_at"] = now
    for furniture in copy.get("furniture") or []:
        furniture["id"] = new_id("furn")
        furniture["room_id"] = copy["id"]
    for appliance in copy.get("appliances") or []:
        appliance["id"] = new_id("appl")
        appliance["room_id"] = copy["id"]
    validated = Room(**copy).model_dump()
    homes[h_idx]["rooms"].append(validated)
    homes[h_idx]["updated_at"] = now
    _save_homes(homes)
    return validated


def reorder_rooms(home_id: str, room_ids: list[str]) -> list[dict] | None:
    homes = _load_homes()
    h_idx = _find_home_index(homes, home_id)
    if h_idx is None:
        return None
    rooms_by_id = {r["id"]: r for r in homes[h_idx].get("rooms") or []}
    reordered = []
    for order, rid in enumerate(room_ids):
        room = rooms_by_id.get(rid)
        if room:
            room["order"] = order
            reordered.append(room)
    remaining = [r for r in (homes[h_idx].get("rooms") or []) if r["id"] not in room_ids]
    reordered.extend(remaining)
    homes[h_idx]["rooms"] = reordered
    homes[h_idx]["updated_at"] = now_iso()
    _save_homes(homes)
    return reordered


def add_furniture(room_id: str, data: FurnitureCreate) -> dict | None:
    homes = _load_homes()
    location = _find_home_containing_room(homes, room_id)
    if location is None:
        return None
    h_idx, r_idx = location
    now = now_iso()
    item = FurnitureItem(id=new_id("furn"), room_id=room_id, created_at=now, updated_at=now, **data.model_dump())
    record = item.model_dump()
    homes[h_idx]["rooms"][r_idx].setdefault("furniture", []).append(record)
    homes[h_idx]["updated_at"] = now
    _save_homes(homes)
    return record


def update_furniture(room_id: str, item_id: str, data: FurnitureCreate) -> dict | None:
    homes = _load_homes()
    location = _find_home_containing_room(homes, room_id)
    if location is None:
        return None
    h_idx, r_idx = location
    furniture = homes[h_idx]["rooms"][r_idx].get("furniture") or []
    for idx, item in enumerate(furniture):
        if item.get("id") == item_id:
            updated = FurnitureItem(
                id=item_id, room_id=room_id, created_at=item.get("created_at"), updated_at=now_iso(),
                **data.model_dump(),
            ).model_dump()
            furniture[idx] = updated
            homes[h_idx]["updated_at"] = now_iso()
            _save_homes(homes)
            return updated
    return None


def delete_furniture(room_id: str, item_id: str) -> bool:
    homes = _load_homes()
    location = _find_home_containing_room(homes, room_id)
    if location is None:
        return False
    h_idx, r_idx = location
    furniture = homes[h_idx]["rooms"][r_idx].get("furniture") or []
    filtered = [f for f in furniture if f.get("id") != item_id]
    if len(filtered) == len(furniture):
        return False
    homes[h_idx]["rooms"][r_idx]["furniture"] = filtered
    homes[h_idx]["updated_at"] = now_iso()
    _save_homes(homes)
    return True


def add_appliance(room_id: str, data: ApplianceCreate) -> dict | None:
    homes = _load_homes()
    location = _find_home_containing_room(homes, room_id)
    if location is None:
        return None
    h_idx, r_idx = location
    now = now_iso()
    item = Appliance(id=new_id("appl"), room_id=room_id, created_at=now, updated_at=now, **data.model_dump())
    record = item.model_dump()
    homes[h_idx]["rooms"][r_idx].setdefault("appliances", []).append(record)
    homes[h_idx]["updated_at"] = now
    _save_homes(homes)
    return record


def update_appliance(room_id: str, item_id: str, data: ApplianceCreate) -> dict | None:
    homes = _load_homes()
    location = _find_home_containing_room(homes, room_id)
    if location is None:
        return None
    h_idx, r_idx = location
    appliances = homes[h_idx]["rooms"][r_idx].get("appliances") or []
    for idx, item in enumerate(appliances):
        if item.get("id") == item_id:
            updated = Appliance(
                id=item_id, room_id=room_id, created_at=item.get("created_at"), updated_at=now_iso(),
                **data.model_dump(),
            ).model_dump()
            appliances[idx] = updated
            homes[h_idx]["updated_at"] = now_iso()
            _save_homes(homes)
            return updated
    return None


def delete_appliance(room_id: str, item_id: str) -> bool:
    homes = _load_homes()
    location = _find_home_containing_room(homes, room_id)
    if location is None:
        return False
    h_idx, r_idx = location
    appliances = homes[h_idx]["rooms"][r_idx].get("appliances") or []
    filtered = [a for a in appliances if a.get("id") != item_id]
    if len(filtered) == len(appliances):
        return False
    homes[h_idx]["rooms"][r_idx]["appliances"] = filtered
    homes[h_idx]["updated_at"] = now_iso()
    _save_homes(homes)
    return True
