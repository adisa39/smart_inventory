from fastapi import APIRouter, Request, UploadFile, File
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.templating import Jinja2Templates
from app.services.detection import run_detection
from app.services.log_manager import save_detections, get_summary

templates = Jinja2Templates(directory="app/templates")
router = APIRouter()

@router.get("/", response_class=HTMLResponse)
async def index(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@router.post("/detect")
async def detect(file: UploadFile = File(...)):
    try:
        detections = await run_detection(file)
        save_detections(detections)
        return JSONResponse({"detections": detections, "summary": get_summary()})
    except Exception as e:
        return JSONResponse({"error": str(e)}, status_code=500)
