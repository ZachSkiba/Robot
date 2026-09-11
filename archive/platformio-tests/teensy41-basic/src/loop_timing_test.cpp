#include <Arduino.h>
#include "loop_timing_test.h"

constexpr uint8_t LED_PIN = LED_BUILTIN;
constexpr uint32_t TEST_DURATION_MS = 5000;

void runLoopTimingTest()
{
    pinMode(LED_PIN, OUTPUT);
    digitalWrite(LED_PIN, LOW);

    Serial.println("=== Teensy Loop Timing Test ===");
    Serial.println("Measuring loop execution and timing jitter...");

    uint32_t start = micros();
    uint32_t lastTimestamp = start;
    uint32_t lastToggle = start;
    uint32_t loopCount = 0;
    uint32_t maxDelta = 0;
    uint32_t minDelta = UINT32_MAX;

    while ((micros() - start) < (TEST_DURATION_MS * 1000UL))
    {
        uint32_t now = micros();
        uint32_t delta = now - lastTimestamp;

        if (delta > maxDelta)
        {
            maxDelta = delta;
        }
        if (delta < minDelta)
        {
            minDelta = delta;
        }

        lastTimestamp = now;
        loopCount++;

        if (now - lastToggle >= 250000UL)
        {
            lastToggle = now;
            digitalWrite(LED_PIN, !digitalRead(LED_PIN));
        }
    }

    Serial.print("loop_count=");
    Serial.println(loopCount);
    Serial.print("min_loop_us=");
    Serial.println(minDelta);
    Serial.print("max_loop_us=");
    Serial.println(maxDelta);
    Serial.println("Loop timing test complete.");
    digitalWrite(LED_PIN, LOW);
}
