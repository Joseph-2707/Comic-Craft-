from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from app.config import get_settings
from app.routes import router
s=get_settings(); s.ensure_directories(); app=FastAPI(title=s.app_name,description="AI-powered five-panel comic story creator.",version="1.0.0"); app.mount("/static",StaticFiles(directory="static"),name="static"); app.include_router(router)
@app.get("/health")
async def health(): return {"status":"ok","demo_mode":s.demo_mode,"app":s.app_name}
