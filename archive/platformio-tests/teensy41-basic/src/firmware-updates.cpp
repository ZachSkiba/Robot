#include <Arduino.h>

// Teensy 4.1 onboard LED
constexpr uint8_t LED_PIN = LED_BUILTIN;

// Timing
constexpr uint32_t HEARTBEAT_PERIOD_MS = 1000;
constexpr uint32_t LED_PERIOD_MS = 500;

// State
bool ledState = false;
uint32_t lastHeartbeat = 0;
uint32_t lastLedToggle = 0;

String command;

void setLed(bool state)
{
    ledState = state;
    digitalWrite(LED_PIN, ledState ? HIGH : LOW);
}

void printStatus()
{
    Serial.println("=== TEENSY STATUS ===");
    Serial.println("Board: Teensy 4.1");
    Serial.println("Firmware: diagnostic-v1");

    Serial.print("Uptime ms: ");
    Serial.println(millis());

    Serial.print("LED: ");
    Serial.println(ledState ? "ON" : "OFF");

    Serial.println("=====================");
}

void handleCommand(String cmd)
{
    cmd.trim();
    cmd.toLowerCase();

    if (cmd == "ping")
    {
        Serial.println("pong");
    }
    else if (cmd == "status")
    {
        printStatus();
    }
    else if (cmd == "led on")
    {
        setLed(true);
        Serial.println("LED ON");
    }
    else if (cmd == "led off")
    {
        setLed(false);
        Serial.println("LED OFF");
    }
    else if (cmd == "help")
    {
        Serial.println("Commands:");
        Serial.println("  ping");
        Serial.println("  status");
        Serial.println("  led on");
        Serial.println("  led off");
        Serial.println("  help");
    }
    else if (cmd.length() > 0)
    {
        Serial.print("Unknown command: ");
        Serial.println(cmd);
    }
}

void readSerial()
{
    while (Serial.available() > 0)
    {
        char c = Serial.read();

        if (c == '\n' || c == '\r')
        {
            if (command.length() > 0)
            {
                handleCommand(command);
                command = "";
            }
        }
        else
        {
            command += c;

            if (command.length() > 64)
            {
                command = "";
                Serial.println("ERROR: command too long");
            }
        }
    }
}

void runDiagnosticFirmware()
{
    const uint32_t now = millis();

    readSerial();

    if (now - lastLedToggle >= LED_PERIOD_MS)
    {
        lastLedToggle = now;
        setLed(!ledState);
    }

    if (now - lastHeartbeat >= HEARTBEAT_PERIOD_MS)
    {
        lastHeartbeat = now;
        Serial.print("Teensy 4.1 heartbeat | uptime_ms=");
        Serial.println(now);
    }
}

void initializeDiagnosticFirmware()
{
    pinMode(LED_PIN, OUTPUT);
    setLed(false);

    Serial.begin(115200);
    delay(1000);

    Serial.println();
    Serial.println("================================");
    Serial.println("Teensy 4.1 Diagnostic Firmware");
    Serial.println("Firmware: diagnostic-v1");
    Serial.println("Type 'help' for commands.");
    Serial.println("================================");
}
