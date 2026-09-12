# Part 2 — How to connect the Teensy

## Step 1 — Plug in the Teensy
Connect the USB cable to your Windows computer.

Do not press the program button yet.

## Step 2 — Attach to WSL
Open Windows PowerShell and run the following.

### PowerShell — one paste

```powershell
usbipd list
```

Find the Teensy row. It will look similar to:

```text
2-2    16c0:0483    USB Serial Device (COM6), USB Serial
```

If the state is already `Attached`, do not attach it again.

If it is `Shared` or `Not shared`, use the appropriate sharing/attachment process.

To attach:

```powershell
usbipd attach --wsl --busid 2-2
```

Replace `2-2` with the actual BUSID shown by your computer.

Verify:

```powershell
usbipd list
```

You want:

```text
Attached
```

The official USB/IP workflow is documented by Microsoft: Connect USB devices to WSL.

## Step 3 — Verify in Ubuntu WSL
Run this in your normal Ubuntu WSL terminal, not the Docker dev container.

### Ubuntu WSL — one paste

```bash
echo "=== TEENSY USB ==="
lsusb | grep -i -E '16c0|teensy' || true

echo
echo "=== SERIAL PORT ==="
ls -l /dev/ttyACM* /dev/ttyUSB* 2>/dev/null || true

echo
echo "=== SERIAL TEST ==="
timeout 5 cat /dev/ttyACM0
```

Expected:

```text
16c0:0483
```

and:

```text
Teensy 4.1 heartbeat
```

If the port is `/dev/ttyACM1` instead of `/dev/ttyACM0`, use the actual port.

Do not assume the port number is permanent.

# Part 3 — Open the correct project in VS Code
Your Teensy project is located here:

```text
/workspace/Robot/archive/platformio-tests/teensy41-basic
```

This is inside your Docker dev container.

## Step 1 — Open VS Code
Open your Robot project:

```text
Robot
```

Attach to the Docker dev container.

You should see a terminal similar to:

```bash
(.venv) devuser@...:/workspace/Robot$
```

## Step 2 — Navigate to the Teensy project

### Docker dev container — one paste

```bash
cd /workspace/Robot/archive/platformio-tests/teensy41-basic

echo "=== PROJECT ==="
pwd

echo
echo "=== FILES ==="
find . -maxdepth 2 -type f \
  ! -path './.pio/*' \
  ! -path './.git/*' \
  -print
```

You should have a PlatformIO project containing something like:

```text
platformio.ini
src/main.cpp
```

Important: Edit the `src/main.cpp` file. That is the source file we will use for the firmware.

# Part 4 — Teensy Firmware Update: Final Reference

## What Part 4 accomplished

Your Teensy now has the `diagnostic-v1` firmware that:

- Blinks the onboard LED every 500 ms
- Sends a heartbeat every second
- Reports uptime
- Accepts serial commands
- Reports LED state
- Supports:
  - `ping`
  - `status`
  - `led on`
  - `led off`
  - `help`

The Teensy Loader is specifically designed to load a compiled HEX file onto Teensy, and the physical Program button provides a way to enter programming mode.

---

# Future Teensy Firmware Update Workflow

This is the version I recommend you save.

There are three environments, and each has one job:

- Windows PowerShell: USB/IP + copying firmware
- Ubuntu WSL: Physical Teensy USB + flashing
- VS Code Dev Container: Edit + compile firmware

Do not try to flash the Teensy from the Docker container.

---

## Step 1 — Edit the firmware

### VS Code Dev Container

Open:

```text
/workspace/Robot/archive/platformio-tests/teensy41-basic/src/main.cpp
```

Make your firmware changes.

---

## Step 2 — Build the new firmware

### VS Code Dev Container

Run:

```bash
cd /workspace/Robot/archive/platformio-tests/teensy41-basic

export PATH="$HOME/.platformio/penv/bin:$PATH"

pio run
```

You want:

```text
[SUCCESS]
```

The new firmware will be here:

```text
/workspace/Robot/archive/platformio-tests/teensy41-basic/.pio/build/teensy41/firmware.hex
```

### Important

This is where a "new firmware" comes from.

There isn't a separate firmware file that Teensy automatically downloads.

You create a new firmware whenever you change the source code and successfully run `pio run`.

---

## Step 3 — Copy the firmware out of Docker

### Windows PowerShell

