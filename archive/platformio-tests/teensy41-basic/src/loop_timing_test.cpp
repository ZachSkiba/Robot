#include <Arduino.h>
#include <stdint.h>

#include "loop_timing_test.h"

namespace
{

// ============================================================
// CONFIGURATION
// ============================================================

constexpr uint32_t TEST_DURATION_MS = 5000UL;

// Target control-loop period.
//
// This is an example target only.
// Your real robot may eventually use 1,000 us for a 1 kHz loop.
constexpr uint32_t TARGET_LOOP_PERIOD_US = 1000UL;

// Number of timing buckets used for the histogram.
constexpr uint8_t HISTOGRAM_BUCKETS = 8;

// Optional LED heartbeat.
//
// Disabled by default because digitalWrite() can affect timing.
constexpr bool ENABLE_LED = false;

#ifdef LED_BUILTIN

constexpr bool HAS_BUILTIN_LED = true;
constexpr uint8_t LED_PIN = LED_BUILTIN;

#else

constexpr bool HAS_BUILTIN_LED = false;
constexpr uint8_t LED_PIN = 0;

#endif

// ============================================================
// RESULTS
// ============================================================

struct LoopTimingResults
{
    uint32_t elapsedUs = 0;

    uint32_t samples = 0;

    uint32_t minimumPeriodUs = UINT32_MAX;

    uint32_t maximumPeriodUs = 0;

    uint64_t totalPeriodUs = 0;

    uint32_t missedDeadlines = 0;

    uint32_t timerResolutionUs = 0;

    uint32_t timerOverheadUs = 0;

