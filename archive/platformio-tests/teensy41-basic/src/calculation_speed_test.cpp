#include <Arduino.h>
#include <math.h>
#include <stdint.h>

#include "calculation_speed_test.h"

namespace
{

// ============================================================
// CONFIGURATION
// ============================================================

// Each individual benchmark runs for approximately 5 seconds.
constexpr uint32_t BENCHMARK_DURATION_MS = 5000UL;

// Number of workload iterations measured as one timing batch.
//
// Batching is important because micros() has different timing
// resolutions on different Arduino-style boards.
//
// For example, classic 16 MHz AVR boards commonly have a
// micros() resolution of approximately 4 microseconds.
constexpr uint32_t BATCH_SIZE = 100UL;

// ============================================================
// COMPILER-PROTECTION SINKS
// ============================================================
//
// These volatile variables prevent the compiler from removing
// the calculations because their results are not used elsewhere.
//

volatile uint32_t integerSink = 0;
volatile float floatSink = 0.0f;
volatile float trigSink = 0.0f;
volatile float robotMathSink = 0.0f;

// ============================================================
// RESULT STRUCTURE
// ============================================================

struct BenchmarkResult
{
    uint32_t elapsedUs = 0;

    uint64_t iterations = 0;

    uint32_t batches = 0;

    uint32_t minimumBatchUs = UINT32_MAX;

    uint32_t maximumBatchUs = 0;

