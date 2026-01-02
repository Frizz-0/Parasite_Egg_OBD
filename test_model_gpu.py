import torch
from YOLOv8_Explainer import yolov8_heatmap

print("Testing YOLOv8_Explainer GPU support...")
print(f"CUDA Available: {torch.cuda.is_available()}")

# Test with GPU
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
print(f"Device: {device}")

try:
    print("\nInitializing model on GPU...")
    model = yolov8_heatmap(
        weight="models/best.pt",
        device=device,
        method="GradCAM",
        conf_threshold=0.4,
        layer=[15, 18, 21]
    )
    
    # Check where model is
    print(f"Model device: {model.device}")
    print(f"Model parameters device: {next(model.model.parameters()).device}")
    
    print("\n✅ Model loaded on GPU successfully!")
    
except Exception as e:
    print(f"❌ Error: {e}")
    import traceback
    traceback.print_exc()
