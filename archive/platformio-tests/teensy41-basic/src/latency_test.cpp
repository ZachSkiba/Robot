```cpp
#include <Arduino.h>
#include "latency_test.h"

// ============================================================
// TEST SETTINGS
// ============================================================

constexpr uint8_t LED_PIN = LED_BUILTIN;

constexpr uint32_t TEST_DURATION_US = 10'000'000UL;  // 10 seconds
constexpr uint32_t LED_PERIOD_US = 250'000UL;        // 250 ms

// Teensy 4.1 runs at 600 MHz by default.
// 600 MHz = 600 cycles per microsecond.
constexpr double CPU_MHZ = 600.0;

// ============================================================
// LATENCY BENCHMARK
// ============================================================

void runLatencyBenchmark()
{
    pinMode(LED_PIN, OUTPUT);
    digitalWrite(LED_PIN, LOW);

    Serial.println("=== Teensy Latency Test ===");
    Serial.println("Measuring loop timing with ARM cycle counter...");
    Serial.println();

    // --------------------------------------------------------
    // Initialize ARM DWT cycle counter
    // --------------------------------------------------------

    ARM_DEMCR |= ARM_DEMCR_TRCENA;
    ARM_DWT_CTRL |= ARM_DWT_CTRL_CYCCNTENA;
    ARM_DWT_CYCCNT = 0;

    // --------------------------------------------------------
    // Start test
    // --------------------------------------------------------

    uint32_t startMicros = micros();
    uint32_t lastToggleMicros = startMicros;

    uint32_t startCycles = ARM_DWT_CYCCNT;

    uint32_t iterations = 0;

    uint32_t minCycles = UINT32_MAX;
    uint32_t maxCycles = 0;

    uint64_t totalCycles = 0;

    uint32_t previousCycles = ARM_DWT_CYCCNT;

    // --------------------------------------------------------
    // Main benchmark loop
    // --------------------------------------------------------

    while ((micros() - startMicros) < TEST_DURATION_US)
    {
        uint32_t currentCycles = ARM_DWT_CYCCNT;

        uint32_t loopCycles = currentCycles - previousCycles;

        previousCycles = currentCycles;

        // Track timing statistics.
        if (loopCycles < minCycles)
        {
            minCycles = loopCycles;
        }

        if (loopCycles > maxCycles)
        {
            maxCycles = loopCycles;
        }

        totalCycles += loopCycles;
        iterations++;

        // ----------------------------------------------------
        // Toggle LED every 250 ms.
        // This proves the processor is still running normally.
        // ----------------------------------------------------

        uint32_t nowMicros = micros();

        if ((nowMicros - lastToggleMicros) >= LED_PERIOD_US)
        {
            lastToggleMicros = nowMicros;
            digitalWrite(LED_PIN, !digitalRead(LED_PIN));
        }
    }

    // --------------------------------------------------------
    // Calculate final measurements
    // --------------------------------------------------------

    uint32_t endCycles = ARM_DWT_CYCCNT;
    uint32_t totalDurationUs = micros() - startMicros;

    uint32_t totalCyclesMeasured = endCycles - startCycles;

    double averageCycles = 0.0;

    if (iterations > 0)
    {
        averageCycles =
            static_cast<double>(totalCycles) /
            static_cast<double>(iterations);
    }

    // Convert CPU cycles to nanoseconds.
    //
    // At 600 MHz:
    //
    // 1 cycle = 1 / 600,000,000 seconds
    //         = 1.6667 nanoseconds

    double averageNanoseconds =
        (averageCycles / CPU_MHZ) * 1000.0;

    double minNanoseconds =
        (static_cast<double>(minCycles) / CPU_MHZ) * 1000.0;

    double maxNanoseconds =
        (static_cast<double>(maxCycles) / CPU_MHZ) * 1000.0;

    // Calculate loop frequency.

    double iterationsPerSecond =
        static_cast<double>(iterations) /
        (static_cast<double>(totalDurationUs) / 1'000'000.0);

    // --------------------------------------------------------
    // Print results
    // --------------------------------------------------------

    Serial.println();
    Serial.println("=== TEST SUMMARY ===");

    Serial.print("Duration:          ");
    Serial.print(totalDurationUs / 1'000'000.0, 3);
    Serial.println(" s");

    Serial.print("Iterations:        ");
    Serial.println(iterations);

    Serial.print("Loops / second:    ");
    Serial.println(iterationsPerSecond, 0);

    Serial.println();

    Serial.print("Average loop:      ");
    Serial.print(averageNanoseconds, 2);
    Serial.println(" ns");

    Serial.print("Average cycles:    ");
    Serial.print(averageCycles, 2);
    Serial.println(" cycles");

    Serial.print("Minimum loop:      ");
    Serial.print(minNanoseconds, 2);
    Serial.println(" ns");

    Serial.print("Minimum cycles:    ");
    Serial.println(minCycles);

    Serial.print("Maximum loop:      ");
    Serial.print(maxNanoseconds, 2);
    Serial.println(" ns");

    Serial.print("Maximum cycles:    ");
    Serial.println(maxCycles);

    Serial.println();

    Serial.print("Total CPU cycles:  ");
    Serial.println(totalCyclesMeasured);

    Serial.println();
    Serial.println("=== TEST COMPLETE ===");

    digitalWrite(LED_PIN, LOW);
}
```
