/*
 * ============================================================================
 * UNIVERSAL BOARD TEST SUITE  (single file, core-only, no extra hardware)
 * ============================================================================
 *
 * Requires: the board + the USB cable you flash it with. Nothing else.
 * Uses only: Serial, millis(), micros(), delay(), and <math.h>/<string.h>/
 * <stdlib.h>/<stddef.h> — APIs guaranteed by every Arduino-framework core
 * (AVR, SAMD, ESP32, Teensy/Teensyduino, RP2040-Arduino, STM32duino, etc).
 * No board-specific headers, no libraries beyond the core, nothing that
 * requires internet, a second machine, or a debugger.
 *
 * HOW TO USE
 *   Arduino IDE : rename this file to universal_board_test.ino, open it
 *                 as its own sketch folder, upload, open Serial Monitor
 *                 at 115200 baud, type "help".
 *   PlatformIO  : drop this file in as src/main.cpp, build, upload,
 *                 `pio device monitor -b 115200`, type "help".
 *
 * ----------------------------------------------------------------------------
 * WHAT'S INCLUDED (fully code-only, compiles unmodified on any core above)
 * ----------------------------------------------------------------------------
 *   - Boot / self-test
 *   - Command-parser self-test        (feeds test vectors into the same
 *                                       parser the live serial console uses)
 *   - Packet framing + checksum self-test (build/verify/corrupt-and-detect)
 *   - Integer calculation benchmark
 *   - Floating-point calculation benchmark
 *   - Trigonometry benchmark
 *   - Numerical correctness suite     (known-answer math, NaN/Inf, wrap,
 *                                       vector normalize)
 *   - Loop timing / jitter
 *   - Simulated real-time control-loop deadline test
 *   - CPU load / stress test
 *   - Software fault-injection test
 *   - Long-duration soak test         (duration you choose, in seconds)
 *   - Board capability report         (type sizes, endianness, toolchain —
 *                                       informational, not pass/fail)
 *
 * ----------------------------------------------------------------------------
 * WHAT'S DELIBERATELY *NOT* INCLUDED, AND WHY
 * ----------------------------------------------------------------------------
 * There is no honest single implementation of these across AVR/ESP32/Teensy/
 * SAMD/RP2040 — the registers and APIs are genuinely different per core.
 * Faking a "universal" version of these would just mean silently doing
 * nothing useful on most boards while claiming PASS. Instead this suite
 * reports them as SKIP, explicitly, every run:
 *   - Free-heap / memory-stability test   (no portable free-RAM call)
 *   - Watchdog configure + recovery test  (register/API differs per core;
 *                                           it also has to reset the board,
 *                                           which would blow up a suite run)
 *   - Reset-reason decode                 (register/API differs per core)
 *   - Internal EEPROM/flash/filesystem    (API differs per core; also
 *                                           destructive to flash write-life,
 *                                           so it's skipped on purpose even
 *                                           where an API exists)
 *   - CPU cycle-accurate timing           (ARM Cortex-M DWT cycle counter
 *                                           only — no AVR/ESP32 equivalent)
 *   - Die temperature                     (most cores don't expose it)
 * If you want these, write one adapter .cpp per core (board_adapter_avr.cpp,
 * board_adapter_esp32.cpp, ...) behind a common header, and wire the calls
 * into runAll(). Don't let anyone hand you a "universal" version of these —
 * there isn't one.
 *
 * ----------------------------------------------------------------------------
 * HONESTY NOTE ON "PACKET INTEGRITY"
 * ----------------------------------------------------------------------------
 * Without a second machine listening on the serial port, firmware running
 * alone can only prove that ITS OWN packet-construction and checksum code
 * is internally consistent (build a packet, verify it, corrupt a byte,
 * confirm the checksum catches it). It CANNOT detect real dropped bytes,
 * duplicated frames, or line-noise corruption on the actual wire — that
 * requires a host-side script reading the port and checking sequence
 * numbers/checksums against what arrived. This suite's `run_packet` test
 * is real and worth running (it catches firmware framing bugs before you
 * ever wire up a receiver), but it is not a substitute for a host-side
 * link test. Say so if anyone asks whether this "tests the USB link" —
 * it doesn't, not fully.
 *
 * ----------------------------------------------------------------------------
 * HONESTY NOTE ON PASS/FAIL FOR THE REAL-TIME DEADLINE TEST
 * ----------------------------------------------------------------------------
 * A 16 MHz AVR will legitimately miss a 1 kHz deadline that a Teensy 4.1
 * won't touch. There is no board-independent "correct" miss count, so this
 * test PASSes as long as it runs to completion and produces sane numbers.
 * The missed-deadline count it prints is the actual engineering answer —
 * read that number, don't just read PASS/FAIL.
 *
 * ----------------------------------------------------------------------------
 * VERIFICATION STATUS OF THIS FILE (read this before you trust it)
 * ----------------------------------------------------------------------------
 * This was syntax- and logic-checked in a sandbox using a stub Serial/
 * millis()/micros() implementation compiled with plain g++ (i.e. every
 * function was exercised and ran without crashing against fake timing).
 * It was NOT compiled against a real avr-gcc / xtensa-esp32 / arm-none-eabi
 * toolchain, because none of those toolchains are reachable from this
 * sandbox. Translation: the logic is sound and the syntax is valid C++,
 * but I have not proven it builds under the real Arduino/PlatformIO
 * toolchain for your specific board. Build it once with `pio run` or the
 * Arduino IDE's verify button before you trust it on hardware, and tell me
 * the error text if you get one — I'd rather fix a real compiler error now
 * than have you find out the hard way mid-test.
 * ============================================================================
 */

