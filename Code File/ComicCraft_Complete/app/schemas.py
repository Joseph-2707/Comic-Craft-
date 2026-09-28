from pydantic import BaseModel, Field, field_validator
def clean(v:str)->str:
    v=v.strip()
    if not v: raise ValueError("Value cannot be empty.")
    return v
class PromptRequest(BaseModel):
    story_prompt:str=Field(min_length=3,max_length=2000); character_name:str=Field(default="Alex",min_length=1,max_length=80); setting:str=Field(default="a colorful city",min_length=1,max_length=120); tone:str=Field(default="adventurous",min_length=1,max_length=60); art_style:str=Field(default="comic book",min_length=1,max_length=80)
    @field_validator("story_prompt","character_name","setting","tone","art_style")
    @classmethod
    def strip(cls,v): return clean(v)
class PanelOutline(BaseModel):
    panel_number:int=Field(ge=1,le=5); title:str=Field(min_length=1,max_length=120); scene_description:str=Field(min_length=1,max_length=1000); image_prompt:str=Field(min_length=1,max_length=1500)
class StoryPanel(BaseModel):
    panel_number:int=Field(ge=1,le=5); title:str; scene_description:str; image_prompt:str; caption:str; narration:str; dialogue:str=""
class ComicLayout(BaseModel):
    panels:list[StoryPanel]=Field(min_length=5,max_length=5); pdf_path:str|None=None
class ImageTestRequest(BaseModel):
    prompt:str=Field(min_length=3,max_length=2000)
    @field_validator("prompt")
    @classmethod
    def strip(cls,v): return clean(v)
