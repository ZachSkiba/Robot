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