#include <Arduino.h>
#include <math.h>
#include <string.h>
#include <stdlib.h>
#include <stddef.h>
#include <stdint.h>

#include "universal-board-test.h"
#include "test_protocol.h"

// ============================================================================
// Forward declarations (a plain .cpp under PlatformIO does not get the
// Arduino IDE's automatic function-prototype generation, so we declare
// everything explicitly rather than relying on definition order).
// ============================================================================

enum TestResult : uint8_t { T_PASS = 0, T_FAIL = 1, T_SKIP = 2 };
enum CommandId {
  CMD_HELP, CMD_STATUS, CMD_RUN_ALL, CMD_RUN_CALC, CMD_RUN_TIMING,
  CMD_RUN_REALTIME, CMD_RUN_STRESS, CMD_RUN_FAULTS, CMD_RUN_NUMERIC,
  CMD_RUN_PACKET, CMD_RUN_SOAK, CMD_REPORT, CMD_IDENTIFY, CMD_UNKNOWN
};

struct TestPacket {
  uint16_t magic;
  uint32_t seq;
  uint32_t timestamp_us;
  uint8_t  payload[16];
  uint16_t checksum;
};

struct Vec3 { float x, y, z; };
struct ControlState { float pos, vel, target; };

const char*  resultStr(TestResult r);
void         recordResult(const char* name, TestResult r, const char* detail = nullptr);
void         resetCounters();
void         printSummary();
void         universalPrintHelp();
void         universalPrintStatus();
void         printBoardCapabilityReport();

uint16_t     crc16(const uint8_t* data, size_t len);
void         buildPacket(TestPacket &p, uint32_t seq);
bool         verifyPacket(const TestPacket &p);

float        vecLength(const Vec3 &v);
Vec3         vecNormalize(const Vec3 &v);
float        wrapAngle(float a);
float        controlLoopWorkload(ControlState &s);
bool         validateSensorRange(float v, float lo, float hi);
float        safeDivide(float a, float b, float fallback);

CommandId    parseCommand(const char* line);
void         handleLine(char* line);

TestResult   testBootSelfTest();
TestResult   testCommandParserSelfTest();
TestResult   testPacketFramingSelfTest();
TestResult   testIntegerBenchmark();
TestResult   testFloatBenchmark();
TestResult   testTrigBenchmark();
TestResult   testNumericalCorrectness();
TestResult   testLoopTiming();
TestResult   testRealtimeDeadline();
TestResult   testCpuStressTest();
TestResult   testFaultInjection();
TestResult   testSoak(uint32_t durationMs);
void         runAll();

// ============================================================================
// Globals
// ============================================================================

uint16_t g_passed = 0, g_failed = 0, g_skipped = 0;

char    g_inputBuf[64];
uint8_t g_inputLen = 0;

// ============================================================================
// Reporting helpers
// ============================================================================

const char* resultStr(TestResult r) {
  switch (r) {
    case T_PASS: return "PASS";
    case T_FAIL: return "FAIL";
    default:     return "SKIP";
  }
}

