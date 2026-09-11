from pathlib import Path

from dotenv import load_dotenv
from fastapi import FastAPI, Form, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from app.services.ai_generator import prepare_post

BASE_DIR = Path(__file__).resolve().parent
load_dotenv(BASE_DIR.parent / ".env")

templates = Jinja2Templates(directory=str(BASE_DIR / "templates"))
app = FastAPI(title="علوم الفنجال")
app.mount("/static", StaticFiles(directory=str(BASE_DIR / "static")), name="static")


@app.get("/", response_class=HTMLResponse)
async def home(request: Request) -> HTMLResponse:
    return templates.TemplateResponse(
        request=request,
        name="index.html",
        context={"result": None, "image": None, "error": None, "form": {}},
    )


@app.post("/prepare", response_class=HTMLResponse)
async def prepare(
    request: Request,
    idea: str = Form(""),
    mood: str = Form("زوارة الخميس"),
    cafe_name: str = Form(""),
    tone: str = Form("حماسي"),
    image_data: str = Form(""),
) -> HTMLResponse:
    form = {"idea": idea.strip(), "mood": mood, "cafe_name": cafe_name.strip(), "tone": tone}
    result = None
    error = None
    if not form["idea"]:
        error = "اكتب فكرة البوست أولاً."
    else:
        try:
            result = prepare_post(**form)
        except Exception:
            error = "تعذر تعديل النص حالياً. جرّب مرة ثانية."
    return templates.TemplateResponse(
        request=request,
        name="index.html",
        context={"result": result, "image": image_data or None, "error": error, "form": form},
    )


