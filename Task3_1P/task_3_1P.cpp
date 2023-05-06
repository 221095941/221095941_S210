// This #include statement was automatically added by the Particle IDE.
#include <ThingSpeak.h>

#include "Adafruit_DHT.h"
#include "Particle.h"

#define DHTPIN 6     // what pin we're connected to

#define DHTTYPE DHT11		// DHT 11 

TCPClient client;

unsigned long myChannelNumber = 2135731;		/*Thingspeak channel id*/
const char * myWriteAPIKey = "3OFNUPK70F9UTA1A"; /*Channel's write API key*/


DHT dht(DHTPIN, DHTTYPE);

int led = D7;

void setup() {
	Serial.begin(9600); 
    pinMode(led, OUTPUT);
	dht.begin();
	ThingSpeak.begin(client);

}

void loop() {
    
	digitalWrite(led, HIGH);

    // Read temperature as Celsius
	float temperature = dht.getTempCelcius();

    // Check if any reads failed and exit early (to try again).
	if (isnan(temperature)) {
		return;
	}
	
	// Avoid sensor errors (frequently goes to 255)
	if (temperature > 50.0){
	    return;
	}
	
	ThingSpeak.writeField(myChannelNumber, 2, temperature, myWriteAPIKey);
	
	digitalWrite(led, LOW);
	delay(30000);
}

