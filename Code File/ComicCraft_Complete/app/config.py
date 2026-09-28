from functools import lru_cache
from pathlib import Path
from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    app_name: str = "ComicCraft"
    demo_mode: bool = True
    allow_image_fallback: bool = True
    gemini_api_key: str | None = None
    gemini_outline_model: str = "gemini-2.5-flash"
    gemini_story_model: str = "gemini-2.5-pro"
    hf_token: str | None = None
    hf_image_model: str = "black-forest-labs/FLUX.1-schnell"
    hf_provider: str = "auto"
    max_panels: int = 5
    image_width: int = 768
    image_height: int = 768
    image_steps: int = 4
    panel_dir: str = "static/panels"
    export_dir: str = "exports"
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8", case_sensitive=False, extra="ignore")
    @property
    def panel_path(self) -> Path: return Path(self.panel_dir)
    @property
    def export_path(self) -> Path: return Path(self.export_dir)
    def ensure_directories(self): self.panel_path.mkdir(parents=True, exist_ok=True); self.export_path.mkdir(parents=True, exist_ok=True)

@lru_cache
def get_settings():
    s=Settings(); s.ensure_directories(); return s
