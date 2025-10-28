#include <Adafruit_SSD1306.h>
#include <splash.h>
#include <SPI.h>
#include <Wire.h>
#include <Adafruit_GFX.h>
#include <Adafruit_SSD1306.h>

#include "servos.h"
#include "emotions.h"
#include "display.h"
#include "milis.h"

// sets up the miilis
unsigned long currentMilis = 0; 

// Create the display object
Adafruit_SSD1306 display(SCREEN_WIDTH, SCREEN_HEIGHT, &Wire, OLED_RESET);

void setup() {
  Serial.begin(9600);

  // OLED SETUP <----->
  if(!display.begin(SSD1306_SWITCHCAPVCC, SCREEN_ADDRESS)) {
    Serial.println(F("SSD1306 allocation failed"));
    while(1);
  } 
  // Clear the buffer
  display.clearDisplay();
  display.setTextSize(1);
  display.setTextColor(SSD1306_WHITE);
  display.setCursor(0,0);
  display.println("Starting Screen.....");
  display.display();
  neutralFaceSetUp();

  // servo setup <----->
  servoY.attach(8);
  servoX.attach(10);
  servoY.write(servoYPOS);
  servoX.write(servoXPOS);

}

void loop() {
  // servo functioanlity <----->
  if (Serial.available()) {
    String cmd = Serial.readStringUntil('\n');

    int emotionIndex = cmd.indexOf("EMO##");
    int getHungerIndex = cmd.indexOf("GETHUNGER##");
    if (emotionIndex != -1){ // if the data being sent over is emotion data
      // TO DO 
      if (cmd.substring(emotionIndex + 5) == "happy" && globalEmotion != "Happy"){ // wasnt happy emotion before, setup happy face
        globalEmotion = "Happy"; // global variable to set multhread funciton to start looping on the needed loop
        Serial.println("Setting oled screen to happy face");
      }
    } else { // else its position data
    Serial.print("Received: ");
    Serial.println(cmd);
    int yIndex = cmd.indexOf('Y');
    int xIndex = cmd.indexOf('X');
      if (yIndex != -1 && xIndex != -1) {
        // Lets us know we got signal
        int servoYPosAdd = cmd.substring(yIndex + 1, yIndex + 4).toInt();
        int servoXPosAdd = cmd.substring(xIndex + 1).toInt();
        servoYPOS += -(servoYPosAdd);
        servoXPOS +=  servoXPosAdd;

        // Keep servoYPOS in valid range
        servoYPOS = constrain(servoYPOS, 0, 180);
        servoXPOS = constrain(servoXPOS, 0, 180);

        Serial.println("Adding Y angle:");
        Serial.println("Y:");
        Serial.println(servoYPosAdd);
        Serial.println(servoYPOS);
        servoY.write(servoYPOS);
        Serial.println("Adding X angle:");
        Serial.println("X:");
        Serial.println(servoXPosAdd);
        Serial.println(servoXPOS);
        servoX.write(servoXPOS);
      }
    }
  }

}