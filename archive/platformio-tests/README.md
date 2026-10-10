# PlatformIO board tests

## Inventory and canonical files

There is one PlatformIO project in this directory:

- `teensy41-basic/platformio.ini` defines the sole environment, `teensy41`
  (`teensy41` board, Teensy platform, Arduino framework).
- `teensy41-basic/src/main.cpp` selects one firmware mode at compile time.
  The checked-in selection is the universal suite.
- `teensy41-basic/src/universal-board-test.cpp` is the canonical portable
  self-test suite; `universal-board-test.h` exposes its entry points.
- `teensy41-basic/src/test_protocol.h` is the shared identification-frame
  helper. `board-test.py` is the host serial runner.
- `diagnostic-firmware.cpp/.h`, `latency_test.cpp/.h`,
  `loop_timing_test.cpp/.h`, `calculation_speed_test.cpp/.h`, and
  `serial_throughput_test.cpp/.h` are distinct firmware modes selected from
  `main.cpp`, not separate PlatformIO projects. The non-universal benchmark
  modules are retained as historical/alternative modes; they are not
  additional board targets.
- `test_suite.h` aggregates the mode headers but has no in-tree consumer.
- `board-test-results.md` contains historical Teensy 4.1 benchmark output.

There are no ESP32 or AVR PlatformIO environments in this tree. The project
name and environment reflect the configured Teensy target; the universal
suite's portability claims describe its intended Arduino-core API surface,
not verified support for every architecture.

## Naming and interface conventions

- Preserve existing project, source-file, function, and protocol identifiers
  as public interfaces unless all consumers can be updated together.
- Use descriptive `lower-kebab-case` for new filenames, `lowerCamelCase` for
  C++ functions and variables, `UPPER_SNAKE_CASE` for macros/constants, and
  lowercase `snake_case` for serial commands.
- Keep serial metadata keys uppercase and prefixed `@TEST_`. Protocol version
  1 identifies the existing field/line framing; universal-suite aggregate
  outcome values are `PASS`, `FAIL`, `PASS_WITH_SKIPS`, `INFO`,
  `INFO_WITH_SKIPS`, or `SKIP`.
- Mark unsupported hardware mechanisms `SKIP` with a reason. Timing and
  benchmark measurements without a board-independent acceptance limit are
  `INFO`, not correctness `PASS` results.

## Build and run

From this directory's project:

```sh
pio run -e teensy41
```

The firmware must be flashed to run it. The serial harness runs from this
directory with `python3 board-test.py`; use `--port` to select a port
explicitly and `--command` to select an individual universal-suite command.
For configurable long runs, use `--command soak --duration <seconds>` (or
`stress`) and set `--timeout` to a value greater than the requested duration.
The harness requires the repository's Python dependencies (`pyserial`).
