import os
import io
import json
import base64
from pathlib import Path
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from pydantic import BaseModel
from PIL import Image
from dotenv import load_dotenv
from google import genai
from google.genai import types

# Load variables from .env
load_dotenv()

BASE_DIR = Path(__file__).resolve().parent

api_key = os.getenv("GEMINI_API_KEY")
if not api_key:
    raise ValueError("GEMINI_API_KEY not found. Add it to your .env file.")

client = genai.Client(api_key=api_key)

app = FastAPI(title="Nexus Spatial AI Engine")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

SYSTEM_INSTRUCTION = """
You are an enterprise AI spatial computing engine for desk ergonomics.
Analyze the camera image and determine the safest, most ergonomically optimal space for the target item.
1. Evaluate desk clearance, reachability, stability, and collision hazards (liquids near keyboard, cables, mouse swing).
2. Return coordinates [ymin, xmin, ymax, xmax] on a 0-1000 scale.
3. Output strict JSON adhering to this schema:
{
  "space_found": true/false,
  "box_2d": [ymin, xmin, ymax, xmax],
  "reasoning": "brief ergonomic explanation",
  "hazards_avoided": ["hazard1", "hazard2"],
  "confidence_score": 98.4
}
"""

class ScanRequest(BaseModel):
    image_base64: str
    target_item: str

@app.get("/")
def serve_index():
    index_path = BASE_DIR / "index.html"
    if not index_path.exists():
        raise HTTPException(status_code=404, detail="index.html not found in project directory.")
    return FileResponse(index_path)

@app.post("/api/scan")
async def scan_workspace(req: ScanRequest):
    try:
        header, encoded = req.image_base64.split(",", 1) if "," in req.image_base64 else ("", req.image_base64)
        img_bytes = base64.b64decode(encoded)
        pil_img = Image.open(io.BytesIO(img_bytes)).convert("RGB")

        prompt = f"Target item: '{req.target_item}'. Identify clear, flat, hazard-free desk placement space."

        response = client.models.generate_content(
            model="gemini-3.6-flash",
            contents=[pil_img, prompt],
            config=types.GenerateContentConfig(
                system_instruction=SYSTEM_INSTRUCTION,
                response_mime_type="application/json"
            )
        )
        return json.loads(response.text)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))