#include <Adafruit_MAX31855.h>
#include <SPI.h>

// Example creating a thermocouple instance with software SPI on any three
// digital IO pins.
#define MAXDO   3
#define MAXCS   4
#define MAXCLK  5

// Initialize the Thermocouple
Adafruit_MAX31855 thermocouple(MAXCLK, MAXCS, MAXDO);

void setup() {
  // put your setup code here, to run once:
  
  Serial.begin(9600);

  while (!Serial) delay(1); // wait for Serial on Leonardo/Zero, etc

  //Serial.println("MAX31855 test");
  // wait for MAX chip to stabilize
  delay(500);
}

void loop() {
  // put your main code here, to run repeatedly:
  //Serial.print("Internal Temp = ");
  //Serial.println(thermocouple.readInternal());

  double c = thermocouple.readCelsius();
  if (isnan(c)) {
    //Serial.println("Something wrong with thermocouple!");
  } else {
    //Serial.print("C = "); 
    Serial.println(c);
  }
  //Serial.print("F = ");
  //Serial.println(thermocouple.readFarenheit());
 
  //delay(1000);
}
