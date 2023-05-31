import RPi.GPIO as GPIO
import time
import sys
import Adafruit_DHT
from Adafruit_IO import MQTTClient
# import adafruit_dht
from datetime import datetime
import signal
from pigpio_dht import DHT11
import requests

GPIO.setmode(GPIO.BOARD)
GPIO.cleanup()

# Ultrasonic Distance Sensor Variables and Setup
ULTRASONIC_PIN_TRIG = 18
ULTRASONIC_PIN_ECHO = 22
Current_Ultrasonic_Distance = 0

GPIO.setup(ULTRASONIC_PIN_TRIG, GPIO.OUT)
GPIO.setup(ULTRASONIC_PIN_ECHO, GPIO.IN)

# Temperature Sensor Variables and Setup
DHT11_PIN = 16
DHT_SENSOR = Adafruit_DHT.DHT11
Current_Temperature = 25


# Buzzer Variables and Setup
BUZZER_PIN = 24
GPIO.setup(BUZZER_PIN,GPIO.OUT)


# Heated Blanket Variables and Setup
# RED LED
HEATED_BLANKET_LED = 26
GPIO.setup(HEATED_BLANKET_LED, GPIO.OUT)

# Autofeeder Variables and Setup
# YELLOW LED
AUTOFEED_LED = 32
GPIO.setup(AUTOFEED_LED, GPIO.OUT)
AUTOFEEDER_ACTIVE = 0
START_TIME = '20:00:00'
END_TIME = '20:00:03'

# Button Variables and Setup
BUTTON_PIN = 37
GPIO.setup(BUTTON_PIN, GPIO.IN, pull_up_down = GPIO.PUD_UP)
BUTTON_PRESSED = False


# Ultrasonic Distance Function - Get current distance
def get_ultrasonic_distance():
      
      GPIO.output(ULTRASONIC_PIN_TRIG, True)
      time.sleep(0.00001)
      GPIO.output(ULTRASONIC_PIN_TRIG, False)
      pulse_start_time = time.time()
      pulse_end_time = time.time()
      
      while (GPIO.input(ULTRASONIC_PIN_ECHO)) == 0:
            pulse_start_time = time.time()
      
      while (GPIO.input(ULTRASONIC_PIN_ECHO)) == 1:
            pulse_end_time = time.time()
      
      pulse_duration = pulse_end_time - pulse_start_time
      distance = (pulse_duration * 34300) / 2
      return distance



# Temperature Function - Get current temperature

def get_temperature(old_temperature):
      humidity, temperature = Adafruit_DHT.read(DHT_SENSOR, DHT11_PIN)
      if humidity is not None and temperature is not None:
            return temperature
      else:
            return old_temperature
            


# Buzzer Function - Run buzzer if variable is true

def run_buzzer(AUTOFEEDER_ACTIVE_BOOL):
      if AUTOFEEDER_ACTIVE_BOOL == 1:
            GPIO.output(BUZZER_PIN, GPIO.HIGH)
      else:
            GPIO.output(BUZZER_PIN, GPIO.LOW)


# Heated Blanket Switch LED - Close switch if distance low and temperature low
def run_heated_blanket(Current_Distance, Current_Temp):
      if (Current_Distance < 30) and (Current_Temp < 35):
            GPIO.output(HEATED_BLANKET_LED, GPIO.HIGH)
      else:
            GPIO.output(HEATED_BLANKET_LED, GPIO.LOW)

# Autofeeder Actuator LED - Close switch for 3 seconds if time equal to a set time
def run_autofeeder(start, end):
      now = datetime.now()
      current_time = now.strftime("%H:%M:%S")
      if current_time > start and current_time < end:
            GPIO.output(AUTOFEED_LED, GPIO.HIGH)
            AUTOFEEDER_ACTIVE = 1
      else:
            AUTOFEEDER_ACTIVE = 0
            GPIO.output(AUTOFEED_LED,GPIO.LOW)



## Interrupt if button pressed and run buzzer and autofeeder

def button_pressed_callback(channel):
    print("Button Pressed")
    global BUTTON_PRESSED
    BUTTON_PRESSED = True
    GPIO.output(BUZZER_PIN, GPIO.HIGH)
    GPIO.output(AUTOFEED_LED, GPIO.HIGH)
    client.publish(IO_FEED, 1, IO_FEED_USERNAME)
    requests.post('https://maker.ifttt.com/trigger/{check_cat}/json/with/key/daCDZ3r1Zc7ts0xrroi7MG')


def button_clear(button_bool):
      # print("button_clear status - " + str(button_bool))
      if button_bool == True:
            time.sleep(3)
            GPIO.output(BUZZER_PIN, GPIO.LOW)
            GPIO.output(AUTOFEED_LED, GPIO.LOW)
            global BUTTON_PRESSED
            BUTTON_PRESSED = False
            client.publish(IO_FEED, 0, IO_FEED_USERNAME)
            print("Button Clear Successful - adafruit updated")
      else:
            pass
            
      
GPIO.add_event_detect(BUTTON_PIN, GPIO.FALLING,
            callback=button_pressed_callback, bouncetime=100)


# MQTT Section 

ADAFRUIT_IO_KEY = 'aio_bmuH958RebMrWcdHmwvVrX61Gd7S'

ADAFRUIT_IO_USERNAME = 'jb_deakin'

IO_FEED = 'SIT210_MQTT_Dashboard'

IO_FEED_USERNAME = 'jb_deakin'


# Define callback functions which will be called when certain events happen.
def connected(client):
    """Connected function will be called when the client connects.
    """
    client.subscribe(IO_FEED, IO_FEED_USERNAME)

def disconnected(client):
    """Disconnected function will be called when the client disconnects.
    """
    print('Disconnected from Adafruit IO!')
    sys.exit(1)

def message(client, feed_id, payload):
    """Message function will be called when a subscribed feed has a new value.
    The feed_id parameter identifies the feed, and the payload parameter has
    the new value.
    """
    print('Feed {0} received new value: {1}'.format(feed_id, payload))


# Create an MQTT client instance.
client = MQTTClient(ADAFRUIT_IO_USERNAME, ADAFRUIT_IO_KEY)

# Setup the callback functions
client.on_connect       =   connected
client.on_disconnect    =   disconnected
client.on_message       =   message

# Connect to the Adafruit IO server.
client.connect()

client.loop_background()




# Main Loop

if __name__ == '__main__':
      try:
            client.publish(IO_FEED, 0, IO_FEED_USERNAME)
            while True:
                  button_clear(BUTTON_PRESSED)
                  Current_Ultrasonic_Distance = get_ultrasonic_distance()
                  print("Distance - " + str(Current_Ultrasonic_Distance))
                  Current_Temperature = get_temperature(Current_Temperature)
                  print("Temp - " + str(Current_Temperature))
                  run_buzzer(AUTOFEEDER_ACTIVE)
                  run_heated_blanket(Current_Ultrasonic_Distance, Current_Temperature)
                  run_autofeeder(START_TIME,END_TIME)

      # Reset by pressing CTRL + C
      except KeyboardInterrupt:
            print("Stopped by User")
            GPIO.cleanup()