First find the current container:

```powershell
docker ps
```

Find the container running your Robot dev environment.

Then copy the HEX:

```powershell
docker cp `
  CONTAINER_ID:/workspace/Robot/archive/platformio-tests/teensy41-basic/.pio/build/teensy41/firmware.hex `
  "$HOME\teensy-flash\firmware.hex"
```

Replace:

```text
CONTAINER_ID
```

with the current container ID.

For example, yours was previously:

```text
209a464b76cb
```

but do not permanently assume that ID. Docker container IDs can change.

Verify it:

```powershell
Get-Item "$HOME\teensy-flash\firmware.hex"
```

---

## Step 4 — Copy the firmware into WSL

### Windows PowerShell

Run:

```powershell
wsl cp /mnt/c/Users/Nick/teensy-flash/firmware.hex /home/nicks/teensy-flash/firmware.hex
```

Then:

### Ubuntu WSL

Verify:

```bash
ls -lh ~/teensy-flash/firmware.hex

stat -c '%s bytes' ~/teensy-flash/firmware.hex
```

You want the file size to match the firmware you just built.

Do not flash an old HEX file by accident.

This was the mistake we caught during this update.

---

## Step 5 — Make sure Teensy is connected to WSL

### Windows PowerShell

Run:

```powershell
usbipd list
```

Find the Teensy.

The BUSID can change, so do not assume `2-2`.

If it says something like:

```text
2-2    16c0:0483    USB Serial Device    Shared
```

attach it:

```powershell
usbipd attach --wsl --busid 2-2
```

Replace `2-2` with whatever BUSID you actually see.

Microsoft's current WSL documentation uses this same `usbipd list` → `usbipd attach --wsl --busid <busid>` workflow.

---

## Step 6 — Verify Teensy in WSL

### Ubuntu WSL

Run:

```bash
lsusb -d 16c0:0483
```

You want:

```text
16c0:0483 ... Teensyduino Serial
```

Then:

```bash
ls -l /dev/ttyACM*
```

You want:

```text
/dev/ttyACM0
```

---

## Step 7 — Put Teensy into programming mode

### Physical Teensy

Press and release the small PROGRAM button once.

The Teensy should change from:

```text
16c0:0483
```

to:

```text
16c0:0478
```

`16c0:0478` = HalfKay bootloader.

If the device disappears from WSL, that is normal in your setup.

---

## Step 8 — Reattach after the button press

### Windows PowerShell

Run:

```powershell
usbipd list
```

You may see:

```text
16c0:0478    USB Input Device    Shared
```

Then:

```powershell
usbipd attach --wsl --busid YOUR_BUS_ID
```

Replace `YOUR_BUS_ID` with the actual BUSID.

### Ubuntu WSL

Verify:

```bash
lsusb -d 16c0:0478
```

You want:

```text
16c0:0478 ... Teensy Halfkay Bootloader
```

---

## Step 9 — Flash the firmware

### Ubuntu WSL

Run:

```bash
sudo teensy_loader_cli \
  --mcu=TEENSY41 \
  -v \
  -w \
  ~/teensy-flash/firmware.hex
```

Successful output looks like:

```text
Found HalfKay Bootloader
Programming..................
Booting
```

Do not press the Program button again.

---

## Step 10 — Reattach the Teensy after flashing

This is an important part of your particular Windows → WSL setup.

After flashing, the Teensy reboots and changes from:

```text
16c0:0478
```

to:

```text
16c0:0483
```

Windows/WSL may temporarily lose the USB connection.

### Windows PowerShell

Run:

```powershell
usbipd list
```

If the Teensy is `Shared` rather than `Attached`:

```powershell
usbipd attach --wsl --busid YOUR_BUS_ID
```

### Ubuntu WSL

Verify:

```bash
lsusb -d 16c0:0483
```

Then:

```bash
ls -l /dev/ttyACM*
```

You should have:

```text
/dev/ttyACM0
```

---

## Step 11 — Verify the new firmware

### Ubuntu WSL

Run:

```bash
timeout 5 cat /dev/ttyACM0
```

For the current diagnostic firmware, you should see:

```text
Teensy 4.1 Diagnostic Firmware
Firmware: diagnostic-v1
Type 'help' for commands.
```

followed by:

```text
Teensy 4.1 heartbeat | uptime_ms=...
```

If you see that, the firmware update is complete.

