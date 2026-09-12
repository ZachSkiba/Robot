#include <Arduino.h>
#include <math.h>

#include "calculation_speed_test.h"

namespace
{

// ============================================================
// TEST CONFIGURATION
// ============================================================

constexpr uint32_t BENCHMARK_DURATION_MS = 5000UL;

// Use volatile sinks so the compiler cannot simply remove
// the calculations because their results are never used.
volatile uint32_t integerSink = 0;
volatile float floatSink = 0.0f;
volatile float trigSink = 0.0f;
volatile float robotMathSink = 0.0f;

// ============================================================
// INTEGER BENCHMARK
// ============================================================
//
// Measures a repeatable integer-heavy workload.
//
// This is NOT "integer instructions per second".
// It measures completed benchmark iterations per second.
//

uint32_t runIntegerBenchmark(uint32_t &elapsedMs)
{
    uint32_t value = 0x12345678UL;
    uint32_t iterations = 0;

    const uint32_t start = millis();

    while ((millis() - start) < BENCHMARK_DURATION_MS)
    {
        // Integer multiply/add
        value = (value * 1664525UL) + 1013904223UL;

        // Integer bit operations
        value ^= value >> 13;
        value ^= value << 17;
        value ^= value >> 5;

        // Additional integer arithmetic
        value += iterations;
        value -= 0x9E3779B9UL;

        iterations++;
    }

    elapsedMs = millis() - start;

    integerSink = value;

    return iterations;
}

// ============================================================
// FLOATING-POINT BENCHMARK
// ============================================================
//
// Measures a repeatable single-precision floating-point workload.
//

uint32_t runFloatBenchmark(uint32_t &elapsedMs)
{
    float value = 0.125f;
    float value2 = 1.375f;

    uint32_t iterations = 0;

    const uint32_t start = millis();

    while ((millis() - start) < BENCHMARK_DURATION_MS)
    {
        value = (value * 1.000123f) + 0.000031f;
        value2 = (value2 * 0.999877f) - 0.000017f;

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

        iterations++;
    }

    elapsedMs = millis() - start;

    floatSink = value + value2;

    return iterations;
}

// ============================================================
// TRIGONOMETRY BENCHMARK
// ============================================================
//
// Measures single-precision sin/cos workload.
//
// sinf() and cosf() are intentionally used instead of sin()
// and cos() because this benchmark is specifically measuring
// 32-bit floating-point trigonometry.
//

uint32_t runTrigBenchmark(uint32_t &elapsedMs)
{
    float angle = 0.1f;
    float result = 0.0f;

    uint32_t iterations = 0;

    constexpr float TWO_PI = 6.28318530718f;

    const uint32_t start = millis();

    while ((millis() - start) < BENCHMARK_DURATION_MS)
    {
        const float halfAngle = angle * 0.5f;

        result += sinf(angle);
        result += cosf(halfAngle);

        angle += 0.01f;

        if (angle >= TWO_PI)
        {
            angle -= TWO_PI;
        }

        iterations++;
    }

    elapsedMs = millis() - start;

    trigSink = result;

    return iterations;
}

// ============================================================
// ROBOT MATH BENCHMARK
// ============================================================
//
// This is intentionally more representative of robotics.
//
// It performs repeated 3D vector / transformation-style
// floating-point calculations.
//
// The workload is NOT intended to be a complete kinematics
// implementation. It is a platform-independent approximation
// of the numerical work commonly performed by robot software.
//

uint32_t runRobotMathBenchmark(uint32_t &elapsedMs)
{
    // Position
    float x = 0.35f;
    float y = -0.20f;
    float z = 0.75f;

    // Direction / vector
    float vx = 0.80f;
    float vy = -0.35f;
    float vz = 0.55f;

    // Transformation-style values
    float r00 = 0.98f;
    float r01 = -0.12f;
    float r02 = 0.08f;

    float r10 = 0.11f;
    float r11 = 0.97f;
    float r12 = -0.16f;

    float r20 = -0.10f;
    float r21 = 0.15f;
    float r22 = 0.98f;

    float result = 0.0f;

    uint32_t iterations = 0;

    const uint32_t start = millis();

    while ((millis() - start) < BENCHMARK_DURATION_MS)
    {
        // ----------------------------------------------------
        // 3D vector transformation
        // ----------------------------------------------------

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

        // ----------------------------------------------------
        // Position update
        // ----------------------------------------------------

        x += nx * 0.001f;
        y += ny * 0.001f;
        z += nz * 0.001f;

        // ----------------------------------------------------
        // Vector magnitude
        // ----------------------------------------------------

        const float magnitude =
            sqrtf(
                (nx * nx) +
                (ny * ny) +
                (nz * nz));

        // ----------------------------------------------------
        // Normalize vector
        // ----------------------------------------------------

        if (magnitude > 0.000001f)
        {
            vx = nx / magnitude;
            vy = ny / magnitude;
            vz = nz / magnitude;
        }

        // ----------------------------------------------------
        // Additional orientation-style calculations
        // ----------------------------------------------------

        const float c = cosf(x);
        const float s = sinf(y);

        result +=
            (vx * c) +
            (vy * s) +
            (vz * z);

        iterations++;
    }

    elapsedMs = millis() - start;

    robotMathSink =
        result +
        x +
        y +
        z +
        vx +
        vy +
        vz;

    return iterations;
}

// ============================================================
// RESULT PRINTING
// ============================================================

void printBenchmarkResult(
    const char *name,
    uint32_t iterations,
    uint32_t elapsedMs)
{
    Serial.print(name);
    Serial.println();

    Serial.print("  Iterations:       ");
    Serial.println(iterations);

    Serial.print("  Duration:         ");
    Serial.print(elapsedMs);
    Serial.println(" ms");

    if (elapsedMs > 0)
    {
        const float iterationsPerSecond =
            (static_cast<float>(iterations) * 1000.0f) /
            static_cast<float>(elapsedMs);

        Serial.print("  Iterations/sec:   ");
        Serial.println(iterationsPerSecond, 2);
    }

    Serial.println();
}

} // namespace

