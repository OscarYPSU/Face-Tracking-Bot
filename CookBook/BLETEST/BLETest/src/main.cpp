#include <Arduino.h>
#include <BLEDevice.h>
#include <BLEUtils.h>
#include <BLEServer.h>

#define LED_PIN 40 // Define our GPIO pin

// 2. Callback Class: This is the "brain" that reacts to your phone
class MyCallbacks: public BLECharacteristicCallbacks {
    void onWrite(BLECharacteristic *pCharacteristic) {
      std::string value = pCharacteristic->getValue();

      if (value.length() > 0) {
        char command = value[0];
        Serial.print("Received Value: ");
        Serial.println(command);

        // Logic to toggle the LED based on the message
        if (command == '1') {
          digitalWrite(LED_PIN, HIGH);
          Serial.println("Action: LED ON 💡");
        } else if (command == '0') {
          digitalWrite(LED_PIN, LOW);
          Serial.println("Action: LED OFF 🌑");
        }
      }
    }
};

// Global pointers so we can reference them if needed
BLECharacteristic *pCharacteristic;

void setup() {
  Serial.begin(115200);
  BLEDevice::init("ESP32-S3");
  BLEServer *pServer = BLEDevice::createServer();
  BLEService *pService = pServer->createService("4fafc201-1fb5-459e-8fcc-c5c9c331914b");

  // Create the characteristic BEFORE starting the service
  BLECharacteristic *pCharacteristic = pService->createCharacteristic(
    "beb5483e-36e1-4688-b7f5-ea07361b26a8",
    BLECharacteristic::PROPERTY_READ |
    BLECharacteristic::PROPERTY_WRITE
  );

  // Link our Callback class to the characteristic
  pCharacteristic->setCallbacks(new MyCallbacks());

  // Set initial value
  pCharacteristic->setValue("Send 1 or 0");
  
  pService->start(); // Now we "open the doors"

  // Start Advertising
  BLEAdvertising *pAdvertising = BLEDevice::getAdvertising();
  pAdvertising->addServiceUUID("4fafc201-1fb5-459e-8fcc-c5c9c331914b");
  pAdvertising->setScanResponse(true);
  BLEDevice::startAdvertising();
  Serial.println("Characteristic defined! Now advertising...");

  // turns and connect to led
  pinMode(LED_PIN, OUTPUT);
  digitalWrite(LED_PIN, LOW);
}

void loop() {
  // put your main code here, to run repeatedly:

}
