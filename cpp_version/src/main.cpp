#include "sensor.h"
#include "thermo.h"

#include<iostream>

#include<unistd.h>

#include <wiringPi.h>

int main(int argc, char *argv[]){

//   wiringPiSetupGpio();
   wiringPiSetup();

  // Thermo t1;
   //Thermo t2;
   //Thermo t3;
   //Thermo t4;
   //t1.init(23);
   //t2.init(24);
   //t3.init(25);
   //t4.init(16);
   
   //double t = t1.getData();

   //std::cout << "Temperature: " << t << std::endl;
   
   digitalWrite(27, HIGH);

   sleep(20);

   digitalWrite(27, LOW);

   //std::cout << "Hello World!" << std::endl;
   //sensor s;
   //s.do_a_thing();
   //sensor_data dat = s.getData();
   //std::cout << dat.a << ", " << dat.b << std::endl;
   return 0;
}