// ============================================================
// PUBLIC BENCHMARK
// ============================================================

void runCalculationSpeedBenchmark()
{
    Serial.println();
    Serial.println("================================");
    Serial.println("Calculation Speed Benchmark");
    Serial.println("================================");
    Serial.println();

    Serial.println("Each benchmark runs for approximately");
    Serial.print(BENCHMARK_DURATION_MS / 1000UL);
    Serial.println(" seconds.");
    Serial.println();

    Serial.println("Results are benchmark iterations/second.");
    Serial.println("Higher is faster.");
    Serial.println();

    // --------------------------------------------------------
    // Integer
    // --------------------------------------------------------

    uint32_t integerTime = 0;

    const uint32_t integerIterations =
        runIntegerBenchmark(integerTime);

    // --------------------------------------------------------
    // Float
    // --------------------------------------------------------

    uint32_t floatTime = 0;

    const uint32_t floatIterations =
        runFloatBenchmark(floatTime);

    // --------------------------------------------------------
    // Trigonometry
    // --------------------------------------------------------

    uint32_t trigTime = 0;

    const uint32_t trigIterations =
        runTrigBenchmark(trigTime);

    // --------------------------------------------------------
    // Robot math
    // --------------------------------------------------------

    uint32_t robotMathTime = 0;

    const uint32_t robotMathIterations =
        runRobotMathBenchmark(robotMathTime);

    // --------------------------------------------------------
    // Results
    // --------------------------------------------------------

    Serial.println();
    Serial.println("================================");
    Serial.println("RESULTS");
    Serial.println("================================");
    Serial.println();

    printBenchmarkResult(
        "Integer arithmetic",
        integerIterations,
        integerTime);

    printBenchmarkResult(
        "32-bit floating point",
        floatIterations,
        floatTime);

    printBenchmarkResult(
        "Trigonometry",
        trigIterations,
        trigTime);

    printBenchmarkResult(
        "Robot-style math",
        robotMathIterations,
        robotMathTime);

    // --------------------------------------------------------
    // Summary table
    // --------------------------------------------------------

    Serial.println("================================");
    Serial.println("SUMMARY");
    Serial.println("================================");
    Serial.println();

    Serial.println(
        "Benchmark             Iterations/sec");

    Serial.println(
        "----------------------------------------");

    if (integerTime > 0)
    {
        Serial.print(
            "Integer arithmetic    ");

        Serial.println(
            (static_cast<float>(integerIterations) * 1000.0f) /
            static_cast<float>(integerTime),
            2);
    }

    if (floatTime > 0)
    {
        Serial.print(
            "32-bit float          ");

        Serial.println(
            (static_cast<float>(floatIterations) * 1000.0f) /
            static_cast<float>(floatTime),
            2);
    }

    if (trigTime > 0)
    {
        Serial.print(
            "Trigonometry          ");

        Serial.println(
            (static_cast<float>(trigIterations) * 1000.0f) /
            static_cast<float>(trigTime),
            2);
    }

    if (robotMathTime > 0)
    {
        Serial.print(
            "Robot-style math      ");

        Serial.println(
            (static_cast<float>(robotMathIterations) * 1000.0f) /
            static_cast<float>(robotMathTime),
            2);
    }

    Serial.println();

    Serial.println(
        "Higher iterations/sec = faster.");

    Serial.println();
    Serial.println("=== TEST COMPLETE ===");
}