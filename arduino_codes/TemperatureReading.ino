#include "ClosedCube_HDC1080.h"
ClosedCube_HDC1080 hdc1080;
// int fanOutputPin = 13;
float readHumidity;
int fanPin = 13;

void setup()
{
  Serial.begin(115200);
  hdc1080.begin(0x40);
  // pinMode(fanPin, OUTPUT);

  // digitalWrite(13, HIGH); 
}

void loop()
{
  {
    
    Serial.print("T=");
    Serial.print(hdc1080.readTemperature());
    Serial.print("C, RH=");
    Serial.print(hdc1080.readHumidity());
    Serial.println("%");
    delay(3000);
  }


}