void recordResult(const char* name, TestResult r, const char* detail) {
  Serial.print(F("["));
  Serial.print(resultStr(r));
  Serial.print(F("] "));
  Serial.print(name);
  if (detail != nullptr) {
    Serial.print(F(" - "));
    Serial.print(detail);
  }
  Serial.println();
  if (r == T_PASS) g_passed++;
  else if (r == T_FAIL) g_failed++;
  else g_skipped++;
}

void resetCounters() { g_passed = 0; g_failed = 0; g_skipped = 0; }

void printSummary() {
  Serial.println(F("========================================"));
  Serial.println(F("SUMMARY"));
  Serial.print(F("Passed:  "));  Serial.println(g_passed);
  Serial.print(F("Failed:  "));  Serial.println(g_failed);
  Serial.print(F("Skipped: "));  Serial.println(g_skipped);
  Serial.print(F("Overall: "));
  if (g_failed > 0)        Serial.println(F("FAIL"));
  else if (g_skipped > 0)  Serial.println(F("PASS WITH SKIPPED TESTS"));
  else                     Serial.println(F("PASS"));
  Serial.print(F("@TEST_RESULT="));
  Serial.println(g_failed > 0 ? F("FAIL") : F("PASS"));
  Serial.println(F("@TEST_COMPLETE"));
  Serial.println(F("========================================"));
}

void universalPrintHelp() {
  Serial.println(F("Universal Board Test Suite - commands:"));
  Serial.println(F("  help                 - show this message"));
  Serial.println(F("  status               - quick uptime check"));
  Serial.println(F("  run_all              - run every included test + report"));
  Serial.println(F("  run_calc             - integer/float/trig benchmarks"));
  Serial.println(F("  run_timing           - loop timing/jitter"));
  Serial.println(F("  run_realtime         - simulated control-loop deadline test"));
  Serial.println(F("  run_stress           - CPU load/stress test"));
  Serial.println(F("  run_faults           - fault-injection test"));
  Serial.println(F("  run_numeric          - numerical correctness suite"));
  Serial.println(F("  run_packet           - packet framing/checksum self-test"));
  Serial.println(F("  run_soak <seconds>   - soak test, e.g. 'run_soak 3600' for 1 hour"));
  Serial.println(F("  report               - board capability report only"));
}

void universalPrintStatus() {
  Serial.print(F("Uptime (ms): "));
  Serial.println(millis());
  Serial.println(F("Ready. Type 'help' for commands."));
}

void printBoardCapabilityReport() {
  Serial.println(F("---- Board Capability Report ----"));
  Serial.print(F("sizeof(char):      "));      Serial.println(sizeof(char));
  Serial.print(F("sizeof(short):     "));      Serial.println(sizeof(short));
  Serial.print(F("sizeof(int):       "));      Serial.println(sizeof(int));
  Serial.print(F("sizeof(long):      "));      Serial.println(sizeof(long));
  Serial.print(F("sizeof(long long): "));      Serial.println(sizeof(long long));
  Serial.print(F("sizeof(float):     "));      Serial.println(sizeof(float));
  Serial.print(F("sizeof(double):    "));      Serial.println(sizeof(double));
  Serial.print(F("sizeof(void*):     "));      Serial.println(sizeof(void*));

  union { uint16_t u16; uint8_t b[2]; } endianTest;
  endianTest.u16 = 0x0102;
  bool little = (endianTest.b[0] == 0x02);
  Serial.print(F("byte order:        "));
  Serial.println(little ? F("little-endian") : F("big-endian"));

#if defined(F_CPU)
  Serial.print(F("F_CPU (Hz):        "));
  Serial.println((unsigned long)F_CPU);
#else
  Serial.println(F("F_CPU:             not defined by this core"));
#endif

#if defined(__VERSION__)
  Serial.print(F("compiler version:  "));
  Serial.println(__VERSION__);
#endif

#if defined(ARDUINO)
  Serial.print(F("Arduino core ver:  "));
  Serial.println(ARDUINO);
#endif

#if defined(__AVR__)
  Serial.println(F("toolchain macro:   __AVR__ (AVR)"));
#elif defined(ESP32)
  Serial.println(F("toolchain macro:   ESP32"));
#elif defined(TEENSYDUINO)
  Serial.println(F("toolchain macro:   TEENSYDUINO"));
#elif defined(ARDUINO_ARCH_SAMD)
  Serial.println(F("toolchain macro:   ARDUINO_ARCH_SAMD"));
#elif defined(ARDUINO_ARCH_RP2040)
  Serial.println(F("toolchain macro:   ARDUINO_ARCH_RP2040"));
#elif defined(ARDUINO_ARCH_STM32)
  Serial.println(F("toolchain macro:   ARDUINO_ARCH_STM32"));
#else
  Serial.println(F("toolchain macro:   none recognized - unlabeled architecture"));
#endif
  Serial.println(F("---- End Report ----"));
}

