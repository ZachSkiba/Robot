#!/usr/bin/env python3
"""Serial runner for the Arduino/Teensy board test firmware.

The firmware must already be built and flashed. This script cannot change the
compile-time test selected in main.cpp.
"""

from __future__ import annotations

import argparse
import math
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


DEFAULT_BAUD_RATE = 2500000
DEFAULT_READ_TIMEOUT = 0.25

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
    "soak": "run_soak",
    "report": "report",
}


def find_ports() -> list[str]:
    """Return likely serial ports, preferring USB CDC devices."""
    ports = list(list_ports.comports())
    preferred = [
        port.device
        for port in ports
        if "acm" in port.device.lower()
        or "usb" in port.device.lower()
        or "usbmodem" in port.device.lower()
    ]
    remaining = [port.device for port in ports if port.device not in preferred]
    return preferred + remaining


def choose_port(requested: Optional[str]) -> str:
    if requested:
        return requested

    ports = find_ports()
    if not ports:
        raise SystemExit(
            "No serial ports found. Attach the board, specify --port explicitly, "
            "or check the OS serial-port list."
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
    if result in ("PASS", "PASS_WITH_SKIPS", "INFO", "INFO_WITH_SKIPS", "SKIP"):
        return 0
    if result == "FAIL":
        return 1
    return 2



def read_result(board: serial.Serial, timeout: float) -> int:
    """Read and validate the final machine-readable test result."""
    found, lines = read_until(board, ("@TEST_COMPLETE",), timeout)

    if not found:
        print(
            "Timed out waiting for @TEST_COMPLETE.",
            file=sys.stderr,
        )
        return 2

    results = [
        line.split("=", 1)[1]
        for line in lines
        if line.startswith("@TEST_RESULT=")
    ]

    if len(results) != 1:
        print(
            f"Expected exactly one @TEST_RESULT marker; got {len(results)}.",
            file=sys.stderr,
        )
        return 2

    return result_code(results[0])



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
        "--baud",
        type=int,
        default=DEFAULT_BAUD_RATE,
        help="Serial baud rate (default: 2500000)",
    )
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
        "--duration",
        type=int,
        help="Duration in seconds for stress/soak commands (1-86400)",
    )
    parser.add_argument(
        "--timeout",
        type=float,
        default=120.0,
        help="Maximum seconds to collect test output (default: 120)",
    )
    return parser.parse_args()


def main() -> int:
    args = parse_args()

    if args.baud <= 0:
        raise SystemExit("--baud must be a positive integer")

    if not math.isfinite(args.timeout) or args.timeout <= 0:
        raise SystemExit("--timeout must be a finite positive number of seconds")
    if args.command and args.mode not in ("auto", "universal"):
        raise SystemExit("--command can only be used with --mode universal")
    if args.duration is not None:
        if args.command not in ("stress", "soak"):
            raise SystemExit("--duration can only be used with --command stress or soak")
        if not 1 <= args.duration <= 86400:
            raise SystemExit("--duration must be between 1 and 86400 seconds")
        if args.timeout <= args.duration:
            raise SystemExit("--timeout must exceed --duration for stress/soak commands")

    command = UNIVERSAL_COMMANDS.get(args.command or "all", "run_all")
    if args.duration is not None:
        command = f"{command} {args.duration}"

    port = choose_port(args.port)
    print(f"Opening {port} at {args.baud} baud...")

    try:
        with serial.Serial(
            port,
            args.baud,
            timeout=DEFAULT_READ_TIMEOUT,
            write_timeout=2.0,
        ) as board:
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
