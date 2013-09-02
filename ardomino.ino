/////////////////////////////////////////////////////////////////////////////
// ArdOmino Sketch Test  
// Biometeorological ArdOmino Skecth to monitor Air Temperature and Relative Humidity. 
// Application Case https://github.com/alfcrisci/Ardomino presented 
// OfficinaIbimet IBIMET CNR http://www.fi.ibimet.cnr.it/
// Author: Alessandor Matese - Alfonso Crisci - OfficinaIbimet
// General scheme and function are done by Mirko Mancini in his work thesis DESIGN AND IMPLEMENTATION OF AN AMBIENT INTELLIGENCE SYSTEM BASED ON ARDUINO AND ANDROID Universita di Parma FAC. DI INGEGNERIA CORSO DI LAUREA IN INGEGNERIA INFORMATICA 
// Mirko Mancin - mirkomancin90@gmail.com  website:  www.mancio90.it forum http://forum.arduino.cc/index.php?topic=157524.0;wap2
// Library reference
// https://github.com/adafruit/DHT-sensor-library 
// https://github.com/harlequin-tech/WiFlyHQ

/////////////////////////////////////////////////////////////////////////////

// Library definition

#include <WiFlyHQ.h>
#include <SoftwareSerial.h>
#include <dht.h>


// Macro Resettig for Microcontroller 

#include <avr/io.h>
#include <avr/wdt.h> 
#define Reset_AVR() wdt_enable(WDTO_30MS); while(1) {}

// Reset every hour to prevent wifly comunication trouble

#define Reset_After_1hour 3600000    


#define Periodo_Invio_Dati 3000     // minimun range time sending interval.(ms)


// Pin defining for DHT22 sensors and variables

#define DHT22_PIN 2      // PIN defining for sensors DHT22
int k=0;// lecture sensor index
float tempsum=0,humsum=0,tempsum_htm=0,rhsum_htm=0,radsum=0;// declared variable to lead five lecture average for readTRHSensor function .
float oldt=0,oldu=0;// declared variables for readTRHSensor function .
dht DHT; // global variable declaration for sensor's class 


// WIFI SETTINGS wireless account RN 171 XV 

WiFly wifly;

const char mySSID[] = "Vodafone-26726417";
const char myPassword[] = "xa5d59ivz3dbwi3";
char MACnode[] = "00:06:66:71:d2:68";
char serverName[] = "http://149.139.8.55"; // Serve IP URL to connect 
#define serverPort 80 // port 
char* macStr;
const char site_time[] = "hunt.net.nz";

SoftwareSerial wifi(8,9);

// Writing procedure
void print_P(const prog_char *str);
void println_P(const prog_char *str);

//SENSOR SETTINGS
float temp_air= 0.0; //sensor 1
float rh_air= 0.0; //sensor 2

unsigned long time = 0;
unsigned long SendTime = 0;;

char rh_airBuffer[8];    
char temp_airBuffer[8];    
char timestamp[8];

// buffer to save for json string
char jsonMsgHead[128];
char jsonMsgBody[128];

void setup(){
  Serial.begin(9600);
  Serial.println(" --- ARDOMINO MONITORING --- ");
  delay(1000);
  Serial.println("Ardomino  started, End Setup !");
  randomSeed(analogRead(A2)); 
}


void loop(){
    time = millis(); 	
    configWIFI();
    SendTime = millis();
    // light_accum = readLightSensor();
    readTRHSensor();
    temp_air= tempsum;
    rh_air= humsum;          
    // value to string conversion
    dtostrf(temp_air, 5, 2, temp_airBuffer);
    dtostrf(rh_air, 5, 2, rh_airBuffer);
    
    // define a fake time 
    sprintf(timestamp, "%d", random(1, 32000));    
       
    // Create json strings for HTTP POST 
    Serial.println("Create  JSON strings");
    sprintf(jsonMsgHead,"{\"timestamp\":%s,\"checksum\":\"%s\",\"mac\":\"%s\"\0", timestamp, "5EB63BBBE01EEED093CB22BB8F5ACDC3", MACnode);
    sprintf(jsonMsgBody,",\"AOnode_ID\":%s,\"AOnode_battery\":%s,\"hrel\":%s,\"tair\":%s}\0","FirenzeDuomo","valbatt", rh_airBuffer, temp_airBuffer);
    
    // JSON string length assessement to make HTTP POST 
    int i; 
    for(i=0; jsonMsgHead[i]!=0; i++); i++;
    for(int j=0;jsonMsgBody[j]!=0; j++, i++);
    
    Serial.println("Send sensors readings....");             
    InvioWIFIHttp(jsonMsgHead,jsonMsgBody, i);            
    Serial.println("Sensors Readings Sent!.");            
    
    Reset_AVR();                             
}

// Reading Sensor procedure

