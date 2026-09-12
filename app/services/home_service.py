from app.models.home import HomeProfile, HomeProfileCreate, HomeProfileUpdate
from app.services.json_store import read_collection, write_collection
from app.utils.dates import now_iso
from app.utils.ids import new_id

COLLECTION = "homes"


def list_homes() -> list[dict]:
    return read_collection(COLLECTION)


def get_home(home_id: str) -> dict | None:
    for home in read_collection(COLLECTION):
        if home.get("id") == home_id:
            return home
    return None


def get_current_home() -> dict | None:
    homes = read_collection(COLLECTION)
    return homes[0] if homes else None


def create_home(data: HomeProfileCreate) -> dict:
    homes = read_collection(COLLECTION)
    now = now_iso()
    profile = HomeProfile(
        id=new_id("home"),
        rooms=[],
        created_at=now,
        updated_at=now,
        **data.model_dump(),
    )
    record = profile.model_dump()
    homes.append(record)
    write_collection(COLLECTION, homes)
    return record


def update_home(home_id: str, data: HomeProfileUpdate) -> dict | None:
    homes = read_collection(COLLECTION)
    for idx, home in enumerate(homes):
        if home.get("id") == home_id:
            updates = data.model_dump(exclude_unset=True)
            home.update(updates)
            home["updated_at"] = now_iso()
            validated = HomeProfile(**home).model_dump()
            homes[idx] = validated
            write_collection(COLLECTION, homes)
            return validated
    return None


def delete_home(home_id: str) -> bool:
    homes = read_collection(COLLECTION)
    filtered = [h for h in homes if h.get("id") != home_id]
    if len(filtered) == len(homes):
        return False
    write_collection(COLLECTION, filtered)
    return True
