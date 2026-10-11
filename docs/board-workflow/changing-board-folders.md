Current folders is in Robot/Archive/platformio-tests/board-test.py and teensy42-basic/platformio.ini
// ============================================================
// HOW TO RUN AN ESP32 PROJECT FROM A NEW FOLDER
// ============================================================
//
// CURRENT WORKFLOW:
// Build -> Flash -> Run the universal board test
//
// ============================================================
// STEP 1 - IDENTIFY THE NEW PROJECT FOLDER
// ============================================================
//
// Example new project:
//
// /workspace/Robot/firmware/esp32-motor-test
//
// Every PlatformIO project must have its own platformio.ini.
//
// ============================================================
// STEP 2 - CHECK THE PLATFORMIO ENVIRONMENT
// ============================================================
//
// Open platformio.ini in the new project folder.
//
// Example:
//
// [env:esp32dev]
//
// If the environment is esp32dev, use:
//
//     -e esp32dev
//
// If the environment has another name, use that name instead.
//
// ============================================================
// STEP 3 - BUILD, FLASH, AND RUN THE TEST
// ============================================================
//
// 🟧 VS CODE DEV CONTAINER
//
// Replace the example project path below with your actual path.
//
//     cd /workspace/Robot/firmware/esp32-motor-test && export
//     PATH="$HOME/.platformio/penv/bin:$PATH" && pio run -e
//     esp32dev && pio run -e esp32dev -t upload
//     --upload-port /dev/ttyUSB0 && cd
//     /workspace/Robot/archive/platformio-tests && python3
//     board-test.py
//
// IMPORTANT:
// Paste the entire command as ONE LINE, without line breaks
// between command arguments.
//
// ============================================================
// STEP 4 - UNDERSTAND WHAT THE COMMAND DOES
// ============================================================
//
// 1. Enters the new project folder.
// 2. Adds PlatformIO to PATH.
// 3. Builds the ESP32 firmware.
// 4. Uploads the new firmware to /dev/ttyUSB0.
// 5. Changes to the shared test-runner folder.
// 6. Runs board-test.py.
//
// The test runner automatically identifies compatible firmware
// and runs its default universal test command.
//
// ============================================================
// STEP 5 - WHAT YOU MAY NEED TO CHANGE
// ============================================================
//
// PROJECT PATH:
//     Change both occurrences of the project directory only
//     if you change the folder.
//
// ENVIRONMENT:
//     Change esp32dev if platformio.ini uses another name.
//
// SERIAL PORT:
//     Change /dev/ttyUSB0 if the ESP32 appears on another port.
//
// TEST RUNNER:
//     Keep the shared board-test.py path if you are using
//     the existing shared runner.
//
// ============================================================
// IMPORTANT LIMITATIONS
// ============================================================
//
// - The new firmware must implement the expected test protocol.
// - The selected environment must target the correct ESP32.
// - The upload port must identify the correct physical board.
// - A successful build does not guarantee a successful upload.
// - The test runner cannot automatically test arbitrary firmware
//   that does not implement its protocol.
//
// ============================================================
// END OF ESP32 NEW-FOLDER INSTRUCTIONS
// ============================================================
//
// One liner
//
//    cd /workspace/Robot/firmware/esp32-motor-test && export PATH="$HOME/.platformio/penv/bin:$PATH" && pio run -e esp32dev && pio run -e esp32dev -t upload --upload-port /dev/ttyUSB0 && cd /workspace/Robot/archive/platformio-tests && python3 board-test.py
//
//
//
//
// ============================================================
// HOW TO RUN A TEENSY 4.1 PROJECT FROM A NEW FOLDER
// ============================================================
//
// CURRENT WORKFLOW:
// Build -> Copy HEX -> Attach HalfKay -> Flash -> Reattach
// -> Run the shared board test runner
//
// Unlike the ESP32 workflow, the Teensy process uses a separate
// HEX transfer and flashing procedure in your current setup.
//
// ============================================================
// STEP 1 - IDENTIFY THE NEW PROJECT FOLDER
// ============================================================
//
// Example:
//
// /workspace/Robot/firmware/teensy-motor-test
//
// ============================================================
// STEP 2 - CHECK THE PLATFORMIO ENVIRONMENT
// ============================================================
//
// Open the new project's platformio.ini.
//
// Example:
//
// [env:teensy41]
//
// Use the environment name defined in that file.
//
// ============================================================
// STEP 3 - BUILD THE NEW FIRMWARE
// ============================================================
//
// 🟧 VS CODE DEV CONTAINER
//
//     cd /workspace/Robot/firmware/teensy-motor-test && export
//     PATH="$HOME/.platformio/penv/bin:$PATH" && pio run -e
//     teensy41
//
// Replace teensy41 if the new project's environment has
// a different name.
//
// Expected output:
//
//     .pio/build/teensy41/firmware.hex
//
// The environment name in this path must match the build.
//
// ============================================================
// STEP 4 - COPY THE HEX FILE OUT OF DOCKER
// ============================================================
//
// 🟦 WINDOWS POWERSHELL
//
// Find the running container:
//
//     docker ps
//
// Copy the HEX file from the new project:
//
//     docker cp <container-id>:/workspace/Robot/firmware/teensy-motor-test/.pio/build/teensy41/firmware.hex "$HOME\teensy-flash\firmware.hex"
//
// Replace:
//     <container-id> with the current container ID
//     teensy41 with the actual PlatformIO environment name
//
// Verify:
//
//     Get-Item "$HOME\teensy-flash\firmware.hex"
//
// ============================================================
// STEP 5 - COPY THE HEX FILE INTO WSL
// ============================================================
//
// 🟦 WINDOWS POWERSHELL
//
// If the Windows destination is unchanged:
//
//     wsl cp /mnt/c/Users/Nick/teensy-flash/firmware.hex ~/teensy-flash/firmware.hex
//
// ============================================================
// STEP 6 - FLASH THE TEENSY
// ============================================================
//
// 1. Press and release the Teensy's PROGRAM button.
// 2. In Windows PowerShell, run:
//
//     usbipd list
//
// 3. Find the Teensy HalfKay bootloader.
// 4. Attach it to WSL:
//
//     usbipd attach --wsl --busid YOUR_BUS_ID
//
// 5. In Ubuntu WSL, verify:
//
//     lsusb -d 16c0:0478
//
// 6. Flash the new HEX:
//
//     sudo teensy_loader_cli --mcu=TEENSY41 -v -w ~/teensy-flash/firmware.hex
//
// ============================================================
// STEP 7 - REATTACH THE RUNNING TEENSY
// ============================================================
//
// After flashing, the Teensy reboots.
//
// In Windows PowerShell:
//
//     usbipd list
//
// If necessary, attach the running Teensy to WSL again:
//
//     usbipd attach --wsl --busid YOUR_BUS_ID
//
// In Ubuntu WSL, verify:
//
//     ls -l /dev/ttyACM*
//
// ============================================================
// STEP 8 - RUN THE SHARED TEST RUNNER
// ============================================================
//
// 🟩 UBUNTU WSL
//
//     cd /workspace/Robot/archive/platformio-tests && python3 board-test.py
//
// This runs the shared test runner against compatible firmware.
//
// ============================================================
// STEP 9 - WHAT YOU MAY NEED TO CHANGE
// ============================================================
//
// PROJECT PATH:
//     Change the project directory in the build command.
//
// ENVIRONMENT:
//     Change teensy41 if the new project uses another name.
//
// HEX SOURCE PATH:
//     Change the project directory and environment in docker cp.
//
// WINDOWS HEX DESTINATION:
//     Can remain $HOME\teensy-flash\firmware.hex.
//
// WSL HEX DESTINATION:
//     Can remain ~/teensy-flash/firmware.hex.
//
// FLASH COMMAND:
//     Keep --mcu=TEENSY41 for the Teensy 4.1.
//
// TEST RUNNER:
//     Keep the shared board-test.py path if the firmware supports
//     its protocol.
//
// ============================================================
// IMPORTANT LIMITATIONS
// ============================================================
//
// - Always flash the HEX built from the intended project.
// - Do not flash a stale HEX from another project.
// - The shared test runner requires compatible firmware.
// - USB bus IDs may change after disconnecting or rebooting.
// - Building does not flash the Teensy automatically.
//
// ============================================================
// END OF TEENSY NEW-FOLDER INSTRUCTIONS
// ============================================================
//
//
//
//
// ============================================================
// HOW TO RUN AN ARDUINO MEGA 2560 PROJECT FROM A NEW FOLDER
// ============================================================
//
// CURRENT WORKFLOW:
// Build -> Flash -> Run the shared board test runner
//
// Unlike the Teensy workflow, the Mega can be uploaded directly
// from the VS Code development container using PlatformIO.
//
// ============================================================
// STEP 1 - IDENTIFY THE NEW PROJECT FOLDER
// ============================================================
//
// Example new project:
//
// /workspace/Robot/firmware/mega-motor-test
//
// Every independent PlatformIO project must have its own
// platformio.ini.
//
// ============================================================
// STEP 2 - CHECK THE PLATFORMIO ENVIRONMENT
// ============================================================
//
// Open platformio.ini in the new project folder.
//
// The environment should look like:
//
// [env:megaatmega2560]
// platform = atmelavr
// board = megaatmega2560
// framework = arduino
// upload_protocol = wiring
// monitor_speed = 250000
//
// PlatformIO's documented board ID for the Arduino Mega 2560
// is megaatmega2560.
//
// Reference:
// https://docs.platformio.org/en/latest/boards/atmelavr/megaatmega2560.html
//
// If the environment has a different name, use that name
// instead of megaatmega2560 in the commands below.
//
// IMPORTANT:
// monitor_speed configures the serial monitor. The firmware
// must independently use the same baud rate in Serial.begin().
//
// ============================================================
// STEP 3 - VERIFY USB ACCESS
// ============================================================
//
// VS CODE DEVELOPMENT CONTAINER
//
// Check that the Mega is visible:
//
//     ls -l /dev/ttyACM0
//
// List detected serial devices:
//
//     export PATH="$HOME/.platformio/penv/bin:$PATH" && pio device list
//
// Previously detected Mega:
//
//     USB VID:PID = 2341:0042
//     Serial device = /dev/ttyACM0
//
// If the port is missing, check USB passthrough before
// attempting to upload.
//
// ============================================================
// STEP 4 - BUILD, FLASH, AND RUN THE TEST
// ============================================================
//
// VS CODE DEVELOPMENT CONTAINER
//
// Replace the example project path with your actual folder.
//
//     cd /workspace/Robot/firmware/mega-motor-test && export PATH="$HOME/.platformio/penv/bin:$PATH" && pio run -e megaatmega2560 && pio run -e megaatmega2560 -t upload --upload-port /dev/ttyACM0 && cd /workspace/Robot/archive/platformio-tests && python3 board-test.py --port /dev/ttyACM0 --baud 250000
//
// Paste the entire command as ONE LINE.
//
// ============================================================
// STEP 5 - UNDERSTAND WHAT THE COMMAND DOES
// ============================================================
//
// 1. Enters the new Mega project folder.
// 2. Adds PlatformIO to PATH.
// 3. Builds the Mega firmware.
// 4. Uploads the firmware to /dev/ttyACM0.
// 5. Changes to the shared test-runner folder.
// 6. Runs board-test.py against the Mega.
//
// The build output is normally:
//
//     .pio/build/megaatmega2560/firmware.hex
//
// PlatformIO handles the HEX file and upload process directly.
// No manual Docker copy, WSL copy, or Teensy HalfKay flashing
// procedure is required.
//
// ============================================================
// STEP 6 - WHAT YOU MAY NEED TO CHANGE
// ============================================================
//
// PROJECT PATH:
//     Change the project directory in the build command.
//
// ENVIRONMENT:
//     Change megaatmega2560 if platformio.ini uses another name.
//
// SERIAL PORT:
//     Change /dev/ttyACM0 if the Mega appears on another port.
//
// BAUD RATE:
//     Change 250000 if the firmware uses another baud rate.
//
// TEST RUNNER:
//     Keep the shared runner path:
//
//     /workspace/Robot/archive/platformio-tests/board-test.py
//
// ============================================================
// IMPORTANT LIMITATIONS
// ============================================================
//
// - The firmware must implement the protocol expected by
//   board-test.py.
// - The shared runner cannot automatically test arbitrary
//   firmware that does not implement its protocol.
// - The Mega has only 8 KB of SRAM and runs at 16 MHz.
// - Some tests may require AVR-specific adaptations.
// - A successful build does not guarantee a successful upload.
// - A successful upload does not guarantee that tests pass.
// - The shared runner's default command is determined by its
//   implementation and the firmware protocol it detects.
//
// ============================================================
// OPTIONAL - RUN A COMPATIBLE UNIVERSAL TEST SUITE
// ============================================================
//
// If the firmware supports the universal-suite protocol:
//
//     cd /workspace/Robot/archive/platformio-tests && python3 board-test.py --port /dev/ttyACM0 --baud 250000 --mode universal --command all
//
// Use this explicit command only when the Mega firmware
// actually supports the universal-suite protocol.
//
// ============================================================
// OPTIONAL - OPEN THE SERIAL MONITOR
// ============================================================
//
//     cd /workspace/Robot/firmware/mega-motor-test && export PATH="$HOME/.platformio/penv/bin:$PATH" && pio device monitor -e megaatmega2560 --port /dev/ttyACM0 --baud 250000
//
// Exit with Ctrl+C.
//
// Do not run the serial monitor and board-test.py simultaneously
// against the same port.
//
// ============================================================
// END OF ARDUINO MEGA NEW-FOLDER INSTRUCTIONS
// ============================================================
//
// ONE-LINER
//
//     cd /workspace/Robot/firmware/mega-motor-test && export PATH="$HOME/.platformio/penv/bin:$PATH" && pio run -e megaatmega2560 && pio run -e megaatmega2560 -t upload --upload-port /dev/ttyACM0 && cd /workspace/Robot/archive/platformio-tests && python3 board-test.py --port /dev/ttyACM0 --baud 250000
//
// ============================================================

