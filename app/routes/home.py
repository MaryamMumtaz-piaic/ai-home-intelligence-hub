from fastapi import APIRouter, Response

from app.models.home import HomeProfile, HomeProfileCreate, HomeProfileUpdate
from app.services import home_service
from app.utils.validation import not_found

router = APIRouter(prefix="/api/home", tags=["home"])


@router.get("", response_model=HomeProfile | None)
def get_home(home_id: str | None = None):
    if home_id:
        home = home_service.get_home(home_id)
    else:
        home = home_service.get_current_home()
    return home


@router.post("", response_model=HomeProfile, status_code=201)
def create_home(data: HomeProfileCreate):
    return home_service.create_home(data)


@router.put("/{home_id}", response_model=HomeProfile)
def update_home(home_id: str, data: HomeProfileUpdate):
    updated = home_service.update_home(home_id, data)
    if updated is None:
        raise not_found("Home", home_id)
    return updated


@router.delete("/{home_id}", status_code=204)
def delete_home(home_id: str):
    if not home_service.delete_home(home_id):
        raise not_found("Home", home_id)
    return Response(status_code=204)
