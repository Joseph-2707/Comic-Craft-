from app.schemas import StoryPanel,ComicLayout
def build_comic_layout(story_panels,image_paths,pdf_path=None):
    if len(story_panels)!=5 or len(image_paths)!=5: raise ValueError("Comic layout requires exactly five panels and five images.")
    panels=[]
    for p,img in zip(story_panels,image_paths):
        x=p.model_copy(); x.image_prompt=f"{img}||{p.image_prompt}"; panels.append(x)
    return ComicLayout(panels=panels,pdf_path=pdf_path)
def extract_image_path(v): return v.split("||",1) if "||" in v else (v,v)
