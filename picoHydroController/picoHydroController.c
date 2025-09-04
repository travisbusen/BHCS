#include <stdio.h>
#include "pico/stdlib.h"
#include "hardware/gpio.h"
#include "pico/time.h"

// define pump objects

typedef struct{
    absolute_time_t nextWateringTime;
    absolute_time_t pumpStopTime;
    bool running;
    uint pin;
} PumpController;

PumpController supplyPump = {0, 0, false, 1};
PumpController salvagePump = {0, 0, false, 2}; // placehoder pin number



bool growLightsOn = false;


// create functions for each peripheral

int readWaterSupplyLevel()
{
    // read the water supply level from the sensor
    // return a value between 0 and 100
    return 50; // placeholder value
}

int readWaterSalvageLevel()
{
    // read the water salvage level from the sensor
    // return a value between 0 and 100
    return 50; // placeholder value
}

void controlGrowLights(){
    // control the grow lights based on the time of day
    // placeholder function 
}

void controlSupplyPump(int waterSupplyLevel, PumpController *pump)
{

    gpio_init(pump->pin);              // initialize the GPIO pin
    gpio_set_dir(pump->pin, GPIO_OUT); // set the GPIO pin as an output

    // get time at start of function
    absolute_time_t now = get_absolute_time();

    if (!pump->running && waterSupplyLevel > 10 && now >= pump->nextWateringTime)
    {
        gpio_put(pump->pin, 1); // turn on the pump
        pump->running = true;
        pump->pumpStopTime = delayed_by_us(now, 3 * 60 * 1000000); // set the pump stop time to 3 minutes from now
        // run the pump for 3 minutes
        if (pump->running && now >= pump->pumpStopTime)
        {
            // If 3 minutes have passed, turn off the pump
            gpio_put(pump->pin, 0);
            pump->running = false; // turn off the pump
            pump->nextWateringTime = delayed_by_us(now, 3 * 60 * 60 * 1000000); // update the next watering time to 3 hours
        }
    }

    // int main() {

    //     absolute_time_t baseline_time = get_absolute_time();
    //     // stdio_init_all(); remove for debugging

    //     const uint PIN = 1;             // GP2 (physical pin 4)
    //     gpio_init(PIN);
    //     gpio_set_dir(PIN, GPIO_OUT);

    //     while (true) {
    //         gpio_put(PIN, 1);           // ON
    //         sleep_ms(3000);
    //         gpio_put(PIN, 0);           // OFF
    //         sleep_ms(3000);
    //     }
}
