/////////////////////////////////////////////////////////////////////////////
//
// Arduino Sketch for the Ardomino Project.
//
// NOTE: This is an experimental "new version" that communicates
//       plain text lines over a TCP socket.
//       To be merged with the original sketch in alfcrisci/ardomino.
//
// Biometeorological ArdOmino Skecth to monitor Air Temperature and Relative Humidity.
//
// Application Case https://github.com/alfcrisci/Ardomino presented
// OfficinaIbimet IBIMET CNR http://www.fi.ibimet.cnr.it/
//
// Author:  Alfonso Crisci - Alessandro Matese -  Mirko Mancin
//
///////////////////////////////////////////////////////////////////////////////

#include "math.h"               // include the Math Library
#include "settings.h"  // See the README file for more information
#include "minbiometeo.h"  // Biometeorological functions

const int MAX_CONNECTION_TIME = 30000; // In milliseconds

String sendGET;
char msget[136];

/**
 * Define variables used.
 */

const char myAO_ID[] = "Firenze_PiazzaDuomo";
float sval_humidity, sval_temperature,voltage;
int reading;
char AO_S1_Buffer[8];    
char AO_S2_Buffer[8];
char AO_Volt_Buffer[8];
char AO_rsii_Buffer[8];

// uint32_t connectTime = 0;

/**
 * Define Server paraemeters from settings.h
 */

const char mySSID[] = WIFI_SSID;
const char myPassword[] = WIFI_PASSWORD;
const char site[] = SERVER_ADDR;
const int site_port = SERVER_PORT;



/**
 * Macro Resettig for Microcontroller 
 */

#include <avr/io.h>
#include <avr/wdt.h> 
#define Reset_AVR() wdt_enable(WDTO_30MS); while(1) {}

// Reset every hour to prevent wifly comunication trouble

#define Reset_After_1hour 3600000    

/**
 * Communication with the DHT 
 */

#include "DHT.h"
#define DHTPIN 4
#define DHTTYPE DHT22

DHT dht; // global variable declaration for sensor's class


/**
 * Wifi communication (via WiFly module)
 */
 
#include <WiFlyHQ.h>
#include <SoftwareSerial.h>

SoftwareSerial wifiSerial(2,3);
WiFly wifly;



//////////////////////////////////////////////////////////////
// Free Memory 
// http://neophob.com/2012/09/arduino-free-memory/
//////////////////////////////////////////////////////////////

int freeRam() {
  int byteCounter = 0; // initialize a counter
  byte *byteArray; // create a pointer to a byte array
 
  // use the malloc function to repeatedly attempt allocating a certain number of bytes to memory
  // More on malloc here: http://en.wikipedia.org/wiki/Malloc
  while ( (byteArray = (byte*) malloc (byteCounter * sizeof(byte))) != NULL ) {
    byteCounter++; // if allocation was successful, then up the count for the next try
    free(byteArray); // free memory after allocating it
  }
 
  free(byteArray); // also free memory after the function finishes
  return byteCounter; // send back the highest number of bytes successfully allocated
}


//////////////////////////////////////////////////////////////
// Setup connection
//////////////////////////////////////////////////////////////


