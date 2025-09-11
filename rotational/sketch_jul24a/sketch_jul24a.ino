#include <Servo.h>
#include <Wire.h>
#include <Adafruit_GFX.h>
#include <Adafruit_SSD1306.h>

#define SCREEN_WIDTH 128
#define SCREEN_HEIGHT 64
#define OLED_ADDR 0x3C


Servo servoX;
Servo servoY;

int servoYPOS = 60;
int servoXPOS = 90;
int ledPin = 9;

Adafruit_SSD1306 display(SCREEN_WIDTH, SCREEN_HEIGHT, &Wire);

void drawAnimeDevil(int frame) {
  display.clearDisplay();

  // Head
  display.drawCircle(64, 32, 25, SSD1306_WHITE);

  // Horns (curved, anime style)
  display.drawLine(48, 10, 53, 0, SSD1306_WHITE); // left horn
  display.drawLine(53, 0, 58, 10, SSD1306_WHITE);
  display.drawLine(80, 10, 75, 0, SSD1306_WHITE); // right horn
  display.drawLine(75, 0, 70, 10, SSD1306_WHITE);

  // Angry anime eyes
  int eyeOffsetY = (frame % 10 == 0) ? 1 : 0; // small blink effect
  display.drawLine(54, 28+eyeOffsetY, 60, 24+eyeOffsetY, SSD1306_WHITE); // left top slant
  display.drawLine(66, 24+eyeOffsetY, 72, 28+eyeOffsetY, SSD1306_WHITE); // right top slant
  display.fillCircle(57, 26+eyeOffsetY, 2, SSD1306_WHITE); // left pupil
  display.fillCircle(69, 26+eyeOffsetY, 2, SSD1306_WHITE); // right pupil

  // Eyebrows (slanted down)
  display.drawLine(52, 22, 60, 24, SSD1306_WHITE); // left
  display.drawLine(66, 24, 74, 22, SSD1306_WHITE); // right

  // Mouth (fanged anime style)
  display.drawLine(56, 42, 72, 42, SSD1306_WHITE); // top line
  display.drawLine(56, 42, 56, 44, SSD1306_WHITE); // left fang
  display.drawLine(72, 42, 72, 44, SSD1306_WHITE); // right fang
  display.drawLine(57, 44, 71, 44, SSD1306_WHITE); // bottom line of mouth

  // Simple flame flicker below face
  for (int i = 0; i < 3; i++) {
    int fx = 60 + i*8;
    int fy = 50 + ((frame + i*2) % 4);
    display.drawPixel(fx, fy, SSD1306_WHITE);
  }

  display.display();
}



void setup() {
  Serial.begin(9600);
  servoY.attach(8);
  servoX.attach(10);

  // initial servo position
  servoY.write(servoYPOS);
  servoX.write(servoXPOS);
  
  display.begin(SSD1306_SWITCHCAPVCC, OLED_ADDR);
}

void loop() {
  static int frame = 0;
  drawAnimeDevil(frame);
  frame++;
  if (Serial.available()) {
    
    String cmd = Serial.readStringUntil('\n');
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
