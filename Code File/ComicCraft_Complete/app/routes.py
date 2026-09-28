from pathlib import Path
from fastapi import APIRouter,Form,HTTPException,Request
from fastapi.responses import FileResponse,HTMLResponse
from fastapi.templating import Jinja2Templates
from app.config import get_settings
from app.schemas import ImageTestRequest,PromptRequest
from app.services.comic_service import ComicService
router=APIRouter(); templates=Jinja2Templates(directory="templates")
def service(): return ComicService(get_settings())
@router.get("/",response_class=HTMLResponse)
async def home(request:Request): return templates.TemplateResponse(request=request,name="index.html",context={"title":"ComicCraft"})
@router.post("/generate",response_class=HTMLResponse)
async def generate(request:Request,story_prompt:str=Form(...),character_name:str=Form(...),setting:str=Form(...),tone:str=Form(...),art_style:str=Form(...)):
    try:
        layout=service().generate(PromptRequest(story_prompt=story_prompt,character_name=character_name,setting=setting,tone=tone,art_style=art_style)); return templates.TemplateResponse(request=request,name="comic_preview.html",context={"title":"Comic Preview","layout":layout})
    except Exception as e: return templates.TemplateResponse(request=request,name="index.html",context={"title":"ComicCraft","error":f"Comic generation failed: {e}"},status_code=500)
@router.post("/generate-comic/json")
async def generate_json(payload:PromptRequest):
    try:
        l=service().generate(payload); return {"success":True,"panels":[p.model_dump() for p in l.panels],"pdf_path":l.pdf_path}
    except Exception as e: raise HTTPException(status_code=500,detail=str(e)) from e
@router.post("/test-image")
async def test_image(payload:ImageTestRequest):
    try: return {"success":True,"image_path":service().images.generate_image(payload.prompt,0)}
    except Exception as e: raise HTTPException(status_code=500,detail=str(e)) from e
@router.get("/download/{filename}")
async def download(filename:str):
    s=get_settings(); name=Path(filename).name
    if name!=filename or not filename.endswith(".pdf"): raise HTTPException(400,"Invalid filename")
    p=s.export_path/name
    if not p.exists(): raise HTTPException(404,"PDF not found")
    return FileResponse(p,media_type="application/pdf",filename=name)
@router.get("/export-success",response_class=HTMLResponse)
async def export_success(request:Request,filename:str|None=None): return templates.TemplateResponse(request=request,name="export_success.html",context={"title":"Export Complete","filename":filename})
