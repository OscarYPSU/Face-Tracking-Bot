// HappyFace.h
#ifndef HappyFace_h
#define HappyFace_h
#include <SPI.h>
#include <Wire.h>
#include <Adafruit_GFX.h>
#include <Adafruit_SSD1306.h>
extern Adafruit_SSD1306 display; // Declare the display object as extern
// Function declarations
void happyFaceSetup();
void happyFaceLoop();

#endif