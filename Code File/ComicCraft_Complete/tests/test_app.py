from pathlib import Path
from fastapi.testclient import TestClient
from app.main import app
client=TestClient(app)
def test_homepage():
 r=client.get('/'); assert r.status_code==200; assert 'ComicCraft' in r.text
def test_health():
 r=client.get('/health'); assert r.status_code==200; assert r.json()['status']=='ok'
def test_json_generation():
 r=client.post('/generate-comic/json',json={'story_prompt':'A fox finds a glowing book.','character_name':'Finn','setting':'forest','tone':'adventurous','art_style':'comic book'}); assert r.status_code==200; d=r.json(); assert d['success']; assert len(d['panels'])==5; assert Path(d['pdf_path']).exists()
def test_image_endpoint():
 r=client.post('/test-image',json={'prompt':'A friendly fox in a comic forest.'}); assert r.status_code==200; assert r.json()['success']; assert Path(r.json()['image_path']).exists()
