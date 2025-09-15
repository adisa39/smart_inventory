from transformers import AutoProcessor, AutoModelForImageTextToText
import torch
from dotenv import load_dotenv
import os

load_dotenv()

token = os.getenv("huggingface_api_key")
if token is None:
    raise ValueError("huggingface_api_key is missing. Please set it in your environment or .env file.")

def load_model():
    # Model setup
    model_id = "LiquidAI/LFM2-VL-450M"
    print("📚 Loading processor...")
    processor = AutoProcessor.from_pretrained(model_id, trust_remote_code=True)

    print("🧠 Loading model...")
    model = AutoModelForImageTextToText.from_pretrained(
        model_id,
        device_map="cpu", # or "auto" if you have a compatible GPU,
        dtype=torch.float32,
        trust_remote_code=True
    )
    return processor, model