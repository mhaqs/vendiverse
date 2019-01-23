#include <SoftwareSerial9.h>

SoftwareSerial9 rx(8,9, false);
SoftwareSerial9 tx(6,7, true);

uint16_t timeoutCounter = 0;

int scoin = 0;
uint16_t mdbRead(){
  uint16_t resp = rx.read();
  resp = resp << 7;
  resp = resp >> 7;
  // Serial.print(resp, BIN);
  // Serial.print(" - ");
  // Serial.println(resp, HEX);
  timeoutCounter = 0;
  return resp;
}

uint16_t COIN_TL100 = 0;
uint16_t COIN_TL25 = 0;
uint16_t COIN_TL50 = 0;

uint16_t COIN_TL100_COUNT = 0;
uint16_t COIN_TL25_COUNT = 0;
uint16_t COIN_TL50_COUNT = 0;

uint8_t dispenseState = 0;

uint16_t mdbPeek(){
  uint16_t resp = rx.peek();
  resp = resp << 7;
  resp = resp >> 7;
  return resp;
}

int mdbAvailable(){
  return rx.available();
}

void mdbWrite(uint16_t data){
  tx.write9(data);
}

// global state variable
unsigned int coinstate;

// structure for storing the coin changer info
struct COIN_INFO {
    byte feature_level;
    unsigned int country_code;
    byte scaling_factor;
    byte decimal_places;
    byte type_routing;
    byte type_credit[16];
}; 

// struct for storing the tube status
struct TUBE_STATUS {
    unsigned int full_status;
    byte status[16];
};

COIN_INFO coin_info = 
    {0,0,0,0,0,{0,0,0,0,0,0,0,0,0,0,0,0,0,0,0}};

TUBE_STATUS tube_status = 
    {0,{0,0,0,0,0,0,0,0,0,0,0,0,0,0,0}};

void setup() {

    Serial.begin(9600);
    rx.begin(9600);
    tx.begin(9600);

    rx.listen();

    coinstate = 0;

    delay(2000);

    Serial.println("START");

}

boolean started = false;
uint8_t coinScaling = 5;
uint8_t decimalPlaces = 2;

void loop() {
  
  while( ! started ){
    delay(1000);
    if ( Serial.available()){
      char c = Serial.read();
      if ( c == '-' ){
        started = true;
      }
    }
  }
  
  

    // run the statemachine
    statemachine();

    // everytime we wait we can do funny stuff here in the meantime :-)
    // but make sure it takes not longer then 100ms, because we have to poll the
    // coin acceptor every 100ms at least!
    do_funny_stuff();

}

unsigned int calculate_checksum(unsigned int data[], unsigned int n) {

    unsigned int checksum = 0x000;

    // sum up all bytes except the last one (thats the checksum!)
    for(int i=0; i < n-1; i++) {
        checksum += data[i];
    }

    // cut off the bits higher than 8 using a simple binary &
    checksum &= 0x0FF;

    // check the calculation against the checksum
    return checksum;
}

bool validate_checksum(unsigned int data[], unsigned int n) {

    unsigned int checksum = calculate_checksum(data, n);

    // check the calculation against the checksum
    return (checksum == (data[n-1] & 0x0FF));
}

void do_funny_stuff() {

}

int errorCounter = 0;

String serialCommand = "";

