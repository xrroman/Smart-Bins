#include <Arduino.h>
#line 1 "/home/arduino/ArduinoApps/microwasteanimals/sketch/sketch.ino"
#include "distance.h"
#include "leds.h"
#include "buzzer.h"
#include <Arduino_RouterBridge.h>

int lastMeasure = 0;

#line 8 "/home/arduino/ArduinoApps/microwasteanimals/sketch/sketch.ino"
int getMeasure();
#line 9 "/home/arduino/ArduinoApps/microwasteanimals/sketch/sketch.ino"
void setBuzzer(int note, int duration);
#line 10 "/home/arduino/ArduinoApps/microwasteanimals/sketch/sketch.ino"
void setAnimalLedFromPython(int on);
#line 11 "/home/arduino/ArduinoApps/microwasteanimals/sketch/sketch.ino"
void setWasteLedFromPython(int colorCode);
#line 13 "/home/arduino/ArduinoApps/microwasteanimals/sketch/sketch.ino"
void setup();
#line 26 "/home/arduino/ArduinoApps/microwasteanimals/sketch/sketch.ino"
void loop();
#line 8 "/home/arduino/ArduinoApps/microwasteanimals/sketch/sketch.ino"
int getMeasure() { return lastMeasure; }
void setBuzzer(int note, int duration) { playBuzz(note, duration); }
void setAnimalLedFromPython(int on) { setAnimalLed(on == 1); }
void setWasteLedFromPython(int colorCode) { setWasteLed(colorCode); }

void setup() {
  Monitor.begin();
  Modulino.begin();
  Bridge.begin();
  Bridge.provide("getMeasure",   getMeasure);
  Bridge.provide("setBuzzer",    setBuzzer);
  Bridge.provide("setAnimalLed", setAnimalLedFromPython);
  Bridge.provide("setWasteLed",  setWasteLedFromPython);
  distance_init();
  leds_init();
  buzzer_init();
}

void loop() {
  if (distance.available()) {
    lastMeasure = distance.get();
  }
  delay(100);
}
