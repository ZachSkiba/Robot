#include <Arduino.h>
#include <stdint.h>
#include <string.h>
#include <ctype.h>

#include "diagnostic-firmware.h"
#include "test_protocol.h"

// ============================================================
// CONFIGURATION
// ============================================================

// Serial communication speed.
//
// For USB CDC serial boards such as some Teensy and Leonardo
// boards, the baud rate may not affect the USB connection.
// It is still useful for normal UART-based boards.
constexpr uint32_t SERIAL_BAUD = 115200UL;

// Timing intervals.
constexpr uint32_t HEARTBEAT_PERIOD_MS = 1000UL;
constexpr uint32_t LED_PERIOD_MS = 500UL;

// Maximum command length, excluding the null terminator.
constexpr size_t COMMAND_BUFFER_SIZE = 64;

// ============================================================
// LED CONFIGURATION
// ============================================================
//
// Some Arduino-style boards define LED_BUILTIN.
// Some boards do not.
//
// If LED_BUILTIN exists, use it.
// Otherwise, disable built-in LED support.
//
// This allows the firmware to compile on boards without a
// built-in LED.
//

#ifdef LED_BUILTIN

constexpr bool HAS_BUILTIN_LED = true;
constexpr uint8_t LED_PIN = LED_BUILTIN;

#else

constexpr bool HAS_BUILTIN_LED = false;
constexpr uint8_t LED_PIN = 0;

#endif

// ============================================================
// STATE
// ============================================================

bool ledState = false;

uint32_t lastHeartbeatMs = 0;
uint32_t lastLedToggleMs = 0;

char commandBuffer[COMMAND_BUFFER_SIZE];
size_t commandLength = 0;

// ============================================================
// LED CONTROL
// ============================================================

void setLed(bool state)
{
    ledState = state;

    if (HAS_BUILTIN_LED)
    {
        digitalWrite(
            LED_PIN,
            ledState ? HIGH : LOW);
    }
}

void initializeLed()
{
    if (HAS_BUILTIN_LED)
    {
        pinMode(LED_PIN, OUTPUT);
        setLed(false);
    }
}

// ============================================================
// SERIAL OUTPUT
// ============================================================

void printBanner()
{
    Serial.println();
    Serial.println(F("================================"));
    Serial.println(F("Universal Diagnostic Firmware"));
    Serial.println(F("================================"));
    Serial.println(F("Firmware: diagnostic-v2"));
    Serial.println(F("Type 'help' for commands."));
    Serial.println();
}

void printStatus()
{
    Serial.println();
    Serial.println(F("=== BOARD STATUS ==="));

    Serial.println(F("Board: configured PlatformIO target"));
    Serial.println(F("Firmware: diagnostic-v2"));

    Serial.print(F("Uptime ms: "));
    Serial.println(millis());

    Serial.print(F("Built-in LED: "));

    if (HAS_BUILTIN_LED)
    {
        Serial.println(F("available"));
    }
    else
    {
        Serial.println(F("not available"));
    }

    Serial.print(F("LED state: "));

    if (HAS_BUILTIN_LED)
    {
        Serial.println(
            ledState ? F("ON") : F("OFF"));
    }
    else
    {
        Serial.println(F("unavailable"));
    }

    Serial.print(F("Serial baud setting: "));
    Serial.println(SERIAL_BAUD);

    Serial.println(F("===================="));
    Serial.println();
}

void printHelp()
{
    Serial.println();
    Serial.println(F("Available commands:"));
    Serial.println(F("  ping"));
    Serial.println(F("  status"));
    Serial.println(F("  led on"));
    Serial.println(F("  led off"));
    Serial.println(F("  help"));
    Serial.println();
}

// ============================================================
// COMMAND PROCESSING
// ============================================================

void convertCommandToLowercase(char *text)
{
    while (*text != '\0')
    {
        *text = static_cast<char>(
            tolower(
                static_cast<unsigned char>(*text)));

        text++;
    }
}

