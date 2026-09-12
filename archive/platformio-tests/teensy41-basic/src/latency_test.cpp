#include <Arduino.h>
#include <stdint.h>

#include "latency_test.h"

namespace
{

// ============================================================
// SETTINGS
// ============================================================

constexpr uint32_t TEST_DURATION_MS = 5000UL;

// A batch is used because many boards cannot measure a tiny
// operation accurately with micros().
constexpr uint32_t BATCH_SIZE = 1000UL;

// ============================================================
// COMPILER-PROTECTION SINK
// ============================================================
//
// Prevents the compiler from removing the benchmark workload.
//

volatile uint32_t benchmarkSink = 0;

// ============================================================
// RESULTS
// ============================================================

struct TimingResults
{
    uint32_t elapsedUs = 0;
    uint32_t iterations = 0;
    uint32_t batches = 0;

    uint32_t minimumBatchUs = UINT32_MAX;
    uint32_t maximumBatchUs = 0;

    uint64_t totalBatchUs = 0;

    uint32_t timerResolutionUs = 0;
    uint32_t timerOverheadUs = 0;
};

// ============================================================
// PORTABLE WORKLOAD
// ============================================================
//
// This is deliberately small and board-independent.
//
// It is not a complete robot control loop.
// It measures the timing behavior of a repeatable firmware
// workload.
//

inline void runMeasuredWork(uint32_t value)
{
    value ^= value << 13;
    value ^= value >> 17;
    value ^= value << 5;

    value += 0x9E3779B9UL;
    value *= 1664525UL;

    benchmarkSink = value;
}

// ============================================================
// DETERMINE MICROS() RESOLUTION
// ============================================================
//
// Reads micros() repeatedly until its value changes.
//
// This detects the practical resolution of micros() on the
// current board under the current firmware conditions.
//

uint32_t measureMicrosResolution()
{
    uint32_t previous = micros();

    for (uint32_t i = 0; i < 100000UL; i++)
    {
        const uint32_t current = micros();

        if (current != previous)
        {
            return current - previous;
        }
    }

    return 0;
}

// ============================================================
// MEASURE TIMER OVERHEAD
// ============================================================
//
// Measures the cost of calling micros() twice.
//
// This is not a perfect measurement of all timing overhead,
// but it provides useful context for interpreting results.
//

uint32_t measureTimerOverhead()
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
// RUN BENCHMARK
// ============================================================

TimingResults runTimingTest()
{
    TimingResults results;

    results.timerResolutionUs =
        measureMicrosResolution();

    results.timerOverheadUs =
        measureTimerOverhead();

    const uint32_t testStart = micros();

    while ((micros() - testStart) <
           (TEST_DURATION_MS * 1000UL))
    {
        const uint32_t batchStart = micros();

        for (uint32_t i = 0; i < BATCH_SIZE; i++)
        {
            runMeasuredWork(results.iterations);
            results.iterations++;
        }

        const uint32_t batchEnd = micros();

        const uint32_t batchElapsed =
            batchEnd - batchStart;

        if (batchElapsed < results.minimumBatchUs)
        {
            results.minimumBatchUs = batchElapsed;
        }

        if (batchElapsed > results.maximumBatchUs)
        {
            results.maximumBatchUs = batchElapsed;
        }

        results.totalBatchUs += batchElapsed;
        results.batches++;
    }

    results.elapsedUs = micros() - testStart;

    return results;
}

// ============================================================
// PRINT RESULTS
// ============================================================

void printTimingResults(const TimingResults &results)
{
    Serial.println();
    Serial.println("================================");
    Serial.println("UNIVERSAL FIRMWARE TIMING TEST");
    Serial.println("================================");
    Serial.println();

    Serial.println("Timing source: Arduino micros()");
    Serial.println("Workload: portable integer firmware loop");
    Serial.println();

    Serial.print("Test duration:       ");
    Serial.print(results.elapsedUs / 1000000.0f, 3);
    Serial.println(" s");

    Serial.print("Batch size:          ");
    Serial.println(BATCH_SIZE);

    Serial.print("Batches:             ");
    Serial.println(results.batches);

    Serial.print("Total iterations:    ");
    Serial.println(results.iterations);

    Serial.println();

    Serial.print("Timer resolution:    ");
    Serial.print(results.timerResolutionUs);
    Serial.println(" us");

    Serial.print("Timer overhead:      ");
    Serial.print(results.timerOverheadUs);
    Serial.println(" us");

    Serial.println();

    if (results.elapsedUs > 0)
    {
        const float iterationsPerSecond =
            (static_cast<float>(results.iterations) *
             1000000.0f) /
            static_cast<float>(results.elapsedUs);

        const float averageIterationUs =
            1000000.0f /
            iterationsPerSecond;

        Serial.print("Iterations/second:   ");
        Serial.println(iterationsPerSecond, 2);

        Serial.print("Average iteration:   ");
        Serial.print(averageIterationUs, 6);
        Serial.println(" us");
    }

    Serial.println();

    Serial.print("Minimum batch:       ");
    Serial.print(results.minimumBatchUs);
    Serial.println(" us");

    Serial.print("Maximum batch:       ");
    Serial.print(results.maximumBatchUs);
    Serial.println(" us");

    if (results.batches > 0)
    {
        const float averageBatchUs =
            static_cast<float>(results.totalBatchUs) /
            static_cast<float>(results.batches);

        const float averageIterationUs =
            averageBatchUs /
            static_cast<float>(BATCH_SIZE);

        Serial.print("Average batch:       ");
        Serial.print(averageBatchUs, 3);
        Serial.println(" us");

        Serial.print("Batch average/iter:  ");
        Serial.print(averageIterationUs, 6);
        Serial.println(" us");

        Serial.print("Minimum iter est.:   ");
        Serial.print(
            static_cast<float>(results.minimumBatchUs) /
            static_cast<float>(BATCH_SIZE),
            6);

        Serial.println(" us");

        Serial.print("Maximum iter est.:   ");
        Serial.print(
            static_cast<float>(results.maximumBatchUs) /
            static_cast<float>(BATCH_SIZE),
            6);

        Serial.println(" us");
    }

    Serial.println();

    Serial.println("INTERPRETATION:");
    Serial.println("- Higher iterations/sec is faster.");
    Serial.println("- Batch timing reduces timer-resolution error.");
    Serial.println("- Results include benchmark and timer overhead.");
    Serial.println("- This is not complete sensor-to-motor latency.");
    Serial.println("- Compare boards using the same compiler settings.");
    Serial.println();

    Serial.println("=== TEST COMPLETE ===");
}

// ============================================================
// PUBLIC FUNCTION
// ============================================================

} // namespace

bool runLatencyBenchmark()
{
    Serial.println();
    Serial.println("Starting universal timing benchmark...");
    Serial.println();

    const TimingResults results =
        runTimingTest();

    printTimingResults(results);

    return results.elapsedUs > 0 &&
           results.batches > 0 &&
           results.iterations > 0;
}