// ============================================================================
// CRC / packet framing
//
// NOTE: this struct's in-memory layout (padding/alignment) is whatever the
// compiler picks for the target it's built on, and is NOT guaranteed to
// match across different architectures. That's fine for this self-test
// (build and verify happen on the same board, same compiler, same run) but
// it means you must NOT just memcpy this struct across the wire to a
// different architecture and expect the bytes to line up. A real wire
// protocol needs explicit byte-by-byte serialization, not a raw struct dump.
// ============================================================================

uint16_t crc16(const uint8_t* data, size_t len) {
  uint16_t crc = 0xFFFF;
  for (size_t i = 0; i < len; i++) {
    crc ^= (uint16_t)data[i] << 8;
    for (uint8_t b = 0; b < 8; b++) {
      if (crc & 0x8000) crc = (crc << 1) ^ 0x1021;
      else crc <<= 1;
    }
  }
  return crc;
}

void buildPacket(TestPacket &p, uint32_t seq) {
  p.magic = 0xABCD;
  p.seq = seq;
  p.timestamp_us = micros();
  for (int i = 0; i < 16; i++) p.payload[i] = (uint8_t)((seq + i) & 0xFF);
  p.checksum = crc16((const uint8_t*)&p, offsetof(TestPacket, checksum));
}

bool verifyPacket(const TestPacket &p) {
  uint16_t chk = crc16((const uint8_t*)&p, offsetof(TestPacket, checksum));
  return chk == p.checksum;
}

// ============================================================================
// Math / control helpers
// ============================================================================

float vecLength(const Vec3 &v) {
  return sqrtf(v.x * v.x + v.y * v.y + v.z * v.z);
}

Vec3 vecNormalize(const Vec3 &v) {
  float len = vecLength(v);
  if (len < 1e-9f) return Vec3{0, 0, 0};
  return Vec3{v.x / len, v.y / len, v.z / len};
}

float wrapAngle(float a) {
  while (a > PI)  a -= 2.0f * PI;
  while (a < -PI) a += 2.0f * PI;
  return a;
}

float controlLoopWorkload(ControlState &s) {
  float error = s.target - s.pos;
  float velTerm = -0.1f * s.vel;
  float output = 0.8f * error + velTerm + 0.05f * sinf(s.pos);
  s.vel += output * 0.001f;
  s.pos += s.vel * 0.001f;
  return output;
}

bool validateSensorRange(float v, float lo, float hi) {
  if (isnan(v) || isinf(v)) return false;
  if (v < lo || v > hi) return false;
  return true;
}

float safeDivide(float a, float b, float fallback) {
  if (fabs(b) < 1e-9f) return fallback;
  return a / b;
}

// ============================================================================
// Individual tests
// ============================================================================

TestResult testBootSelfTest() {
  bool ok = true;
  int ia = 17 * 3;
  if (ia != 51) ok = false;
  float fa = 2.5f * 4.0f;
  if (fabs(fa - 10.0f) > 0.0001f) ok = false;
  unsigned long m0 = millis();
  delay(5);
  unsigned long m1 = millis();
  unsigned long elapsed = m1 - m0; // unsigned subtraction -> correct even across millis() wraparound
  if (elapsed < 3) ok = false;
  return ok ? T_PASS : T_FAIL;
}

TestResult testCommandParserSelfTest() {
  struct { const char* in; CommandId expect; } vectors[] = {
    {"help",          CMD_HELP},
    {"status",        CMD_STATUS},
    {"run_all",       CMD_RUN_ALL},
    {"run_calc",      CMD_RUN_CALC},
    {"run_soak",      CMD_RUN_SOAK},
    {"bogus_cmd_xyz", CMD_UNKNOWN},
    {"",              CMD_UNKNOWN},
  };
  bool ok = true;
  for (size_t i = 0; i < sizeof(vectors) / sizeof(vectors[0]); i++) {
    if (parseCommand(vectors[i].in) != vectors[i].expect) ok = false;
  }
  return ok ? T_PASS : T_FAIL;
}

