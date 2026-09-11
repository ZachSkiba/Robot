#include <Arduino.h>

void setup() {
    Serial.begin(115200);
    delay(1000);
    Serial.println("Teensy 4.1 firmware online");
}

void loop() {
    static uint32_t last_ms = 0;

    if (millis() - last_ms >= 1000) {
        last_ms = millis();
        Serial.println("Teensy 4.1 heartbeat");
    }
}
