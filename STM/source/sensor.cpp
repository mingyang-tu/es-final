#include "sensor.h"
#include <cstdio>

#define TimeStep            (float)SAMPLE_RATE / 1000
#define SAMPLE_RATE         2
#define SAMPLE_PERIOD       2ms
#define Rotation_threshold  1
#define SCALE_MULTIPLIER    0.004

Sensor::Sensor(events::EventQueue &event_queue)
   :_event_queue(event_queue)
{
    BSP_ACCELERO_Init();    
    BSP_GYRO_Init();
    Calibrate();
    _event_queue.call_every(SAMPLE_RATE, this, &Sensor::update);
}

void Sensor::Calibrate(){
    printf("Calibrating Sensors.....\n");
    int n = 0;
    for(int i = 0; i < 3; ++i){
        _AccOffset[i] = 0;
        _GyroOffset[i] = 0;
    }
    while(n < 2000){
        BSP_ACCELERO_AccGetXYZ(_pAccDataXYZ);
        BSP_GYRO_GetXYZ(_pGyroDataXYZ);
        for(int i = 0; i < 3; ++i){
            _AccOffset[i] += _pAccDataXYZ[i];
            _GyroOffset[i] += _pGyroDataXYZ[i];
        }
        ThisThread::sleep_for(SAMPLE_PERIOD);
        ++n;
    }
    for(int i = 0; i < 3; ++i){
        _AccOffset[i] /= n;
        _GyroOffset[i] /= n;
    }
    for (int i = 0; i < 3; ++i){
        printf("%d ", _AccOffset[i]);
        printf("%f ", _GyroOffset[i]);
    }
    printf("Done calibration\n");
}

void Sensor::button_fall(){
    button_state=1;
}

void Sensor::update(){
    BSP_GYRO_GetXYZ(_pGyroDataXYZ);
    rotation_distance += ((_pGyroDataXYZ[0] - _GyroOffset[0]) * SCALE_MULTIPLIER)*TimeStep; 
    ThisThread::sleep_for(SAMPLE_PERIOD);
}

void Sensor::check_left_right(uint8_t& right, uint8_t& left) {
    BSP_ACCELERO_AccGetXYZ(_pAccDataXYZ);
    if((_pAccDataXYZ[0] - _AccOffset[0])*SCALE_MULTIPLIER > 0.8)
        left = 1;
    if((_pAccDataXYZ[0] - _AccOffset[0])*SCALE_MULTIPLIER < -0.8)
        right = 1;
    accumulate_x = 0.8 * accumulate_x + 0.2 * _pAccDataXYZ[0];
}

void Sensor::check_shot_up_down(uint8_t& shot,uint8_t& up, uint8_t& down) {
    //printf("Rotation distance = %f", rotation_distance);
    BSP_ACCELERO_AccGetXYZ(_pAccDataXYZ);
    if((_pAccDataXYZ[1] - _AccOffset[1] )*SCALE_MULTIPLIER < -1.0)
        shot = 1;
    if((_pAccDataXYZ[1] - _AccOffset[1] )*SCALE_MULTIPLIER > 4.0){
        if(edge==0){
            up = 1;
            edge=1;
        }
    }
    else if((_pAccDataXYZ[1] - _AccOffset[1] )*SCALE_MULTIPLIER < -4.0){
        if(edge==0){
            down = 1;
            edge=1;
        }
    }
    else
        edge=0;
    //accumulate_y = 0.9 * accumulate_y + 0.1 * _pAccDataXYZ[1];
}

void Sensor::check_button_fall(uint8_t& enter) {
    if(button_state==1){
        enter=1;
        button_state=0;
    }
    else enter=0;
}

void Sensor::getAction(uint8_t& right, uint8_t& left, uint8_t& shot, uint8_t& enter,uint8_t& up, uint8_t& down){
    check_left_right(right, left);
    check_shot_up_down(shot,up,down);
    check_button_fall(enter);
}