void handleCommand(char *command)
{
    // Remove leading spaces.
    char *start = command;

    while (*start == ' ' || *start == '\t')
    {
        start++;
    }

    // Remove trailing spaces.
    size_t length = strlen(start);

    while (length > 0)
    {
        const char lastCharacter = start[length - 1];

        if (lastCharacter == ' ' ||
            lastCharacter == '\t')
        {
            start[length - 1] = '\0';
            length--;
        }
        else
        {
            break;
        }
    }

    convertCommandToLowercase(start);

    if (strcmp(start, "identify") == 0)
    {
        printTestProtocol(
            "diagnostic",
            "diagnostic",
            "diagnostic_001");
    }
    else if (strcmp(start, "ping") == 0)
    {
        Serial.println(F("pong"));
    }
    else if (strcmp(start, "status") == 0)
    {
        Serial.println(F("@TEST_START"));
        printStatus();
        Serial.println(F("@TEST_RESULT=PASS"));
        Serial.println(F("@TEST_COMPLETE"));
    }
    else if (strcmp(start, "led on") == 0)
    {
        if (HAS_BUILTIN_LED)
        {
            setLed(true);
            Serial.println(F("LED ON"));
        }
        else
        {
            Serial.println(
                F("ERROR: board has no built-in LED"));
        }
    }
    else if (strcmp(start, "led off") == 0)
    {
        if (HAS_BUILTIN_LED)
        {
            setLed(false);
            Serial.println(F("LED OFF"));
        }
        else
        {
            Serial.println(
                F("ERROR: board has no built-in LED"));
        }
    }
    else if (strcmp(start, "help") == 0)
    {
        printHelp();
    }
    else if (strlen(start) > 0)
    {
        Serial.print(F("Unknown command: "));
        Serial.println(start);
        Serial.println(F("Type 'help' for available commands."));
    }
}

// ============================================================
// SERIAL INPUT
// ============================================================
//
// This function is non-blocking.
//
// It reads only the bytes currently available and returns.
// That allows the heartbeat and LED timing to continue running.
//

void readSerial()
{
    while (Serial.available() > 0)
    {
        const char character =
            static_cast<char>(Serial.read());

        // A newline or carriage return completes the command.
        if (character == '\n' ||
            character == '\r')
        {
            if (commandLength > 0)
            {
                commandBuffer[commandLength] = '\0';

                // Only process a complete, bounded command frame. Mixed
                // output is invalid input and must not become a command.
                if (commandLength < COMMAND_BUFFER_SIZE - 1)
                {
                    handleCommand(commandBuffer);
                }

                commandLength = 0;
                commandBuffer[0] = '\0';
            }

            continue;
        }

        // Ignore other control characters.
        if (static_cast<unsigned char>(character) < 32)
        {
            continue;
        }

        // Store the character if there is room.
        if (commandLength <
            COMMAND_BUFFER_SIZE - 1)
        {
            commandBuffer[commandLength] =
                character;

            commandLength++;
            commandBuffer[commandLength] = '\0';
        }
        else
        {
            // Reset the current command so a long or malformed
            // command cannot permanently block the parser.
            commandLength = 0;
            commandBuffer[0] = '\0';

            Serial.println(
                F("ERROR: command too long"));
        }
    }
}

// ============================================================
// PERIODIC TASKS
// ============================================================

void updateLed(uint32_t nowMs)
{
    if (!HAS_BUILTIN_LED)
    {
        return;
    }

    if ((nowMs - lastLedToggleMs) >=
        LED_PERIOD_MS)
    {
        lastLedToggleMs = nowMs;

        setLed(!ledState);
    }
}

void sendHeartbeat(uint32_t nowMs)
{
    if ((nowMs - lastHeartbeatMs) >=
        HEARTBEAT_PERIOD_MS)
    {
        lastHeartbeatMs = nowMs;

        Serial.print(F("Board heartbeat | uptime_ms="));
        Serial.println(nowMs);
    }
}

// ============================================================
// PUBLIC INITIALIZATION FUNCTION
// ============================================================

void initializeDiagnosticFirmware()
{
    initializeLed();

    Serial.begin(SERIAL_BAUD);

    // Do not use while (!Serial) here.
    //
    // That can block forever on boards that use hardware UART
    // or when no serial monitor is connected.
    //
    // A short delay gives some USB boards time to initialize
    // without making the firmware dependent on a computer.
    delay(100);

    const uint32_t nowMs = millis();

    lastHeartbeatMs = nowMs;
    lastLedToggleMs = nowMs;

    commandLength = 0;
    commandBuffer[0] = '\0';

    printBanner();
}

// ============================================================
// PUBLIC RUNTIME FUNCTION
// ============================================================
//
// Call this repeatedly from loop().
//

void runDiagnosticFirmware()
{
    const uint32_t nowMs = millis();

    readSerial();

    updateLed(nowMs);

    sendHeartbeat(nowMs);
}