TestResult testPacketFramingSelfTest() {
  bool ok = true;
  const int N = 20;
  for (int i = 0; i < N; i++) {
    TestPacket p;
    buildPacket(p, (uint32_t)i);
    if (!verifyPacket(p)) ok = false;
    if (p.seq != (uint32_t)i) ok = false;
    if (p.magic != 0xABCD) ok = false;
  }
  // A checksum that never catches corruption is worse than no checksum -
  // prove it actually detects a flipped bit before trusting it anywhere else.
  TestPacket bad;
  buildPacket(bad, 99);
  bad.payload[0] ^= 0xFF;
  if (verifyPacket(bad)) ok = false; // corruption MUST be detected
  return ok ? T_PASS : T_FAIL;
}

TestResult testIntegerBenchmark() {
  const uint32_t ITERS = 100000UL;
  unsigned long start = micros();
  volatile long acc = 0;
  for (uint32_t i = 0; i < ITERS; i++) {
    acc += (long)i * 3 - 7;
    acc %= 100000L;
  }
  unsigned long elapsed = micros() - start;
  Serial.print(F("  integer ops: "));
  Serial.print(ITERS);
  Serial.print(F(" iterations in "));
  Serial.print(elapsed);
  Serial.println(F(" us"));
  if (elapsed == 0) return T_FAIL; // clock not advancing, or loop optimized away
  double opsPerSec = (double)ITERS * 1000000.0 / (double)elapsed;
  Serial.print(F("  approx "));
  Serial.print(opsPerSec);
  Serial.println(F(" ops/sec"));
  return T_PASS;
}

TestResult testFloatBenchmark() {
  const uint32_t ITERS = 20000UL;
  unsigned long start = micros();
  volatile float acc = 1.0f;
  for (uint32_t i = 0; i < ITERS; i++) {
    acc = acc * 1.0001f + 0.0001f;
    if (acc > 1e6f) acc = 1.0f; // keep bounded so we're timing steady-state work, not overflow
  }
  unsigned long elapsed = micros() - start;
  Serial.print(F("  float ops: "));
  Serial.print(ITERS);
  Serial.print(F(" iterations in "));
  Serial.print(elapsed);
  Serial.println(F(" us"));
  if (elapsed == 0) return T_FAIL;
  if (isnan(acc) || isinf(acc)) return T_FAIL;
  return T_PASS;
}

TestResult testTrigBenchmark() {
  const uint32_t ITERS = 5000UL;
  unsigned long start = micros();
  volatile float acc = 0.0f;
  for (uint32_t i = 0; i < ITERS; i++) {
    float x = (float)i * 0.001f;
    acc += sinf(x) + cosf(x) + tanf(x * 0.1f);
  }
  unsigned long elapsed = micros() - start;
  Serial.print(F("  trig calls: "));
  Serial.print(ITERS * 3);
  Serial.print(F(" in "));
  Serial.print(elapsed);
  Serial.println(F(" us"));
  if (elapsed == 0) return T_FAIL;
  if (isnan(acc) || isinf(acc)) return T_FAIL;
  return T_PASS;
}

TestResult testNumericalCorrectness() {
  bool ok = true;
  const float eps = 0.001f;

  if (fabs(sinf(0.0f)) > eps) ok = false;
  if (fabs(cosf(0.0f) - 1.0f) > eps) ok = false;
  if (fabs(sqrtf(4.0f) - 2.0f) > eps) ok = false;
  if (fabs(sqrtf(2.0f) * sqrtf(2.0f) - 2.0f) > 0.001f) ok = false;

  Vec3 v{3.0f, 4.0f, 0.0f};
  Vec3 n = vecNormalize(v);
  if (fabs(vecLength(n) - 1.0f) > eps) ok = false;

  float wrapped = wrapAngle(3.5f * PI);
  if (wrapped < -PI - eps || wrapped > PI + eps) ok = false;

  volatile float zero = 0.0f;
  volatile float one = 1.0f;
  float nanVal = zero / zero;
  float infVal = one / zero;
  if (!isnan(nanVal)) ok = false;
  if (!isinf(infVal)) ok = false;

  return ok ? T_PASS : T_FAIL;
}

