import hashlib
from pathlib import Path
from PIL import Image,ImageDraw,ImageFont
class ImageGenerator:
    def __init__(self,s): self.s=s
    def generate_image(self,prompt,panel_number):
        out=self.s.panel_path/f"panel_{panel_number}_{hashlib.sha256(prompt.encode()).hexdigest()[:10]}.png"
        if out.exists(): return out.as_posix()
        if self.s.demo_mode or not self.s.hf_token: self._placeholder(prompt,panel_number,out); return out.as_posix()
        try:
            from huggingface_hub import InferenceClient
            c=InferenceClient(provider=self.s.hf_provider,api_key=self.s.hf_token)
            img=c.text_to_image(prompt=prompt,model=self.s.hf_image_model,width=self.s.image_width,height=self.s.image_height,num_inference_steps=self.s.image_steps)
            img.save(out); return out.as_posix()
        except Exception:
            if not self.s.allow_image_fallback: raise
            self._placeholder(prompt,panel_number,out); return out.as_posix()
    def _placeholder(self,prompt,n,out):
        w,h=self.s.image_width,self.s.image_height; im=Image.new("RGB",(w,h),"white"); d=ImageDraw.Draw(im); m=35; d.rectangle((m,m,w-m,h-m),outline="black",width=8); d.ellipse((w*.28,h*.2,w*.72,h*.64),outline="black",width=7); d.line((w*.5,h*.64,w*.42,h*.82),fill="black",width=7); d.line((w*.5,h*.64,w*.58,h*.82),fill="black",width=7)
        try: f=ImageFont.truetype("arial.ttf",28); sf=ImageFont.truetype("arial.ttf",20)
        except OSError: f=sf=ImageFont.load_default()
        d.text((55,55),f"COMICCRAFT • PANEL {n}",font=f,fill="black"); d.text((55,h-100)," ".join(prompt.split())[:120],font=sf,fill="black"); im.save(out)
