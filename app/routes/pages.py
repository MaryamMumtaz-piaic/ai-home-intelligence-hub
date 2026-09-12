from fastapi import APIRouter, Request

from app.templates_config import templates

router = APIRouter()


@router.get("/")
def index(request: Request):
    return templates.TemplateResponse(request, "index.html", {"page": "home"})


@router.get("/home")
def home_page(request: Request):
    return templates.TemplateResponse(request, "home.html", {"page": "my-home"})


@router.get("/rooms")
def rooms_page(request: Request):
    return templates.TemplateResponse(request, "rooms.html", {"page": "rooms"})


@router.get("/rooms/{room_id}")
def room_detail_page(request: Request, room_id: str):
    return templates.TemplateResponse(request, "room-detail.html", {"page": "rooms", "room_id": room_id})


@router.get("/insights")
def insights_page(request: Request):
    return templates.TemplateResponse(request, "insights.html", {"page": "insights"})


@router.get("/recommendations")
def recommendations_page(request: Request):
    return templates.TemplateResponse(request, "recommendations.html", {"page": "recommendations"})


@router.get("/tasks")
def tasks_page(request: Request):
    return templates.TemplateResponse(request, "tasks.html", {"page": "tasks"})


@router.get("/settings")
def settings_page(request: Request):
    return templates.TemplateResponse(request, "settings.html", {"page": "settings"})


@router.get("/about")
def about_page(request: Request):
    return templates.TemplateResponse(request, "about.html", {"page": "about"})


@router.get("/faq")
def faq_page(request: Request):
    return templates.TemplateResponse(request, "faq.html", {"page": "faq"})


@router.get("/contact")
def contact_page(request: Request):
    return templates.TemplateResponse(request, "contact.html", {"page": "contact"})
