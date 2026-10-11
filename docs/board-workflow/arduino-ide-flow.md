# Arduino IDE — Quick Workflow for All Boards

## 1. Standard Workflow

1. Open **Arduino IDE**.
2. Plug the board into the computer using a USB data cable.
3. Select the correct **board model**.
4. Select the correct **COM port**.
5. Open or write the sketch (`.ino`).
6. Click **Verify (✓)** to compile.
7. Click **Upload (→)** to flash the firmware.
8. Open **Serial Monitor** if needed and select the baud rate configured in the firmware.

## 2. Board Selection

| Board | Arduino IDE Board Selection |
|---|---|
| Arduino Uno R3 | Arduino Uno |
| Arduino Mega 2560 R3 | Arduino Mega or Mega 2560 |
| Elegoo ESP32 Dev Module | ESP32 Dev Module |
| Teensy 4.1 | Teensy 4.1 |

**Before uploading:**
- Install the required board package if the board is not listed.
- For ESP32, install **esp32 by Espressif Systems**.
- For Teensy 4.1, install the required **Teensyduino support**.
- Select the COM port belonging to the connected board.

## 3. Important Notes

- Building or verifying a sketch does not upload it to the board.
- A successful upload does not guarantee that the firmware or tests work correctly.
- Use the baud rate configured by `Serial.begin()` in the firmware.
- Close Serial Monitor before running another program that needs the same serial port.
- The Uno's previous build exceeded its available 2 KB SRAM. Fix this before trusting its test results.
- The universal test suite must support the selected board and its hardware limitations.

## 4. Troubleshooting

If uploading fails:

1. Check the selected board and COM port.
2. Confirm that the USB cable supports data.
3. Close other applications using the serial port.
4. Check that the required board package and drivers are installed.
5. Follow any board-specific upload instructions.

**Official reference:** [Arduino IDE — Upload a Sketch](https://support.arduino.cc/hc/en-us/articles/4733418441116-Upload-a-sketch-in-Arduino-IDE)
