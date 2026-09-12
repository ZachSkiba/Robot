#include <Arduino.h>
#include "test_protocol.h"

// ============================================================
// SELECT WHICH PROGRAM TO RUN
// ============================================================
//
// Choose ONE program.
//
// 1) Latency benchmark
//    Include:  "latency_test.h"
//    Function: runLatencyBenchmark()
//
// 2) Loop timing test
//    Include:  "loop_timing_test.h"
//    Function: runLoopTimingTest()
//
// 3) Serial throughput test
//    Include:  "serial_throughput_test.h"
//    Function: runSerialThroughputTest()
//
// 4) Calculation speed test
//    Include:  "calculation_speed_test.h"
//    Function: runCalculationSpeedBenchmark()
//
// 5) Diagnostic firmware
//    Include:  "diagnostic-firmware.h"
//    Functions:
//      initializeDiagnosticFirmware()
//      runDiagnosticFirmware()
//
// 6) Universal board test suite
//    Include:  "universal-board-test.h"
//    Functions:
//      initializeUniversalBoardTest()
//      runUniversalBoardTest()
//
// ============================================================

// CHANGE THIS: define ONE program only.

// #define RUN_LATENCY_BENCHMARK
// #define RUN_LOOP_TIMING_TEST
// #define RUN_SERIAL_THROUGHPUT_TEST
// #define RUN_CALCULATION_SPEED_TEST
#define RUN_DIAGNOSTIC_FIRMWARE
// #define RUN_UNIVERSAL_BOARD_TEST

#if defined(RUN_LATENCY_BENCHMARK)
#include "latency_test.h"
#elif defined(RUN_LOOP_TIMING_TEST)
#include "loop_timing_test.h"
#elif defined(RUN_SERIAL_THROUGHPUT_TEST)
#include "serial_throughput_test.h"
#elif defined(RUN_CALCULATION_SPEED_TEST)
#include "calculation_speed_test.h"
#elif defined(RUN_DIAGNOSTIC_FIRMWARE)
#include "diagnostic-firmware.h"
#elif defined(RUN_UNIVERSAL_BOARD_TEST)
#include "universal-board-test.h"
#else
#error "Define exactly one RUN_* test selection in main.cpp"
#endif


// ============================================================
// SETTINGS
// ============================================================

// CHANGE THIS: Serial speed
// Common: 9600, 115200
constexpr uint32_t SERIAL_BAUD = 115200;

// CHANGE THIS: startup delay
// Unit: milliseconds
constexpr uint32_t STARTUP_DELAY_MS = 1000;

void announceFirmware()
{
#if defined(RUN_UNIVERSAL_BOARD_TEST)
    printTestProtocol("universal", "universal-board", "universal_board_001");
#elif defined(RUN_DIAGNOSTIC_FIRMWARE)
    printTestProtocol("diagnostic", "diagnostic", "diagnostic_001");
#elif defined(RUN_LATENCY_BENCHMARK)
    printTestProtocol("benchmark", "latency", "latency_001");
#elif defined(RUN_LOOP_TIMING_TEST)
    printTestProtocol("benchmark", "loop", "loop_001");
#elif defined(RUN_SERIAL_THROUGHPUT_TEST)
    printTestProtocol("benchmark", "serial", "serial_001");
#elif defined(RUN_CALCULATION_SPEED_TEST)
    printTestProtocol("benchmark", "calculation", "calculation_001");
#endif
}

void waitForStart()
{
    String input = "";

    // Wait for the PC/Python program to say READY.
    while (true)
    {
        while (Serial.available() > 0)
        {
            char c = Serial.read();

            if (c == '\n' || c == '\r')
            {
                input.trim();
                input.toUpperCase();

                if (input == "IDENTIFY")
                {
                    announceFirmware();
                }
                else if (input == "READY")
                {
                    Serial.println();
                    Serial.println("================================");
                    Serial.println("Board Test Runner");
                    Serial.println("================================");
                    Serial.println("Board is connected.");
                    Serial.println("Type YES and press Enter to start.");
                    Serial.println();
                    Serial.println(F("@TEST_START_READY"));

                    input = "";

                    // Now wait for YES.
                    while (true)
                    {
                        while (Serial.available() > 0)
                        {
                            char c2 = Serial.read();

                            if (c2 == '\n' || c2 == '\r')
                            {
                                input.trim();
                                input.toUpperCase();

                                if (input == "YES")
                                {
                                    Serial.println();
                                    Serial.println("Starting test...");
                                    Serial.println();

                                    return;
                                }

                                if (input.length() > 0)
                                {
                                    Serial.println("Please type YES to start.");
                                }

                                input = "";
                            }
                            else
                            {
                                input += c2;

                                if (input.length() > 32)
                                {
                                    input = "";
                                    Serial.println("Input too long. Type YES.");
                                }
                            }
                        }
                    }
                }

                input = "";
            }
            else
            {
                input += c;

                if (input.length() > 32)
                {
                    input = "";
                }
            }
        }
    }
}

