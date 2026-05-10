#line 1 "/home/arduino/ArduinoApps/microwasteanimals/sketch/leds.h"
#pragma once
#include <Modulino.h>

// 4 módulos Pixels independientes
ModulinoPixels leds_animal;   // addr 0 - alerta depredador
ModulinoPixels leds_green;    // addr 1 - label verde
ModulinoPixels leds_yellow;   // addr 2 - label amarillo
ModulinoPixels leds_blue;     // addr 3 - label azul

const int NUM_LEDS = 8;

void leds_init() {
  leds_animal.begin();
  leds_green.begin();
  leds_yellow.begin();
  leds_blue.begin();
}

void _fill(ModulinoPixels& strip, ModulinoColor c, int brightness) {
  for (int i = 0; i < NUM_LEDS; i++) strip.set(i, c, brightness);
  strip.show();
}

void _off(ModulinoPixels& strip) {
  for (int i = 0; i < NUM_LEDS; i++) strip.set(i, 0, 0, 0);
  strip.show();
}

// Pixels 0 - animal alert
void setAnimalLed(bool on) {
  on ? _fill(leds_animal, RED, 100) : _off(leds_animal);
}

// Pixels 1,2,3 - waste labels
// colorCode: 0=off, 1=verde, 2=amarillo, 3=azul
void setWasteLed(int colorCode) {
  _off(leds_green);
  _off(leds_yellow);
  _off(leds_blue);
  switch (colorCode) {
    case 1: _fill(leds_green,  GREEN,  80); break;
    case 2: _fill(leds_yellow, YELLOW, 80); break;
    case 3: _fill(leds_blue,   BLUE,   80); break;
  }
}

void turnOffLeds() {
  _off(leds_animal);
  _off(leds_green);
  _off(leds_yellow);
  _off(leds_blue);
}