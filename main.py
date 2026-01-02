import streamlit as st
import requests
import numpy as np
from PIL import Image
import os
import io
import base64

# Parasite descriptions
PARASITE_DESCRIPTIONS = {
    "Ancylostoma Spp": "Ancylostoma (hookworm) parasites attach to the small intestine and feed on blood, causing anemia and protein deficiency.",
    "Ascaris Lumbricoides": "A large roundworm that inhabits the small intestine, causing malnutrition and intestinal blockages in severe cases.",
    "Enterobius Vermicularis": "Pinworm infection, commonly affecting children, causing itching around the anal area, especially at night.",
    "Fasciola Hepatica": "Liver fluke parasite that infects the bile ducts and liver, causing digestive issues and liver damage.",
    "Hymenolepis": "Dwarf tapeworm, the smallest tapeworm in humans, causing intestinal inflammation and malabsorption.",
    "Schistosoma": "Parasitic flatworm that lives in blood vessels, causing chronic inflammation and organ damage.",
    "Taenia Sp": "Tapeworm that lives in the intestine, causing nutrient deficiencies and weight loss.",
    "Trichuris Trichiura": "Whipworm that infects the colon, causing diarrhea, anemia, and rectal prolapse in heavy infections.",
    'Unknown Species': "Species couldnt be identified"
}

