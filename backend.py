from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi import Depends, Security, status
from fastapi.security import APIKeyHeader
from fastapi.middleware.cors import CORSMiddleware
from ultralytics import YOLO
from YOLOv8_Explainer import yolov8_heatmap
import numpy as np
from PIL import Image
import io
import base64
import tempfile
import os

app = FastAPI(title="Parasite Detection API", description="YOLO-based parasite detection system")

#ADDING API KEY
API_KEY = 'kawai_so_oppai'
API_KEY_NAME = 'access_token'
API_KEY_HEADER = APIKeyHeader(name=API_KEY_NAME, auto_error=False)

async def get_api_key(header_key: str = Security(API_KEY_HEADER)):
    if header_key == API_KEY:
        return header_key
    raise HTTPException( status_code=status.HTTP_403_FORBIDDEN, detail="Access denied")


# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Parasite descriptions (same as Streamlit app)
PARASITE_DESCRIPTIONS = {
    "Ancylostoma Spp": "Ancylostoma (hookworm) parasites attach to the small intestine and feed on blood, causing anemia and protein deficiency.",
    "Ascaris Lumbricoides": "A large roundworm that inhabits the small intestine, causing malnutrition and intestinal blockages in severe cases.",
    "Enterobius Vermicularis": "Pinworm infection, commonly affecting children, causing itching around the anal area, especially at night.",
    "Fasciola Hepatica": "Liver fluke parasite that infects the bile ducts and liver, causing digestive issues and liver damage.",
    "Hymenolepis": "Dwarf tapeworm, the smallest tapeworm in humans, causing intestinal inflammation and malabsorption.",
    "Schistosoma": "Parasitic flatworm that lives in blood vessels, causing chronic inflammation and organ damage.",
    "Taenia Sp": "Tapeworm that lives in the intestine, causing nutrient deficiencies and weight loss.",
    "Trichuris Trichiura": "Whipworm that infects the colon, causing diarrhea, anemia, and rectal prolapse in heavy infections.",
    'Unknown Species': "Species couldn't be identified"
}

# Load model globally
try:
    model = YOLO('models/best.pt')
except FileNotFoundError:
    model = None

@app.get("/")
def home():
    return {"status": "success", "message": "YOLO Parasites API is running"}

@app.get("/health")
def health_check():
    """Health check endpoint"""
    return {"status": "healthy", "model_loaded": model is not None}


@app.post("/predict")
async def predict_parasite(
    token: str = Depends(get_api_key),
    file: UploadFile = File(...),
    confidence_threshold: float = 0.5,
    show_boxes: bool = True,
    show_labels: bool = True
):
    """
    Predict parasites in uploaded image
    
    Parameters:
    - file: Image file (JPG, JPEG, PNG, BMP)
    - confidence_threshold: Confidence threshold (0.0-1.0)
    - show_boxes: Include bounding boxes in annotated image
    - show_labels: Include labels on annotated image
    """
    
    if model is None:
        raise HTTPException(status_code=500, detail="Model not loaded. Please ensure 'models/best.pt' exists.")
    
    try:
        # Read uploaded file
        contents = await file.read()
        image = Image.open(io.BytesIO(contents))
        
        width, height = image.size
        img_array = np.array(image)
        
        # Run YOLO prediction
        results = model.predict(img_array, conf=confidence_threshold)
        result = results[0]
        
        # Generate annotated image
        if show_boxes:
            line_width = 3 if (width >= 500 or height >= 500) else 1
            if show_labels:
                annotated_image = result.plot(line_width=line_width)
            else:
                annotated_image = result.plot(labels=False, line_width=line_width)
        else:
            annotated_image = img_array
        
        # Convert annotated image to base64
        annotated_pil = Image.fromarray(annotated_image)
        img_buffer = io.BytesIO()
        annotated_pil.save(img_buffer, format='PNG')
        img_base64 = base64.b64encode(img_buffer.getvalue()).decode()

        # Creating a heatmap image
        # Save image to temporary file since yolov8_heatmap expects img_path
        with tempfile.NamedTemporaryFile(delete=False, suffix='.jpg') as tmp_file:
            tmp_path = tmp_file.name
            Image.fromarray(img_array).save(tmp_path)
        
        try:
            xmodel = yolov8_heatmap(weight='models/best.pt', method="GradCAM", conf_threshold=0.2, show_box=False, layer=[18,20,22]) 
            ximg_list = xmodel(img_path=tmp_path)
            
            # Extract the first image from the returned list
            if isinstance(ximg_list, list) and len(ximg_list) > 0:
                ximg = ximg_list[0]
            else:
                ximg = ximg_list
            
            # Convert heatmap image to base64
            # ximg is already a PIL Image object, so use it directly
            if isinstance(ximg, Image.Image):
                xannotated_pil = ximg
            else:
                xannotated_pil = Image.fromarray(ximg)
            
            ximg_buffer = io.BytesIO()
            xannotated_pil.save(ximg_buffer, format='PNG')
            image_heatmap = base64.b64encode(ximg_buffer.getvalue()).decode()
        finally:
            # Clean up temporary file
            if os.path.exists(tmp_path):
                os.remove(tmp_path)
        
        # Extract detections
        detections = result.boxes
        
        detection_list = []
        for idx, detection in enumerate(detections):
            conf = float(detection.conf)
            class_id = int(detection.cls)
            class_name = result.names[class_id]
            
            # Determine confidence emoji
            if conf > 0.8:
                conf_emoji = "🟢"
            elif conf > 0.6:
                conf_emoji = "🟡"
            else:
                conf_emoji = "🔴"
            
            # Handle low confidence detections
            if conf < 0.5:
                species_name = "Unknown Species"
            else:
                species_name = class_name
            
            detection_dict = {
                "index": idx + 1,
                "name": species_name,
                "confidence": conf,
                "confidence_percentage": f"{conf:.1%}",
                "confidence_emoji": conf_emoji,
                "description": PARASITE_DESCRIPTIONS.get(species_name, "No description available.")
            }
            detection_list.append(detection_dict)
        
        
        # Calculate summary statistics
        if len(detections) > 0:
            confidences = [float(d.conf) for d in detections]
            avg_confidence = np.mean(confidences)
            unique_classes = set([result.names[int(d.cls)] for d in detections])
        else:
            avg_confidence = 0.0
            unique_classes = set()
        
        return {
            "image_base64": img_base64,
            "image_heatmap" : image_heatmap,
            "detections": detection_list,
            "total_detections": len(detections),
            "avg_confidence": f"{avg_confidence:.1%}" if avg_confidence > 0 else "0.0%",
            "unique_species": len(unique_classes)
        }
        
    except Exception as e:
        raise HTTPException(
            status_code=400,
            detail=f"Error processing image: {str(e)}"
        )


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)