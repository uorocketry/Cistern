#include "sensor.h"
#include "thermo.h"

#include<iostream>

#include<unistd.h>

#include <wiringPi.h>

int main(int argc, char *argv[]){

//  wiringPiSetupGpio();
  wiringPiSetupGpio();

   //Thermo t1;
   //Thermo t2;
   //Thermo t3;
   //Thermo t4;
   //t1.init(23);
   //t1.init(24);
   //t1.init(25);
   //t1.init(16);

   //double t = t1.getData();

   //std::cout << "Temperature: " << t << std::endl;

   digitalWrite(21, HIGH);
   
   std::cout << "Hello - just set things" << std::endl;

   sleep(30);

   digitalWrite(21, LOW);

   //std::cout << "Hello World!" << std::endl;
   //sensor s;
   //s.do_a_thing();
   //sensor_data dat = s.getData();
   //std::cout << dat.a << ", " << dat.b << std::endl;
   return 0;
}
