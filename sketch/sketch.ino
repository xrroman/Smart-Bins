#include "distance.h"

void setup() {
  Monitor.begin();
  distance_init();
}

void loop() {
  getDistance();
  delay(100);
}