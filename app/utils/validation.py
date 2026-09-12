from fastapi import HTTPException


def not_found(entity: str, entity_id: str) -> HTTPException:
    return HTTPException(status_code=404, detail=f"{entity} '{entity_id}' was not found.")


def bad_request(message: str) -> HTTPException:
    return HTTPException(status_code=400, detail=message)
