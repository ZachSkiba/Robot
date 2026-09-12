#include <Arduino.h>
#include <stdint.h>
#include <string.h>

#include "serial_throughput_test.h"

namespace
{

// ============================================================
// CONFIGURATION
// ============================================================

constexpr uint32_t TEST_DURATION_MS = 10000UL;

// Send one packet every 10 milliseconds.
// This is a 100 Hz packet rate.
constexpr uint32_t PACKET_PERIOD_MS = 10UL;

// Fixed packet size in bytes.
constexpr size_t PACKET_SIZE = 32;

// Serial speed for UART-based boards.
constexpr uint32_t SERIAL_BAUD = 115200UL;

// ============================================================
// PACKET FORMAT
// ============================================================
//
// Every packet is exactly 32 bytes:
//
// Bytes 0-3:   Packet magic
// Bytes 4-7:   Packet sequence number
// Bytes 8-11:  Firmware timestamp in milliseconds
// Bytes 12-15: Test identifier
// Bytes 16-31: Deterministic payload
//
// Fixed-size binary packets make byte counting reliable.
//

struct SerialPacket
{
    uint32_t magic;
    uint32_t sequence;
    uint32_t timestampMs;
    uint32_t testId;
    uint8_t payload[16];
};

static_assert(
    sizeof(SerialPacket) == PACKET_SIZE,
    "SerialPacket must be exactly PACKET_SIZE bytes");

// ============================================================
// RESULTS
// ============================================================

struct ThroughputResults
{
    uint32_t elapsedMs = 0;

    uint32_t packetsSent = 0;

    uint32_t bytesSent = 0;

    uint32_t scheduledPackets = 0;

    uint32_t missedPacketSlots = 0;
};

// ============================================================
// PACKET CREATION
// ============================================================

void createPacket(
    SerialPacket &packet,
    uint32_t sequence,
    uint32_t timestampMs)
{
    packet.magic = 0x524F424FUL; // "ROBO"
    packet.sequence = sequence;
    packet.timestampMs = timestampMs;
    packet.testId = 0x00000001UL;

    for (uint8_t i = 0; i < sizeof(packet.payload); i++)
    {
        packet.payload[i] =
            static_cast<uint8_t>(
                (sequence + i) & 0xFFU);
    }
}

// ============================================================
// RUN THROUGHPUT TEST
// ============================================================

ThroughputResults runThroughputTest()
{
    ThroughputResults results;

    SerialPacket packet;

    const uint32_t startMs = millis();

    uint32_t nextPacketMs = startMs;
    uint32_t sequence = 0;

    while ((millis() - startMs) < TEST_DURATION_MS)
    {
        const uint32_t nowMs = millis();

        if (static_cast<int32_t>(
                nowMs - nextPacketMs) >= 0)
        {
            createPacket(
                packet,
                sequence,
                nowMs);

            // Count the actual bytes accepted by Serial.write().
            const size_t bytesWritten =
                Serial.write(
                    reinterpret_cast<const uint8_t *>(&packet),
                    sizeof(packet));

            results.bytesSent +=
                static_cast<uint32_t>(bytesWritten);

            if (bytesWritten == sizeof(packet))
            {
                results.packetsSent++;
            }

            sequence++;

            results.scheduledPackets++;

            nextPacketMs += PACKET_PERIOD_MS;

            // If transmission took too long, skip missed packet
            // slots instead of sending a burst of old packets.
            if (static_cast<int32_t>(
                    nowMs - nextPacketMs) >= 0)
            {
                const uint32_t missed =
                    (nowMs - nextPacketMs) /
                    PACKET_PERIOD_MS;

                results.missedPacketSlots +=
                    missed + 1UL;

                nextPacketMs =
                    nowMs + PACKET_PERIOD_MS;
            }
        }

        // No delay() here.
        // The loop remains available for serial transmission
        // and other firmware work.
    }

    // Ensure all queued bytes have physically finished sending
    // before measuring the final completed time.
    Serial.flush();

    results.elapsedMs =
        millis() - startMs;

    return results;
}

// ============================================================
// PRINT RESULTS
// ============================================================

void printResults(
    const ThroughputResults &results)
{
    Serial.println();
    Serial.println(F("================================"));
    Serial.println(F("UNIVERSAL SERIAL THROUGHPUT TEST"));
    Serial.println(F("================================"));
    Serial.println();

    Serial.println(F("Packet format: fixed-size binary packet"));

    Serial.print(F("Packet size:          "));
    Serial.print(PACKET_SIZE);
    Serial.println(F(" bytes"));

    Serial.print(F("Target packet period: "));
    Serial.print(PACKET_PERIOD_MS);
    Serial.println(F(" ms"));

    Serial.print(F("Configured baud:      "));
    Serial.println(SERIAL_BAUD);

    Serial.println();

    Serial.print(F("Elapsed time:         "));
    Serial.print(results.elapsedMs / 1000.0f, 3);
    Serial.println(F(" s"));

    Serial.print(F("Packets sent:         "));
    Serial.println(results.packetsSent);

    Serial.print(F("Scheduled packets:    "));
    Serial.println(results.scheduledPackets);

    Serial.print(F("Bytes accepted:       "));
    Serial.println(results.bytesSent);

    Serial.print(F("Missed packet slots:  "));
    Serial.println(results.missedPacketSlots);

    Serial.println();

    if (results.elapsedMs > 0)
    {
        const float bytesPerSecond =
            static_cast<float>(results.bytesSent) *
            1000.0f /
            static_cast<float>(results.elapsedMs);

        const float bitsPerSecond =
            bytesPerSecond * 8.0f;

        const float packetsPerSecond =
            static_cast<float>(results.packetsSent) *
            1000.0f /
            static_cast<float>(results.elapsedMs);

        Serial.print(F("Bytes/second:         "));
        Serial.println(bytesPerSecond, 2);

        Serial.print(F("Bits/second:          "));
        Serial.println(bitsPerSecond, 2);

        Serial.print(F("Kilobytes/second:     "));
        Serial.println(bytesPerSecond / 1000.0f, 3);

        Serial.print(F("Packets/second:       "));
        Serial.println(packetsPerSecond, 2);

        Serial.print(F("Effective bit rate:   "));
        Serial.print(bitsPerSecond / 1000.0f, 3);
        Serial.println(F(" kbit/s"));
    }

    Serial.println();

    Serial.println(F("INTERPRETATION:"));
    Serial.println(F("- Bytes accepted is the number returned by Serial.write()."));
    Serial.println(F("- Serial.write() may queue bytes instead of transmitting them."));
    Serial.println(F("- Serial.flush() waits for queued serial data to finish."));
    Serial.println(F("- Results depend on baud rate, buffers, USB, and host behavior."));
    Serial.println(F("- This measures serial transport, not robot-control latency."));
    Serial.println(F("- Binary packets avoid variable-length text overhead."));
    Serial.println();

    Serial.println(F("=== SERIAL THROUGHPUT TEST COMPLETE ==="));
}

} // namespace

// ============================================================
// PUBLIC FUNCTION
// ============================================================

bool runSerialThroughputTest()
{
    Serial.println();
    Serial.println(F("Starting serial throughput test..."));
    Serial.println(F("The test will transmit binary packets."));
    Serial.println();

    const ThroughputResults results =
        runThroughputTest();

    printResults(results);

    return results.elapsedMs > 0 &&
           results.scheduledPackets > 0 &&
           results.packetsSent > 0;
}