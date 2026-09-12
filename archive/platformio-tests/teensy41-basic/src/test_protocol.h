#ifndef TEST_PROTOCOL_H
#define TEST_PROTOCOL_H

#include <Arduino.h>

inline void printTestProtocol(
    const char *protocol,
    const char *name,
    const char *testId)
{
    Serial.print(F("@TEST_PROTOCOL="));
    Serial.println(protocol);
    Serial.print(F("@TEST_NAME="));
    Serial.println(name);
    Serial.print(F("@TEST_ID="));
    Serial.println(testId);
    Serial.println(F("@TEST_VERSION=1"));
    Serial.println(F("@TEST_READY"));
}

#endif
