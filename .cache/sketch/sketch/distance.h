#line 1 "/home/arduino/ArduinoApps/microwasteanimals/sketch/distance.h"
#pragma once
#include "Modulino.h"

ModulinoDistance distance;

const int DIST_EMPTY = 450;
const int DIST_MID   = 250;
const int DIST_FULL  = 100;

void distance_init() {
  distance.begin();
}

int getDistance() {
  int measure = 999; // Default value
  
  if (distance.available()) {
    measure = distance.get();
    if (measure >= DIST_EMPTY) {
      Monitor.println("EMPTY - Bin is empty");
    } else if (measure >= DIST_MID) {
      Monitor.println("MID - Bin is half full");
    } else if (measure >= DIST_FULL) {
      Monitor.println("FULL - Bin getting full");
    } else {
      Monitor.println("ALERT - No more space");
    }
  }
  return measure;
}