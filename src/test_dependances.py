import torch
print(f"PyTorch version: {torch.__version__}")
print(f"CUDA disponible: {torch.cuda.is_available()}")

try:
    import bitsandbytes
    print(f"✅ bitsandbytes installé: {bitsandbytes.__version__}")
except ImportError:
    print("❌ bitsandbytes non installé")

try:
    from transformers import AutoTokenizer
    print("✅ transformers OK")
except ImportError:
    print("❌ transformers non installé")

try:
    from peft import LoraConfig
    print("✅ peft OK")
except ImportError:
    print("❌ peft non installé")