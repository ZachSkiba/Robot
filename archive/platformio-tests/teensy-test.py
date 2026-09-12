#!/usr/bin/env python3
"""Serial runner for the Arduino/Teensy board test firmware.

The firmware must already be built and flashed. This script cannot change the
compile-time test selected in main.cpp.
"""

from __future__ import annotations

import argparse
import sys
import time
from typing import Optional

try:
    import serial
    from serial.tools import list_ports
except ImportError as exc:
    raise SystemExit(
        "pyserial is required. Install it with: python3 -m pip install pyserial"
    ) from exc


BAUD_RATE = 115200
DEFAULT_TIMEOUT = 0.25

LEGACY_MODES = {
    "latency": "Latency benchmark",
    "loop": "Loop timing test",
    "serial": "Serial throughput test",
    "calculation": "Calculation speed benchmark",
}

PROTOCOL_MODES = {
    "latency": ("benchmark", "latency"),
    "loop": ("benchmark", "loop"),
    "serial": ("benchmark", "serial"),
    "calculation": ("benchmark", "calculation"),
    "diagnostic": ("diagnostic", "diagnostic"),
    "universal": ("universal", "universal-board"),
}

UNIVERSAL_COMMANDS = {
    "all": "run_all",
    "calc": "run_calc",
    "timing": "run_timing",
    "realtime": "run_realtime",
    "stress": "run_stress",
    "faults": "run_faults",
    "numeric": "run_numeric",
    "packet": "run_packet",
    "report": "report",
}


def find_ports() -> list[str]:
    """Return likely serial ports, preferring USB CDC devices."""
    ports = list(list_ports.comports())
    preferred = [
        port.device
        for port in ports
        if "ACM" in port.device or "USB" in port.device
    ]
    remaining = [port.device for port in ports if port.device not in preferred]
    return preferred + remaining


def choose_port(requested: Optional[str]) -> str:
    if requested:
        return requested

    ports = find_ports()
    if not ports:
        raise SystemExit(
            "No serial ports found. Attach the board and check /dev/ttyACM* or "
            "/dev/ttyUSB*."
        )

    if len(ports) == 1:
        return ports[0]

    print("Available serial ports:")
    for index, port in enumerate(ports, 1):
        print(f"  {index}) {port}")

    while True:
        answer = input("Select a port: ").strip()
        try:
            selected = ports[int(answer) - 1]
        except (ValueError, IndexError):
            print("Enter one of the listed numbers.")
            continue
        return selected


def read_lines(board: serial.Serial, duration: float) -> list[str]:
    """Read and print lines for a bounded period."""
    lines: list[str] = []
    deadline = time.monotonic() + duration
    while time.monotonic() < deadline:
        raw = board.readline()
        if not raw:
            continue
        line = raw.decode("utf-8", errors="replace").rstrip("\r\n")
        print(line, flush=True)
        lines.append(line)
    return lines


def read_until(
    board: serial.Serial,
    markers: tuple[str, ...],
    timeout: float,
) -> tuple[bool, list[str]]:
    """Read output until a marker appears or timeout expires."""
    lines: list[str] = []
    deadline = time.monotonic() + timeout
    while time.monotonic() < deadline:
        raw = board.readline()
        if not raw:
            continue
        line = raw.decode("utf-8", errors="replace").rstrip("\r\n")
        print(line, flush=True)
        lines.append(line)
        if any(marker in line for marker in markers):
            return True, lines
    return False, lines


def send_command(board: serial.Serial, command: str) -> None:
    print(f"\n> {command}", flush=True)
    board.write((command + "\n").encode("ascii"))
    board.flush()


def read_protocol(board: serial.Serial, timeout: float) -> Optional[dict[str, str]]:
    """Read the machine-readable firmware announcement."""
    values: dict[str, str] = {}
    deadline = time.monotonic() + timeout
    while time.monotonic() < deadline:
        raw = board.readline()
        if not raw:
            continue
        line = raw.decode("utf-8", errors="replace").rstrip("\r\n")
        print(line, flush=True)
        if line == "@TEST_READY":
            values["TEST_READY"] = "1"
        if line.startswith("@TEST_") and "=" in line:
            key, value = line[1:].split("=", 1)
            values[key] = value
        required = {
            "TEST_PROTOCOL",
            "TEST_NAME",
            "TEST_VERSION",
            "TEST_ID",
            "TEST_READY",
        }
        if required.issubset(values):
            return values
    return None


def result_code(result: str) -> int:
    if result == "PASS":
        return 0
    if result == "FAIL":
        return 1
    return 2


