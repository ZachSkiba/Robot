#include <Arduino.h>

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
// 4) Diagnostic firmware
//    Include:  "firmware-updates.h"
//    Functions:
//      initializeDiagnosticFirmware()
//      runDiagnosticFirmware()
//
// ============================================================

// CHANGE THIS: uncomment ONE include only.

#include "latency_test.h"

// #include "latency_test.h"
// #include "loop_timing_test.h"
// #include "serial_throughput_test.h"
// #include "firmware-updates.h"


// ============================================================
// SETTINGS
// ============================================================

// CHANGE THIS: Serial speed
// Common: 9600, 115200
constexpr uint32_t SERIAL_BAUD = 115200;

// CHANGE THIS: startup delay
// Unit: milliseconds
constexpr uint32_t STARTUP_DELAY_MS = 1000;

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

                if (input == "READY")
                {
                    Serial.println();
                    Serial.println("================================");
                    Serial.println("Teensy Test Runner");
                    Serial.println("================================");
                    Serial.println("Teensy is connected.");
                    Serial.println("Type YES and press Enter to start.");
                    Serial.println();

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

    delay(100);

    waitForStart();

    Serial.println("Starting selected test...");
    Serial.println();

    // CHANGE THIS: call the function matching the include above.

    runLatencyBenchmark();

    // Other options:
    // runLatencyBenchmark();
    // runLoopTimingTest();
    // runSerialThroughputTest();

    // Diagnostic firmware is slightly different:
    // initializeDiagnosticFirmware();
}

void loop()
{
    // Most tests do everything inside setup(), so loop stays empty.

    // For diagnostic firmware, use:
    // runDiagnosticFirmware();
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
//       209a464b76cb:/workspace/Robot/archive/platformio-tests/teensy41-basic/.pio/build/teensy41/firmware.hex `
//       "$HOME\teensy-flash\firmware.hex"
//
// IMPORTANT:
// Replace 209a464b76cb with the current container ID.
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
// STEP 10 — RUN THE TEST
//
// ============================================================
//
// 🟩 UBUNTU WSL
//
// Run:
//
//     python3 ~/teensy-test.py
//
// The program will:
//
//     1. Connect to the Teensy.
//     2. Wait for the "Type YES..." prompt.
//     3. Display the prompt.
//     4. Let you type YES.
//     5. Send YES to the Teensy.
//     6. Start the selected test.
//     7. Display the test results automatically.
//
// Example:
//
//     Connected to Teensy.
//     Waiting for Teensy prompt...
//
//     =================================
//     Teensy Test Runner
//     =================================
//     Selected program is ready.
//     Type YES and press Enter to start.
//
//     Type YES and press Enter:
//     > YES
//
//     === TEST OUTPUT ===
//     === Teensy Latency Test ===
//     Measuring loop cadence with micros()...
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
//     → cat /dev/ttyACM0
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