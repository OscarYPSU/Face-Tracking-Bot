#include <SPI.h>
#include <Wire.h>
#include <Adafruit_GFX.h>
#include <Adafruit_SSD1306.h>

#include "HappyFace.h" // This one include pulls in everything we need

void setup() {
  happyFaceSetup();
}

void loop() {
  happyFaceLoop();
}