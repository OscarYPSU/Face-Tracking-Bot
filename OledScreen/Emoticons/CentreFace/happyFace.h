// HappyFace.h
#ifndef HappyFace_h
#define HappyFace_h

#include <Arduino.h>
#include <SPI.h>
#include <Wire.h>
#include <Adafruit_GFX.h>
#include <Adafruit_SSD1306.h>

// OLED display dimensions
#define SCREEN_WIDTH 128
#define SCREEN_HEIGHT 64

// Declaration for SSD1306 display
#define OLED_RESET     -1
#define SCREEN_ADDRESS 0x3C
extern Adafruit_SSD1306 display; // Declare the display object as extern

// Function declarations
void happyFaceSetup();
void happyFaceLoop();

#endif