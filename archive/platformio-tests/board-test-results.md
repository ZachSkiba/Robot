## Teensy 4.1
# Latency Test
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

# Calculation Speed
=== TEST OUTPUT ===
Starting test...
Starting selected test...
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
  Iterations/sec:    49137600.00
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
  Iterations/sec:    2739995.50
  Average iteration: 0.364964 us
  Minimum batch:     33 us
  Maximum batch:     42 us
  Average batch:     36.363 us
  Batch avg/iter:    0.363626 us
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
Integer arithmetic    49137600.00
32-bit float          14213931.00
Trigonometry          2739995.50
Robot-style math      4309804.00
NOTES:
- Results are benchmark iterations/sec.
- They are not CPU instruction counts.
- The same source can run on many Arduino boards.
- Timer resolution differs between processors.
- Compiler optimization affects the results.
- Robot-style math is not complete 6-DOF kinematics.
=== TEST COMPLETE ===


## ESP 32



## Arduino Mega