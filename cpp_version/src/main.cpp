#include "sensor.h"
#include<iostream>


int main(int argc, char *argv[]){
   std::cout << "Hello World!" << std::endl;
   sensor s;
   s.do_a_thing();
   sensor_data dat = s.getData();
   std::cout << dat.a << ", " << dat.b << std::endl;
   return 0;
}
