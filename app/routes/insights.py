from fastapi import APIRouter, Response

from app.models.maintenance import MaintenanceItem, MaintenanceItemCreate
from app.services import maintenance_service
from app.services.json_store import load_reference_data
from app.utils.validation import not_found

router = APIRouter(prefix="/api", tags=["insights"])


@router.get("/reference/room-types")
def room_types():
    return load_reference_data("room_types.json")


@router.get("/reference/furniture-catalog")
def furniture_catalog():
    return load_reference_data("furniture_catalog.json")


@router.get("/reference/appliance-categories")
def appliance_categories():
    return load_reference_data("appliance_categories.json")


@router.get("/reference/maintenance-categories")
def maintenance_categories():
    return load_reference_data("maintenance_categories.json")


class MaintenanceCreateBody(MaintenanceItemCreate):
    home_id: str


@router.get("/maintenance", response_model=list[MaintenanceItem])
def list_maintenance(home_id: str):
    return maintenance_service.list_items(home_id)


@router.post("/maintenance", response_model=MaintenanceItem, status_code=201)
def create_maintenance(data: MaintenanceCreateBody):
    home_id = data.home_id
    item_data = MaintenanceItemCreate(**data.model_dump(exclude={"home_id"}))
    return maintenance_service.create_item(home_id, item_data)


@router.put("/maintenance/{item_id}", response_model=MaintenanceItem)
def update_maintenance(item_id: str, data: MaintenanceItemCreate):
    item = maintenance_service.update_item(item_id, data)
    if item is None:
        raise not_found("Maintenance item", item_id)
    return item


@router.delete("/maintenance/{item_id}", status_code=204)
def delete_maintenance(item_id: str):
    if not maintenance_service.delete_item(item_id):
        raise not_found("Maintenance item", item_id)
    return Response(status_code=204)
