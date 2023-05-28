#include "DigitalIn.h"
#include "PinNames.h"
#include "mbed.h"
#include "run.h"

#include <algorithm>
#include <cstdint>
#include <cstdio>
#include <string>

#define WIFI_IDW0XX1    2

#if (defined(TARGET_DISCO_L475VG_IOT01A) || defined(TARGET_DISCO_F413ZH))
#include "ISM43362Interface.h"
ISM43362Interface wifi(false);

#else

#if MBED_CONF_APP_WIFI_SHIELD == WIFI_IDW0XX1
#include "SpwfSAInterface.h"
SpwfSAInterface wifi(MBED_CONF_APP_WIFI_TX, MBED_CONF_APP_WIFI_RX);
#endif // MBED_CONF_APP_WIFI_SHIELD == WIFI_IDW0XX1

#endif

static EventQueue event_queue(/* event count */ 16 * EVENTS_EVENT_SIZE);

InterruptIn button(BUTTON1);

// Thread thread;

UDPSocket socket;
Sensor _sensor(event_queue);
WIFI   _wifi(wifi, &_sensor, event_queue, &socket);

void reset() {
    event_queue.call(callback(&_sensor, &Sensor::Calibrate));
}

void enter() {
    event_queue.call(callback(&_sensor, &Sensor::button_fall));
}

int main()
{
    printf("==========================================\n");
    printf("====== Doodle Jump (STM32 and WiFi) ======\n");
    printf("==========================================\n");
    button.fall(&enter);
    event_queue.dispatch_forever();
    printf("\nDone\n");
}
