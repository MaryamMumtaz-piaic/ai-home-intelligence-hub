from pydantic import BaseModel
from fastapi import APIRouter, Response

from app.models.appliance import Appliance, ApplianceCreate
from app.models.furniture import FurnitureItem, FurnitureCreate
from app.models.room import Room, RoomCreate, RoomUpdate
from app.services import room_service
from app.utils.validation import not_found

router = APIRouter(prefix="/api/rooms", tags=["rooms"])


class RoomCreateBody(RoomCreate):
    home_id: str


class ReorderBody(BaseModel):
    home_id: str
    room_ids: list[str]


@router.get("", response_model=list[Room])
def list_rooms(home_id: str):
    return room_service.list_rooms(home_id)


@router.post("", response_model=Room, status_code=201)
def add_room(data: RoomCreateBody):
    home_id = data.home_id
    room_data = RoomCreate(**data.model_dump(exclude={"home_id"}))
    room = room_service.add_room(home_id, room_data)
    if room is None:
        raise not_found("Home", home_id)
    return room


@router.get("/{room_id}", response_model=Room)
def get_room(room_id: str):
    room = room_service.get_room(room_id)
    if room is None:
        raise not_found("Room", room_id)
    return room


@router.put("/{room_id}", response_model=Room)
def update_room(room_id: str, data: RoomUpdate):
    room = room_service.update_room(room_id, data)
    if room is None:
        raise not_found("Room", room_id)
    return room


@router.delete("/{room_id}", status_code=204)
def delete_room(room_id: str):
    if not room_service.delete_room(room_id):
        raise not_found("Room", room_id)
    return Response(status_code=204)


@router.post("/{room_id}/duplicate", response_model=Room)
def duplicate_room(room_id: str):
    room = room_service.duplicate_room(room_id)
    if room is None:
        raise not_found("Room", room_id)
    return room


@router.post("/reorder", response_model=list[Room])
def reorder_rooms(data: ReorderBody):
    rooms = room_service.reorder_rooms(data.home_id, data.room_ids)
    if rooms is None:
        raise not_found("Home", data.home_id)
    return rooms


@router.post("/{room_id}/furniture", response_model=FurnitureItem, status_code=201)
def add_furniture(room_id: str, data: FurnitureCreate):
    item = room_service.add_furniture(room_id, data)
    if item is None:
        raise not_found("Room", room_id)
    return item


@router.put("/{room_id}/furniture/{item_id}", response_model=FurnitureItem)
def update_furniture(room_id: str, item_id: str, data: FurnitureCreate):
    item = room_service.update_furniture(room_id, item_id, data)
    if item is None:
        raise not_found("Furniture item", item_id)
    return item


@router.delete("/{room_id}/furniture/{item_id}", status_code=204)
def delete_furniture(room_id: str, item_id: str):
    if not room_service.delete_furniture(room_id, item_id):
        raise not_found("Furniture item", item_id)
    return Response(status_code=204)


@router.post("/{room_id}/appliances", response_model=Appliance, status_code=201)
def add_appliance(room_id: str, data: ApplianceCreate):
    item = room_service.add_appliance(room_id, data)
    if item is None:
        raise not_found("Room", room_id)
    return item


@router.put("/{room_id}/appliances/{item_id}", response_model=Appliance)
def update_appliance(room_id: str, item_id: str, data: ApplianceCreate):
    item = room_service.update_appliance(room_id, item_id, data)
    if item is None:
        raise not_found("Appliance", item_id)
    return item


@router.delete("/{room_id}/appliances/{item_id}", status_code=204)
def delete_appliance(room_id: str, item_id: str):
    if not room_service.delete_appliance(room_id, item_id):
        raise not_found("Appliance", item_id)
    return Response(status_code=204)
