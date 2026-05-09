#line 1 "/home/arduino/ArduinoApps/microwasteanimals/sketch/distance.h"
#pragma once
#include "Modulino.h"

ModulinoDistance distance;

const int DANGER_ZONE = 10;
const int WARNING_ZONE = 30;
const int CAUTION_ZONE = 50;
const int SAFE_ZONE = 100;

void distance_init() {
  Modulino.begin();
  distance.begin();
}

void getDistance() {
  if (distance.available()) {
    int measure = distance.get();
    if (measure < DANGER_ZONE) {
      Monitor.println("STOP! Too close!");
    } else if (measure < WARNING_ZONE) {
      Monitor.println("WARNING - Very close");
    } else if (measure < CAUTION_ZONE) {
      Monitor.println("CAUTION - Getting close");
    } else {
      Monitor.println("SAFE");
    }
  }
}