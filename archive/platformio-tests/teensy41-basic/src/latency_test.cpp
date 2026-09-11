#include <Arduino.h>
#include "latency_test.h"

constexpr uint8_t LED_PIN = LED_BUILTIN;
constexpr uint32_t TEST_DURATION_US = 10'000'000UL;
constexpr uint32_t LED_PERIOD_US = 250'000UL;

void runLatencyBenchmark()
{
    pinMode(LED_PIN, OUTPUT);
    digitalWrite(LED_PIN, LOW);

    Serial.println("=== Teensy Latency Test ===");
    Serial.println("Measuring loop cadence with micros()...");

    uint32_t start = micros();
    uint32_t lastSample = start;
    uint32_t lastToggle = start;
    uint32_t iterations = 0;
    uint64_t totalLoopUs = 0;
    uint32_t minLoopUs = UINT32_MAX;
    uint32_t maxLoopUs = 0;

    while ((micros() - start) < TEST_DURATION_US)
    {
        uint32_t now = micros();
        uint32_t loopDeltaUs = now - lastSample;

        if (loopDeltaUs < minLoopUs)
        {
            minLoopUs = loopDeltaUs;
        }

        if (loopDeltaUs > maxLoopUs)
        {
            maxLoopUs = loopDeltaUs;
        }

        totalLoopUs += loopDeltaUs;
        lastSample = now;
        iterations++;

        if ((now - lastToggle) >= LED_PERIOD_US)
        {
            lastToggle = now;
            digitalWrite(LED_PIN, !digitalRead(LED_PIN));
        }
    }

    uint32_t totalDurationUs = micros() - start;
    uint32_t avgLoopUs = iterations > 0 ? (uint32_t)(totalLoopUs / iterations) : 0;

    Serial.println();
    Serial.println("=== TEST SUMMARY ===");
    Serial.print("Duration:       ");
    Serial.print(totalDurationUs / 1000000.0f, 2);
    Serial.println(" s");
    Serial.print("Iterations:     ");
    Serial.println(iterations);
    Serial.print("Average loop:   ");
    Serial.print(avgLoopUs);
    Serial.println(" us");
    Serial.print("Min loop:       ");
    Serial.print(minLoopUs);
    Serial.println(" us");
    Serial.print("Max loop:       ");
    Serial.print(maxLoopUs);
    Serial.println(" us");
    Serial.println();
    Serial.println("=== TEST COMPLETE ===");

    digitalWrite(LED_PIN, LOW);
}