# Set page configuration
st.set_page_config(
    page_title="Parasite Detection System",
    page_icon="🔬",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
    <style>
            
    @media (prefers-color-scheme: light){
        .main {
            padding: 2rem;
            background-color:blue;
        }
            
        .header {
            text-align: center;
            margin-bottom: 2rem;
            
        }
        .prediction-box {
            background-color: #f0f2f6;
            padding: 1.5rem;
            border-radius: 0.5rem;
            margin: 1rem 0;
            border-left: 4px solid #1f77b4;
        }
        .confidence-high {
            color: #28a745;
        }
        .confidence-medium {
            color: #ffc107;
        }
        .confidence-low {
            color: #dc3545;
        }
        [data-testid="column"]{
            border-radius :10rem;
            color:blue;    
        }
    }

    @media (prefers-color-scheme: dark) {
        .custom-box {
            background-color: #333333;
            border: 1px solid #4CAF50;
        }
            
        .prediction-box {
        background-color: black;
        padding: 1.5rem;
        border-radius: 200rem;
        margin: 1rem 0;
        border-left: 4px solid #1f77b4;
      
    }
    }
    </style>
    """, unsafe_allow_html=True)

# Title and description
st.markdown("""
    <div class="header">
    <h1>🦠 Parasite Detection System</h1>
    <p>Advanced AI-powered parasite identification from microscopic images</p>
    </div>
    """, unsafe_allow_html=True)

# Backend URL
BACKEND_URL = "http://127.0.0.1:8000"
HEADERS = {'access_token' : 'kawai_so_oppai'}

# Check backend health
# @st.cache_resource
def check_backend_health():
    """Check if backend is running"""
    try:
        response = requests.get(f"{BACKEND_URL}/health", timeout=2)
        return response.status_code == 200
    except:
        return False

# Main interface
col1, col2 = st.columns([1, 1], gap="large", border=True,)

with col1:
    st.subheader("📤 Upload Image")
    
    # Image upload options
    upload_option = st.radio("Choose input method:", ["Upload Image", "Use Sample"])
    
    if upload_option == "Upload Image":
        uploaded_file = st.file_uploader(
            "Select an image file",
            type=['jpg', 'jpeg', 'png', 'bmp'],
            help="Upload a microscopic image of parasite specimen"
        )
        image_source = uploaded_file
    else:
        # Try to use sample image
        sample_path = 'data/02.jpg'
        if os.path.exists(sample_path):
            image_source = sample_path
            st.info("Using sample image from data folder")
        else:
            st.warning("No sample image found in data folder")
            image_source = None

with col2:
    st.subheader("⚙️ Settings")
    
    confidence_threshold = st.slider(
        "Confidence Threshold",
        min_value=0.0,
        max_value=1.0,
        value=0.5,
        step=0.05,
        help="Only show predictions above this confidence level"
    )
    
    show_boxes = st.checkbox("Show Bounding Boxes", value=True)
    show_labels = st.checkbox("Show Labels on Image", value=True)

# Process and display results
if image_source is not None:
    # Check backend health
    if not check_backend_health():
        st.error("❌ Backend server is not running. Please start the backend with: python backend.py")
    else:
        # Load image
        if isinstance(image_source, str):
            image = Image.open(image_source)
            # Read file bytes for backend
            with open(image_source, 'rb') as f:
                image_bytes = f.read()
        else:
            image = Image.open(image_source)
            image_bytes = image_source.getvalue()

        # Send to backend for prediction
        with st.spinner("🔍 Analyzing image..."):
            try:
                files = {'file': image_bytes}
                params = {
                    'confidence_threshold': confidence_threshold,
                    'show_boxes': show_boxes,
                    'show_labels': show_labels
                }
                
                response = requests.post(
                    f"{BACKEND_URL}/predict",
                    headers=HEADERS,
                    files=files,
                    params=params,
                    timeout=30
                )
                
                if response.status_code == 200:
                    result = response.json()
                    
                    # Create two columns for image and results
                    img_col, result_col = st.columns([1, 1], gap="large")
                    
                    with img_col:
                        st.subheader("Image Analysis")
                        
                        # Display annotated image from backend
                        if result.get('image_base64'):
                            img_data = base64.b64decode(result['image_base64'])
                            annotated_image = Image.open(io.BytesIO(img_data))
                            st.image(annotated_image, width='stretch')
                        else:
                            st.image(image,width='stretch', caption="Original Image")

                        # Heatmap section with on-demand generation
                        st.divider()
                        st.subheader("Heatmap Analysis")
                        
                        # Generate heatmap button
                        if st.button("🔥 Generate Heatmap", use_container_width=True, key="generate_heatmap"):
                            with st.spinner("Generating heatmap (GPU intensive)..."):
                                try:
                                    # Re-upload the file for heatmap generation
                                    if isinstance(image_source, str):
                                        with open(image_source, 'rb') as f:
                                            heatmap_files = {'file': f.read()}
                                    else:
                                        heatmap_files = {'file': image_source.getvalue()}
                                    
                                    heatmap_response = requests.post(
                                        f"{BACKEND_URL}/generate_heatmap",
                                        headers=HEADERS,
                                        files=heatmap_files,
                                        timeout=60
                                    )
                                    
                                    if heatmap_response.status_code == 200:
                                        heatmap_result = heatmap_response.json()
                                        if heatmap_result.get('image_heatmap'):
                                            heatmap_data = base64.b64decode(heatmap_result['image_heatmap'])
                                            heatmap_image = Image.open(io.BytesIO(heatmap_data))
                                            st.image(heatmap_image, width='stretch', caption=f"Heatmap")
                                        else:
                                            st.error('Failed to generate heatmap')
                                    else:
                                        st.error(f"Heatmap generation error: {heatmap_response.text}")
                                
                                except Exception as e:
                                    st.error(f"Error: {str(e)}")

                    with result_col:
                        st.subheader("Detection Results")
                        
                        detections = result.get('detections', [])
                        
                        if len(detections) == 0:
                            st.warning("⚠️ No parasites detected in this image.")
                        else:
                            st.success(f"✅ Found **{len(detections)}** parasite(s)")
                            
                            # Display each detection
                            for detection in detections:
                                idx = detection['index']
                                class_name = detection['name']
                                conf = detection['confidence']
                                conf_emoji = detection['confidence_emoji']
                                description = detection['description']
                                conf_percentage = detection['confidence_percentage']
                                
                                # Determine confidence class
                                if conf > 0.8:
                                    conf_class = "confidence-high"
                                elif conf > 0.6:
                                    conf_class = "confidence-medium"
                                else:
                                    conf_class = "confidence-low"
                                
                                st.markdown(f"""
                                <div class="prediction-box">
                                <h4>{idx}. {class_name}</h4>
                                <p><span class="{conf_class}"><b>Confidence: {conf_percentage}</b> {conf_emoji}</span></p>
                                <hr style="margin: 0.5rem 0;">
                                <p><i>{description}</i></p>
                                </div>
                                """, unsafe_allow_html=True)
                        
                        # Summary statistics
                        st.divider()
                        st.subheader("📈 Summary")
                        
                        if len(detections) > 0:
                            col1_s, col2_s, col3_s = st.columns(3)
                            
                            with col1_s:
                                st.metric("Total Detections", result['total_detections'])
                            
                            with col2_s:
                                st.metric("Avg Confidence", result['avg_confidence'])
                            
                            with col3_s:
                                st.metric("Unique Species", result['unique_species'])
                        else:
                            st.metric("Total Detections", "0")
                
                else:
                    st.error(f"Error from backend: {response.text}")
            
            except requests.exceptions.ConnectionError:
                st.error("❌ Cannot connect to backend. Please ensure it's running on http://127.0.0.1:8000")
            except Exception as e:
                st.error(f"Error: {str(e)}")

# Footer
st.divider()
st.markdown("""
    <div style="text-align: center; color: gray; margin-top: 2rem;">
    <p><small>🔬 Parasite Detection System | Powered by YOLOv8 | For educational and diagnostic purposes</small></p>
    </div>
    """, unsafe_allow_html=True)
