import os
import io
import re
import json
import base64
import traceback
from pathlib import Path
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from pydantic import BaseModel
from PIL import Image
from dotenv import load_dotenv
from google import genai
from google.genai import types

load_dotenv()

BASE_DIR = Path(__file__).resolve().parent

api_key = os.getenv("GEMINI_API_KEY")
if not api_key:
    raise ValueError("GEMINI_API_KEY not found. Please add it to your .env file.")

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
You are a high-precision spatial robotics vision engine specializing in physical object placement and surface affordance.

CRITICAL OBSTACLE EXCLUSIONS (NEVER OVERLAP THESE):
1. EXISTING POSTERS / CHARTS / BOARDS:
   - Any wall charts, blue/white lab notice boards, hung posters, or frames are OBSTACLES.
   - Do NOT place a painting or poster over an existing poster or notice board.
2. HUMANS & CLOTHING:
   - Head, hair, face, neck, shoulders, chest, and arms are strictly forbidden.
3. MONITORS & ELECTRONICS:
   - Computer screens, displays, switches, conduits, and power lines.

SURFACE AFFORDANCE RULES:
1. WALL-MOUNTED (painting, poster, clock, whiteboard, calendar, frame):
   - MUST target visible, continuous, vertical BARE WALL space (e.g. blank paint/concrete).
   - Select the large, continuous, empty wall section completely clear of posters and people.
2. TABLETOP / FLAT SURFACE (bottle, cup, mug, phone, laptop, pen, keys):
   - MUST target a genuine, flat, horizontal tabletop or desk surface.
   - If the camera only shows people, faces, or walls with no flat table surface visible in the foreground, return space_found: false.
3. FLOOR OBJECTS (bag, box, suitcase, shoes):
   - MUST target open floor clearance.

OUTPUT FORMAT (strict JSON only):
{
  "space_found": true/false,
  "surface_type": "wall" | "table" | "floor" | "none",
  "box_2d": [ymin, xmin, ymax, xmax] or null,
  "reasoning": "Explain exact position, confirming it is bare wall/table clear of existing posters, monitors, and humans.",
  "hazards_avoided": ["hazard 1", "hazard 2"],
  "confidence_score": 96.0
}
"""

# Prioritize models with high free-tier quotas and low latency
MODEL_CANDIDATES = [
    "gemini-3.6-flash",
    "gemini-2.5-flash-lite",
]
class ScanRequest(BaseModel):
    image_base64: str
    target_item: str

@app.get("/")
def serve_index():
    index_path = BASE_DIR / "index.html"
    if not index_path.exists():
        raise HTTPException(status_code=404, detail="index.html not found.")
    return FileResponse(index_path)

@app.post("/api/scan")
async def scan_workspace(req: ScanRequest):
    try:
        header, encoded = req.image_base64.split(",", 1) if "," in req.image_base64 else ("", req.image_base64)
        img_bytes = base64.b64decode(encoded)
        pil_img = Image.open(io.BytesIO(img_bytes)).convert("RGB")
        pil_img.thumbnail((1024, 1024))

        prompt = f"""
        TARGET ITEM: '{req.target_item}'

        SPATIAL TASK:
        1. Determine required surface (wall for painting/poster, table for bottle/pen, floor for box).
        2. Identify and completely mask out all people, clothes, existing notice boards/posters, and computer monitors.
        3. Identify an open, unoccupied patch of the required surface.
        4. Return normalized bounding box [ymin, xmin, ymax, xmax] on a 0-1000 scale.
        """

        raw_text = None
        last_err = None

        for model_name in MODEL_CANDIDATES:
            try:
                response = client.models.generate_content(
                    model=model_name,
                    contents=[pil_img, prompt],
                    config=types.GenerateContentConfig(
                        system_instruction=SYSTEM_INSTRUCTION,
                        response_mime_type="application/json"
                    )
                )
                if response and response.text:
                    raw_text = response.text.strip()
                    break
            except Exception as err:
                last_err = err
                print(f"[Model Fallback] {model_name} failed: {err}")
                continue

        # Catch quota/rate limit errors without crashing into a 500 error
        if not raw_text:
            err_str = str(last_err)
            if "429" in err_str or "RESOURCE_EXHAUSTED" in err_str:
                return {
                    "space_found": False,
                    "surface_type": "none",
                    "box_2d": None,
                    "reasoning": "Gemini API daily limit reached (429). Create a new key in a brand new project on Google AI Studio to reset the 20-request limit.",
                    "hazards_avoided": ["API Quota Exceeded"],
                    "confidence_score": 0.0
                }
            return {
                "space_found": False,
                "surface_type": "none",
                "box_2d": None,
                "reasoning": f"Vision engine unavailable: {err_str}",
                "hazards_avoided": ["Service Error"],
                "confidence_score": 0.0
            }

        clean_json = re.sub(r"^```(?:json)?\s*", "", raw_text, flags=re.IGNORECASE)
        clean_json = re.sub(r"\s*```$", "", clean_json)

        result = json.loads(clean_json)

        if result.get("space_found") and result.get("box_2d"):
            box = [max(0, min(1000, int(v))) for v in result["box_2d"]]
            result["box_2d"] = box

        return result

    except Exception as e:
        print("\n=== SERVER EXCEPTION IN /api/scan ===")
        traceback.print_exc()
        print("=====================================\n")
        raise HTTPException(status_code=500, detail=str(e))