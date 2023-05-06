// This #include statement was automatically added by the Particle IDE.
#include <BH1750Lib.h>

// Initialise the light sensor.
BH1750Lib lightSensor;

// Threshold value for sensor 
int light_threshold = 10000; 

// IFTTT event name
String event_light_sensor = "Light_Sensor_Triggered";

void setup(){
    
    lightSensor.begin(BH1750LIB_MODE_CONTINUOUSHIGHRES);
}

void loop() {
    // Reading for Particle events 
    int lux = lightSensor.lightLevel();
    Particle.publish("Lux Measured", String(lux), PRIVATE);
    
    // IFTTT Section
    String data = "";
    
    if (lux > light_threshold){
        data = "Light";
        // Trigger the integration
        Particle.publish(event_light_sensor, data, PRIVATE);
    } else {
        data = "Dark";
    }
    
    // Delay
    delay(600000);
}
