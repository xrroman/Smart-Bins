#include <Arduino.h>
#line 1 "/home/arduino/ArduinoApps/microwasteanimals/sketch/sketch.ino"
#include "distance.h"

#line 3 "/home/arduino/ArduinoApps/microwasteanimals/sketch/sketch.ino"
void setup();
#line 8 "/home/arduino/ArduinoApps/microwasteanimals/sketch/sketch.ino"
void loop();
#line 3 "/home/arduino/ArduinoApps/microwasteanimals/sketch/sketch.ino"
void setup() {
  Monitor.begin();
  distance_init();
}

void loop() {
  getDistance();
  delay(100);
}
