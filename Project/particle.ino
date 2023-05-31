// This #include statement was automatically added by the Particle IDE.
#include <Adafruit_MQTT.h>
#include "Adafruit_MQTT/Adafruit_MQTT.h" 
#include "Adafruit_MQTT/Adafruit_MQTT_SPARK.h" 
#include "Adafruit_MQTT/Adafruit_MQTT.h" 


// This #include statement was automatically added by the Particle IDE.
// #include <MQTT.h>

// This #include statement was automatically added by the Particle IDE.
#include <Adafruit_IO_Particle.h>
#include "Adafruit_IO_Client.h"


// This #include statement was automatically added by the Particle IDE.
#include <Adafruit_DHT.h>


// DHT Setup
#define DHTPIN 2
#define DHTTYPE DHT11

DHT dht(DHTPIN, DHTTYPE);

float current_temp = 0.0;

// Weight Sensor Setup
#define FORCE_SENSOR_PIN A3 

int current_weight = 0;

// Heated Blanket LED Setup (Green)
const int blanketPin = D4;

// Unpleasant Buzzer LED Setup (Blue)
const int buzzerPin = D3;
int autofeeder_status = 0;

// MQTT Setup

#define AIO_SERVER      "io.adafruit.com" 
#define AIO_SERVERPORT  1883                   
#define AIO_USERNAME    "jb_deakin" 
#define AIO_KEY         "aio_bmuH958RebMrWcdHmwvVrX61Gd7S" 
#define AIO_FEED "jb_deakin.SIT210_MQTT_Dashboard"

TCPClient client;   // TCP Client used by Adafruit IO library
 
// Create the AIO client object
Adafruit_IO_Client  AIOClient = Adafruit_IO_Client(client, AIO_KEY);

Adafruit_IO_Feed    testFeed = AIOClient.getFeed(AIO_FEED);


void setup() 
{
    dht.begin();
    pinMode(buzzerPin, OUTPUT);
    pinMode(blanketPin, OUTPUT);
    // Start the Adafruit IO Client
    AIOClient.begin();
    
    // Start a serial port connection
    Serial.begin(9600);
}



// Main

void loop() {
    
    delay(2000); // Poll once every 2 seconds
    float temp_C = dht.getTempCelcius();
    
    if (!(isnan(temp_C)))
        current_temp = temp_C;
    }
    
    Particle.publish("current_temp", String(current_temp));
    
    current_weight = analogRead(FORCE_SENSOR_PIN);
    Particle.publish("current_weight", String(current_weight));
    
    
    if (current_weight > 500 && current_temp < 30){
        // Turn on green led for blanket
        digitalWrite(blanketPin, HIGH);
    } else{
        digitalWrite(blanketPin, LOW);
    }
    
    // Buzzer if autofeeder status is true and weight high
    
    time32_t now();
    
    // if some multiple of 4PM 
    if (((2158934400 - (int)Time.now()) % 86400) == 0){
        autofeeder_status = 1;
    } else {
        autofeeder_status = 0;
    }
    
    if (current_weight > 500 && autofeeder_status == 1){
        digitalWrite(buzzerPin, HIGH);
    } else{
        digitalWrite(buzzerPin, LOW);
    }
    
    // Test LEDs
    //digitalWrite(blanketPin, HIGH);
    //digitalWrite(buzzerPin, HIGH);

    
    // MQTT Feed section
    FeedData latest = testFeed.receive();
    // Particle.publish("Button State", String(latest));
    
    if(latest.isValid())
    {
        Particle.publish("Button State", String(latest));
        if (String(latest) == "1"){
            digitalWrite(buzzerPin, HIGH);
            delay(5000); // Delay 5 seconds
            digitalWrite(buzzerPin, LOW);
        }
    }
    else
    {
        Particle.publish("Button State", "Failed to Read");
    }
    
 } 

    
