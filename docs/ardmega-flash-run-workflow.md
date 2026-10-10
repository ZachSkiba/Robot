//
//      cd /workspace/Robot/archive/platformio-tests/teensy41-basic && export PATH="$HOME/.platformio/penv/bin:$PATH" && pio run -e megaatmega2560 && pio run -e megaatmega2560 -t upload --upload-port /dev/ttyACM0 && cd /workspace/Robot/archive/platformio-tests && python3 board-test.py
//
//
// ============================================================
// BUILD + FLASH + RUN AN ARDUINO MEGA 2560 TEST
// ============================================================
//
// IMPORTANT:
//
// The .cpp files are source code.
// The Arduino Mega does NOT receive new code just because
// you run "pio run".
//
// "pio run -e megaatmega2560" builds the source code into:
//
//     .pio/build/megaatmega2560/firmware.hex
//
// The Arduino Mega can be flashed directly from the VS Code
// development container using PlatformIO.
//
// Unlike the Teensy workflow, no Docker file copy, WSL copy,
// or HalfKay bootloader workflow is required.
//
// ============================================================
// STEP 1 - CHOOSE THE PROGRAM
// ============================================================
//
// Open:
//
//     src/main.cpp
//
// Check the active #define selection.
//
// Example:
//
//     #define RUN_UNIVERSAL_BOARD_TEST
//
// Available selections in the existing source may include:
//
//     RUN_LATENCY_BENCHMARK
//     RUN_LOOP_TIMING_TEST
//     RUN_SERIAL_THROUGHPUT_TEST
//     RUN_CALCULATION_SPEED_TEST
//     RUN_DIAGNOSTIC_FIRMWARE
//     RUN_UNIVERSAL_BOARD_TEST
//
// IMPORTANT:
//
// These are examples of selections from the existing project.
// They must be compatible with the Arduino Mega's AVR core.
//
// Choose exactly ONE selection if the source uses mutually
// exclusive compile-time selections.
//
// The firmware must be implemented to execute the selected
// test automatically after startup if you want a one-shot
// build, flash, and run workflow.
//
// ============================================================
// STEP 2 - BUILD THE CODE
// ============================================================
//
// 🟧 VS CODE DEVELOPMENT CONTAINER
//
// Run:
//
//     cd /workspace/Robot/archive/platformio-tests/teensy41-basic && export PATH="$HOME/.platformio/penv/bin:$PATH" && pio run -e megaatmega2560
//
// Wait for:
//
//     [SUCCESS]
//
// New firmware is created at:
//
//     .pio/build/megaatmega2560/firmware.hex
//
// Verify the file:
//
//     ls -lh .pio/build/megaatmega2560/firmware.hex
//
// IMPORTANT:
//
// The environment name must match the environment defined
// in platformio.ini.
//
// ============================================================
// STEP 3 - VERIFY USB ACCESS
// ============================================================
//
// 🟧 VS CODE DEVELOPMENT CONTAINER
//
// Check that the Arduino Mega is visible:
//
//     ls -l /dev/ttyACM0
//
// List available serial devices:
//
//     pio device list
//
// Previously identified hardware:
//
//     Arduino Mega 2560 R3
//     USB VID:PID = 2341:0042
//     Serial device = /dev/ttyACM0
//
// These details may change if the board is reconnected or
// assigned a different device name.
//
// IMPORTANT:
//
// The device must be visible inside the development container,
// not merely in Windows or Ubuntu WSL.
//
// If /dev/ttyACM0 is missing, check USB passthrough before
// attempting to upload.
//
// ============================================================
// STEP 4 - FLASH THE NEW FIRMWARE
// ============================================================
//
// 🟧 VS CODE DEVELOPMENT CONTAINER
//
// Run:
//
//     cd /workspace/Robot/archive/platformio-tests/teensy41-basic && export PATH="$HOME/.platformio/penv/bin:$PATH" && pio run -e megaatmega2560 -t upload --upload-port /dev/ttyACM0
//
// PlatformIO will:
//
//     1. Build the firmware if necessary.
//     2. Connect to the Mega's bootloader.
//     3. Upload the compiled firmware.
//     4. Verify the upload as supported by the upload tool.
//     5. Reset the board as part of the upload process.
//
// A successful upload should end with:
//
//     [SUCCESS]
//
// IMPORTANT:
//
// The Mega uses the AVR upload process, not the ESP32 esptool
// process or the Teensy HalfKay bootloader.
//
// If uploading fails, verify the port, USB passthrough,
// board environment, and bootloader before changing settings.
//
// ============================================================
// STEP 5 - RUN THE TEST
// ============================================================
//
// The desired workflow is:
//
//     Edit src/main.cpp.
//     Build the firmware.
//     Upload the firmware.
//     Let the Mega run the selected test.
//
// If the firmware automatically executes the test in setup(),
// it may already have completed before you open the serial
// monitor. In that case, reset the board or run the shared
// Python test runner promptly after uploading.
//
// To run the existing universal suite using the shared runner:
//
//     cd /workspace/Robot/archive/platformio-tests && python3 board-test.py --port /dev/ttyACM0 --baud 250000 --mode universal --command all
//
// IMPORTANT:
//
// The command above assumes the Mega firmware implements the
// universal-suite protocol and accepts the requested commands.
//
// The shared runner does not make an incompatible firmware
// compatible, and it cannot change the compile-time selection
// in main.cpp.
//
// If you want the exact one-shot command to build, flash, and
// then run the universal suite, use:
//
//     cd /workspace/Robot/archive/platformio-tests/teensy41-basic && export PATH="$HOME/.platformio/penv/bin:$PATH" && pio run -e megaatmega2560 && pio run -e megaatmega2560 -t upload --upload-port /dev/ttyACM0 && sleep 2 && cd /workspace/Robot/archive/platformio-tests && python3 board-test.py --port /dev/ttyACM0 --baud 250000 --mode universal --command all
//
// This command is appropriate only after the Mega firmware
// has been made compatible with the universal test runner.
//
// ============================================================
// STEP 6 - SERIAL MONITOR
// ============================================================
//
// 🟧 VS CODE DEVELOPMENT CONTAINER
//
// To view serial output manually:
//
//     pio device monitor -e megaatmega2560 --port /dev/ttyACM0 --baud 250000
//
// Exit the monitor with:
//
//     Ctrl+C
//
// IMPORTANT:
//
// Do not run the serial monitor and board-test.py against the
// same serial port at the same time.
//
// Only one program should own the serial port at a time.
//
// The monitor baud rate must match the firmware's configured
// serial baud rate.
//
// If the firmware uses:
//
//     Serial.begin(250000);
//
// then 250000 is the matching monitor speed.
//
// Changing monitor_speed alone does not change the firmware's
// baud rate or make the Mega's serial link faster.
//
// ============================================================
// STEP 7 - VERIFY TEST RESULTS
// ============================================================
//
// The firmware or compatible test runner should report the
// results over serial.
//
// Expected protocol markers may include:
//
//     @TEST_RESULT=PASS
//     @TEST_COMPLETE
//
// Other possible outcomes:
//
//     PASS
//         Implemented correctness checks passed.
//
//     FAIL
//         One or more correctness checks failed.
//
//     PASS_WITH_SKIPS
//         Applicable tests passed, but some capabilities were
//         skipped.
//
//     INFO
//         Measurements were collected without a correctness
//         PASS claim.
//
// IMPORTANT:
//
// A successful firmware upload is NOT a successful test.
//
// Verify the actual test results.
//
// ============================================================
// STEP 8 - SELECT A DIFFERENT TEST
// ============================================================
//
// To run a different test:
//
//     1. Open src/main.cpp.
//     2. Disable the currently active RUN_* selection.
//     3. Enable the desired selection.
//     4. Build the Mega environment.
//     5. Upload the new firmware.
//     6. Run the test or compatible test runner.
//
// Example:
//
//     // #define RUN_LATENCY_BENCHMARK
//     // #define RUN_LOOP_TIMING_TEST
//     // #define RUN_SERIAL_THROUGHPUT_TEST
//     // #define RUN_CALCULATION_SPEED_TEST
//     // #define RUN_DIAGNOSTIC_FIRMWARE
//     #define RUN_UNIVERSAL_BOARD_TEST
//
// Only one mutually exclusive selection should be active.
//
// ============================================================
// QUICK VERSION
// ============================================================
//
// 🟧 VS CODE DEVELOPMENT CONTAINER
//
// Edit src/main.cpp
//         ↓
// Select the desired test
//         ↓
// Build:
//     pio run -e megaatmega2560
//         ↓
// Upload:
//     pio run -e megaatmega2560 -t upload --upload-port /dev/ttyACM0
//         ↓
// Run the test using the firmware's supported execution path
//
// For the universal suite, if firmware compatibility is
// confirmed:
//
//     cd /workspace/Robot/archive/platformio-tests && python3 board-test.py --port /dev/ttyACM0 --baud 250000 --mode universal --command all
//
// ============================================================
// IMPORTANT - ARDUINO MEGA LIMITATIONS
// ============================================================
//
// The Arduino Mega 2560 has:
//
//     CPU frequency: 16 MHz
//     Flash:         256 KB nominal
//     SRAM:          8 KB
//
// The usable application flash is lower than the nominal
// total because bootloader space is reserved.
//
// Compared with the Teensy 4.1 and ESP32, the Mega has
// substantially less processing power and RAM.
//
// Therefore:
//
//     - Large buffers and arrays can exhaust SRAM.
//     - Floating-point and trigonometric calculations may
//       execute substantially more slowly.
//     - High-frequency timing measurements have different
//       resolution and overhead.
//     - Hardware cycle-counter tests need an AVR-specific
//       implementation or must be skipped.
//     - Watchdog, reset-reason, memory, and peripheral tests
//       may need board-specific adapters.
//     - Results should not be compared across boards without
//       accounting for their different clock rates, timer
//       implementations, and hardware.
//
// ============================================================
// FINAL RULE
// ============================================================
//
// Every time you change the source code, rebuild and upload
// the firmware before expecting the Mega to run the changes.
//
// Building does NOT change the program stored on the board.
//
// Uploading replaces the applicable firmware image.
//
// Each upload installs a new firmware image.
//
// The Mega, ESP32, and Teensy can share the same general
// test-runner architecture only if their firmware implements
// compatible protocols and handles hardware differences.
//
// The Mega's universal-suite compatibility and automatic
// execution must be verified in the actual source before
// treating the one-shot command as validated.
//
// ============================================================