from arduino.app_utils import App, Bridge
from arduino.app_bricks.web_ui import WebUI
from arduino.app_bricks.video_objectdetection import VideoObjectDetection
from datetime import datetime, UTC
from collections import defaultdict
import time
import requests

ANIMAL_LABELS        = {"rubber-ducky"}
WASTE_LABELS         = {"verde": 1, "amarillo": 2, "azul": 3}
API_ENDPOINT         = "https://backend-production-1353.up.railway.app/api/update-bin"
API_HEADERS          = {"Content-Type": "application/json"}

FULL_BIN_MM          = 100
HALF_BIN_MM          = 250
ALERT_DURATION       = 10
BUZZ_FREQ            = 262
TRIGGER_COUNT_ANIMAL = 15
TRIGGER_COUNT_WASTE  = 5

alert_until          = 0
animal_led_on        = False
waste_led_code       = 0
label_counters       = defaultdict(int)

ui               = WebUI()
detection_stream = VideoObjectDetection(confidence=0.5, debounce_sec=0.0)

def _reset_counters():
    label_counters.clear()

def _set_alert():
    global alert_until, animal_led_on
    alert_until   = time.time() + ALERT_DURATION
    animal_led_on = True
    try:
        Bridge.call("setAnimalLed", 1, timeout=3)
        Bridge.call("setBuzzer", BUZZ_FREQ, 500, timeout=3)
    except Exception as e:
        print(f"Bridge error (alert): {e}")

def _clear_alert():
    global animal_led_on
    if not animal_led_on:
        return
    try:
        Bridge.call("setAnimalLed", 0, timeout=3)
        animal_led_on = False  # solo actualizar si tuvo éxito
    except Exception as e:
        print(f"Bridge error (clear alert): {e}")
        time.sleep(0.5)

def _set_waste_led(code: int):
    global waste_led_code
    if waste_led_code == code:
        return
    try:
        Bridge.call("setWasteLed", code, timeout=3)
        waste_led_code = code  # solo actualizar si tuvo éxito
    except Exception as e:
        print(f"Bridge error (waste led): {e}")
        time.sleep(0.5)

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
        trigger = None

        if label in ANIMAL_LABELS:
            trigger = TRIGGER_COUNT_ANIMAL
        elif label in WASTE_LABELS:
            trigger = TRIGGER_COUNT_WASTE

        if trigger is not None:
            label_counters[label] += 1
            print(f"[counter] {label}: {label_counters[label]}/{trigger}")

            if label_counters[label] >= trigger:
                print(f"[trigger] {label} fired!")
                _reset_counters()

                if label in ANIMAL_LABELS:
                    _set_alert()

                if label in WASTE_LABELS:
                    _set_waste_led(WASTE_LABELS[label])

def _override_th(sid, threshold):
    try:
        detection_stream.override_threshold(threshold)
    except Exception as e:
        print(f"override_th error (ignored): {e}")

ui.on_message("override_th", _override_th)
detection_stream.on_detect_all(_on_detections)

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
    _set_waste_led(0)

App.run(user_loop=loop)