void readTRHSensor(){

//  DHT22 Air temperature humidity

int chk = DHT.read22(DHT22_PIN);// read from sensors of temperature and umidity

switch (chk)//check
{
case 0: //return value : 0 -> Reading gone fine.

if ((DHT.temperature-oldt)>100){
	tempsum=tempsum+oldt;} else {
	tempsum=tempsum+DHT.temperature;
	oldt=DHT.temperature;
  }// writing on serial port value in %f3.1 format
  
humsum=DHT.humidity+humsum;
Serial.println(DHT.temperature,1);
Serial.println(DHT.humidity,1);

oldu=DHT.humidity;// writing humidity data

break;
case -1: //valore di ritorno : -1 -> Data read but corrupted
Serial.print("Checksum error");
tempsum=tempsum+oldt;//write temperature data
humsum=oldu+humsum;

break;
case -2: //valore di ritorno : -2 -> Time limit overload no reading.
Serial.print("Time out error");
tempsum=tempsum+oldt;//write temperature data
humsum=oldu+humsum;
break;
default: // Other error class done by value.
Serial.print("Unknown error");
tempsum=tempsum+oldt;////write temperature data
humsum=oldu+humsum;
break;
} 
    tempsum=tempsum/5;
    humsum=humsum/5;    
}



// Wireless configuration and restart in error with next reset. 
// Function Author: Mirko Mancini 


int configWIFI(){
    println_P(PSTR("Starting"));
    print_P(PSTR("Free memory: "));
    Serial.println(wifly.getFreeMemory(),DEC);

    wifi.begin(9600);    // define baud rate of Serial ArdOmino port
    if (!wifly.begin(&wifi, &Serial)) {
        println_P(PSTR("Failed to start wifly"));
	Reset_AVR();
    }

    char buf[32];
    /* Join wifi network if not already associated */
    if (!wifly.isAssociated()) {
	/* Setup the WiFly to connect to a wifi network */
	println_P(PSTR("Joining network"));
	wifly.setSSID(mySSID);
	//wifly.setPassphrase(myPassword);
        wifly.setKey(myPassword);
	wifly.enableDHCP();

	if (wifly.join()) {
	    println_P(PSTR("Joined wifi network"));
	} else {
	    println_P(PSTR("Failed to join wifi network"));
	    Reset_AVR();
	}
    } else {
        println_P(PSTR("Already joined network"));
    }

    print_P(PSTR("MAC: "));
    macStr = (char *)(wifly.getMAC(buf, sizeof(buf)));
    Serial.println(macStr);
    print_P(PSTR("IP: "));
    Serial.println(wifly.getIP(buf, sizeof(buf)));
    print_P(PSTR("Netmask: "));
    Serial.println(wifly.getNetmask(buf, sizeof(buf)));
    print_P(PSTR("Gateway: "));
    Serial.println(wifly.getGateway(buf, sizeof(buf)));
    print_P(PSTR("SSID: "));
    Serial.println(wifly.getSSID(buf, sizeof(buf)));

    wifly.setDeviceID("Wifly-WebClient");
    print_P(PSTR("DeviceID: "));
    Serial.println(wifly.getDeviceID(buf, sizeof(buf)));

    if (wifly.isConnected()) {
        println_P(PSTR("Old connection active. Closing"));
	wifly.close();
    }
    
    if (wifly.open(serverName, serverPort)) {
        print_P(PSTR("Connected to "));
	Serial.println(serverName);

	Serial.println("WIFI ALREADY");
    } else {
        println_P(PSTR("Failed to connect"));
        Reset_AVR();
    }   
}

// to print variable in memory
void print_P(const prog_char *str)
{
    char ch;
    while ((ch=pgm_read_byte(str++)) != 0) {
	Serial.write(ch);
    }
}

void println_P(const prog_char *str)
{
    print_P(str);
    Serial.println();
}

// Sending Json formatted data procedure 
// Waiting server's response to send next data packet. 
// Function Author Mirko Mancini 



void InvioWIFIHttp(char* jsonStringHead,char* jsonStringBody, int lungh)
{
  Serial.println("Create POST request");
  
  wifly.print("POST /cgi-bin/ardomino_collect.py HTTP/1.0\r\n");
  wifly.print("Content-Length: ");
  wifly.print(lungh);
  wifly.print("\r\n\r\n");
  wifly.print(jsonStringHead);
  wifly.print(jsonStringBody);
  
  Serial.println("Waiting server 's response");
  //Waiting server 's response
  while(wifly.available()==0){}
  
     if(wifly.available() > 0) {
       char buf[200] = "buffer";
       int exit = 0;
       
       while(exit<2){
           wifly.gets(buf, sizeof(buf));
           Serial.println(buf);
           if(buf[0]==0){ 
             exit++; 
           }
           if(buf[0]=='{'){
             delay(50);
             long timeSend = parsingJSONString(buf, sizeof(buf));
             timeSend *= 1000;
            // Wating this value to reset microcontroller
             delay(timeSend);            
           }
       }      
    }   
}

// function for raw JSON  parsing code Author Mirko Mancini 

long parsingJSONString(char buffer[], int len){
    int k;
    unsigned long m;
    
    for(int i=0; i<len; i++){
      if((buffer[i]=='"')&&(buffer[i+1]=='c')&&(buffer[i+2]=='f')&&(buffer[i+3]=='g')&&(buffer[i+4]=='"')){
        for(k=i+23; buffer[k]!='"'; k++){
          Serial.print(buffer[k]);          
        }
        unsigned long value=0;
        Serial.println();
        
        for(int l=k-1, m=1; l>i+22; l--){
          value += m*((int)buffer[l]-48);
          m *= 10;
        }
        
        return value;
      }
    }
    
    return 0;
}
