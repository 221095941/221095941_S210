// This #include statement was automatically added by the Particle IDE.
#include <BH1750Lib.h>

// Initialise the light sensor.
BH1750Lib lightSensor;

// Threshold value for sensor 
int light_threshold = 10000; 

// IFTTT event name
String event_light_sensor = "Light_Sensor_Triggered";

String data = "";


void setup(){
    
    lightSensor.begin(BH1750LIB_MODE_CONTINUOUSHIGHRES);
}

void loop() {
    // Reading for Particle events 
    int lux = lightSensor.lightLevel();
    Particle.publish("Lux Measured", String(lux), PRIVATE);
    
    // IFTTT Section
    
    if (lux > light_threshold){
        if (data = "Dark"){
        data = "Light";
        Particle.publish(event_light_sensor, data, PRIVATE);
        }

    } 
    if (lux < light_threshold){
        if (data = "Light"){
            data = "Dark";
            Particle.publish(event_light_sensor, data, PRIVATE);
        }
    }
    // Delay
    delay(600000);
}
