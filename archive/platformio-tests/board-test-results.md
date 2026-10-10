# Historical benchmark captures

These are saved Teensy 4.1 measurements from the individual legacy benchmark
firmware modes, not results from the current universal-suite default. They
document neither an ESP32 nor an AVR build or physical test. Benchmark values
depend on the flashed source revision, compiler, framework, and measurement
conditions; do not use them as current cross-board comparisons.

## Teensy 4.1

================================
Calculation Speed Benchmark
================================

Portable Arduino-style benchmark
Higher iterations/sec = faster

Benchmark duration: 5 seconds
Batch size:         100


================================
DETAILED RESULTS
================================

Integer arithmetic
  Duration:          5.000 s
  Iterations:        245688000
  Batches:           2456880
  Iterations/sec:    49137592.00
  Average iteration: 0.020351 us
  Minimum batch:     1 us
  Maximum batch:     3 us
  Average batch:     1.900 us
  Batch avg/iter:    0.019001 us

32-bit floating point
  Duration:          5.000 s
  Iterations:        71069700
  Batches:           710697
  Iterations/sec:    14213931.00
  Average iteration: 0.070354 us
  Minimum batch:     6 us
  Maximum batch:     7 us
  Average batch:     6.900 us
  Batch avg/iter:    0.069003 us

Trigonometry
  Duration:          5.000 s
  Iterations:        13700000
  Batches:           137000
  Iterations/sec:    2739997.75
  Average iteration: 0.364964 us
  Minimum batch:     33 us
  Maximum batch:     42 us
  Average batch:     36.364 us
  Batch avg/iter:    0.363638 us

Robot-style math
  Duration:          5.000 s
  Iterations:        21549100
  Batches:           215491
  Iterations/sec:    4309804.00
  Average iteration: 0.232029 us
  Minimum batch:     23 us
  Maximum batch:     24 us
  Average batch:     23.066 us
  Batch avg/iter:    0.230660 us

================================
SUMMARY
================================

Benchmark             Iterations/sec
----------------------------------------
Integer arithmetic    49137592.00
32-bit float          14213931.00
Trigonometry          2739997.75
Robot-style math      4309804.00


================================
UNIVERSAL FIRMWARE TIMING TEST
================================

Timing source: Arduino micros()
Workload: portable integer firmware loop

Test duration:       5.000 s
Batch size:          1000
Batches:             369668
Total iterations:    369668000

Timer resolution:    1 us
Timer overhead:      0 us

Iterations/second:   73933464.00
Average iteration:   0.013526 us

Minimum batch:       13 us
Maximum batch:       14 us
Average batch:       13.396 us
Batch average/iter:  0.013396 us
Minimum iter est.:   0.013000 us
Maximum iter est.:   0.014000 us

INTERPRETATION:
- Higher iterations/sec is faster.
- Batch timing reduces timer-resolution error.
- Results include benchmark and timer overhead.
- This is not complete sensor-to-motor latency.
- Compare boards using the same compiler settings.

=== TEST COMPLETE ===
@TEST_RESULT=PASS
@TEST_COMPLETE


================================
UNIVERSAL LOOP TIMING TEST
================================

Timing source: Arduino micros()
Test duration:       5.000 s
Target loop period:  1000 us
Timer resolution:    1 us
Timer overhead:      0 us

Samples:             36142723
Minimum period:      0 us
Maximum period:      1 us
Average period:      0.138 us
Average loop rate:   7228545.000 Hz
Worst positive jitter: 0.862 us
Periods over target:  0
Miss percentage:      0.000%

Timing histogram:
  < 1x target:        36142723
  1x to 2x target:    0
  2x to 3x target:    0
  3x to 4x target:    0
  4x to 5x target:    0
  5x to 10x target:   0
  10x to 100x target: 0
  > 100x target:      0

INTERPRETATION:
- This measures loop period, not pure execution time.
- micros() over

================================
UNIVERSAL SERIAL THROUGHPUT TEST
================================

Packet format: fixed-size binary packet
Packet size:          32 bytes
Target packet period: 10 ms
Configured baud:      115200

Elapsed time:         10.000 s
Packets sent:         1000
Scheduled packets:    1000
Bytes accepted:       32000
Missed packet slots:  0

Bytes/second:         3200.00
Bits/second:          25600.00
Kilobytes/second:     3.200
Packets/second:       100.00
Effective bit rate:   25.600 kbit/s

