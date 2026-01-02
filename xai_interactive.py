import streamlit as st
import os
import cv2
import numpy as np
from PIL import Image
from YOLOv8_Explainer import yolov8_heatmap
import torch
import time

st.set_page_config(page_title="YOLOv8 Heatmap Explorer", layout="wide")
st.title("🔥 YOLOv8 Heatmap Parameter Tuner")

# Check GPU availability
gpu_available = torch.cuda.is_available()
device_name = torch.cuda.get_device_name(0) if gpu_available else "CPU"
device_status = f"✅ GPU: {device_name}" if gpu_available else "❌ CPU Mode"
st.info(device_status, icon="⚡")

# Sidebar for controls
st.sidebar.header("⚙️ Parameters")

# Method selection
method = st.sidebar.radio(
    "CAM Method",
    options=["GradCAM", "GradCAMPlusPlus", "EigenCAM", "HiResCAM", "LayerCAM", "EigenGradCAM"],
    index=2
)

# Layer selection
st.sidebar.subheader("Target Layers")
col1, col2, col3 = st.sidebar.columns(3)
with col1:
    layer1 = st.number_input("Layer 1", min_value=0, max_value=25, value=15, step=1)
with col2:
    layer2 = st.number_input("Layer 2", min_value=0, max_value=25, value=18, step=1)
with col3:
    layer3 = st.number_input("Layer 3", min_value=0, max_value=25, value=21, step=1)

layers = [layer1, layer2, layer3]

# Confidence threshold
conf_threshold = st.sidebar.slider(
    "Confidence Threshold",
    min_value=0.0, max_value=1.0, value=0.4, step=0.05
)

# Ratio (heatmap density)
ratio = st.sidebar.slider(
    "Heatmap Density Ratio",
    min_value=0.01, max_value=0.2, value=0.02, step=0.01,
    help="0.01 = sparse hotspots, 0.1+ = dense coverage"
)

# Renormalize option
renormalize = st.sidebar.checkbox("Renormalize CAM", value=False)

# Show bounding boxes
show_box = st.sidebar.checkbox("Show Bounding Boxes", value=False)

# Image selection
data_dir = "data"
image_files = sorted([f for f in os.listdir(data_dir) if f.lower().endswith(('.jpg', '.jpeg', '.png'))])

selected_images = st.sidebar.multiselect(
    "Select Images to Display",
    options=image_files,
    default=image_files[:2]
)

st.sidebar.markdown("---")
if st.sidebar.button("🔄 Regenerate Heatmaps", use_container_width=True):
    st.rerun()

# Main content
st.markdown("### Current Settings")
col1, col2, col3, col4 = st.columns(4)
with col1:
    st.metric("Method", method)
with col2:
    st.metric("Layers", f"{layers}")
with col3:
    st.metric("Confidence", f"{conf_threshold:.2f}")
with col4:
    st.metric("Ratio", f"{ratio:.3f}")

st.markdown("---")

# Initialize heatmap generator with current parameters
try:
    with st.spinner("Initializing model..."):
        model = yolov8_heatmap(
            weight="models/best.pt",
            device = torch.device("cuda" if torch.cuda.is_available() else "cpu"),
            method=method,
            conf_threshold=conf_threshold,
            show_box=show_box,
            layer=layers,
            ratio=ratio,
            renormalize=renormalize,
        )
    
    # Process and display images
    if selected_images:
        st.markdown(f"### Processing {len(selected_images)} Image(s)")
        
        # GPU memory monitoring
        if gpu_available:
            col1, col2, col3 = st.columns(3)
            with col1:
                st.metric("GPU Memory Total", f"{torch.cuda.get_device_properties(0).total_memory / 1e9:.2f} GB")
            with col2:
                allocated = torch.cuda.memory_allocated(0) / 1e9
                st.metric("GPU Memory Allocated", f"{allocated:.2f} GB")
            with col3:
                reserved = torch.cuda.memory_reserved(0) / 1e9
                st.metric("GPU Memory Reserved", f"{reserved:.2f} GB")
        
        # Create columns for side-by-side display
        cols = st.columns(min(len(selected_images), 3))
        
        for idx, img_file in enumerate(selected_images):
            img_path = os.path.join(data_dir, img_file)
            
            with st.spinner(f"Processing {img_file}..."):
                # Time the processing
                start_time = time.time()
                
                # Generate heatmap (returns list of PIL Images)
                results = model(img_path=img_path)
                
                elapsed = time.time() - start_time
                
                if results and len(results) > 0:
                    heatmap_img = results[0]  # Already a PIL Image from yolov8_heatmap
                    
                    # Load original for comparison
                    original = cv2.imread(img_path)
                    original_rgb = cv2.cvtColor(original, cv2.COLOR_BGR2RGB)
                    
                    # Display in column
                    col_idx = idx % len(cols)
                    with cols[col_idx]:
                        st.subheader(f"{img_file} ({elapsed:.2f}s)")
                        
                        # Tabs for original vs heatmap
                        tab1, tab2 = st.tabs(["Original", "Heatmap"])
                        with tab1:
                            st.image(original_rgb, use_container_width=True)
                        with tab2:
                            st.image(heatmap_img, use_container_width=True)
                else:
                    st.warning(f"No results for {img_file}")
    else:
        st.info("👈 Select images from the sidebar to get started")

except Exception as e:
    st.error(f"❌ Error: {str(e)}")
    st.info("Make sure 'models/best.pt' exists and the data directory has images")

st.markdown("---")
st.markdown("""
### Tips for Best Results:
- **Sparse heatmaps?** → Lower `Ratio` (0.01-0.02)
- **Too dense?** → Higher `Ratio` (0.05-0.1)
- **Wrong regions?** → Try different CAM methods or layers
- **Small objects?** → Use earlier layers (8-15) for more spatial detail
- **Better clarity?** → Enable `Renormalize CAM`
""")
