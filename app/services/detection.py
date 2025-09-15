import cv2
import numpy as np
from PIL import Image
from app.services.log_manager import save_detections
from .load_model import load_model
import json, re 

# Load model globally
processor, model = load_model()

def extract_and_merge_json(text: str):
    matches = re.findall(r"\{.*?\}", text, re.DOTALL)
    merged = {}
    for match in matches:
        try:
            data = json.loads(match)
            if "objects" in data:
                for obj, count in data["objects"].items():
                    merged[obj] = merged.get(obj, 0) + int(count)
        except Exception:
            continue
    return merged

async def run_detection(file) -> dict:
    contents = await file.read()
    nparr = np.frombuffer(contents, np.uint8)
    frame = cv2.imdecode(nparr, cv2.IMREAD_COLOR)

    image = Image.fromarray(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))

    conversation = [
        {
            "role": "user",
            "content": [
                {"type": "image", "image": image},
                {"type": "text", "text": """Detect all objects. Return strictly:
                {"objects": {"label": count}}"""}
            ],
        },
    ]

    inputs = processor.apply_chat_template(
        conversation,
        add_generation_prompt=True,
        return_tensors="pt",
        return_dict=True,
        tokenize=True,
    ).to(model.device)

    outputs = model.generate(**inputs, max_new_tokens=200)
    detections_raw = processor.decode(outputs[0], skip_special_tokens=True)
    detections = extract_and_merge_json(detections_raw)
    return detections
