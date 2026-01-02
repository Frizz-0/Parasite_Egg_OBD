import torch
import sys

print("=" * 50)
print("GPU/CUDA Diagnostic Report")
print("=" * 50)
print(f"PyTorch Version: {torch.__version__}")
print(f"CUDA Available: {torch.cuda.is_available()}")
print(f"CUDA Version: {torch.version.cuda}")
print(f"cuDNN Version: {torch.backends.cudnn.version()}")
print(f"Device Count: {torch.cuda.device_count()}")

if torch.cuda.is_available():
    print(f"\nCurrent Device: {torch.cuda.current_device()}")
    print(f"Device Name: {torch.cuda.get_device_name(0)}")
    print(f"Device Properties: {torch.cuda.get_device_properties(0)}")
    
    # Test GPU memory
    print(f"\nGPU Memory:")
    print(f"  Total: {torch.cuda.get_device_properties(0).total_memory / 1e9:.2f} GB")
    print(f"  Allocated: {torch.cuda.memory_allocated(0) / 1e9:.2f} GB")
    print(f"  Cached: {torch.cuda.memory_reserved(0) / 1e9:.2f} GB")
    
    # Test tensor on GPU
    print(f"\nTesting GPU tensor operation...")
    x = torch.randn(1000, 1000, device='cuda')
    y = torch.randn(1000, 1000, device='cuda')
    z = torch.mm(x, y)
    print(f"✅ GPU tensor operation successful!")
else:
    print("\n❌ CUDA is NOT available!")
    print("You need to install CUDA-enabled PyTorch:")
    print("  pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu118")
    sys.exit(1)

print("\n" + "=" * 50)
print("GPU is properly configured and ready!")
print("=" * 50)
