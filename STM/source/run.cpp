#include "run.h"
#include "NetworkInterface.h"
#include <algorithm>
#include <cstdint>
#include <cstdio>
#include <cstdlib>

#define IP_address "192.168.50.70"
#define Port_number 9876
#define SEND_INT 5ms
SocketAddress addr(IP_address, Port_number);

WIFI::WIFI(WiFiInterface &wifi, Sensor *sensor, events::EventQueue &event_queue,
           UDPSocket *socket)
    : _wifi(wifi), _sensor(sensor),
      _event_queue(event_queue), // _led1(LED1, 1), _led2(LED2, 1),
      _socket(socket) {
  connect_start();
}

void WIFI::connect_start() {
  // Thread start_blink1(callback(blink, &_led1));
  // ThisThread::sleep_for(100ms);
  // Thread start_blink2(callback(blink, &_led2));

  printf("\nConnecting to %s...\n", MBED_CONF_APP_WIFI_SSID);
  int countConnect = 0;
  int ret = _wifi.connect(MBED_CONF_APP_WIFI_SSID, MBED_CONF_APP_WIFI_PASSWORD,
                          NSAPI_SECURITY_WPA_WPA2);
  while (ret != 0 && countConnect <= 2) {
    if (countConnect == 2) {
      printf("Stop retry connection. Please check your WIFI.\n");
      break;
    }
    countConnect++;
    printf("Connection error! Connect again... try %d times \n", countConnect);
    ret = _wifi.connect(MBED_CONF_APP_WIFI_SSID, MBED_CONF_APP_WIFI_PASSWORD,
                        NSAPI_SECURITY_WPA_WPA2);
  }
  // start_blink1.terminate();
  // start_blink2.terminate();
  if (ret == 0)
    printf("CONNECTION SUCCESS\n\n");
  // printf("MAC: %s\n", _wifi.get_mac_address());
  // printf("IP: %d\n", _wifi.get_ip_address());

  nsapi_error_t response;
  response = _socket->open(&_wifi);
  if (0 != response) {
    printf("Error opening: %d\n", response);
  }
  _event_queue.call_every(SEND_INT, this, &WIFI::send_data);
  //_led2 = 1;
  //_led1 = 1;
  count_reconnect = 0;
}

WIFI::~WIFI() {
  //_led1 = 0;
  //_led2 = 0;
  _socket->close();
  _wifi.disconnect();
}

void WIFI::send_data() {
  char data[64];
  nsapi_error_t response;

  uint8_t enter = 0, up = 0;
  int8_t move = 0;
  _sensor->getAction(move, enter, up);
  int len = sprintf(data, "{\"move\":%d,\"enter\":%d,\"up\":%d}",
                    move, enter, up);
  printf("{\"move\":%d,\"enter\":%d,\"up\":%d}\n", move, enter, up);

//   int acce_x, acce_z;
//   float gyro;
//   _sensor->get_acce_gyro(acce_x, acce_z, gyro);
//   int len = sprintf(data, "{\"acce_x\":%d,\"acce_z\":%d,\"gyro\":%f}", acce_x, acce_z, gyro);
//   printf("{\"acce_x\":%d,\"acce_z\":%d,\"gyro\":%f}\n", acce_x, acce_z, gyro);

  response = _socket->sendto(addr, data, len);
  // printf("%d\n", response);
  if (0 >= response) {
    count_reconnect++;
    //_led2 = 0;
  } else {
    count_reconnect = 0;
    //_led2 = 1;
  }

  if (count_reconnect >= 20) {
    //_led1 = 0;
    _socket->close();
    _wifi.disconnect();
    connect_start();
  }
}