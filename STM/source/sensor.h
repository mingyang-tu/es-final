#include "mbed.h"
#include "stm32l475e_iot01.h"
#include "stm32l475e_iot01_accelero.h"
#include "stm32l475e_iot01_gyro.h"

class Sensor{

public:
    Sensor(events::EventQueue &event_queue);

    void Calibrate();
    
    void button_fall();

    void update();

    void check_left_right(uint8_t& right, uint8_t& left);

    void check_shot_up_down(uint8_t& shot,uint8_t& up, uint8_t& down);

    void check_jump(uint8_t& jump);

    void check_button_fall(uint8_t& enter);

    void getAction(uint8_t& right, uint8_t& left, uint8_t& shot,uint8_t& enter,uint8_t& up,uint8_t& down);

private:
    events::EventQueue  &_event_queue;
    int16_t             _pAccDataXYZ[3] = {0};
    float               _pGyroDataXYZ[3] = {0};

    float               rotation_distance = 0;
    int                 accumulate_y = 0;
    int                 accumulate_x = 0;
    //int8_t            _hit = 0;
    //int8_t            check = 0;
    int                 _AccOffset[3] = {};
    float               _GyroOffset[3] = {};

    bool                button_state=0;
    bool                edge;
};