import cv2
import json
import re
from PIL import Image
from load_model import load_model

# Load model (offline)
processor, model = load_model()

# Webcam or vid
vid_path = "sample_vid1.mp4" # or 0 for webcam
cap = cv2.VideoCapture(vid_path)

print("📸 Press 's' to snap an image, or 'q' to quit.")

def extract_and_merge_json(text: str):
    """Extract all JSON objects from text and merge them."""
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

while True:
    ret, frame = cap.read()
    if not ret:
        break

    # Show live feed
    cv2.imshow("Smart Inventory Counter", frame)

    key = cv2.waitKey(1) & 0xFF

    if key == ord("s"):
        # Convert frame → PIL image
        image = Image.fromarray(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))

        # Strong structured prompt
        conversation = [
            {
                "role": "user",
                "content": [
                    {"type": "image", "image": image},
                    {
                        "type": "text",
                        "text": """
                        Detect all objects in this image.
                        Return the result strictly as JSON in this format:
                        {"objects": {"object_label": count, "another_object": count, ...}}
                        Only include objects you actually detect.
                        """,
                    },
                ],
            },
        ]

        # Run model
        inputs = processor.apply_chat_template(
            conversation,
            add_generation_prompt=True,
            return_tensors="pt",
            return_dict=True,
            tokenize=True,
        ).to(model.device)

        outputs = model.generate(**inputs, max_new_tokens=200)
        detections_raw = processor.decode(outputs[0], skip_special_tokens=True)

        print("\n📥 Raw model output:", detections_raw)

        # Extract + merge JSONs
        detections = extract_and_merge_json(detections_raw)

        print("✅ Parsed detections:", detections)

        # Overlay detections on frame
        y0 = 30
        for i, (obj, count) in enumerate(detections.items()):
            text = f"{obj}: {count}"
            cv2.putText(frame, text, (10, y0 + i * 30),
                        cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)

        cv2.imshow("Smart Inventory Counter", frame)

    elif key == ord("q"):
        break

cap.release()
cv2.destroyAllWindows()
