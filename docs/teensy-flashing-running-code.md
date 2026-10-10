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
// STEP 1 - CHOOSE THE PROGRAM
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
// STEP 2 - BUILD THE CODE
// ============================================================
//
// 🟧 VS CODE DEV CONTAINER
//
// Run:
//
//     cd /workspace/Robot/archive/platformio-tests/teensy41-basic && export PATH="$HOME/.platformio/penv/bin:$PATH" && pio run
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
// STEP 3 - COPY THE NEW HEX OUT OF DOCKER
// ============================================================
//
// 🟦 WINDOWS POWERSHELL
//
// Find the Robot container:
//
//     docker ps
//
// Replace <container-id> with the ID reported by `docker ps`.
//
//     docker cp <container-id>:/workspace/Robot/archive/platformio-tests/teensy41-basic/.pio/build/teensy41/firmware.hex "$HOME\teensy-flash\firmware.hex"
//
// Current: docker cp 76b7d87f245c:/workspace/Robot/archive/platformio-tests/teensy41-basic/.pio/build/teensy41/firmware.hex "$HOME\teensy-flash\firmware.hex"
//
// Verify the file:
//
//     Get-Item "$HOME\teensy-flash\firmware.hex"
//
// ============================================================
//
// STEP 4 - COPY THE HEX INTO WSL
// ============================================================
//
// 🟦 WINDOWS POWERSHELL
//
//     wsl cp /mnt/c/Users/Nick/teensy-flash/firmware.hex ~/teensy-flash/firmware.hex
//
// ============================================================
//
// STEP 5 - PUT TEENSY INTO PROGRAMMING MODE
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
// STEP 6 - ATTACH HALF KAY TO WSL
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
// Then attach it
// Replace <bus-id> with the actual BUSID:
//
//     usbipd attach --wsl --busid 2-2
//
// ============================================================
//
// STEP 7 - FLASH THE NEW FIRMWARE
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
// STEP 8 - REATTACH THE RUNNING TEENSY
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
// STEP 9 - VERIFY THE SERIAL DEVICE
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
// STEP 10 - RUN THE PYTHON TEST RUNNER
//
// ============================================================
//
// 🟩 UBUNTU WSL
//
// Run from WSL or the development environment:
//
//     cd /workspace/Robot/archive/platformio-tests && python3 board-test.py
//
// The program identifies the firmware currently flashed and then:
//
//     1. Find and open the board's serial port.
//     2. Send the default universal-suite command, or the command selected
//        with --command.
//     3. Return the result from the machine-readable protocol. INFO-only
//        commands report measurements without claiming a correctness PASS.
//        PASS_WITH_SKIPS indicates that some capabilities were skipped.
//
// Example:
//
//     Opening /dev/ttyACM0 at 2500000 baud...
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
//     → usbipd attach --wsl --busid <bus-id>
//
// 🟩 UBUNTU WSL
//     teensy_loader_cli ...
//     → reattach if necessary
//     → cd /workspace/Robot/archive/platformio-tests
//     → python3 board-test.py
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