//
// ============================================================
// HOW TO RUN AN ARDUINO UNO R3 PROJECT FROM A NEW FOLDER
// ============================================================
//
// CURRENT WORKFLOW:
// Build -> Flash -> Run the shared board test runner
//
// Unlike the Teensy workflow, the Uno can be uploaded directly
// from the VS Code development container using PlatformIO.
//
// ============================================================
// STEP 1 - IDENTIFY THE NEW PROJECT FOLDER
// ============================================================
//
// Example new project:
//
// /workspace/Robot/firmware/uno-motor-test
//
// Every independent PlatformIO project must have its own
// platformio.ini.
//
// ============================================================
// STEP 2 - CHECK THE PLATFORMIO ENVIRONMENT
// ============================================================
//
// Open platformio.ini in the new project folder.
//
// The environment should look like:
//
// [env:uno]
// platform = atmelavr
// board = uno
// framework = arduino
// upload_protocol = arduino
// monitor_speed = 250000
//
// PlatformIO's documented board ID for the Arduino Uno R3
// is uno.
//
// Reference:
// https://docs.platformio.org/page/boards/atmelavr/uno.html
//
// If the environment has a different name, use that name
// instead of uno in the commands below.
//
// IMPORTANT:
//
// monitor_speed configures the serial monitor. The firmware
// must independently use the same baud rate in Serial.begin().
//
// The upload baud rate used by the bootloader is separate from
// the firmware's serial communication baud rate.
//
// ============================================================
// STEP 3 - VERIFY USB ACCESS
// ============================================================
//
// VS CODE DEVELOPMENT CONTAINER
//
// Check that the Uno is visible:
//
//     ls -l /dev/ttyACM0
//
// List detected serial devices:
//
//     export PATH="$HOME/.platformio/penv/bin:$PATH" && pio device list
//
// The serial port may differ depending on USB passthrough,
// the USB interface, and connected devices.
//
// IMPORTANT:
//
// Do not assume the Uno uses the same USB identification as
// the Mega. Genuine and clone boards may use different USB
// interfaces and identifiers.
//
// If the port is missing, check USB passthrough before
// attempting to upload.
//
// ============================================================
// STEP 4 - BUILD, FLASH, AND RUN THE TEST
// ============================================================
//
// VS CODE DEVELOPMENT CONTAINER
//
// Replace the example project path with your actual folder.
//
//     cd /workspace/Robot/firmware/uno-motor-test && export PATH="$HOME/.platformio/penv/bin:$PATH" && pio run -e uno && pio run -e uno -t upload --upload-port /dev/ttyACM0 && cd /workspace/Robot/archive/platformio-tests && python3 board-test.py --port /dev/ttyACM0 --baud 250000
//
// Paste the entire command as ONE LINE.
//
// IMPORTANT:
//
// This command assumes the selected firmware implements the
// protocol expected by the shared test runner.
//
// ============================================================
// STEP 5 - UNDERSTAND WHAT THE COMMAND DOES
// ============================================================
//
// 1. Enters the new Uno project folder.
// 2. Adds PlatformIO to PATH.
// 3. Builds the Uno firmware.
// 4. Uploads the firmware to /dev/ttyACM0.
// 5. Changes to the shared test-runner folder.
// 6. Runs board-test.py against the Uno.
//
// The build output is normally:
//
//     .pio/build/uno/firmware.hex
//
// PlatformIO handles the HEX file and upload process directly.
// No manual Docker copy, WSL copy, or Teensy HalfKay flashing
// procedure is required.
//
// ============================================================
// STEP 6 - WHAT YOU MAY NEED TO CHANGE
// ============================================================
//
// PROJECT PATH:
//     Change the project directory in the build command.
//
// ENVIRONMENT:
//     Change uno if platformio.ini uses another environment
//     name. The environment's board setting should still target
//     the correct Uno hardware.
//
// SERIAL PORT:
//     Change /dev/ttyACM0 if the Uno appears on another port.
//
// BAUD RATE:
//     Change 250000 if the firmware uses another baud rate.
//
// TEST RUNNER:
//     Keep the shared runner path:
//
//     /workspace/Robot/archive/platformio-tests/board-test.py
//
// ============================================================
// IMPORTANT - EXISTING FIRMWARE SOURCE
// ============================================================
//
// If you are reusing the existing test firmware, check:
//
//     src/main.cpp
//
// Select the desired firmware using its RUN_* definition.
//
// Example:
//
//     #define RUN_LOOP_TIMING_TEST
//
// Only one mutually exclusive selection should be active.
//
// The firmware must compile for the Uno's ATmega328P.
//
// A new project folder also needs its own source files and
// required headers. Creating platformio.ini alone does not
// copy the existing test firmware into the new project.
//
// ============================================================
// STEP 7 - RUN THE TEST
// ============================================================
//
// The default shared runner command is:
//
//     cd /workspace/Robot/archive/platformio-tests && python3 board-test.py --port /dev/ttyACM0 --baud 250000
//
// The runner must detect a compatible firmware announcement
// and use a protocol supported by the selected firmware.
//
// IMPORTANT:
//
// Benchmark firmware may use the READY/YES startup handshake.
//
// The universal test suite and diagnostic firmware use their
// own command-driven execution paths in the existing source.
//
// Do not assume all three automatically behave the same way.
//
// For the universal suite, if the firmware and runner support
// these explicit arguments:
//
//     cd /workspace/Robot/archive/platformio-tests && python3 board-test.py --port /dev/ttyACM0 --baud 250000 --mode universal --command all
//
// Verify supported arguments first:
//
//     python3 board-test.py --help
//
// Use the explicit universal command only when compatible
// firmware and runner behavior have been confirmed.
//
// ============================================================
// OPTIONAL - OPEN THE SERIAL MONITOR
// ============================================================
//
//     cd /workspace/Robot/firmware/uno-motor-test && export PATH="$HOME/.platformio/penv/bin:$PATH" && pio device monitor -e uno --port /dev/ttyACM0 --baud 250000
//
// Exit with Ctrl+C.
//
// Do not run the serial monitor and board-test.py simultaneously
// against the same port.
//
// ============================================================
// IMPORTANT - ARDUINO UNO R3 LIMITATIONS
// ============================================================
//
// The Arduino Uno R3 has:
//
//     Microcontroller: ATmega328P
//     CPU frequency:  16 MHz
//     Flash:          32 KB nominal
//     SRAM:           2 KB
//     EEPROM:         1 KB
//
// Usable application flash is lower than nominal capacity
// because bootloader space is reserved.
//
// Compared with the Mega 2560, the Uno has substantially less
// RAM and flash.
//
// Therefore:
//
//     - Large arrays can exhaust SRAM.
//     - Dynamic String operations can increase memory pressure.
//     - Floating-point and trigonometric calculations can be
//       substantially slower.
//     - Timing resolution and overhead differ across boards.
//     - Hardware-specific cycle-counter tests may be skipped.
//     - Watchdog, reset-reason, memory, and peripheral tests
//       may need board-specific implementations.
//     - Results should not be compared across boards without
//       accounting for hardware and timing differences.
//
// IMPORTANT:
//
// Check PlatformIO's reported RAM and flash usage after each
// build. Successful compilation does not guarantee reliable
// runtime behavior, especially with only 2 KB of SRAM.
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
// and test results before treating the workflow as validated.
//
// ============================================================
// END OF ARDUINO UNO R3 NEW-FOLDER INSTRUCTIONS
// ============================================================
//
// ONE-LINER
//
//     cd /workspace/Robot/firmware/uno-motor-test && export PATH="$HOME/.platformio/penv/bin:$PATH" && pio run -e uno && pio run -e uno -t upload --upload-port /dev/ttyACM0 && cd /workspace/Robot/archive/platformio-tests && python3 board-test.py --port /dev/ttyACM0 --baud 250000
//
// ============================================================