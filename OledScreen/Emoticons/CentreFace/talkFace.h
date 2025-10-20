#ifndef talkFaceH
#define talkFaceH

#include <Adafruit_GFX.h>
#include <Adafruit_SSD1306.h>
extern Adafruit_SSD1306 display; // Declare the display object as extern 
void talkFaceSetup();
void talkFaceLoop();

#endif