// ============================================================
// MAIN PROGRAM
// ============================================================

void setup()
{
    Serial.begin(SERIAL_BAUD);

    delay(STARTUP_DELAY_MS);

    announceFirmware();

#if defined(RUN_UNIVERSAL_BOARD_TEST)
    initializeUniversalBoardTest();
#elif defined(RUN_DIAGNOSTIC_FIRMWARE)
    initializeDiagnosticFirmware();
#else
    waitForStart();

    Serial.println("Starting selected test...");
    Serial.println();

#if defined(RUN_LATENCY_BENCHMARK)
    Serial.println(F("@TEST_START"));
    const bool passed = runLatencyBenchmark();
#elif defined(RUN_LOOP_TIMING_TEST)
    Serial.println(F("@TEST_START"));
    const bool passed = runLoopTimingTest();
#elif defined(RUN_SERIAL_THROUGHPUT_TEST)
    Serial.println(F("@TEST_START"));
    const bool passed = runSerialThroughputTest();
#elif defined(RUN_CALCULATION_SPEED_TEST)
    Serial.println(F("@TEST_START"));
    const bool passed = runCalculationSpeedBenchmark();
#endif
    Serial.print(F("@TEST_RESULT="));
    Serial.println(passed ? F("PASS") : F("FAIL"));
    Serial.println(F("@TEST_COMPLETE"));
#endif
}

void loop()
{
#if defined(RUN_UNIVERSAL_BOARD_TEST)
    runUniversalBoardTest();
#elif defined(RUN_DIAGNOSTIC_FIRMWARE)
    runDiagnosticFirmware();
#endif
}

// ============================================================
// BUILD + FLASH + RUN A TEENSY TEST
// ============================================================
//
// IMPORTANT:
// The .cpp files are source code.
// The Teensy does NOT get the new code just because you run
// "pio run".
//
// "pio run" builds the source code into:
//     .pio/build/teensy41/firmware.hex
//
// You then copy that HEX file out of Docker and flash it to
// the Teensy.
//
// ============================================================
//
// STEP 1 — CHOOSE THE PROGRAM
// ============================================================
//
// Change the active #include above and the function called
// in setup().
//
// Example:
//
//     #include "latency_test.h"
//
//     runLatencyBenchmark();
//
// ============================================================
//
// STEP 2 — BUILD THE CODE
// ============================================================
//
// 🟧 VS CODE DEV CONTAINER
//
// Run:
//
//     cd /workspace/Robot/archive/platformio-tests/teensy41-basic
//
//     export PATH="$HOME/.platformio/penv/bin:$PATH"
//
//     pio run
//
// Wait for:
//
//     [SUCCESS]
//
// New firmware is created at:
//
//     .pio/build/teensy41/firmware.hex
//
// ============================================================
//
// STEP 3 — COPY THE NEW HEX OUT OF DOCKER
// ============================================================
//
// 🟦 WINDOWS POWERSHELL
//
// Find the Robot container:
//
//     docker ps
//
// Use the CONTAINER ID for 6-DOF-Robotic-Arm.
//
// Example:
//
//     docker cp `
//   Then copy
//       53a87d23ff37:/workspace/Robot/archive/platformio-tests/teensy41-basic/.pio/build/teensy41/firmware.hex `
//   Press enter
//       "$HOME\teensy-flash\firmware.hex"
//
// IMPORTANT:
// Replace 53a87d23ff37 with the current container ID.
//
// Verify the file:
//
//     Get-Item "$HOME\teensy-flash\firmware.hex"
//
// ============================================================
//
// STEP 4 — COPY THE HEX INTO WSL
// ============================================================
//
// 🟦 WINDOWS POWERSHELL
//
//     wsl cp /mnt/c/Users/Nick/teensy-flash/firmware.hex /home/nicks/teensy-flash/firmware.hex
//
// ============================================================
//
// STEP 5 — PUT TEENSY INTO PROGRAMMING MODE
// ============================================================
//
// Physical Teensy:
//
//     Press and release the small PROGRAM button once.
//
// The Teensy should change from:
//
//     16c0:0483 = running firmware / USB Serial
//
// to:
//
//     16c0:0478 = HalfKay bootloader
//
// ============================================================
//
// STEP 6 — ATTACH HALF KAY TO WSL
// ============================================================
//
// 🟦 WINDOWS POWERSHELL
//
//     usbipd list
//
// Find the Teensy. It should show:
//
//     16c0:0478    USB Input Device
//
// Then attach it:
//
//     usbipd attach --wsl --busid 2-2
//
// Replace YOUR_BUS_ID with the actual BUSID.
//
// Example:
//
//     usbipd attach --wsl --busid 2-2
//
// ============================================================
//
// STEP 7 — FLASH THE NEW FIRMWARE
// ============================================================
//
// 🟩 UBUNTU WSL
//
//     lsusb -d 16c0:0478
//
// You should see the HalfKay bootloader.
//