    uint64_t totalBatchUs = 0;
};

// ============================================================
// PORTABLE INTEGER WORKLOAD
// ============================================================
//
// This is a repeatable integer-heavy workload.
//
// The reported result is:
//     completed benchmark iterations per second
//
// It is NOT a count of CPU instructions.
//

inline void runIntegerWork(uint32_t iteration)
{
    uint32_t value = iteration;

    value ^= value << 13;
    value ^= value >> 17;
    value ^= value << 5;

    value += 0x9E3779B9UL;
    value *= 1664525UL;
    value += 1013904223UL;

    integerSink = value;
}

// ============================================================
// PORTABLE FLOATING-POINT WORKLOAD
// ============================================================
//
// This intentionally uses 32-bit float values.
//

inline void runFloatWork(uint32_t iteration)
{
    float value =
        0.125f + static_cast<float>(iteration) * 0.000001f;

    float value2 = 1.375f;

    value =
        (value * 1.000123f) +
        0.000031f;

    value2 =
        (value2 * 0.999877f) -
        0.000017f;

    value += value2 * 0.125f;
    value2 += value * 0.0625f;

    if (value > 1000.0f)
    {
        value *= 0.001f;
    }

    if (value2 < -1000.0f)
    {
        value2 *= 0.001f;
    }

    floatSink = value + value2;
}

// ============================================================
// PORTABLE TRIGONOMETRY WORKLOAD
// ============================================================
//
// Uses sinf() and cosf() explicitly for single-precision math.
//

inline void runTrigWork(uint32_t iteration)
{
    constexpr float FULL_TURN_RADIANS = 6.28318530718f;

    float angle =
        0.1f + static_cast<float>(iteration % 1000UL) * 0.001f;

    float result = 0.0f;

    result += sinf(angle);
    result += cosf(angle * 0.5f);

    angle += 0.01f;

    if (angle >= FULL_TURN_RADIANS)
    {
        angle -= FULL_TURN_RADIANS;
    }

    trigSink = result + angle;
}

// ============================================================
// ROBOT-STYLE MATH WORKLOAD
// ============================================================
//
// This is not a complete 6-DOF kinematics implementation.
//
// It approximates common robotics numerical operations:
//
// - 3D vector transformation
// - matrix/vector multiplication
// - vector magnitude
// - vector normalization
// - position updates
// - orientation-style trigonometry
//
// Later, this should be replaced or supplemented with your
// actual forward-kinematics and inverse-kinematics code.
//

inline void runRobotMathWork(uint32_t iteration)
{
    float x = 0.35f +
              static_cast<float>(iteration % 100UL) * 0.0001f;

    float y = -0.20f;
    float z = 0.75f;

    float vx = 0.80f;
    float vy = -0.35f;
    float vz = 0.55f;

    // Approximate rotation matrix.
    const float r00 = 0.98f;
    const float r01 = -0.12f;
    const float r02 = 0.08f;

    const float r10 = 0.11f;
    const float r11 = 0.97f;
    const float r12 = -0.16f;

    const float r20 = -0.10f;
    const float r21 = 0.15f;
    const float r22 = 0.98f;

    // --------------------------------------------------------
    // Matrix/vector multiplication
    // --------------------------------------------------------

    const float nx =
        (r00 * vx) +
        (r01 * vy) +
        (r02 * vz);

    const float ny =
        (r10 * vx) +
        (r11 * vy) +
        (r12 * vz);

    const float nz =
        (r20 * vx) +
        (r21 * vy) +
        (r22 * vz);

    // --------------------------------------------------------
    // Position update
    // --------------------------------------------------------

    x += nx * 0.001f;
    y += ny * 0.001f;
    z += nz * 0.001f;

    // --------------------------------------------------------
    // Vector magnitude
    // --------------------------------------------------------

    const float magnitude =
        sqrtf(
            (nx * nx) +
            (ny * ny) +
            (nz * nz));

    // --------------------------------------------------------
    // Vector normalization
    // --------------------------------------------------------

    if (magnitude > 0.000001f)
    {
        vx = nx / magnitude;
        vy = ny / magnitude;
        vz = nz / magnitude;
    }

    // --------------------------------------------------------
    // Orientation-style calculations
    // --------------------------------------------------------

    const float c = cosf(x);
    const float s = sinf(y);

    const float result =
        (vx * c) +
        (vy * s) +
        (vz * z);

    robotMathSink =
        result +
        x +
        y +
        z +
        vx +
        vy +
        vz;
}

// ============================================================
// GENERIC BENCHMARK RUNNER
// ============================================================
//
// The workload is supplied as a function pointer.
//
// This keeps the timing logic identical for all workloads.
//

using WorkloadFunction = void (*)(uint32_t iteration);

BenchmarkResult runBenchmark(
    WorkloadFunction workload)
{
    BenchmarkResult result;

    const uint32_t startUs = micros();

    while ((micros() - startUs) <
           (BENCHMARK_DURATION_MS * 1000UL))
    {
        const uint32_t batchStartUs = micros();

        for (uint32_t i = 0; i < BATCH_SIZE; i++)
        {
            workload(
                static_cast<uint32_t>(
                    result.iterations + i));
        }

        const uint32_t batchEndUs = micros();

        const uint32_t batchElapsedUs =
            batchEndUs - batchStartUs;

        if (batchElapsedUs < result.minimumBatchUs)
        {
            result.minimumBatchUs = batchElapsedUs;
        }

        if (batchElapsedUs > result.maximumBatchUs)
        {
            result.maximumBatchUs = batchElapsedUs;
        }

        result.totalBatchUs += batchElapsedUs;

        result.batches++;

        result.iterations += BATCH_SIZE;
    }

    result.elapsedUs = micros() - startUs;

    return result;
}

// ============================================================
// PRINT ONE RESULT
// ============================================================

void printBenchmarkResult(
    const char *label,
    const BenchmarkResult &result)
{
    Serial.println(label);

    Serial.print("  Duration:          ");
    Serial.print(result.elapsedUs / 1000000.0f, 3);
    Serial.println(" s");

    Serial.print("  Iterations:        ");
    Serial.println(
        static_cast<unsigned long>(
            result.iterations));

    Serial.print("  Batches:           ");
    Serial.println(result.batches);

    if (result.elapsedUs > 0)
    {
        const float iterationsPerSecond =
            static_cast<float>(result.iterations) *
            1000000.0f /
            static_cast<float>(result.elapsedUs);

        const float averageIterationUs =
            1000000.0f /
            iterationsPerSecond;

        Serial.print("  Iterations/sec:    ");
        Serial.println(iterationsPerSecond, 2);

        Serial.print("  Average iteration: ");
        Serial.print(averageIterationUs, 6);
        Serial.println(" us");
    }
    else
    {
        Serial.println("  Iterations/sec:    unavailable");
    }

    Serial.print("  Minimum batch:     ");
    Serial.print(result.minimumBatchUs);
    Serial.println(" us");

    Serial.print("  Maximum batch:     ");
    Serial.print(result.maximumBatchUs);
    Serial.println(" us");

    if (result.batches > 0)
    {
        const float averageBatchUs =
            static_cast<float>(result.totalBatchUs) /
            static_cast<float>(result.batches);

        const float averageBatchIterationUs =
            averageBatchUs /
            static_cast<float>(BATCH_SIZE);

        Serial.print("  Average batch:     ");
        Serial.print(averageBatchUs, 3);
        Serial.println(" us");

        Serial.print("  Batch avg/iter:    ");
        Serial.print(averageBatchIterationUs, 6);
        Serial.println(" us");
    }

    Serial.println();
}

// ============================================================
// PUBLIC BENCHMARK FUNCTION
// ============================================================

} // namespace

