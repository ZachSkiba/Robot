```cpp
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
```cpp
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
```