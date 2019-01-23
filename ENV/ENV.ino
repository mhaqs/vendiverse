#include <Wire.h>
#include <dht11.h>
#include <avr/wdt.h>

int pinRed = 1;
int pinGreen = 0;
int pinBlue = 2;
int pinCooler = 8;
int pinLight1 = 9;
int pinLight2 = 10;
int pinLight3 = 11;
int pinBuzzer = 12;

int pinTemp1 = 3;
int pinTemp2 = 4;

byte temp1 = 99;
byte temp2 = 99;

dht11 DHT11;

void setup() {
  wdt_disable();
  
  Wire.begin(0x11);
  Wire.onReceive(receiveEvent);
  Wire.onRequest(requestEvent);
  
  pinMode(pinRed, OUTPUT);
  pinMode(pinGreen, OUTPUT);
  pinMode(pinBlue, OUTPUT);

  pinMode(pinCooler, OUTPUT);
  pinMode(pinLight1, OUTPUT);
  pinMode(pinLight2, OUTPUT);
  pinMode(pinLight3, OUTPUT);

  pinMode(pinBuzzer, OUTPUT);

  digitalWrite(pinRed, LOW);
  digitalWrite(pinGreen, LOW);
  digitalWrite(pinBlue, LOW);

  digitalWrite(pinCooler, LOW);
  digitalWrite(pinLight1, LOW);
  digitalWrite(pinLight2, LOW);
  digitalWrite(pinLight3, LOW);

  digitalWrite(pinBuzzer, LOW);

  
}

uint16_t counter = 0;

void loop() {
  // put your main code here, to run repeatedly:

  counter ++;
  wdt_reset();
  
  if ( counter > 5000 ){
      counter = 0;
      
      DHT11.attach(pinTemp1);
      int chk1 = DHT11.read();
     
      if ( chk1 == 0 ){
        temp1 = (byte)DHT11.temperature;
      } else {
        temp1 = 100;
      }

      delay(10);

      DHT11.attach(pinTemp2);
      int chk2 = DHT11.read();
     
      if ( chk2 == 0 ){
        temp2 = (byte)DHT11.temperature;
      } else {
        temp2 = 100;
      }
  }

  delay(1);
}

void receiveEvent(int howMany){
  if ( Wire.available()){
    uint8_t c = Wire.read();
    bool cmd = bitRead(c, 7);
    c <<= 1;
    c >>= 1;

    if ( c == 0 ){
      digitalWrite(pinRed, cmd ? HIGH : LOW );
    } else if ( c == 1 ){
      digitalWrite(pinGreen, cmd ? HIGH : LOW );
    } else if ( c == 2 ){
      digitalWrite(pinBlue, cmd ? HIGH : LOW );
    } else if ( c == 3 ){
      digitalWrite(pinCooler, cmd ? HIGH : LOW );
    } else if ( c == 4 ){
      digitalWrite(pinLight1, cmd ? HIGH : LOW );
    } else if ( c == 5 ){
      digitalWrite(pinLight2, cmd ? HIGH : LOW );
    } else if ( c == 6 ){
      digitalWrite(pinLight3, cmd ? HIGH : LOW );
    } else if ( c == 7 ){
      buzz();
    }
    
  }
}

void requestEvent(){
  byte output[2];
  output[0] = temp1;
  output[1] = temp2;
  Wire.write(output, 2);
}

void buzz(){
  
}

