#include <Servo.h>
#include <Wire.h>


Servo servoX;
Servo servoY;

int servoYPOS = 60;
int servoXPOS = 90;
int ledPin = 9;
String globalEmotion = "";


void setup() {
  Serial.begin(9600);
  servoY.attach(8);
  servoX.attach(10);

  // initial servo position
  servoY.write(servoYPOS);
  servoX.write(servoXPOS);

}

void loop() {
  //static int frame = 0;
  //drawAnimeDevil(frame);
  //frame++;

  if (Serial.available()) {
    String cmd = Serial.readStringUntil('\n');

    int emotionIndex = cmd.indexOf("EMO##");
    if (emotionIndex != -1){ // if the data being sent over is emotion data
      // TO DO 
      if (cmd.substring(emotionIndex + 5) == "happy" && globalEmotion != "Happy"){ // wasnt happy emotion before, setup happy face
        happyFaceSetup();
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
