import torch
from fastapi import FastAPI, File, UploadFile, Response
from fastapi.middleware.cors import CORSMiddleware
from PIL import Image
import io
import json

# Initialize FastAPI app
app = FastAPI(
    title="Coffee Bean Roast Level Detector",
    description="API for detecting coffee bean roast levels using YOLOv5",
    version="0.0.1"
)

# Allow CORS for frontend access
origins = ["https://cysyiu.github.io"]  # Update with your frontend URL in production
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Load YOLOv5 model
model = torch.hub.load('/home/site/wwwroot/backend/yolov5', 'custom', path='/home/site/wwwroot/backend/best.pt', source='local')
model.conf = 0.5  # Confidence threshold

# Health check endpoint
@app.get('/health')
def get_health():
    return {"msg": "OK"}

# Endpoint to detect roast level and return JSON
@app.post("/detect")
async def detect_roast_level(file: UploadFile = File(...)):
    # Read and process image
    image_bytes = await file.read()
    input_image = Image.open(io.BytesIO(image_bytes)).convert("RGB")
    
    # Perform detection
    results = model(input_image)
    detect_res = results.pandas().xyxy[0].to_json(orient="records")
    detect_res = json.loads(detect_res)
    
    return {"result": detect_res}

# Endpoint to detect and return annotated image
@app.post("/detect-image")
async def detect_roast_level_image(file: UploadFile = File(...)):
    # Read and process image
    image_bytes = await file.read()
    input_image = Image.open(io.BytesIO(image_bytes)).convert("RGB")
    
    # Perform detection
    results = model(input_image)
    results.render()  # Add bounding boxes and labels
    
    # Convert to JPEG
    for img in results.imgs:
        bytes_io = io.BytesIO()
        img_base64 = Image.fromarray(img)
        img_base64.save(bytes_io, format="JPEG")
        return Response(content=bytes_io.getvalue(), media_type="image/jpeg")
