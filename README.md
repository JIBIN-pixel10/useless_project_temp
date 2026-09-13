<img width="1280" height="640" alt="git (1)" src="https://github.com/user-attachments/assets/8920b256-2ba8-4988-b824-5351134eb4bd" />



# [NEXUS // Spatial AI Workspace Optimizer] 🎯


## Basic Details
### Team Name: [Waguri]


### Team Members
- Team Lead: Jibin James - School of Engineering, CUSAT

### Project Description
An enterprise-grade multimodal spatial computing HUD that scans your desk via live webcam feed to mathematically compute where to set down everyday items. It combines real-time WebRTC video streams with Google Gemini Flash vision reasoning to evaluate spill zones, reachability, and clutter before locking onto coordinates with military-style targeting reticles.

### The Problem (that doesn't exist)
Human beings have been setting cups, phones, and water bottles down on flat surfaces for thousands of years using basic depth perception and common sense. However, this relies on unverified biological intuition rather than high-performance spatial computing. What if placing your water bottle 3 centimeters too close to your mouse pad decreases your daily desk operational efficiency by 2.4%? Humanity simply cannot afford such unoptimized desk entropy.Obviously it is a very big problem that requires instant recognition . I saw the problem and as a hero i decided to solve this. Blehhh

### The Solution (that nobody asked for)
Instead of using your eyes and hands like a normal person, point an HD (HD is mandatory :()zcamera at your table, launch a dark-mode cyberpunk glassmorphism terminal, type what you are holding, and wait for a trillion-parameter cloud foundation model to run safety, clearance, and spill-hazard telemetry before telling you the single approved coordinate box where you are permitted to set your mug. Isnt this just useless ,  I mean cant u decide where you need to keep a bottle
duh...

## Technical Details
### Technologies/Components Used
For Software:
Languages: Python 3.10+, JavaScript (ES6+), HTML5, CSS3

Frameworks: FastAPI, Uvicorn

Libraries: google-genai (Gemini SDK), Pillow (PIL), Pydantic, python-dotenv

APIs & Web Standards: Gemini 3.6 Flash Multimodal Vision API, WebRTC MediaStreams API (getUserMedia), HTML5 Canvas 2D Context API

Tools: Visual Studio Code, Git, Browser DevTools


### Implementation
For Software:
# Installation
git clone https://github.com/your-username/nexus-spatial-optimizer.git
cd nexus-spatial-optimizer
pip install fastapi uvicorn python-dotenv pydantic pillow google-genai


Set up environment credentials in a .env file:

GEMINI_API_KEY=your_gemini_api_key_here

# Run
uvicorn app:app --reload --port 8000


For Software:
<img width="1917" height="975" alt="first stage" src="https://github.com/user-attachments/assets/aef0cca2-86c6-4172-a71d-246a45378651" />


1.Initial Standby State (first stage.jpg)

System Status: Engine online, live WebRTC camera feed streaming without coordinate drift.

Controls: Minimalist floating bottom dock with active target input field (Water Bottle) ready for real-time spatial evaluation.

HUD Layer: Clean glassmorphism interface with subtle grid overlays and quick-action navigation controls.

<img width="1912" height="955" alt="running" src="https://github.com/user-attachments/assets/ab2eb576-813f-4bb9-81a2-6ec440d3f08e" />

2. Live Spatial Analysis (running.jpg)

Inference State: High-resolution sensor capture sent to the multi-model backend pipeline.

Visual Feedback: Animated cyan laser scanline sweeps vertically across the viewport while disabling input to signify ongoing spatial calculations.

Affordance Evaluation: The vision engine analyzes target geometry, classifies required surface type, and computes negative exclusion masks (filtering out people, furniture, and monitors).

<img width="1528" height="763" alt="result" src="https://github.com/user-attachments/assets/0984567a-74f7-4f5b-9cf4-39d7dc754b75" />

3. Precision Target Lock (result.jpg)Bounding Lock: System successfully identifies a clean, continuous bare wall section on the left for mounting a tv.Exclusion Accuracy: Coordinates strictly avoid the ceiling electrical conduits, foreground user, and background cubicle seating.Telemetry Diagnostics: Top-left heads-up display presents the ergonomic rationale, confidence score ($94.5\%$), and explicit catalog of avoided hazards (electrical conduits, switch box, people in background).

# Diagrams
<img width="962" height="717" alt="Screenshot 2026-09-13 152610" src="https://github.com/user-attachments/assets/926606e3-a352-4ea1-9469-2ed07c68d3de" />


1. Client Layer (Browser HUD)Landing Modal & Permission Gate: The system begins in a standby state with camera access unengaged. Clicking "Engage Camera" explicitly requests WebRTC sensor permissions, complying with browser security policies while preventing unwanted feed activation.Mirrored Stream & Input: The browser establishes a live WebRTC video feed. The user enters a target object (e.g., tv, painting, bottle) into the dock and triggers "EXECUTE SCAN".Frame Capture: A hidden HTML5 canvas captures the exact current video frame and serializes it into a compressed Base64 JPEG payload, which is dispatched via an asynchronous POST /api/scan request.
2.  Backend Layer (FastAPI & Gemini Multimodal Pipeline)Ingestion & Preprocessing: FastAPI decodes the Base64 image bytes into an RGB image, downscales it to a maximum bounding size of $1024 \times 1024$ to preserve bandwidth and latency, and injects spatial affordance grounding instructions.Affordance & Hazard Rules: The model is instructed to match objects to valid physical surfaces (e.g., vertical bare walls for wall mounts, flat horizontal planes for bottles) while explicitly establishing exclusion zones over humans, clothes, displays, and existing notice posters.Model Fallback Pipeline: The request queries gemini-3.6-flash as the primary engine. If unavailable or rate-limited, it automatically falls back to gemini-2.5-flash-lite. If free quotas are exceeded (HTTP 429), it intercepts the exception to return a clean status instead of crashing the server.Sanitization & Clamping: The backend strips any Markdown fences, parses the raw JSON, and clamps normalized bounding box values to the standard $[0, 1000]$ coordinate range.
   Spatial Projection & Feedback Layer (HUD Overlay)Positive Lock (space_found: true):Mirror Inversion: Because user webcams operate in selfie mirror mode, the frontend recalculates the horizontal axis ($\text{mirroredX} = 1000 - x$) so the overlay matches user-perceived space.Reticle Animation: A Linear Interpolation (LERP) loop animates the bounding box brackets smoothly over the live feed.Telemetry HUD: The diagnostic card renders confidence scores, placement rationale, and an itemized summary of mitigated hazards.Negative Lock / Blocked (space_found: false):If no matching surface is visible (e.g., searching for a table plane when only a wall is shown) or quota limits are hit, the canvas clears active brackets and displays an explanatory hazard card detailing why placement was rejected.


# Build Photos
<img width="276" height="197" alt="Screenshot 2026-09-13 115112" src="https://github.com/user-attachments/assets/e6f69720-020b-4df4-953a-69d89b3b27f0" />
__pycache__/: Auto-generated Python directory that stores compiled bytecode (.pyc files) to accelerate module loading on subsequent executions.

.env: Local environment configuration storing secret credentials, primarily your GEMINI_API_KEY, isolated from source control.

.gitignore: Git configuration file specifying which files or folders (like .env, __pycache__, or large weights) Git should avoid tracking or pushing to GitHub.

app.py (Status: M - Modified): The FastAPI backend server handling API routing (/api/scan), multi-model fallback execution, image preprocessing, and Gemini spatial grounding instructions.

index.html (Status: M - Modified): The single-page frontend application containing the WebRTC camera stream handler, cyberpunk HUD overlay, canvas coordinate rendering, and mirror-inversion logic.

README.md: Project documentation outlining the architecture, features, setup instructions, and build screenshots.

yolov8n.pt: A pre-trained PyTorch weight file for the Ultralytics YOLOv8 Nano object detection model—likely a remnant from earlier local vision testing before switching to Gemini multimodal inference.

### Project Demo
deplyed project link : https://useless-project-temp-ar3c.onrender.com/
# Video
demo link : https://youtu.be/mf6twTIVyts



## Team Contributions
- [Jibin James]: [Whole project]     #single everywhere:(


---
Made with ❤️ at TinkerHub Useless Projects 

![Static Badge](https://img.shields.io/badge/TinkerHub-24?color=%23000000&link=https%3A%2F%2Fwww.tinkerhub.org%2F)
![Static Badge](https://img.shields.io/badge/UselessProjects--26-26?link=https%3A%2F%2Ftinkerhub.org%2Fevents%2F1M8ORET9A1%2Fuseless-projects-3.0)



