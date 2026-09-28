import json,re
from pydantic import BaseModel,ValidationError
from app.config import Settings
from app.schemas import PanelOutline,StoryPanel
class OutlineResponse(BaseModel): panels:list[PanelOutline]
class StoryResponse(BaseModel): panels:list[StoryPanel]
class GeminiService:
    def __init__(self,s):
        self.s=s
        self.client=None
        if s.gemini_api_key and not s.demo_mode:
            try:
                from google import genai
                self.client=genai.Client(api_key=s.gemini_api_key)
            except ImportError as e:
                raise RuntimeError("google-genai is required when DEMO_MODE=false. Run: pip install -r requirements.txt") from e
    @property
    def available(self): return self.client is not None and not self.s.demo_mode
    def generate_outline(self,story_prompt,character_name,setting,tone,art_style):
        if not self.available: return self._demo_outline(story_prompt,character_name,setting,tone,art_style)
        p=f"""Create a cohesive five-panel comic outline. User story: {story_prompt}. Main character: {character_name}. Setting: {setting}. Tone: {tone}. Art style: {art_style}. Return exactly 5 panels, same character continuity, clear beginning/development/climax/ending. Each panel needs panel_number, title, scene_description, image_prompt. No markdown fences."""
        from google.genai import types
        r=self.client.models.generate_content(model=self.s.gemini_outline_model,contents=p,config=types.GenerateContentConfig(response_mime_type="application/json",response_schema=OutlineResponse,temperature=.8))
        return self._normalize_outline(self._parse(r,OutlineResponse).panels)
    def generate_story(self,outline,character_name,tone):
        if not self.available: return self._demo_story(outline,character_name,tone)
        p=f"""Expand this five-panel outline into polished comic content. Main character: {character_name}. Tone: {tone}. Outline: {json.dumps([x.model_dump() for x in outline])}. Return exactly five panels in order. Preserve panel number/title/scene_description/image_prompt. Add concise caption, narration and useful natural dialogue. No markdown fences."""
        from google.genai import types
        r=self.client.models.generate_content(model=self.s.gemini_story_model,contents=p,config=types.GenerateContentConfig(response_mime_type="application/json",response_schema=StoryResponse,temperature=.9))
        return self._normalize_story(self._parse(r,StoryResponse).panels,outline)
    def _parse(self,r,cls):
        if getattr(r,"parsed",None) is not None: return cls.model_validate(r.parsed)
        raw=getattr(r,"text",None)
        if not raw: raise RuntimeError("Gemini returned an empty response.")
        raw=re.sub(r"^```(?:json)?\s*","",raw.strip(),flags=re.I); raw=re.sub(r"\s*```$","",raw)
        try: return cls.model_validate_json(raw)
        except ValidationError as e: raise RuntimeError(f"Gemini returned invalid structured data: {e}") from e
    @staticmethod
    def _normalize_outline(p):
        if len(p)!=5: raise RuntimeError(f"Expected exactly 5 outline panels, received {len(p)}")
        p=sorted(p,key=lambda x:x.panel_number)
        if [x.panel_number for x in p]!=[1,2,3,4,5]: raise RuntimeError("Panel numbers must be 1 through 5")
        return p
    @staticmethod
    def _normalize_story(p,o):
        if len(p)!=5: raise RuntimeError("Expected exactly 5 story panels")
        d={x.panel_number:x for x in p}; out=[]
        for src in o:
            x=d.get(src.panel_number)
            if not x: raise RuntimeError("Story response is missing a panel")
            x.title=src.title; x.scene_description=src.scene_description; x.image_prompt=src.image_prompt; out.append(x)
        return out
    @staticmethod
    def _demo_outline(story_prompt,character_name,setting,tone,art_style):
        beats=[("The Beginning",f"{character_name} discovers the first clue connected to: {story_prompt}."),("A New Path",f"{character_name} follows the clue deeper into {setting}."),("The Turning Point",f"A surprising obstacle tests {character_name} and changes the plan."),("The Big Moment",f"{character_name} faces the central challenge with courage and creativity."),("A New Chapter",f"The adventure ends with a meaningful discovery and a hint of what comes next.")]
        return [PanelOutline(panel_number=i,title=t,scene_description=d,image_prompt=f"{character_name}, consistent character design, {setting}, {tone} mood, {art_style} style, cinematic comic panel, panel {i}: {d}") for i,(t,d) in enumerate(beats,1)]
    @staticmethod
    def _demo_story(outline,character_name,tone):
        caps=["A small clue can begin a huge adventure.","The world seems different when you follow a mystery.","Every adventure has a moment when the plan changes.","Courage turns an obstacle into an opportunity.","The final page is only the beginning of another story."]
        ds=[f"{character_name}: I have to find out where this leads.",f"{character_name}: There has to be an answer somewhere ahead.",f"{character_name}: This wasn't part of the plan.",f"{character_name}: I can handle this. Let's keep moving!",f"{character_name}: I wonder what the next chapter will bring."]
        return [StoryPanel(**p.model_dump(),caption=caps[i-1],narration=f"In this {tone} moment, {character_name} moves the story forward, noticing details that will matter later.",dialogue=ds[i-1]) for i,p in enumerate(outline,1)]
