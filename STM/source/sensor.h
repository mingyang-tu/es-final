#include "mbed.h"
#include "stm32l475e_iot01.h"
#include "stm32l475e_iot01_accelero.h"
#include "stm32l475e_iot01_gyro.h"

class Sensor {

public:
  Sensor(events::EventQueue &event_queue);

  void Calibrate();

  void button_fall();

  void check_left_right(int8_t &move);

  void check_up(uint8_t &up);

  void check_jump(uint8_t &jump);

  void check_button_fall(uint8_t &enter);

  void getAction(int8_t &move, uint8_t &enter, uint8_t &up);

private:
  events::EventQueue &_event_queue;
  int16_t _pAccDataXYZ[3] = {0};

  int _AccOffset[3] = {};

  int accumulate_x = 0;
  int accumulate_y = 0;

  bool button_state = 0;
};