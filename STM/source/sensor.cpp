#include "sensor.h"
#include <cstdio>

#define SAMPLE_PERIOD 2ms
#define ROTATION_THRESHOLD 285

const int LEFT_RIGHT_THRESHOLDS[] = {96, 191, 285, 376, 465, 550, 631, 707, 778};
int THRES_SIZE = sizeof(LEFT_RIGHT_THRESHOLDS) / sizeof(LEFT_RIGHT_THRESHOLDS[0]);

Sensor::Sensor(events::EventQueue &event_queue) : _event_queue(event_queue) {
  BSP_ACCELERO_Init();
  Calibrate();
}

void Sensor::Calibrate() {
  printf("Calibrating Sensors.....\n");
  int n = 2000;
  for (int i = 0; i < 3; ++i) {
    _AccOffset[i] = 0;
  }
  for (int j = 0; j < n; ++j) {
    BSP_ACCELERO_AccGetXYZ(_pAccDataXYZ);
    for (int i = 0; i < 3; ++i) {
      _AccOffset[i] += _pAccDataXYZ[i];
    }
    ThisThread::sleep_for(SAMPLE_PERIOD);
  }
  for (int i = 0; i < 3; ++i) {
    _AccOffset[i] /= n;
  }
  printf("AccOffset = (%d, %d, %d)\n", _AccOffset[0], _AccOffset[1],
         _AccOffset[2]);
  printf("Done calibration\n");
}

void Sensor::button_fall() { button_state = 1; }

void Sensor::check_left_right(int8_t &move) {
  BSP_ACCELERO_AccGetXYZ(_pAccDataXYZ);
  accumulate_x = (accumulate_x + _pAccDataXYZ[0] - _AccOffset[0]) >> 1;
  if (accumulate_x > 0) {
    for (int i = THRES_SIZE-1; i >= 0; --i) {
      if (accumulate_x > LEFT_RIGHT_THRESHOLDS[i]) {
        move = -i-1;
        break;
      }
    }
  } else if (accumulate_x < 0) {
    for (int i = THRES_SIZE-1; i >= 0; --i) {
      if (accumulate_x < -LEFT_RIGHT_THRESHOLDS[i]) {
        move = i+1;
        break;
      }
    }
  } else {
    move = 0;
  }
}

void Sensor::check_up(uint8_t &up) {
  BSP_ACCELERO_AccGetXYZ(_pAccDataXYZ);
  accumulate_y = (accumulate_y + _pAccDataXYZ[1] - _AccOffset[1]) >> 1;
  if (accumulate_y > ROTATION_THRESHOLD)
    up = 1;
  else
    up = 0;
}

void Sensor::check_button_fall(uint8_t &enter) {
  if (button_state == 1) {
    enter = 1;
    button_state = 0;
  } else
    enter = 0;
}

void Sensor::getAction(int8_t &move, uint8_t &enter, uint8_t &up) {
  check_left_right(move);
  check_up(up);
  check_button_fall(enter);
}