bool runCalculationSpeedBenchmark()
{
    Serial.println();
    Serial.println("================================");
    Serial.println("Calculation Speed Benchmark");
    Serial.println("================================");
    Serial.println();

    Serial.println("Portable Arduino-style benchmark");
    Serial.println("Higher iterations/sec = faster");
    Serial.println();

    Serial.print("Benchmark duration: ");
    Serial.print(BENCHMARK_DURATION_MS / 1000UL);
    Serial.println(" seconds");

    Serial.print("Batch size:         ");
    Serial.println(BATCH_SIZE);

    Serial.println();

    // --------------------------------------------------------
    // Integer benchmark
    // --------------------------------------------------------

    const BenchmarkResult integerResult =
        runBenchmark(runIntegerWork);

    // --------------------------------------------------------
    // Floating-point benchmark
    // --------------------------------------------------------

    const BenchmarkResult floatResult =
        runBenchmark(runFloatWork);

    // --------------------------------------------------------
    // Trigonometry benchmark
    // --------------------------------------------------------

    const BenchmarkResult trigResult =
        runBenchmark(runTrigWork);

    // --------------------------------------------------------
    // Robot-style math benchmark
    // --------------------------------------------------------

    const BenchmarkResult robotMathResult =
        runBenchmark(runRobotMathWork);

    // --------------------------------------------------------
    // Print detailed results
    // --------------------------------------------------------

    Serial.println();
    Serial.println("================================");
    Serial.println("DETAILED RESULTS");
    Serial.println("================================");
    Serial.println();

    printBenchmarkResult(
        "Integer arithmetic",
        integerResult);

    printBenchmarkResult(
        "32-bit floating point",
        floatResult);

    printBenchmarkResult(
        "Trigonometry",
        trigResult);

    printBenchmarkResult(
        "Robot-style math",
        robotMathResult);

    // --------------------------------------------------------
    // Summary
    // --------------------------------------------------------

    Serial.println("================================");
    Serial.println("SUMMARY");
    Serial.println("================================");
    Serial.println();

    Serial.println(
        "Benchmark             Iterations/sec");

    Serial.println(
        "----------------------------------------");

    if (integerResult.elapsedUs > 0)
    {
        Serial.print("Integer arithmetic    ");
        Serial.println(
            static_cast<float>(integerResult.iterations) *
            1000000.0f /
            static_cast<float>(integerResult.elapsedUs),
            2);
    }

    if (floatResult.elapsedUs > 0)
    {
        Serial.print("32-bit float          ");
        Serial.println(
            static_cast<float>(floatResult.iterations) *
            1000000.0f /
            static_cast<float>(floatResult.elapsedUs),
            2);
    }

    if (trigResult.elapsedUs > 0)
    {
        Serial.print("Trigonometry          ");
        Serial.println(
            static_cast<float>(trigResult.iterations) *
            1000000.0f /
            static_cast<float>(trigResult.elapsedUs),
            2);
    }

    if (robotMathResult.elapsedUs > 0)
    {
        Serial.print("Robot-style math      ");
        Serial.println(
            static_cast<float>(robotMathResult.iterations) *
            1000000.0f /
            static_cast<float>(robotMathResult.elapsedUs),
            2);
    }

    Serial.println();

    Serial.println("NOTES:");
    Serial.println("- Results are benchmark iterations/sec.");
    Serial.println("- They are not CPU instruction counts.");
    Serial.println("- The same source can run on many Arduino boards.");
    Serial.println("- Timer resolution differs between processors.");
    Serial.println("- Compiler optimization affects the results.");
    Serial.println("- Robot-style math is not complete 6-DOF kinematics.");
    Serial.println();

    Serial.println("=== TEST COMPLETE ===");

    return integerResult.elapsedUs > 0 &&
           floatResult.elapsedUs > 0 &&
           trigResult.elapsedUs > 0 &&
           robotMathResult.elapsedUs > 0 &&
           integerResult.iterations > 0 &&
           floatResult.iterations > 0 &&
           trigResult.iterations > 0 &&
           robotMathResult.iterations > 0;
}