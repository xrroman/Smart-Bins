#include <Arduino.h>
#line 1 "/home/arduino/ArduinoApps/microwasteanimals/sketch/sketch.ino"
#include "distance.h"
#include "leds.h"
#include "buzzer.h"

int NUM_LOOP = 0;

#line 7 "/home/arduino/ArduinoApps/microwasteanimals/sketch/sketch.ino"
void setup();
#line 16 "/home/arduino/ArduinoApps/microwasteanimals/sketch/sketch.ino"
void loop();
#line 7 "/home/arduino/ArduinoApps/microwasteanimals/sketch/sketch.ino"
void setup() {
  Serial.begin(9600);
  Monitor.begin();
  Modulino.begin();
  distance_init();
  leds_init();
  buzzer_init();
}

void loop() {
  if( NUM_LOOP == 0) {
      playBuzz(NOTE_C4, 5000);
  }
  int measure = getDistance();
  if (measure < DIST_FULL) {
      setLeds(RED, 100);    // Rojo fijo si está lleno
  } else if (measure < DIST_MID) {
      setLeds(YELLOW, 50);  // Amarillo fijo si está a medias
  } else {
      setLeds(GREEN, 20);   // Verde fijo si está vacío
  }
  NUM_LOOP += 1;
  delay(100);
}