void setup_wifly() {
    char buf[32];

    showString(PSTR("WiFly Module initialization\n"));
    showString(PSTR("    Free memory: "));
    Serial.println(wifly.getFreeMemory(),DEC);

    wifiSerial.begin(9600);
    if (!wifly.begin(&wifiSerial, &Serial)) {
        showString(PSTR("    ERROR: Failed to start wifly\n"));
	terminal();
    }

    /* Join wifi network if not already associated */
	
    if (!wifly.isAssociated()) {
	
	/* Setup the WiFly to connect to a wifi network */
	
	showString(PSTR("    INFO: Joining network\n"));
	wifly.setSSID(mySSID);
	wifly.setPassphrase(myPassword);
	wifly.enableDHCP();
	   
	if (wifly.join()) {
	    showString(PSTR("    INFO: Joined wifi network\n"));
	} else {
	    showString(PSTR("    ERROR: Failed to join wifi network\n"));
	    terminal();
	}
    } else {
        showString(PSTR("    INFO: Already joined network\n"));
    }

    //terminal();

    showString(PSTR("    MAC: "));
    Serial.println(wifly.getMAC(buf, sizeof(buf)));
    showString(PSTR("    IP: "));
   Serial.println(wifly.getIP(buf, sizeof(buf)));
    showString(PSTR("    Netmask: "));
    Serial.println(wifly.getNetmask(buf, sizeof(buf)));
    showString(PSTR("    Gateway: "));
    Serial.println(wifly.getGateway(buf, sizeof(buf)));
    wifly.setDeviceID("Wifly-WebClient");
    showString(PSTR("    DeviceID: "));
    Serial.println(wifly.getDeviceID(buf, sizeof(buf)));
    
    if (wifly.isConnected()) {
        showString(PSTR("    INFO: Old connection active. Closing\n"));
	wifly.close();
    }
	
    
}



//////////////////////////////////////////////////////////////
// Connect the WiFly serial to the serial monitor.
//////////////////////////////////////////////////////////////

void terminal() {
  showString(PSTR("Opening WiFly <-> Serial communication..\n"));
    while (1) {
	if (wifly.available() > 0) {
	    Serial.write(wifly.read());
	}
	if (Serial.available() > 0) {
	    wifly.write(Serial.read());
	}
    }
}





void loop_read() {
  delay(dht.getMinimumSamplingPeriod());
  sval_humidity = dht.getHumidity();
  sval_temperature = dht.getTemperature();
  reading = analogRead(0);
   // converting that reading to voltage, for 3.3v arduino use 3.3
  voltage = reading * 5.0; //5 is the resistenze factor
  voltage /= 1024.0; 
   if (isnan(sval_humidity) || isnan(sval_temperature)) {
    showString(PSTR("ERROR: Failed reading values from DHT\n"));
  }
  else {
       
     
    // value to string conversion
	   
      
       
       dtostrf(sval_temperature, 4, 2, AO_S1_Buffer);
       dtostrf(sval_humidity, 4, 2, AO_S2_Buffer);
       dtostrf(voltage, 4, 2, AO_Volt_Buffer);
       
       sprintf(msget,"GET /cgi-bin/biomino_update.py?ID=%s&tmp=%s&rh=%s&tmrt=-99.9&vv=-99.9&vdir=-99.9&vbatt=%s&login=basic HTTP/1.0",
       myAO_ID,
       AO_S1_Buffer,
       AO_S2_Buffer,
       AO_Volt_Buffer);   
       
       //Serial.println(msget);
    
       sendGET=String(msget);
       
       
	
  }
}


void InvioHttp()
{   // Try to make a HTTP request..
   
    if (wifly.open(site, site_port)) {
        showString(PSTR("    INFO: Connected to "));
	   Serial.println(site);
	} else {
        showString(PSTR("    ERROR: Failed to connection to server\n"));
    }
    int freeMemory = wifly.getFreeMemory();
    freeRam();
    showString(PSTR(" INFO: WiFly: Sending sensors data\n"));
    Serial.println(sendGET);
      	
    /* Send the request */
              wifly.println(sendGET);
              wifly.println();
              
              Serial.println(F("Waiting server 's response"));
   // Loop for reading response
   
   while(wifly.available()==0){}
 
   if (wifly.available() > 0) {
	char ch = wifly.read();
	Serial.write(ch);
	if (ch == '\n') {
	    /* add a carriage return */ 
	    Serial.write('\r');
	}
    }

    if (Serial.available() > 0) {
	wifly.write(Serial.read());
    }
}

// Standard setup/loop functions
//------------------------------------------------------------

void setup() {
  Serial.begin(115200);
  showString(PSTR("--- Ardomino Serial Console ---\n"));
  setup_wifly();
  dht.setup(4); // data pin 4
  showString(PSTR("*** Ardomino Initialization done!\n"));
  delay(5000); 
}


void loop() {
  
      loop_read();
      InvioHttp();
      delay(300000);
      Reset_AVR();
}


 
    
