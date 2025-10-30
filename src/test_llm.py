from transformers import AutoModelForCausalLM, AutoTokenizer
import torch

print("Chargement du tokenizer...")
tokenizer = AutoTokenizer.from_pretrained("mistralai/Mistral-7B-v0.1")

print("Chargement du modèle (cela peut prendre quelques minutes)...")
model = AutoModelForCausalLM.from_pretrained(
    "mistralai/Mistral-7B-v0.1",
    device_map="auto",
    torch_dtype=torch.float16,
    load_in_8bit=True  # Quantization 8-bit (moins agressive que 4-bit)
)

print("✅ Modèle chargé avec succès!")

# Test rapide
prompt = "Bonjour, je suis"
inputs = tokenizer(prompt, return_tensors="pt").to(model.device)
outputs = model.generate(**inputs, max_new_tokens=20)
print(tokenizer.decode(outputs[0]))