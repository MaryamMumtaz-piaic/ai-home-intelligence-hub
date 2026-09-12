import logging

from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from fastapi.staticfiles import StaticFiles

from app.routes import ai, feedback, home, insights, pages, recommendations, rooms, tasks
from app.templates_config import templates

logging.basicConfig(level=logging.INFO)

app = FastAPI(title="AI Home Intelligence Hub", description="Understand your home. Improve every space.")

app.mount("/static", StaticFiles(directory="static"), name="static")

app.include_router(pages.router)
app.include_router(home.router)
app.include_router(rooms.router)
app.include_router(insights.router)
app.include_router(ai.router)
app.include_router(recommendations.router)
app.include_router(tasks.router)
app.include_router(feedback.router)


@app.exception_handler(404)
async def not_found_handler(request: Request, exc):
    if request.url.path.startswith("/api"):
        return JSONResponse(status_code=404, content={"detail": "Not found."})
    return templates.TemplateResponse(request, "404.html", {"page": "404"}, status_code=404)
