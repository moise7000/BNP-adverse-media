from transformers import AutoModelForCausalLM, AutoTokenizer
from peft import LoraConfig, get_peft_model, prepare_model_for_kbit_training
from trl import SFTTrainer

# Charger Mistral 7B
model = AutoModelForCausalLM.from_pretrained(
    "mistralai/Mistral-7B-v0.1",
    load_in_4bit=True  # QLoRA
)

# Configuration LoRA
lora_config = LoraConfig(
    r=16,  # rang LoRA
    lora_alpha=32,
    target_modules=["q_proj", "v_proj"],  # couches à adapter
    lora_dropout=0.05,
    task_type="CAUSAL_LM"
)

# Fine-tuning
trainer = SFTTrainer(
    model=model,
    train_dataset=dataset,
    peft_config=lora_config,
    # ... autres paramètres
)

trainer.train()
