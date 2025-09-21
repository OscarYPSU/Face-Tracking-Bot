// HappyFace.cpp
#include "HappyFace.h"
#include "display.h"

// Smiley face dimensions
const int faceRadius = 20;
const int faceX = SCREEN_WIDTH / 2;
const int faceY = SCREEN_HEIGHT / 2;
const int eyeRadius = 4;
const int eyeOffsetX = 8;
const int eyeOffsetY = 8;
const int smileWidth = 24;
const int smileHeight = 10;
const int smileYOffset = 6;

// Animation variables
unsigned long animationTimer = 0;
unsigned long blinkTimer = 0;
bool blinking = false;

// Function to draw a smile (arc)
void drawSmile(int x, int y, int width, int height, int yOffset) {
  int startX = x - width/2;
  int endX = x + width/2;
  int centerY = y + yOffset;
  
  for (int i = 0; i < width; i += 2) {
    int currentX = startX + i;
    int smileY = centerY + height * (1 - pow((2.0 * (currentX - x) / width), 2));
    display.drawPixel(currentX, smileY, SSD1306_WHITE);
    display.drawPixel(currentX+1, smileY, SSD1306_WHITE);
  }
}

void happyFaceSetup() {
  Serial.begin(9600);
  
  if(!display.begin(SSD1306_SWITCHCAPVCC, SCREEN_ADDRESS)) {
    Serial.println(F("SSD1306 allocation failed"));
    for(;;);
  }
  
  display.clearDisplay();
  
  // Display startup message
  display.setTextSize(1);
  display.setTextColor(SSD1306_WHITE);
  display.setCursor(10, 20);
  display.println(F("Smiley Face"));
  display.setCursor(10, 40);
  display.println(F("Initializing..."));
  display.display();
  delay(2000);
  
  display.clearDisplay();
}

void happyFaceLoop() {
  animationTimer++;
  
  blinkTimer++;
  if (blinkTimer > 20 || blinking) {
    if (!blinking) {
      blinking = true;
      blinkTimer = 0;
    } else if (blinkTimer > 5) {
      blinking = false;
      blinkTimer = 0;
    }
  }
  
  display.clearDisplay();
  display.drawCircle(faceX, faceY, faceRadius, SSD1306_WHITE);
  
  if (!blinking) {
    display.fillCircle(faceX - eyeOffsetX, faceY - eyeOffsetY, eyeRadius, SSD1306_WHITE);
    display.fillCircle(faceX + eyeOffsetX, faceY - eyeOffsetY, eyeRadius, SSD1306_WHITE);
  }
  
  int smileOffset = sin(animationTimer * 0.1) * 2;
  drawSmile(faceX, faceY, smileWidth, smileHeight, smileYOffset + smileOffset);
  
  display.display();
  delay(50);
}