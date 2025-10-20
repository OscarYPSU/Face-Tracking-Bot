#include <Adafruit_SSD1306.h>
#include <splash.h>

#include <SPI.h>
#include <Wire.h>
#include <Adafruit_GFX.h>
#include <Adafruit_SSD1306.h>

#include "HappyFace.h" // This one include pulls in everything we need
#include "angryFace.h"
#include "display.h"
#include "study.h"
#include "talkFace.h"
#include "neutralFace.h"
#include "milis.h"

// sets up the miilis
unsigned long currentMilis = 0; 


// tachi
// Pet stats
int hunger = 50;      // 0 = full, 100 = starving
int health = 100;     // 0 = dead, 100 = healthy
int sleepiness = 0;   // 0 = wide awake, 100 = exhausted
int happiness = 80; // 0 = Depressed, 50 = content, 100 = happy
// also want to add statuses
int age = 0; // add a age system

// Time tracking for each stat
unsigned long lastHungerUpdate = 0;
unsigned long lastHealthUpdate = 0;
unsigned long lastHappinessUpdate = 0;
unsigned long lastAgeUpdate = 0;

// interval for each stat
const unsigned long healthUpdateInterval = 60000; // 1 minutes
const unsigned long hungerUpdateInterval = 600000; // 10 minutes
const unsigned long happinessUpdateInterval = 300000; // 5 minutes
const unsigned long ageUpdateInterval = 1200000; // 20 minutes

// Create the display object
Adafruit_SSD1306 display(SCREEN_WIDTH, SCREEN_HEIGHT, &Wire, OLED_RESET);

void setup() {
  Serial.begin(9600);
  
  // Initialize the OLED display
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
}

void loop() {
  unsigned long currentMilis = millis();
  // hunger update interval
  if (currentMilis - lastHungerUpdate >= hungerUpdateInterval){
    lastHungerUpdate = currentMilis;
    hunger -= 1;
    Serial.println("Current Hunger: " + String(hunger));

    // clamps hunger so it doesnt go below 0
    if (hunger < 0){
      hunger = 0;
    }
  }
}