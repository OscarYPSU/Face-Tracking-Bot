#include <SPI.h>
#include <Wire.h>
#include <Adafruit_GFX.h>
#include <Adafruit_SSD1306.h>

#include "HappyFace.h" // This one include pulls in everything we need
#include "angryFace.h"
#include "display.h"

// Create the display object
Adafruit_SSD1306 display(SCREEN_WIDTH, SCREEN_HEIGHT, &Wire, OLED_RESET);

void setup() {
  Serial.begin(9600);
  
  // Initialize the OLED display
  if(!display.begin(SSD1306_SWITCHCAPVCC, SCREEN_ADDRESS)) {
    Serial.println(F("SSD1306 allocation failed"));
    for(;;); // Don't proceed, loop forever
  }
  
  // Clear the buffer
  display.clearDisplay();
  
	display.setTextSize(1);
	display.println("Screen");
  display.println("Starting...");
  
  // Actually display the text on screen
  display.display();
  
}

void loop() {
}