// A simple statemachine for the coinchanger
void statemachine() {

    unsigned int reply[40];
    unsigned int data[40];

    uint8_t peeked;

    while ( Serial.available()){
      char c = (char)Serial.read();
      Serial.print(c);
      serialCommand = serialCommand + c;
      if ( c == '-' ){
        break;
      }
    }
    
    // This will print the coinstate and then wait 10ms to avoid the buffers to be flooded
    // Serial.print("State ");
    // Serial.println(coinstate, DEC);
    delay(10);
    timeoutCounter ++;
    if ( timeoutCounter > 100){
      timeoutCounter = 0;
      coinstate = 0;
    }
            
    switch(coinstate) {
        // We have just powered up
        case 0:
            mdbWrite(0x108);
            mdbWrite(0x008);
            coinstate++;
        break;
        // we have already sent the reset command
        case 1:
            // wait for an answer
            if(mdbAvailable() < 1) {
                return;
            }
            if(mdbRead() == 0x100) {
                // ACK received go ahead in the statemachine
                coinstate ++;
            } else {
                // No ACK received, start again from the beginning
                coinstate = 0;
                errorCounter ++;

                if ( errorCounter > 100 ){
                  while (true){
                    Serial.println("C.MAXERROR");
                    delay(5000);
                  }
                }
            }
        break;
        // Poll the coin changer
        case 2:
            mdbWrite(0x10B);
            mdbWrite(0x00B);
            coinstate++;
        break;
        // Wait for the JUST RESET to be received
        case 3:
            // Check if the received byte is just an ACK
            // read and discard it if so
            if(mdbPeek() == 0x100) {
                mdbRead();
                coinstate = 2;
                delay(50);
                return;
            }

            // If the first byte is no ACK, wait for 2 bytes to be received
            if(mdbAvailable() < 2) {
                return;
            }
            // read the 2 bytes and verify it is the JUST RESET
            for(int i = 0; i < 2; i++) {
                reply[i] = mdbRead();
            }

            if(reply[0] == 0x000 && reply[1] == 0x100) {
                // JUST RESET received, send ACk and go ahead
                Serial.println("C.START");
                mdbWrite(0x100);
                coinstate++;
            } else if(reply[0] == 0x00B && reply[1] == 0x10B) {
                // STATUS received, send ACk and go ahead
                Serial.println("C.START");
                mdbWrite(0x100);
                coinstate++;
            } else {
                // something else received send RET
                mdbWrite(0x0AA);
            }
        
        break;
        // send the SETUP command
        case 4:
            mdbWrite(0x109);
            mdbWrite(0x009);
            coinstate++;
        break;
        // wait for the answer
        case 5:
            // Wait for 24 bytes to be received
            // Serial.println(mdbAvailable(), DEC);
            if(mdbAvailable() < 24) {
                return;
            }
            
            // read the replied 23 databytes + checksum
            for(int i = 0; i < 24; i++){
                reply[i] = mdbRead();
            }

            
            // validate the checksum
            if(validate_checksum(reply, 24)) {
                // checksum oki send ACK, go ahead
                mdbWrite(0x100);
                coinstate++;

                // Changer MDB Level
                Serial.print("C.L:");
                Serial.println(reply[0], DEC);

                // Country code
                if ( bitRead(reply[1], 7)){
                  Serial.print("C.CC:");
                  uint16_t countryCode = reply[1];
                  countryCode <<= 8;
                  countryCode |= reply[2];
                  Serial.println(countryCode, DEC);
                // Country phone code
                } else {
                  Serial.print("C.PC:");
                  uint16_t countryCode = reply[1];
                  countryCode <<= 8;
                  countryCode |= reply[2];
                  Serial.println(countryCode, DEC);
                }

                // Coin scaling (Generally 5 )
                Serial.print("C.CS:" );
                coinScaling = reply[3];
                Serial.println(coinScaling, DEC);

                // Decimal places (Generally 2)
                Serial.print("C.DP:" );
                decimalPlaces = reply[4];
                Serial.println(decimalPlaces, DEC);

                // Coin types
                {
                  uint16_t coinTypes = reply[5];
                  coinTypes <<= 8;
                  coinTypes |= reply[6];
                  for ( int k = 0; k < 16; k ++ ){
                    if ( bitRead(coinTypes, k)){
                      Serial.print("C.R:");
                      Serial.println(k, DEC);
                    }
                  }
                }
    
                {
                  for ( int k = 7; k < 23; k ++ ){
                    if ( reply[k] > 0x00 ){
                      uint16_t coinValue = reply[k] * coinScaling;
                      /*
                      Serial.print(k-7, DEC);
                      Serial.print(" : ");
                      Serial.println(coinValue);
                      */
                      if ( coinValue == 100 ){
                        COIN_TL100 = k - 7;
                      } else if ( coinValue == 50 ){
                        COIN_TL50 = k - 7;
                      } else if ( coinValue == 25 ){
                        COIN_TL25 = k - 7;
                      }
                    }
                  }
                }
            } else {
                // checksum incorrect, send RET
                Serial.println("ERROR:1");
                mdbWrite(0x0AA);
            }
        break;
        // store device info
        case 6:
            coin_info.feature_level     = reply[0];
            coin_info.country_code      = (reply[1] << 8 | reply[2]);
            coin_info.scaling_factor    = reply[3];
            coin_info.decimal_places    = reply[4];
            coin_info.type_routing      = (reply[5] << 8 | reply[6]);
            for(int i = 0; i < 16; i++) {
                coin_info.type_credit[i] = reply[i+7];
            }
            coinstate++;
        break;
        // send TUBE STATUS command
        case 7:
            mdbWrite(0x10A);
            mdbWrite(0x00A);
            coinstate++;
        break;
        // wait for the answer 
        case 8:
            // Wait for 19 bytes to be received
            // Serial.println(mdbAvailable(), DEC);
            if(mdbAvailable() < 19) {
                return;
            }
            // read the replied 18 databytes + checksum
            for(int i = 0; i < 19; i++){
                reply[i] = mdbRead();
            }
            // validate the checksum
            if(validate_checksum(reply, 19)) {
                // checksum ok send ACK, go ahead
                mdbWrite(0x000);
                coinstate++;

                uint16_t tubeFull = reply[0];
                tubeFull <<= 8;
                tubeFull |= reply[1];

                for ( int k = 0; k < 16; k ++ ){
                  if ( bitRead(tubeFull, k)){
                    if ( k == COIN_TL100 ){
                      COIN_TL100_COUNT = -1;
                    } else if ( k == COIN_TL50 ){
                      COIN_TL50_COUNT = -1;
                    } else if ( k == COIN_TL25 ){
                      COIN_TL25_COUNT = -1;
                    }

                    if ( dispenseState == 0 ){
                      Serial.print("C.TF:");
                      Serial.println(k, DEC);
                    }
                  }
                }

                for ( int k = 2; k < 18; k ++ ){
                  // Serial.println(reply[k], BIN);
                  if ( reply[k] > 0x00 ){
                    if ( (k-2) == COIN_TL100){
                      if ( dispenseState == 0 ){
                        Serial.print("C.TC:100:");
                        Serial.println(reply[k], DEC);
                      }
                      COIN_TL100_COUNT = reply[k];
                    } else if ( (k-2) == COIN_TL50){
                      if ( dispenseState == 0 ){
                        Serial.print("C.TC:050:");
                        Serial.println(reply[k], DEC);
                      }
                      COIN_TL50_COUNT = reply[k];
                    } else if ( (k-2) == COIN_TL25){
                      if ( dispenseState == 0 ){
                        Serial.print("C.TC:025:");
                        Serial.println(reply[k], DEC);
                      }
                      COIN_TL25_COUNT = reply[k];
                    }
                  }
                }

                if ( dispenseState == 3 ){
                  coinstate = 12;
                  // coinstate = 0;
                  dispenseState = 0;
                }
                
            } else {
                // checksum incorrect, send RET
                Serial.println("ERROR:1");
                mdbWrite(0x0AA);
            }
        break;
        // store tube status info
        case 9:
            tube_status.full_status = (reply[0] << 8 | reply[1]);
            for(int i=0; i < 19; i++) {
                tube_status.status[i] = reply[i+2];
            }
            coinstate ++;
        break;
        // send coin type command    
        case 10:
            // prepare the data for the coin type command
            data[0] = 0x10C;
            data[1] = 0x00C;
            data[2] = 0x0FF;
            data[3] = 0x0FF;
            data[4] = 0x0FF;
            // calculate the necessary checksum
            data[5] = calculate_checksum(data, 6);
            for(int i = 0; i < 6; i++) {
                mdbWrite(data[i]);
            }
            coinstate++;
        break;
        // wait for the ACK of the coin changer
        case 11:
            reply[0] = mdbRead();
            if(reply[0] == 0x100) {
                // ACK received go ahead
                coinstate++;
            } else {
                // No ACK received, send the coin type command again
                Serial.println("ERROR:1");
                coinstate--;
            }
        break;
        // Now we should be able to dispense a coin
        case 12:
            Serial.println("C.READY");
            coinstate++;
        break;
        // Lets poll the coin changer no forever
        case 13:
            // COIN DISPENSE ( C.D:01:050- )
            if ( serialCommand.endsWith("-")){
              // Serial.println(serialCommand);
              if ( serialCommand.substring(0,4) == "C.D:"){
                dispenseState = 1;
                uint8_t num = serialCommand.substring(4,6).toInt();
                uint8_t coin = serialCommand.substring(7, 10).toInt();

                uint8_t cType = 0;
                if ( coin == 100 ){
                  cType = COIN_TL100;
                  COIN_TL100_COUNT -= num;
                } else if ( coin == 50){
                  cType = COIN_TL50;
                  COIN_TL50_COUNT -= num;
                } else if ( coin == 25 ){
                  cType = COIN_TL25;
                  COIN_TL25_COUNT -= num;
                }

                uint8_t dcmd = num;
                dcmd <<=4;
                dcmd |= cType;

                mdbWrite(0x10D);                  
                mdbWrite(dcmd);
                mdbWrite(dcmd + 0x0D);

                coinstate ++; 
                
                /*
                Serial.print("Dispensing ");
                Serial.print(num, DEC);
                Serial.print(" ");
                Serial.print(coin, DEC);
                */
              } else if ( serialCommand.substring(0,4) == "C.TC"){
                // uint8_t coin = serialCommand.substring(5,8).toInt();
                // uint8_t coin = serialCommand.substring(8, 11).toInt();

                // Serial.println(coin, DEC);
                

                // if ( coin == 100 ){
                  Serial.print("C.TC:100:");
                  Serial.println(COIN_TL100_COUNT, DEC);
                // } else if ( coin == 50){
                  Serial.print("C.TC:050:");
                  Serial.println(COIN_TL50_COUNT, DEC);
                // } else if ( coin == 25 ){
                  Serial.print("C.TC:025:");
                  Serial.println(COIN_TL25_COUNT, DEC);
                //}
              }

              serialCommand = "";
            } else {
              mdbWrite(0x10B);
              mdbWrite(0x00B);
              coinstate++;
            }
        break;
        case 14:
            // Check if the received byte is just an ACK
            // read and discard it if so
            peeked = mdbPeek();

            // Just ack, no activity
            if(peeked == 0x00) {
                mdbRead();
                mdbRead();

                if ( dispenseState == 1 ){
                  // Serial.println("Dispense state 1, advancing to 2");
                  dispenseState = 2;
                } else if ( dispenseState == 2 ) {
                  // Serial.println("Checking tubes...");
                  dispenseState = 3;
                  coinstate = 7;
                  return;
                } else {
                  
                }

                coinstate = 13;
                return;
            // Manuel dispense
            } else if ( bitRead(peeked, 7)){
              for ( int k = 0; k < 3 ; k++){
                data[k] = mdbRead();
              }

              mdbWrite(0x000);
              Serial.println("C.OK");
              coinstate = 13;
              return;
            // Coin deposit
            } else if ( bitRead(peeked, 6)){
              for ( int k = 0; k < 3 ; k++){
                data[k] = mdbRead();
              }

              mdbWrite(0x000);

              uint8_t coinDestination = 0;
              if ( bitRead(data[0], 4)){
                coinDestination = 1;
              }
              
              if ((data[0] & COIN_TL100) == COIN_TL100 ){
                Serial.print("C.D100.");
                Serial.println(coinDestination == 0 ? 'C' : 'T');
                COIN_TL100_COUNT += 1;
              } else if ((data[0] & COIN_TL50) == COIN_TL50 ){
                Serial.print("C.D50.");
                Serial.println(coinDestination == 0 ? 'C' : 'T');
                COIN_TL50_COUNT += 1;
              } else if ((data[0] & COIN_TL25) == COIN_TL25 ){
                Serial.print("C.D25.");
                Serial.println(coinDestination == 0 ? 'C' : 'T');
                COIN_TL25_COUNT += 1;
              } else {
                Serial.println("C.D!");
              }
              
              mdbWrite(0x000);

              coinstate = 13;
              return;
            // Status received
            } else {
              uint8_t k = 0;
              while ( mdbAvailable()){
                data[k] = mdbRead();
                k++;
              }

              // Serial.println(k, DEC);
              //Serial.print(data[0], BIN);
              //Serial.print(" - ");
              // Serial.println(data[1], BIN);

              mdbWrite(0x000);

              if ( data[0] == 0x001 && data[1] == 0x101){
                // Escrow request
                Serial.println("C.PO");
                // Dispenser paying out
              } else if (data[0] == 0x02 && data[1] == 0x102){
                
              } else {
                // Serial.print(data[0], HEX );
                // Serial.print(" -- ");
                // Serial.println(data[1], HEX );
              }

              coinstate = 13;
              return;
            }
        break;
        // Lets write the reply to the console for testing purposes
        case 15:
            for(int i = 0; i < 17; i++) {
                /*
                Serial.print("Byte ");
                Serial.print(i, DEC);
                Serial.print(" = ");
                Serial.println(reply[i]);
                */
            }
            delay(50);
            coinstate = 13;
        break;
    }

}


