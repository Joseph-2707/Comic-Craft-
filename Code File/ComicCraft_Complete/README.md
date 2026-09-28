# ComicCraft — AI Comic Story Creator

A complete FastAPI + Jinja2 application implementing the documented five-panel ComicCraft pipeline: Gemini outline, Gemini story expansion, Hugging Face image generation, layout binding, and FPDF2 PDF export. DEMO_MODE runs the full pipeline without API keys.

## Structure
```text
ComicCraft_Complete/
├── app/{__init__.py,main.py,config.py,schemas.py,routes.py}
├── app/services/{__init__.py,comic_service.py,gemini_service.py,image_generator.py,layout_builder.py,exporters.py}
├── templates/{base.html,index.html,comic_preview.html,export_success.html}
├── static/css/style.css
├── static/panels/.gitkeep
├── exports/.gitkeep
├── tests/test_app.py
├── .env.example
├── .gitignore
├── requirements.txt
└── README.md
```

## Windows / VS Code
```powershell
py -3.11 -m venv .venv
.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
pip install -r requirements.txt
copy .env.example .env
uvicorn app.main:app --reload
```
Open http://127.0.0.1:8000 and http://127.0.0.1:8000/docs.

### Demo mode
`.env` defaults to `DEMO_MODE=true`; no API keys are required. The story pipeline, images, frontend, and PDF export all work locally using deterministic demo content/placeholders.

### Real AI mode
Set:
```env
DEMO_MODE=false
GEMINI_API_KEY=your_key
HF_TOKEN=your_huggingface_token
GEMINI_OUTLINE_MODEL=gemini-2.5-flash
GEMINI_STORY_MODEL=gemini-2.5-pro
HF_IMAGE_MODEL=black-forest-labs/FLUX.1-schnell
HF_PROVIDER=auto
```
Model names are configurable so they can be changed if availability differs for your account/provider.

## Tests
```powershell
pytest -q
```
Tests cover homepage, health, five-panel JSON generation, PDF creation, and image generation.

## API
`GET /health`

`POST /generate-comic/json` with:
```json
{"story_prompt":"A brave fox discovers a hidden library.","character_name":"Finn","setting":"enchanted forest","tone":"adventurous","art_style":"comic book"}
```

`POST /test-image` with `{"prompt":"A fox in a comic forest"}`.

## Workflow
```text
form -> /generate -> outline -> story -> 5 images -> layout -> PDF -> preview/download
```

The implementation keeps exactly five panels as specified in the project documentation and separates AI, image, layout, export, routing, and UI responsibilities.
