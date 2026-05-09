#line 1 "/home/arduino/ArduinoApps/microwasteanimals/sketch/leds.h"
#pragma once
#include <Modulino.h>

ModulinoPixels leds;

const int NUM_LEDS = 8;

void leds_init() {
  leds.begin();
}

void setLeds(ModulinoColor c, int brightness = 50) {
  for (int i = 0; i < NUM_LEDS; i++) {
    leds.set(i, c, brightness);
  }
  leds.show();
}

void turnOffLeds() {
  for (int i = 0; i < NUM_LEDS; i++) {
    leds.set(i, WHITE, 0);
  }
  leds.show();
}