    uint32_t histogram[HISTOGRAM_BUCKETS] = {};
};

// ============================================================
// TIMER INFORMATION
// ============================================================

uint32_t measureMicrosResolution()
{
    const uint32_t start = micros();

    for (uint32_t i = 0; i < 100000UL; i++)
    {
        const uint32_t current = micros();

        if (current != start)
        {
            return current - start;
        }
    }

    return 0;
}

uint32_t measureMicrosOverhead()
{
    uint32_t minimumOverhead = UINT32_MAX;

    for (uint32_t i = 0; i < 1000UL; i++)
    {
        const uint32_t start = micros();
        const uint32_t end = micros();

        const uint32_t elapsed = end - start;

        if (elapsed < minimumOverhead)
        {
            minimumOverhead = elapsed;
        }
    }

    if (minimumOverhead == UINT32_MAX)
    {
        return 0;
    }

    return minimumOverhead;
}

// ============================================================
// OPTIONAL LED SUPPORT
// ============================================================

void initializeLed()
{
    if (ENABLE_LED && HAS_BUILTIN_LED)
    {
        pinMode(LED_PIN, OUTPUT);
        digitalWrite(LED_PIN, LOW);
    }
}

void updateLed(uint32_t nowUs)
{
    static uint32_t lastToggleUs = 0;

    constexpr uint32_t LED_PERIOD_US = 500000UL;

    if (!ENABLE_LED || !HAS_BUILTIN_LED)
    {
        return;
    }

    if ((nowUs - lastToggleUs) >= LED_PERIOD_US)
    {
        lastToggleUs = nowUs;

        digitalWrite(
            LED_PIN,
            !digitalRead(LED_PIN));
    }
}

// ============================================================
// HISTOGRAM
// ============================================================
//
// Bucket meanings:
//
// 0: 0 to 1x target period
// 1: 1x to 2x target period
// 2: 2x to 3x target period
// 3: 3x to 4x target period
// 4: 4x to 5x target period
// 5: 5x to 10x target period
// 6: 10x to 100x target period
// 7: greater than 100x target period
//

void recordHistogram(
    LoopTimingResults &results,
    uint32_t periodUs)
{
    uint8_t bucket = 0;

    if (periodUs < TARGET_LOOP_PERIOD_US)
    {
        bucket = 0;
    }
    else if (periodUs < TARGET_LOOP_PERIOD_US * 2UL)
    {
        bucket = 1;
    }
    else if (periodUs < TARGET_LOOP_PERIOD_US * 3UL)
    {
        bucket = 2;
    }
    else if (periodUs < TARGET_LOOP_PERIOD_US * 4UL)
    {
        bucket = 3;
    }
    else if (periodUs < TARGET_LOOP_PERIOD_US * 5UL)
    {
        bucket = 4;
    }
    else if (periodUs < TARGET_LOOP_PERIOD_US * 10UL)
    {
        bucket = 5;
    }
    else if (periodUs < TARGET_LOOP_PERIOD_US * 100UL)
    {
        bucket = 6;
    }
    else
    {
        bucket = 7;
    }

    results.histogram[bucket]++;
}

// ============================================================
// RUN TIMING TEST
// ============================================================

LoopTimingResults runTimingTest()
{
    LoopTimingResults results;

    results.timerResolutionUs =
        measureMicrosResolution();

    results.timerOverheadUs =
        measureMicrosOverhead();

    initializeLed();

    const uint32_t testStartUs = micros();

    uint32_t previousTimestampUs = testStartUs;

    while ((micros() - testStartUs) <
           (TEST_DURATION_MS * 1000UL))
    {
        const uint32_t nowUs = micros();

        const uint32_t periodUs =
            nowUs - previousTimestampUs;

        previousTimestampUs = nowUs;

        if (periodUs < results.minimumPeriodUs)
        {
            results.minimumPeriodUs = periodUs;
        }

        if (periodUs > results.maximumPeriodUs)
        {
            results.maximumPeriodUs = periodUs;
        }

        results.totalPeriodUs += periodUs;

        results.samples++;

        if (periodUs > TARGET_LOOP_PERIOD_US)
        {
            results.missedDeadlines++;
        }

        recordHistogram(
            results,
            periodUs);

        updateLed(nowUs);

    }

    results.elapsedUs = micros() - testStartUs;

    if (ENABLE_LED && HAS_BUILTIN_LED)
    {
        digitalWrite(LED_PIN, LOW);
    }

    return results;
}

// ============================================================
// PRINT RESULTS
// ============================================================

void printHistogram(
    const LoopTimingResults &results)
{
    Serial.println(F("Timing histogram:"));

    Serial.print(F("  < 1x target:        "));
    Serial.println(results.histogram[0]);

    Serial.print(F("  1x to 2x target:    "));
    Serial.println(results.histogram[1]);

    Serial.print(F("  2x to 3x target:    "));
    Serial.println(results.histogram[2]);

    Serial.print(F("  3x to 4x target:    "));
    Serial.println(results.histogram[3]);

    Serial.print(F("  4x to 5x target:    "));
    Serial.println(results.histogram[4]);

    Serial.print(F("  5x to 10x target:   "));
    Serial.println(results.histogram[5]);

    Serial.print(F("  10x to 100x target: "));
    Serial.println(results.histogram[6]);

    Serial.print(F("  > 100x target:      "));
    Serial.println(results.histogram[7]);
}

void printResults(
    const LoopTimingResults &results)
{
    Serial.println();
    Serial.println(F("================================"));
    Serial.println(F("UNIVERSAL LOOP TIMING TEST"));
    Serial.println(F("================================"));
    Serial.println();

    Serial.println(F("Timing source: Arduino micros()"));

    Serial.print(F("Test duration:       "));
    Serial.print(results.elapsedUs / 1000000.0f, 3);
    Serial.println(F(" s"));

    Serial.print(F("Target loop period:  "));
    Serial.print(TARGET_LOOP_PERIOD_US);
    Serial.println(F(" us"));

    Serial.print(F("Timer resolution:    "));
    Serial.print(results.timerResolutionUs);
    Serial.println(F(" us"));

    Serial.print(F("Timer overhead:      "));
    Serial.print(results.timerOverheadUs);
    Serial.println(F(" us"));

    Serial.println();

    Serial.print(F("Samples:             "));
    Serial.println(results.samples);

    Serial.print(F("Minimum period:      "));
    Serial.print(results.minimumPeriodUs);
    Serial.println(F(" us"));

    Serial.print(F("Maximum period:      "));
    Serial.print(results.maximumPeriodUs);
    Serial.println(F(" us"));

    if (results.samples > 0)
    {
        const float averagePeriodUs =
            static_cast<float>(results.totalPeriodUs) /
            static_cast<float>(results.samples);

        Serial.print(F("Average period:      "));
        Serial.print(averagePeriodUs, 3);
        Serial.println(F(" us"));

        if (averagePeriodUs > 0.0f)
        {
            const float frequencyHz =
                1000000.0f / averagePeriodUs;

            Serial.print(F("Average loop rate:   "));
            Serial.print(frequencyHz, 3);
            Serial.println(F(" Hz"));
        }

        const float jitterUs =
            static_cast<float>(results.maximumPeriodUs) -
            averagePeriodUs;

        Serial.print(F("Worst positive jitter: "));
        Serial.print(jitterUs, 3);
        Serial.println(F(" us"));
    }

    Serial.print(F("Periods over target:  "));
    Serial.println(results.missedDeadlines);

    if (results.samples > 0)
    {
        const float missedPercentage =
            static_cast<float>(results.missedDeadlines) *
            100.0f /
            static_cast<float>(results.samples);

        Serial.print(F("Miss percentage:      "));
        Serial.print(missedPercentage, 3);
        Serial.println(F("%"));
    }

    Serial.println();

    printHistogram(results);

    Serial.println();

    Serial.println(F("INTERPRETATION:"));
    Serial.println(F("- This measures loop period, not pure execution time."));
    Serial.println(F("- micros() overhead is included in each measurement."));
    Serial.println(F("- Timer resolution differs between boards."));
    Serial.println(F("- LED timing is disabled by default."));
    Serial.println(F("- Interrupts and background tasks affect jitter."));
    Serial.println(F("- A missed period is not automatically a missed control deadline."));
    Serial.println(F("- Use the real robot control loop for final validation."));

    Serial.println();
    Serial.println(F("=== LOOP TIMING TEST COMPLETE ==="));
}

} // namespace

// ============================================================
// PUBLIC FUNCTION
// ============================================================

bool runLoopTimingTest()
{
    Serial.println();
    Serial.println(F("Starting universal loop timing test..."));
    Serial.println();

    const LoopTimingResults results =
        runTimingTest();

    printResults(results);

    return results.samples > 0 &&
           results.minimumPeriodUs != UINT32_MAX &&
           results.maximumPeriodUs >= results.minimumPeriodUs;
}