// Then:
//
//     sudo teensy_loader_cli --mcu=TEENSY41 -v -w ~/teensy-flash/firmware.hex
//
// Successful output:
//
//     Found HalfKay Bootloader
//     Programming..................
//     Booting
//
// ============================================================
//
// STEP 8 — REATTACH THE RUNNING TEENSY
//
// ============================================================
//
// After flashing, the Teensy reboots into your new program.
//
// 🟦 WINDOWS POWERSHELL
//
//     usbipd list
//
// If it shows the Teensy as Shared, attach it again:
//
//     usbipd attach --wsl --busid YOUR_BUS_ID
//
// It should now identify as:
//
//     16c0:0483 = USB Serial
//
//
// ============================================================
//
// STEP 9 — VERIFY THE SERIAL DEVICE
//
// ============================================================
//
// 🟩 UBUNTU WSL
//
// Check that the Teensy is available:
//
//     ls -l /dev/ttyACM*
//
// Usually:
//
//     /dev/ttyACM0
//
// DO NOT use:
//
//     cat /dev/ttyACM0
//
// The Python test runner will handle reading AND sending
// commands to the Teensy.
//
//
// ============================================================
//
// STEP 10 — RUN THE PYTHON TEST RUNNER
//
// ============================================================
//
// 🟩 UBUNTU WSL
//
// Run from WSL or the development environment:
//
//     cd /workspace/Robot/archive/platformio-tests
//     python3 ~/teensy-test.py
//
// The program will identify the firmware currently flashed and then:
//
//     1. Find and open the board's serial port.
//     2. Start a benchmark using READY/YES.
//     3. Ask diagnostic firmware for status, or send run_all to the universal suite.
//     4. Return a PASS/FAIL result from the machine-readable protocol.
//
// Example:
//
//     Opening /dev/ttyACM0 at 115200 baud...
//
//     =================================
//     Board Test Runner
//     =================================
//     Detected protocol: benchmark / latency
//
// IMPORTANT:
// The legacy tests are compile-time selections. Flash the matching selection
// before running it. The universal suite is the only image that can run its
// complete collection of tests from one flashed program.
//
//     === TEST SUMMARY ===
//     Duration:       10.00 s
//     Iterations:     ...
//     Average loop:   ... us
//     Min loop:       ... us
//     Max loop:       ... us
//
//     === TEST COMPLETE ===
//
// ============================================================
//
// IMPORTANT:
//
// The Python test runner replaces:
//
//     cat /dev/ttyACM0
//
// You should NOT use cat for these interactive tests.
//
// ============================================================
//
// ============================================================
//
// QUICK VERSION
// ============================================================
//
// 🟧 DEV CONTAINER
//     Edit code
//     → pio run
//
// 🟦 WINDOWS POWERSHELL
//     docker cp ...
//     → wsl cp ...
//     → press PROGRAM button
//     → usbipd list
//     → usbipd attach --wsl --busid ...
//
// 🟩 UBUNTU WSL
//     teensy_loader_cli ...
//     → reattach if necessary
//     → cd /workspace/Robot/archive/platformio-tests
//     → python3 teensy-test.py
//
// ============================================================
//
// IMPORTANT:
// Every time you build new code, you must flash the NEW HEX
// if you want the Teensy to actually run that new code.
//
// Building does NOT change the Teensy.
// Flashing replaces the program stored on the Teensy's flash
// memory with the newly built firmware.
//
// You are NOT permanently accumulating programs on the Teensy.
// Each flash installs the new firmware image.
//
// ============================================================