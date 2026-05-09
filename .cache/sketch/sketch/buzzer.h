#line 1 "/home/arduino/ArduinoApps/microwasteanimals/sketch/buzzer.h"
#pragma once
#include <Modulino.h>

ModulinoBuzzer buzzer;

#define NOTE_C4  262
int note = NOTE_C4;
int time = 4;

void buzzer_init() {
  buzzer.begin();
}

void playBuzz(int note, int time) {
    buzzer.tone(note, time);
}
