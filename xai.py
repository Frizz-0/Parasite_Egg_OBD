from YOLOv8_Explainer import yolov8_heatmap, display_images
from ultralytics import YOLO
import os
from pathlib import Path

# Initialize the heatmap generator
model = yolov8_heatmap(
    weight="models/best.pt", 
    method="EigenCAM",      # Try: GradCAM, HiResCAM, EigenCAM, LayerCAM
    conf_threshold=0.4,
    show_box=False,                 # Show bounding boxes for reference
    # layer=[12, 18, 21],            # Mid-to-deep layers (best for most models)
    layer=[22],
    ratio=0.02,                    # Adjust: 0.01 (sparse), 0.05 (dense)
    # renormalize=True               # IMPORTANT: Normalizes within bboxes for clarity
)

# Process multiple images
data_dir = "data"
image_files = sorted([f for f in os.listdir(data_dir) if f.lower().endswith(('.jpg', '.jpeg', '.png'))])

print(f"Found {len(image_files)} images to process: {image_files}\n")

all_images = []
for img_file in image_files:
    img_path = os.path.join(data_dir, img_file)
    print(f"Processing: {img_file}")
    images = model(img_path=img_path)
    all_images.extend(images)

# Show results for all images
print(f"\nDisplaying heatmaps for {len(all_images)} images...")
display_images(all_images)

# model = YOLO('models/best.pt')

# for i, layer in enumerate(model.model.model):
#     print(f"Index {i}: {layer}")

# device: device = torch.device("cuda:0" if torch.cuda.is_available() else "cpu")