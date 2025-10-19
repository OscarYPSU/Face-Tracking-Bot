#ifndef studyH
#define studyH
#include <SPI.h>
#include <Wire.h>
#include <Adafruit_GFX.h>
#include <Adafruit_SSD1306.h>
extern Adafruit_SSD1306 display; // Declare the display object as extern
// Function declarations
void studySetup();
void studyLoop();

#endif