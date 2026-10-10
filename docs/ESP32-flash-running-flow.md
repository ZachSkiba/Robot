// 
//          cd /workspace/Robot/archive/platformio-tests/teensy41-basic && export PATH="$HOME/.platformio/penv/bin:$PATH" && pio run -e esp32dev && pio run -e esp32dev -t upload --upload-port /dev/ttyUSB0 && cd /workspace/Robot/archive/platformio-tests && python3 board-test.py
//
//============================================================
// BUILD + FLASH + RUN AN ESP32 TEST
// ============================================================
//
// IMPORTANT:
//
// The .cpp files are source code.
// The ESP32 does NOT get the new code just because you run
// "pio run".
//
// "pio run -e esp32dev" builds the source code into:
//
//     .pio/build/esp32dev/firmware.bin
//
// Unlike the Teensy workflow, the ESP32 can be flashed directly
// from the VS Code development container using PlatformIO.
//
// No Docker file copy, HEX conversion, or HalfKay bootloader
// workflow is required.
//
// ============================================================
//
// STEP 1 - CHOOSE THE PROGRAM
// ============================================================
//
// Change the active #define selection in src/main.cpp.
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
// These selections must be implemented and compatible with
// the ESP32 environment.
//
// Choose exactly ONE selection.
//
// The firmware should run the selected test automatically
// after startup. It should not require a Python command such
// as "--mode universal" or "--command all".
//
// ============================================================
//
// STEP 2 - BUILD THE CODE
// ============================================================
//
// 🟧 VS CODE DEV CONTAINER
//
// Run:
//
//     cd /workspace/Robot/archive/platformio-tests/teensy41-basic && export PATH="$HOME/.platformio/penv/bin:$PATH" && pio run -e esp32dev
//
// Wait for:
//
//     [SUCCESS]
//
// New firmware is created at:
//
//     .pio/build/esp32dev/firmware.bin
//
// Verify the file:
//
//     ls -lh .pio/build/esp32dev/firmware.bin
//
// ============================================================
//
// STEP 3 - VERIFY USB ACCESS
// ============================================================
//
// 🟧 VS CODE DEV CONTAINER
//
// Check that the ESP32 serial adapter is visible:
//
//     ls -l /dev/ttyUSB0
//
// Check USB devices:
//
//     lsusb
//
// The previously identified adapter was:
//
//     Silicon Labs CP210x UART Bridge
//
// Expected serial device:
//
//     /dev/ttyUSB0
//
// IMPORTANT:
//
// The device must be visible inside the development container,
// not merely in Windows or Ubuntu WSL.
//
// If the device is missing, check USB passthrough before
// attempting to upload.
//
// Do not rebuild the container automatically. A rebuild does
// not guarantee that USB passthrough will be fixed.
//
// ============================================================
//
// STEP 4 - FLASH THE NEW FIRMWARE
// ============================================================
//
// 🟧 VS CODE DEV CONTAINER
//
// Run:
//
//     cd /workspace/Robot/archive/platformio-tests/teensy41-basic && export PATH="$HOME/.platformio/penv/bin:$PATH" && pio run -e esp32dev -t upload --upload-port /dev/ttyUSB0
//
// PlatformIO will:
//
//     1. Build the ESP32 firmware if necessary.
//     2. Connect to the ESP32 bootloader.
//     3. Write the firmware to flash.
//     4. Verify the written data.
//     5. Reset the ESP32.
//
// Expected successful output includes:
//
//     Hash of data verified.
//     Hard resetting via RTS pin...
//
//     [SUCCESS]
//
// If the upload fails to connect, the board may require manual
// bootloader entry. On many ESP32 development boards, hold BOOT
// during the connection attempt.
//
// ============================================================
//
// STEP 5 - RUN THE SELECTED TEST
// ============================================================
//
//      cd /workspace/Robot/archive/platformio-tests && python3 board-test.py
//
// The intended workflow is:
//
//     Edit the selected test in src/main.cpp.
//     Build the firmware.
//     Upload the firmware.
//     Let the ESP32 start the selected test automatically.
//
// No Python test-selection command should be necessary.
//
// Example firmware startup:
//
//     =================================
//     ESP32 Board Test
//     =================================
//     Board: ESP32
//     Firmware: universal-board-test
//     Test starting...
//
// The actual startup messages depend on the implementation.
//
// IMPORTANT:
//
// Automatic execution must be implemented in the ESP32
// firmware's setup() function.
//
// If setup() waits for a "READY", "YES", or other serial
// command, the firmware must be changed before this workflow
// can operate fully automatically.
//
// ============================================================
//
// STEP 6 - VERIFY SERIAL OUTPUT
// ============================================================
//
// 🟩 UBUNTU WSL
//
// The serial device may appear as:
//
//     /dev/ttyUSB0
//
// Check:
//
//     ls -l /dev/ttyUSB0
//
// Optionally verify the chip:
//
//     python3 -m esptool --port /dev/ttyUSB0 chip_id
//
// Previously identified hardware:
//
//     Chip: ESP32-D0WD-V3
//     Revision: 3.1
//     Crystal: 40MHz
//     MAC: e0:8c:fe:5c:0c:8c
//
// These details identify the chip. They do not prove that the
// newly flashed test firmware is executing correctly.
//
// IMPORTANT:
//
// Only one application should own the serial port at a time.
//
// If PlatformIO or another serial monitor has the port open,
// close it before opening a separate serial monitor.
//
// ============================================================
//
// STEP 7 - VIEW TEST RESULTS
// ============================================================
//
// The ESP32 firmware should print its own results over serial.
//
// Example:
//
//     === TEST SUMMARY ===
//     Duration:       10.00 s
//     Iterations:     ...
//     Average loop:   ... us
//     Min loop:       ... us
//     Max loop:       ... us
//
//     @TEST_RESULT=PASS
//     @TEST_COMPLETE
//
// The exact measurements and markers depend on the selected
// test and its implementation.
//
// The firmware should distinguish:
//
//     PASS
//         The test passed its implemented criteria.
//
//     FAIL
//         The test detected a failure.
//
//     PASS_WITH_SKIPS
//         The test passed, but some capabilities were skipped.
//
//     INFO
//         Measurements were collected without claiming a
//         correctness PASS.
//
// Do not report a PASS merely because the firmware uploaded.
//
// ============================================================
//
// STEP 8 - SELECT A DIFFERENT TEST
// ============================================================
//
// To run a different test:
//
//     1. Open src/main.cpp.
//     2. Disable the currently active RUN_* selection.
//     3. Enable the desired RUN_* selection.
//     4. Build the ESP32 environment.
//     5. Upload the new firmware.
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
// Only one selection should be active.
//
// The universal suite can expose multiple tests through one
// firmware image, but only if the implementation provides
// those tests and their runtime selection mechanism.
//
// ============================================================
//
// QUICK VERSION
// ============================================================
//
// 🟧 VS CODE DEV CONTAINER
//
//     Edit src/main.cpp
//         ↓
//     Select the desired RUN_* test
//         ↓
//     Build:
//
//     pio run -e esp32dev
//         ↓
//     Upload:
//
//     pio run -e esp32dev -t upload --upload-port /dev/ttyUSB0
//         ↓
//     ESP32 reboots and runs the selected firmware
//
// 🟩 SERIAL OUTPUT
//
//     Read the test summary and result markers.
//     Verify PASS, FAIL, INFO, or PASS_WITH_SKIPS.
//
// ============================================================
//
// IMPORTANT
// ============================================================
//
// Every time you change the source code, you must build and
// upload the new firmware if you want the ESP32 to run it.
//
// Building does NOT change the program stored on the ESP32.
//
// Uploading replaces the applicable firmware stored in flash.
//
// You are NOT permanently accumulating programs on the ESP32.
// Each upload installs a new firmware image.
//
// The ESP32 and Teensy can share the same general testing
// architecture, but their hardware-specific tests must account
// for differences in timers, GPIO, ADC, serial interfaces,
// and peripheral support.
//
// ============================================================
//
// CURRENT LIMITATION
// ============================================================
//
// The direct build-and-upload workflow has been demonstrated
// successfully for the ESP32.
//
// However, automatic test execution, self-contained serial
// reporting, and complete compatibility of the universal test
// suite must be verified in the actual ESP32 source before
// this document can be considered fully validated.
//
// ============================================================
```