INTERPRETATION:
- Bytes accepted is the number returned by Serial.write().
- Serial.write() may queue bytes instead of transmitting them.
- Serial.flush() waits for queued serial data to finish.
- Results depend on baud rate, buffers, USB, and host behavior.
- This measures serial transport, not robot-control latency.
- Binary packets avoid variable-length text overhead.

=== SERIAL THROUGHPUT TEST COMPLETE ===
@TEST_RESULT=PASS
@TEST_COMPLETE


========================================
UNIVERSAL BOARD TEST SUITE
========================================
[PASS] Boot / self-test
[PASS] Command parser self-test
[PASS] Packet serialization + checksum self-test
  integer ops: 100000 iterations in 3168 us
  approx 31565656.57 ops/sec
[INFO] Integer calculation benchmark
  float ops: 20000 iterations in 635 us
[INFO] Floating-point calculation benchmark
  trig calls: 15000 in 2708 us
[INFO] Trigonometry benchmark
[PASS] Numerical correctness
  min/avg/max (us): 0 / 0.06 / 1
  p50/p95/p99 (us): 0 / 1 / 1
  (timer granularity/overhead, not a control-loop period - see run_realtime for that)
[INFO] Timing primitive characterization
  workload cycles min/avg/max: 53 / 90.05 / 106
  workload cycles p50/p95/p99: 102 / 102 / 105
  target: 1000 us/cycle (1000 Hz)
  exec min/avg/max (us): 0 / 0.00 / 0
  exec p50/p95/p99 (us): 0 / 0 / 0
  deadline misses (finish time > scheduled start + period): 0 / 100
  max consecutive misses: 0
  worst start-time lateness (us): 0
  worst finish-time lateness (us): 0
  (lateness figures are worst-case only, not full percentile distributions - a deliberate scope limit)
  (missed-deadline count is the real answer, not PASS/FAIL - see file header)
[INFO] Control workload timing
.
.
  2334096 mixed-workload iterations in 2000 ms
  dual-accumulator check: consistent
  iteration-rate samples (per ~200ms window): first=233047 last=233450
[PASS] CPU sustained workload test
[PASS] Defensive logic / fault handling
  soak duration: 5000 ms
  loop iterations: 2832004
  max single-iteration time (us): 3
  packet errors: 0
  calc errors: 0
  control-state dual-accumulator mismatches: 0
  timing outliers (>20x this run's own average): 0
[PASS] Long-duration soak (5s demo run)

---- Board Capability Report ----
sizeof(char):      1
sizeof(short):     2
sizeof(int):       4
sizeof(long):      4
sizeof(long long): 8
sizeof(float):     4
sizeof(double):    8
sizeof(void*):     4
sizeof(size_t):    4
sizeof(uint8_t):   1
sizeof(uint16_t):  2
sizeof(uint32_t):  4
sizeof(uint64_t):  8
FLT_EPSILON:       0.0000001192
FLT_MAX:           ovf
FLT_MIN:           0.0000000000
sizeof(TestPacket) [raw, may include padding]: 32
Serialized packet body size [padding-free]:    26
byte order:        little-endian
F_CPU (Hz):        600000000
compiler version:  15.2.1 20251203
Arduino core ver:  10805
toolchain macro:   TEENSYDUINO
---- End Report ----

---- Needs a per-core adapter (not included - see file header) ----
[SKIP] Memory / heap stability - no portable free-RAM API
[SKIP] Watchdog configure + recovery - register/API differs per core; resets the board
[SKIP] Reset-reason decode - register/API differs per core
[SKIP] Internal EEPROM/flash/FS test - API differs per core; destructive by design, skipped
  hardware cycle counter: ARM_DWT_CYCCNT
  CPU frequency (Hz): 600000000
  cycles min/avg/max: 15 / 19.00 / 19
  execution time (us) min/avg/max: 0.0250 / 0.0317 / 0.0317
  cycles p50/p95/p99: 19 / 19 / 19
[PASS] CPU cycle-counter timing
[SKIP] Die temperature - not exposed on most cores
[SKIP] Stack usage / stack canary - stack layout/introspection differs per core

========================================
SUMMARY
Passed:  8
Failed:  0
Skipped: 6
Info:    5
Overall: PASS WITH SKIPPED TESTS
@TEST_RESULT=PASS_WITH_SKIPS
@TEST_COMPLETE


## ESP 32



## Arduino Mega