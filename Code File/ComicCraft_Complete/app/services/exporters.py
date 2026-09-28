from datetime import datetime,timezone
from pathlib import Path
from fpdf import FPDF
from app.services.layout_builder import extract_image_path
class ComicPDF(FPDF):
    def footer(self): self.set_y(-12); self.set_font("Helvetica",size=8); self.cell(0,8,f"ComicCraft - Page {self.page_no()}",align="C")
def save_pdf(layout,s):
    s.ensure_directories(); out=s.export_path/f"comic_{datetime.now(timezone.utc).strftime('%Y%m%d_%H%M%S_%f')}.pdf"; pdf=ComicPDF(); pdf.set_auto_page_break(auto=True,margin=15)
    for p in layout.panels:
        img,orig=extract_image_path(p.image_prompt); pdf.add_page(); pdf.set_font("Helvetica","B",20); pdf.cell(0,12,f"Panel {p.panel_number}: {p.title}",new_x="LMARGIN",new_y="NEXT")
        if Path(img).exists(): pdf.image(img,x=15,y=30,w=180,h=105,keep_aspect_ratio=True)
        pdf.set_y(143); pdf.set_font("Helvetica","I",10); pdf.multi_cell(0,6,p.scene_description); pdf.ln(3); pdf.set_font("Helvetica","B",11); pdf.multi_cell(0,6,f"Caption: {p.caption}"); pdf.ln(2); pdf.set_font("Helvetica",size=11); pdf.multi_cell(0,6,f"Narration: {p.narration}")
        if p.dialogue: pdf.ln(2); pdf.set_font("Helvetica","B",11); pdf.multi_cell(0,6,f"Dialogue: {p.dialogue}")
        pdf.ln(3); pdf.set_font("Helvetica",size=8); pdf.set_text_color(80,80,80); pdf.multi_cell(0,5,f"Image prompt: {orig}"); pdf.set_text_color(0,0,0)
    pdf.output(str(out)); return out.as_posix()