def read_result(board: serial.Serial, timeout: float) -> int:
    """Print output until a machine-readable result arrives."""
    found, lines = read_until(board, ("@TEST_COMPLETE",), timeout)
    if not found:
        print("Timed out waiting for @TEST_RESULT and @TEST_COMPLETE.", file=sys.stderr)
        return 2
    for line in reversed(lines):
        if line.startswith("@TEST_RESULT="):
            return result_code(line.split("=", 1)[1])
    print("Completed without a machine-readable result.", file=sys.stderr)
    return 2


def run_legacy(board: serial.Serial, timeout: float = 30.0) -> int:
    """Start a legacy test using the READY/YES handshake."""
    send_command(board, "READY")
    found, _ = read_until(
        board,
        ("@TEST_START_READY",),
        timeout=5.0,
    )
    if not found:
        print("Did not receive the legacy test prompt.", file=sys.stderr)
        print(
            "The flashed firmware may be the universal suite or a different "
            "program.",
            file=sys.stderr,
        )
        return 2

    answer = input("Type YES and press Enter to start: ").strip().upper()
    if answer != "YES":
        print("Test cancelled. Type YES exactly to start.")
        return 2

    send_command(board, "YES")
    return read_result(board, timeout)


def run_universal(board: serial.Serial, command: str, timeout: float) -> int:
    """Run one command supported by universal-board-test.cpp."""
    send_command(board, command)
    return read_result(board, timeout)


def run_diagnostic(board: serial.Serial, timeout: float) -> int:
    """Ask diagnostic firmware for a machine-readable health result."""
    send_command(board, "status")
    return read_result(board, timeout)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--port", help="Serial port, for example /dev/ttyACM0")
    parser.add_argument(
        "--mode",
        choices=["auto", *PROTOCOL_MODES],
        default="auto",
        help="Expected firmware mode; auto reads the firmware announcement",
    )
    parser.add_argument(
        "--command",
        choices=list(UNIVERSAL_COMMANDS),
        help="Universal-suite command alias, such as all or timing",
    )
    parser.add_argument(
        "--timeout",
        type=float,
        default=30.0,
        help="Seconds to collect output after starting a test",
    )
    return parser.parse_args()


def main() -> int:
    args = parse_args()

    if args.command and args.mode not in ("auto", "universal"):
        raise SystemExit("--command can only be used with --mode universal")

    command = UNIVERSAL_COMMANDS.get(args.command or "all", "run_all")

    port = choose_port(args.port)
    print(f"Opening {port} at {BAUD_RATE} baud...")

    try:
        with serial.Serial(port, BAUD_RATE, timeout=DEFAULT_TIMEOUT) as board:
            # Opening a native USB serial port often resets the board.
            time.sleep(2.0)
            board.reset_input_buffer()
            board.reset_output_buffer()
            send_command(board, "identify")
            protocol = read_protocol(board, 8.0)
            if protocol is None:
                board.reset_input_buffer()
                send_command(board, "identify")
                protocol = read_protocol(board, 3.0)
            if protocol is None:
                print("No machine-readable firmware announcement received.", file=sys.stderr)
                print("Flash firmware that emits @TEST_PROTOCOL and @TEST_READY.", file=sys.stderr)
                return 2

            detected = (protocol.get("TEST_PROTOCOL"), protocol.get("TEST_NAME"))
            print(
                f"Detected protocol: {detected[0]} / {detected[1]} "
                f"(id={protocol.get('TEST_ID')}, "
                f"version={protocol.get('TEST_VERSION')})"
            )

            if args.mode != "auto":
                expected = PROTOCOL_MODES[args.mode]
                if detected != expected:
                    print(
                        f"Expected {expected[0]} / {expected[1]}, "
                        f"but detected {detected[0]} / {detected[1]}.",
                        file=sys.stderr,
                    )
                    return 2

            if detected[0] == "universal":
                return run_universal(board, command, args.timeout)
            if detected[0] == "diagnostic":
                return run_diagnostic(board, args.timeout)
            if detected[0] == "benchmark":
                return run_legacy(board, args.timeout)

            print(f"Unsupported TEST_PROTOCOL: {detected[0]}", file=sys.stderr)
            return 2
    except serial.SerialException as exc:
        print(f"Could not open or use {port}: {exc}", file=sys.stderr)
        return 1
    except KeyboardInterrupt:
        print("\nStopped.")
        return 130


if __name__ == "__main__":
    raise SystemExit(main())
