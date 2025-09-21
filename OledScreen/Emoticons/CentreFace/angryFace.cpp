#include "angryFace.h"
#include "display.h"

void angryFaceSetup(){
  display.clearDisplay();
  display.drawCircle(64,32,20, SSD1306_WHITE);
  // Show the display buffer on the screen
  display.display();
}