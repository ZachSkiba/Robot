//
//
//   cd /workspace/Robot/archive/platformio-tests/teensy41-basic && export PATH="$HOME/.platformio/penv/bin:$PATH" && pio run -e uno && pio run -e uno -t upload --upload-port /dev/ttyACM0 && cd /workspace/Robot/archive/platformio-tests && python3 board-test.py --port /dev/ttyACM0 --baud 250000
//
// ============================================================
// BUILD + FLASH + RUN AN ARDUINO UNO R3 TEST
// ============================================================
//
// IMPORTANT:
//
// The .cpp files are source code.
//
// The Arduino Uno R3 does NOT receive new code just because
// you run "pio run".
//
// "pio run -e uno" builds the source code into:
//
//     .pio/build/uno/firmware.hex
//
// The Arduino Uno R3 can be flashed directly from the VS Code
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
// These selections are defined by the existing firmware.
// Choose exactly ONE selection if the source uses mutually
// exclusive compile-time selections.
//
// The selected code must compile for the Uno's ATmega328P.
//
// The universal suite and diagnostic firmware use different
// execution paths. Check their initialization and serial
// protocol before assuming the shared test runner supports
// them.
//
// ============================================================
// STEP 2 - BUILD THE CODE
// ============================================================
//
// 🟧 VS CODE DEVELOPMENT CONTAINER
//
// Run:
//
//     cd /workspace/Robot/archive/platformio-tests/teensy41-basic && export PATH="$HOME/.platformio/penv/bin:$PATH" && pio run -e uno
//
// Wait for:
//
//     [SUCCESS]
//
// New firmware is created at:
//
//     .pio/build/uno/firmware.hex
//
// Verify the file:
//
//     ls -lh .pio/build/uno/firmware.hex
//
// IMPORTANT:
//
// The environment name must match the environment defined
// in platformio.ini.
//
// The standard PlatformIO environment for an Arduino Uno R3
// is typically:
//
//     [env:uno]
//     platform = atmelavr
//     board = uno
//     framework = arduino
//
// Do not overwrite the existing Mega environment. Add a
// separate Uno environment if one does not already exist.
//
// ============================================================
// STEP 3 - VERIFY USB ACCESS
// ============================================================
//
// 🟧 VS CODE DEVELOPMENT CONTAINER
//
// Check that the Arduino Uno is visible:
//
//     ls -l /dev/ttyACM0
//
// List available serial devices:
//
//     pio device list
//
// The serial port may differ depending on USB passthrough,
// the USB interface, and connected devices.
//
// IMPORTANT:
//
// The device must be visible inside the development container,
// not merely in Windows or Ubuntu WSL.
//
// If /dev/ttyACM0 is missing, check USB passthrough before
// attempting to upload.
//
// Do not assume the Uno uses the same USB identification as
// the Mega. Genuine and clone boards may use different USB
// interfaces and identifiers.
//
// ============================================================
// STEP 4 - FLASH THE NEW FIRMWARE
// ============================================================
//
// 🟧 VS CODE DEVELOPMENT CONTAINER
//
// Run:
//
//     cd /workspace/Robot/archive/platformio-tests/teensy41-basic && export PATH="$HOME/.platformio/penv/bin:$PATH" && pio run -e uno -t upload --upload-port /dev/ttyACM0
//
// PlatformIO will:
//
//     1. Build the firmware if necessary.
//     2. Connect through the Uno's serial bootloader.
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
// The Uno uses the AVR upload process, not the ESP32 esptool
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
//     Run the selected test using its supported execution path.
//
// For the shared universal test runner:
//
//     cd /workspace/Robot/archive/platformio-tests && python3 board-test.py --port /dev/ttyACM0 --baud 250000
//
// IMPORTANT:
//
// The command above assumes the firmware is compatible with
// the shared runner and that its serial baud rate is 250000.
//
// The universal firmware currently has its own command-driven
// interface. Its initialization does not automatically invoke
// waitForStart() in main.cpp.
//
// Therefore, do not assume it will display the same YES prompt
// as the benchmark tests.
//
// The diagnostic firmware also has its own command interface.
// Its compatibility with the shared runner must be verified.
//
// If the runner supports explicit universal mode and the
// firmware accepts the expected commands, the following may
// be appropriate:
//
//     cd /workspace/Robot/archive/platformio-tests && python3 board-test.py --port /dev/ttyACM0 --baud 250000 --mode universal --command all
//
// Verify the available arguments using:
//
//     python3 board-test.py --help
//
// Do not assume that the optional arguments exist unless
// the script confirms them.
//
// ============================================================
// STEP 6 - ONE-SHOT BUILD + FLASH + RUN
// ============================================================
//
// 🟧 VS CODE DEVELOPMENT CONTAINER
//
// For a compatible benchmark firmware that waits for the
// shared runner's READY/YES handshake:
//
//     cd /workspace/Robot/archive/platformio-tests/teensy41-basic && export PATH="$HOME/.platformio/penv/bin:$PATH" && pio run -e uno && pio run -e uno -t upload --upload-port /dev/ttyACM0 && sleep 2 && cd /workspace/Robot/archive/platformio-tests && python3 board-test.py --port /dev/ttyACM0 --baud 250000
//
// IMPORTANT:
//
// This is a one-shot build, flash, and runner command.
//
// It is not a guarantee that every test selection is compatible
// with the runner.
//
// Universal and diagnostic firmware require their own
// compatible command-handling workflow.
//
// A successful build and upload do not guarantee a passing
// hardware test.
//
// ============================================================
// STEP 7 - SERIAL MONITOR
// ============================================================
//
// 🟧 VS CODE DEVELOPMENT CONTAINER
//
// To view serial output manually:
//
//     pio device monitor -e uno --port /dev/ttyACM0 --baud 250000
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
// ============================================================
// STEP 8 - VERIFY TEST RESULTS
// ============================================================
//
// The firmware or compatible test runner should report results
// over serial.
//
// Expected protocol markers may include:
//
//     @TEST_PROTOCOL=benchmark
//     @TEST_NAME=loop
//     @TEST_READY
//     @TEST_RESULT=PASS
//     @TEST_COMPLETE
//
// Possible outcomes:
//
//     PASS
//         Implemented correctness checks passed.
//
//     FAIL
//         One or more correctness checks failed.
//
//     INFO
//         Measurements were collected without a correctness
//         PASS claim.
//
//     SKIP
//         A test is unsupported or not applicable.
//
// IMPORTANT:
//
// A successful firmware upload is NOT a successful test.
//
// Verify the actual test output.
//
// ============================================================
// STEP 9 - SELECT A DIFFERENT TEST
// ============================================================
//
// To run a different test:
//
//     1. Open src/main.cpp.
//     2. Disable the currently active RUN_* selection.
//     3. Enable the desired selection.
//     4. Build the Uno environment.
//     5. Upload the new firmware.
//     6. Run the test using its supported execution path.
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
// IMPORTANT - ARDUINO UNO R3 LIMITATIONS
// ============================================================
//
// The Arduino Uno R3 has:
//
//     CPU frequency: 16 MHz
//     Flash:         32 KB nominal
//     SRAM:          2 KB
//     EEPROM:        1 KB
//
// The usable application flash is lower than nominal capacity
// because bootloader space is reserved.
//
// Compared with the Arduino Mega 2560, ESP32, and Teensy 4.1,
// the Uno has substantially less RAM and flash.
//
// Therefore:
//
//     - Large arrays can exhaust SRAM.
//     - Dynamic String operations can increase memory pressure.
//     - Floating-point and trigonometric calculations can be
//       substantially slower.
//     - Timing resolution and overhead differ from other boards.
//     - Hardware-specific cycle-counter tests may be skipped.
//     - Watchdog, reset-reason, memory, and peripheral tests
//       may require board-specific implementations.
//     - USB serial behavior depends on the board's USB interface.
//     - Results should not be compared across boards without
//       accounting for hardware and timing differences.
//
// ============================================================
// FINAL RULE
// ============================================================
//
// Every time you change the source code, rebuild and upload
// the firmware before expecting the Uno to run those changes.
//
// Building does NOT change the program stored on the board.
//
// Uploading installs a new firmware image.
//
// The Uno, Mega, ESP32, and Teensy can share the same general
// test-runner architecture only when their firmware implements
// compatible protocols and accounts for hardware differences.
//
// Verify the Uno's actual build, upload, serial announcement,
// and test results before treating this workflow as validated.
//
// ============================================================
```