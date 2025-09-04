#include <stdio.h>
#include "pico/stdlib.h"
#include "hardware/gpio.h"

int main() {
    stdio_init_all();

    const uint PIN = 1;             // GP2 (physical pin 4)
    gpio_init(PIN);
    gpio_set_dir(PIN, GPIO_OUT);

    while (true) {
        gpio_put(PIN, 1);           // ON
        sleep_ms(3000);
        gpio_put(PIN, 0);           // OFF
        sleep_ms(3000);
    }
}
