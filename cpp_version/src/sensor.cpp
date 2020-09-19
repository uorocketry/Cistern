#include "sensor.h"
#include <iostream>

using namespace std;

void sensor::do_a_thing()
{
   cout << "Doing a thing!" << endl;
}
sensor_data sensor::getData()
{
   sensor_data d;
   d.a = 0;
   d.b = 1.0;

   return d;
}
