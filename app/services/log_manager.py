import os
import json
from datetime import datetime

LOG_FILE = "detections_log.json"


def _read_log() -> list:
    """Read detections log as list."""
    if not os.path.exists(LOG_FILE):
        return []
    with open(LOG_FILE, "r", encoding="utf-8") as f:
        try:
            return json.load(f)
        except json.JSONDecodeError:
            return []


def _write_log(data: list) -> None:
    """Write detections log safely."""
    with open(LOG_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2)


def save_detections(detections: dict) -> None:
    """
    Save detections to log.
    If an object already exists, increment count and update timestamp.
    Otherwise, insert as new entry.

    detections = {"bottle": 2, "box": 1}
    """
    log = _read_log()
    now = datetime.utcnow().isoformat()

    for label, count in detections.items():
        existing = next((item for item in log if item["label"] == label), None)
        if existing:
            existing["total"] += count
            existing["timestamp"] = now
        else:
            log.append({
                "timestamp": now,
                "label": label,
                "total": count
            })

    _write_log(log)
    print(f"✅ Saved {len(detections)} items to detections_log.json")


def remove_item(label: str) -> None:
    """Remove all entries of a given label."""
    log = _read_log()
    updated = [item for item in log if item["label"].lower() != label.lower()]
    _write_log(updated)
    print(f"❌ Removed '{label}' from detections_log.json")


def clear_detections() -> None:
    """Clear the entire detections log."""
    _write_log([])
    print("🗑️ detections_log.json cleared!")


def load_detections() -> list:
    """Return all saved detections as a list of dicts."""
    return _read_log()


def get_summary() -> dict:
    """
    Return a dictionary summary of totals.
    Example: {"bottle": 5, "box": 2}
    """
    log = _read_log()
    summary = {}
    for item in log:
        summary[item["label"]] = summary.get(item["label"], 0) + item["total"]
    return summary
