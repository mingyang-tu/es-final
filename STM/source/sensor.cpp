#include "sensor.h"
#include <cstdint>
#include <cstdio>
#include <cmath>

#define Rad2Deg            57.29578
#define TimeStep           0.000025
#define SAMPLE_PERIOD      2ms
#define PITCH_THRESHOLD    15
#define ROLL_DELTA         4.
#define MAX_ROLL           10

Sensor::Sensor(events::EventQueue &event_queue) : _event_queue(event_queue) {
    BSP_ACCELERO_Init();
    BSP_GYRO_Init();
    Calibrate();
}

void Sensor::Calibrate() {
    printf("Calibrating Sensors.....\n");
    int n = 2000;
    for (int i = 0; i < 3; ++i) {
        _GyroOffset[i] = 0;
    }
    for (int j = 0; j < n; ++j) {
        BSP_ACCELERO_AccGetXYZ(_pAccDataXYZ);
        BSP_GYRO_GetXYZ(_pGyroDataXYZ);
        for (int i = 0; i < 3; ++i) {
            _GyroOffset[i] += _pGyroDataXYZ[i];
        }
        _AngleOffset[0] += atan2f(_pAccDataXYZ[0], _pAccDataXYZ[2]);
        _AngleOffset[1] += atan2f(_pAccDataXYZ[1], _pAccDataXYZ[2]);
        ThisThread::sleep_for(SAMPLE_PERIOD);
    }
    for (int i = 0; i < 3; ++i) {
        _GyroOffset[i] /= (float)n;
    }
    for (int i = 0; i < 2; ++i) {
        _AngleOffset[i] /= (float)n;
        _AngleOffset[i] *= Rad2Deg;
    }
    printf("AngleOffset = (%f, %f, -)\n", _AngleOffset[0], _AngleOffset[1]);
    printf("GyroOffset = (%f, %f, %f)\n", _GyroOffset[0], _GyroOffset[1], _GyroOffset[2]);
    printf("Done calibration\n");
}

void Sensor::button_fall() { button_state = 1; }

void Sensor::check_left_right(int8_t &move) {
    BSP_ACCELERO_AccGetXYZ(_pAccDataXYZ);
    BSP_GYRO_GetXYZ(_pGyroDataXYZ);
    float ang_acc = atan2f(_pAccDataXYZ[0], _pAccDataXYZ[2]) * Rad2Deg - _AngleOffset[0];
    accumulate_x = 0.98 * (accumulate_x - (_pGyroDataXYZ[1] - _GyroOffset[1]) * TimeStep) + 0.02 * ang_acc;
    move = -int8_t(accumulate_x / ROLL_DELTA);
    if (move > MAX_ROLL) move = MAX_ROLL;
    if (move < -MAX_ROLL) move = -MAX_ROLL;
}

void Sensor::check_up(uint8_t &up) {
    BSP_ACCELERO_AccGetXYZ(_pAccDataXYZ);
    float ang_acc = atan2f(_pAccDataXYZ[1], _pAccDataXYZ[2]) * Rad2Deg - _AngleOffset[1];
    accumulate_y = 0.98 * (accumulate_y + (_pGyroDataXYZ[0] - _GyroOffset[0]) * TimeStep) + 0.02 * ang_acc;
    if (accumulate_y > PITCH_THRESHOLD)
        up = 1;
    else
        up = 0;
}

void Sensor::check_button_fall(uint8_t &enter) {
    if (button_state == 1) {
        enter = 1;
        button_state = 0;
    }
    else
        enter = 0;
}

void Sensor::get_acce_gyro(int &acce_x, int &acce_z, float &gyro) {
    BSP_ACCELERO_AccGetXYZ(_pAccDataXYZ);
    BSP_GYRO_GetXYZ(_pGyroDataXYZ);
    acce_x = _pAccDataXYZ[0];
    acce_z = _pAccDataXYZ[2];
    gyro = _pGyroDataXYZ[1] - _GyroOffset[1];
}

void Sensor::getAction(int8_t &move, uint8_t &enter, uint8_t &up) {
    check_left_right(move);
    check_up(up);
    check_button_fall(enter);
}
