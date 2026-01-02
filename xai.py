from YOLOv8_Explainer import yolov8_heatmap, display_images

# Initialize the heatmap generator
# 'weight' is the path to your .pt file
model = yolov8_heatmap(
    weight="models/best.pt", 
    method="EigenCAM",      # Common methods: GradCAM, HiResCAM, EigenCAM
    conf_threshold=0.4,
    show_box=False
)

# Generate the heatmap for an image
images = model(img_path="data/01.jpg")

# Show the results
display_images(images)

