#include <Arduino.h>
#include "serial_throughput_test.h"

constexpr uint32_t REPORT_EVERY_MS = 1000;

void runSerialThroughputTest()
{
    Serial.println("=== Teensy Serial Throughput Test ===");
    Serial.println("Sending fixed-size packets every 10 ms...");

    uint32_t start = millis();
    uint32_t lastReport = start;
    uint32_t packets = 0;
    uint32_t bytesSent = 0;

    while (millis() - start < 10000UL)
    {
        uint32_t now = millis();

        if (now % 10 == 0)
        {
            Serial.print("PKT");
            Serial.print(packets);
            Serial.print("|");
            Serial.print(millis());
            Serial.print("|");
            Serial.println("0123456789ABCDEF");

            packets++;
            bytesSent += 28;
        }

        if (now - lastReport >= REPORT_EVERY_MS)
        {
            lastReport = now;
            Serial.print("throughput_report | packets=");
            Serial.print(packets);
            Serial.print(" | bytes=");
            Serial.println(bytesSent);
        }
    }

    Serial.println("Serial throughput test complete.");
}
