from app.services.gemini_service import GeminiService
from app.services.image_generator import ImageGenerator
from app.services.layout_builder import build_comic_layout
from app.services.exporters import save_pdf
class ComicService:
    def __init__(self,s): self.s=s; self.gemini=GeminiService(s); self.images=ImageGenerator(s)
    def generate(self,r):
        outline=self.gemini.generate_outline(r.story_prompt,r.character_name,r.setting,r.tone,r.art_style); story=self.gemini.generate_story(outline,r.character_name,r.tone); imgs=[self.images.generate_image(p.image_prompt,p.panel_number) for p in story]; layout=build_comic_layout(story,imgs); layout.pdf_path=save_pdf(layout,self.s); return layout
