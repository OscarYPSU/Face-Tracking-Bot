#include "neutralFace.h"
#include "display.h"
#include "milis.h"


void neutralFaceSetUp(){
  //temproryu place holder
  display.clearDisplay();
  display.setTextSize(1);
  display.setTextColor(SSD1306_WHITE);
  display.setCursor(0,0);
  display.println("Neutral Face");
  display.display();
}

void neutralFaceLoop(){
}