from fastapi import APIRouter

from app.models.feedback import ContactSubmission, Feedback
from app.services.json_store import append_reference_log
from app.utils.dates import now_iso
from app.utils.ids import new_id

router = APIRouter(prefix="/api", tags=["feedback"])


@router.post("/feedback")
def submit_feedback(data: Feedback):
    record = data.model_dump()
    record["id"] = new_id("fb")
    record["created_at"] = now_iso()
    append_reference_log("feedback.json", record)
    return {"message": "Feedback submitted."}


@router.post("/contact")
def submit_contact(data: ContactSubmission):
    record = data.model_dump()
    record["id"] = new_id("contact")
    record["created_at"] = now_iso()
    append_reference_log("contacts.json", record)
    return {"message": "Message received."}