TestResult testLoopTiming() {
  const int N = 200;
  unsigned long periods[N];
  unsigned long last = micros();
  for (int i = 0; i < N; i++) {
    volatile int x = i * 2 + 1; (void)x; // minimal representative "tick" workload
    unsigned long now = micros();
    periods[i] = now - last; // unsigned subtraction -> correct across micros() wraparound
    last = now;
  }
  unsigned long minP = periods[1], maxP = 0;
  double sum = 0;
  for (int i = 1; i < N; i++) {
    unsigned long p = periods[i];
    if (p < minP) minP = p;
    if (p > maxP) maxP = p;
    sum += p;
  }
  double avg = sum / (N - 1);
  Serial.print(F("  min/avg/max period (us): "));
  Serial.print(minP); Serial.print(F(" / ")); Serial.print(avg);
  Serial.print(F(" / ")); Serial.println(maxP);
  Serial.println(F("  (micros() resolution varies by core - this measures THIS board, not a universal number)"));
  if (maxP > 1000000UL) return T_FAIL; // a 1-second gap in a tight loop means something is badly wrong
  return T_PASS;
}

TestResult testRealtimeDeadline() {
  const uint32_t targetPeriodUs = 1000; // 1 kHz target
  const int N = 500;
  ControlState st{0.0f, 0.0f, 1.0f};
  unsigned long maxExec = 0, minExec = 0xFFFFFFFFUL, sumExec = 0;
  uint16_t missed = 0;

  for (int i = 0; i < N; i++) {
    unsigned long t0 = micros();
    volatile float out = controlLoopWorkload(st); (void)out;
    unsigned long t1 = micros();
    unsigned long exec = t1 - t0;
    if (exec > maxExec) maxExec = exec;
    if (exec < minExec) minExec = exec;
    sumExec += exec;
    if (exec > targetPeriodUs) missed++;
    while ((micros() - t0) < targetPeriodUs) { /* hold to fixed-rate period */ }
  }

  double avgExec = (double)sumExec / N;
  Serial.print(F("  target: ")); Serial.print(targetPeriodUs); Serial.println(F(" us/cycle (1000 Hz)"));
  Serial.print(F("  exec min/avg/max (us): "));
  Serial.print(minExec); Serial.print(F(" / ")); Serial.print(avgExec);
  Serial.print(F(" / ")); Serial.println(maxExec);
  Serial.print(F("  missed deadlines: ")); Serial.print(missed); Serial.print(F(" / ")); Serial.println(N);
  Serial.print(F("  worst-case margin (us): ")); Serial.println((long)targetPeriodUs - (long)maxExec);
  Serial.println(F("  (missed-deadline count is the real answer here, not PASS/FAIL - see file header notes)"));

  if (minExec > maxExec) return T_FAIL; // sanity check on the stats themselves, not the workload
  return T_PASS;
}

TestResult testCpuStressTest() {
  const unsigned long durationMs = 2000; // short demo duration; lengthen for a real stress run
  unsigned long start = millis();
  uint32_t iterations = 0;
  volatile long dummyI = 0;
  volatile float dummyF = 1.0f;
  while (millis() - start < durationMs) {
    dummyI = (dummyI * 3 + 7) % 1000003L;
    dummyF = sinf(dummyF) + cosf(dummyF * 0.5f);
    if (isnan(dummyF) || isinf(dummyF)) dummyF = 1.0f; // guard against divergence
    iterations++;
  }
  unsigned long actualElapsed = millis() - start;
  Serial.print(F("  ")); Serial.print(iterations);
  Serial.print(F(" mixed-workload iterations in ")); Serial.print(actualElapsed); Serial.println(F(" ms"));
  if (iterations == 0) return T_FAIL; // board effectively frozen, or clock broken
  return T_PASS;
}

TestResult testFaultInjection() {
  bool ok = true;

  if (validateSensorRange(NAN, 0, 100))      ok = false; // must reject NaN
  if (validateSensorRange(INFINITY, 0, 100)) ok = false; // must reject Inf
  if (validateSensorRange(500.0f, 0, 100))   ok = false; // must reject out-of-range
  if (!validateSensorRange(50.0f, 0, 100))   ok = false; // must accept valid input

  float r = safeDivide(10.0f, 0.0f, -1.0f);
  if (r != -1.0f) ok = false; // must fall back, not divide by zero

  TestPacket bad;
  buildPacket(bad, 1);
  bad.checksum ^= 0xFFFF;
  if (verifyPacket(bad)) ok = false; // corrupted checksum must be caught

  uint32_t seqs[5] = {0, 1, 2, 4, 5}; // deliberate gap at index 3
  bool gapDetected = false;
  for (int i = 1; i < 5; i++) if (seqs[i] != seqs[i - 1] + 1) gapDetected = true;
  if (!gapDetected) ok = false;

  return ok ? T_PASS : T_FAIL;
}

