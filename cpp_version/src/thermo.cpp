#include "thermo.h"
#include <wiringPi.h>
#include <wiringPiSPI.h>

#include <iostream>

uint32_t sign_extend_14_32(uint32_t x) {
    const int bits = 14;
    uint32_t m = 1u << (bits -1);
    return (x ^ m ) - m;

}

void Thermo::init(int gpioPin) {

    spiDevice = wiringPiSPISetup(0, 500000);
    enablePin = gpioPin;

    pinMode(gpioPin, INPUT);
    digitalWrite(gpioPin, HIGH);

}

double Thermo::getData() {

    std::cout << "test!" << std::endl;

    unsigned char data[4];

    digitalWrite(enablePin, LOW);
    wiringPiSPIDataRW(0, data, 4);
    digitalWrite(enablePin, HIGH);

    for(int i=0;i<4;i++){

    std::cout << (int)data[i] << ", ";

    }
    std::cout << std::endl;

    uint32_t temp;
    temp = data[0];
    temp = temp << 6 | data[1] >> 2;

    return (double) sign_extend_14_32(temp) / 4;
}

