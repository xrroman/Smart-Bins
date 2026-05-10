from arduino.app_utils import App, Bridge
from arduino.app_bricks.web_ui import WebUI
from arduino.app_bricks.video_objectdetection import VideoObjectDetection
from datetime import datetime, UTC
from collections import defaultdict
import time
import requests

ANIMAL_LABELS  = {"rubber-ducky"}
WASTE_LABELS   = {"verde": 1, "amarillo": 2, "azul": 3}
API_ENDPOINT   = "https://backend-production-1353.up.railway.app/api/update-bin"
API_HEADERS    = {"Content-Type": "application/json"}

FULL_BIN_MM    = 100
HALF_BIN_MM    = 250
ALERT_DURATION = 10
BUZZ_FREQ      = 262
TRIGGER_COUNT  = 10

alert_until    = 0
label_counters = defaultdict(int)

ui               = WebUI()
detection_stream = VideoObjectDetection(confidence=0.5, debounce_sec=0.0)

# ── helpers ──────────────────────────────────────────────────────────────────

def _reset_counters():
    label_counters.clear()

def _set_alert():
    global alert_until
    alert_until = time.time() + ALERT_DURATION
    try:
        Bridge.call("setAnimalLed", 1, timeout=3)
        Bridge.call("setBuzzer", BUZZ_FREQ, 500, timeout=3)
    except Exception as e:
        print(f"Bridge error (alert): {e}")

def _clear_alert():
    try:
        Bridge.call("setAnimalLed", 0, timeout=3)
    except Exception as e:
        print(f"Bridge error (clear alert): {e}")

def _post_distance(measure: int):
    try:
        res = requests.post(
            API_ENDPOINT,
            headers=API_HEADERS,
            json={"id": "1", "postDistance": measure},
            timeout=5,
        )
        print(f"API response: {res.status_code} {res.text}")
    except requests.exceptions.Timeout:
        print("API error: timeout")
    except requests.exceptions.ConnectionError:
        print("API error: connection refused")
    except Exception as e:
        print(f"API error: {e}")

# ── detections ────────────────────────────────────────────────────────────────

def _on_detections(detections: dict):
    for key, values in detections.items():
        for value in values:
            try:
                ui.send_message("detection", {
                    "content":    key,
                    "confidence": value.get("confidence"),
                    "timestamp":  datetime.now(UTC).isoformat(),
                })
            except Exception as e:
                print(f"UI error: {e}")

        label = key.lower()
        if label in ANIMAL_LABELS or label in WASTE_LABELS:
            label_counters[label] += 1
            print(f"[counter] {label}: {label_counters[label]}/{TRIGGER_COUNT}")

            if label_counters[label] >= TRIGGER_COUNT:
                print(f"[trigger] {label} fired!")
                _reset_counters()

                if label in ANIMAL_LABELS:
                    _set_alert()

                if label in WASTE_LABELS:
                    try:
                        Bridge.call("setWasteLed", WASTE_LABELS[label], timeout=3)
                    except Exception as e:
                        print(f"Bridge error (waste led): {e}")

def _override_th(sid, threshold):
    try:
        detection_stream.override_threshold(threshold)
    except Exception as e:
        print(f"override_th error (ignored): {e}")

ui.on_message("override_th", _override_th)
detection_stream.on_detect_all(_on_detections)

# ── main loop ─────────────────────────────────────────────────────────────────

def loop():
    time.sleep(2)

    measure = None
    try:
        measure = Bridge.call("getMeasure", timeout=3)
    except Exception as e:
        print(f"getMeasure timeout/error (skipping): {e}")

    if measure is not None:
        try:
            ui.send_message("distance", {"value": measure, "unit": "mm"})
        except Exception as e:
            print(f"UI error (distance): {e}")
        _post_distance(measure)

    if time.time() < alert_until:
        try:
            Bridge.call("setBuzzer", BUZZ_FREQ, 500, timeout=3)
        except Exception as e:
            print(f"Bridge error (buzz loop): {e}")
        return

    _clear_alert()

    try:
        Bridge.call("setWasteLed", 0, timeout=3)
    except Exception as e:
        print(f"Bridge error (waste off): {e}")

App.run(user_loop=loop)