TestResult testSoak(uint32_t durationMs) {
  unsigned long start = millis();
  uint32_t loopCount = 0, packetErrors = 0, calcErrors = 0;
  unsigned long maxLoopUs = 0;

  while (millis() - start < durationMs) {
    unsigned long t0 = micros();

    TestPacket p;
    buildPacket(p, loopCount);
    if (!verifyPacket(p)) packetErrors++;

    ControlState cs{0.0f, 0.0f, 1.0f};
    volatile float o = controlLoopWorkload(cs);
    if (isnan(o) || isinf(o)) calcErrors++;

    unsigned long dt = micros() - t0;
    if (dt > maxLoopUs) maxLoopUs = dt;
    loopCount++;
  }

  Serial.print(F("  soak duration: ")); Serial.print(durationMs); Serial.println(F(" ms"));
  Serial.print(F("  loop iterations: ")); Serial.println(loopCount);
  Serial.print(F("  max single-iteration time (us): ")); Serial.println(maxLoopUs);
  Serial.print(F("  packet errors: ")); Serial.println(packetErrors);
  Serial.print(F("  calc errors: ")); Serial.println(calcErrors);

  if (packetErrors > 0 || calcErrors > 0) return T_FAIL;
  if (loopCount == 0) return T_FAIL;
  return T_PASS;
}

// ============================================================================
// Command parsing / dispatch
// ============================================================================

CommandId parseCommand(const char* line) {
  if (strcmp(line, "identify") == 0)    return CMD_IDENTIFY;
  if (strcmp(line, "help") == 0)         return CMD_HELP;
  if (strcmp(line, "status") == 0)       return CMD_STATUS;
  if (strcmp(line, "run_all") == 0)      return CMD_RUN_ALL;
  if (strcmp(line, "run_calc") == 0)     return CMD_RUN_CALC;
  if (strcmp(line, "run_timing") == 0)   return CMD_RUN_TIMING;
  if (strcmp(line, "run_realtime") == 0) return CMD_RUN_REALTIME;
  if (strcmp(line, "run_stress") == 0)   return CMD_RUN_STRESS;
  if (strcmp(line, "run_faults") == 0)   return CMD_RUN_FAULTS;
  if (strcmp(line, "run_numeric") == 0)  return CMD_RUN_NUMERIC;
  if (strcmp(line, "run_packet") == 0)   return CMD_RUN_PACKET;
  if (strcmp(line, "run_soak") == 0)     return CMD_RUN_SOAK;
  if (strcmp(line, "report") == 0)       return CMD_REPORT;
  return CMD_UNKNOWN;
}

void runAll() {
  resetCounters();
  Serial.println(F("========================================"));
  Serial.println(F("UNIVERSAL BOARD TEST SUITE"));
  Serial.println(F("========================================"));
  unsigned long suiteStart = millis();

  recordResult("Boot / self-test",                       testBootSelfTest());
  recordResult("Command parser self-test",                testCommandParserSelfTest());
  recordResult("Packet framing + checksum self-test",     testPacketFramingSelfTest());
  recordResult("Integer calculation benchmark",           testIntegerBenchmark());
  recordResult("Floating-point calculation benchmark",    testFloatBenchmark());
  recordResult("Trigonometry benchmark",                  testTrigBenchmark());
  recordResult("Numerical correctness",                   testNumericalCorrectness());
  recordResult("Loop timing / jitter",                    testLoopTiming());
  recordResult("Simulated real-time control loop",        testRealtimeDeadline());
  recordResult("CPU load / stress test",                  testCpuStressTest());
  recordResult("Software fault-injection",                testFaultInjection());
  recordResult("Long-duration soak (5s demo run)",        testSoak(5000));

  Serial.println();
  printBoardCapabilityReport();
  Serial.println();

  Serial.println(F("---- Needs a per-core adapter (not included - see file header) ----"));
  recordResult("Memory / heap stability",          T_SKIP, "no portable free-RAM API");
  recordResult("Watchdog configure + recovery",    T_SKIP, "register/API differs per core; resets the board");
  recordResult("Reset-reason decode",              T_SKIP, "register/API differs per core");
  recordResult("Internal EEPROM/flash/FS test",    T_SKIP, "API differs per core; destructive by design, skipped");
  recordResult("CPU cycle-accurate timing",        T_SKIP, "Cortex-M DWT cycle counter only");
  recordResult("Die temperature",                  T_SKIP, "not exposed on most cores");

  unsigned long suiteElapsed = millis() - suiteStart;
  Serial.println();
  printSummary();
  Serial.print(F("Total suite time: ")); Serial.print(suiteElapsed); Serial.println(F(" ms"));
}

void handleLine(char* line) {
  char cmd[32];
  uint32_t argVal = 0;
  bool hasArg = false;

  char* spacePos = strchr(line, ' ');
  if (spacePos != nullptr) {
    size_t cmdLen = (size_t)(spacePos - line);
    if (cmdLen >= sizeof(cmd)) cmdLen = sizeof(cmd) - 1;
    memcpy(cmd, line, cmdLen);
    cmd[cmdLen] = '\0';
    argVal = (uint32_t)atol(spacePos + 1);
    hasArg = true;
  } else {
    strncpy(cmd, line, sizeof(cmd) - 1);
    cmd[sizeof(cmd) - 1] = '\0';
  }

  CommandId id = parseCommand(cmd);
  switch (id) {
    case CMD_IDENTIFY:
      printTestProtocol(
          "universal",
          "universal-board",
          "universal_board_001");
      break;
    case CMD_HELP:    universalPrintHelp(); break;
    case CMD_STATUS:  universalPrintStatus(); break;
    case CMD_RUN_ALL: runAll(); break;

    case CMD_RUN_CALC:
      resetCounters();
      recordResult("Integer benchmark", testIntegerBenchmark());
      recordResult("Float benchmark", testFloatBenchmark());
      recordResult("Trig benchmark", testTrigBenchmark());
      printSummary();
      break;

    case CMD_RUN_TIMING:
      resetCounters();
      recordResult("Loop timing", testLoopTiming());
      printSummary();
      break;

    case CMD_RUN_REALTIME:
      resetCounters();
      recordResult("Real-time deadline", testRealtimeDeadline());
      printSummary();
      break;

    case CMD_RUN_STRESS:
      resetCounters();
      recordResult("CPU stress", testCpuStressTest());
      printSummary();
      break;

    case CMD_RUN_FAULTS:
      resetCounters();
      recordResult("Fault injection", testFaultInjection());
      printSummary();
      break;

    case CMD_RUN_NUMERIC:
      resetCounters();
      recordResult("Numerical correctness", testNumericalCorrectness());
      printSummary();
      break;

    case CMD_RUN_PACKET:
      resetCounters();
      recordResult("Packet framing", testPacketFramingSelfTest());
      printSummary();
      break;

    case CMD_RUN_SOAK: {
      uint32_t seconds = (hasArg && argVal > 0) ? argVal : 5;
      resetCounters();
      Serial.print(F("Running soak test for "));
      Serial.print(seconds);
      Serial.println(F(" seconds..."));
      recordResult("Long-duration soak", testSoak(seconds * 1000UL));
      printSummary();
      break;
    }

    case CMD_REPORT:
      printBoardCapabilityReport();
      break;

    default:
      Serial.print(F("Unknown command: "));
      Serial.println(cmd);
      Serial.println(F("Type 'help' for a list of commands."));
  }
}

// ============================================================================
// Arduino entry points
// ============================================================================

void initializeUniversalBoardTest() {
  Serial.begin(115200);
  unsigned long t0 = millis();
  while (!Serial && (millis() - t0) < 3000) {
    // Wait briefly for native-USB boards to enumerate. Serial's operator
    // bool() returns true immediately on plain-UART boards, so this is a
    // no-op there. The 3s timeout is a safety net in case any core handles
    // this differently than expected - never block forever on hardware.
  }
  universalPrintHelp();
}

void runUniversalBoardTest() {
  while (Serial.available()) {
    char c = Serial.read();
    if (c == '\n' || c == '\r') {
      if (g_inputLen > 0) {
        g_inputBuf[g_inputLen] = '\0';
        handleLine(g_inputBuf);
        g_inputLen = 0;
      }
    } else if (g_inputLen < sizeof(g_inputBuf) - 1) {
      g_inputBuf[g_inputLen++] = c;
    }
  }
}