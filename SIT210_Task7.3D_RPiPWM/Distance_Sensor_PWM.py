import RPi.GPIO as GPIO
import time


GPIO.setmode(GPIO.BOARD)

PIN_TRIGGER = 7
PIN_ECHO = 11

LED_PIN = 12

GPIO.setup(PIN_TRIGGER, GPIO.OUT)
GPIO.setup(PIN_ECHO, GPIO.IN)

GPIO.setup(LED_PIN, GPIO.OUT)

global pwm_percentage
pwm_percentage = 0

global pi_pwm
pi_pwm = GPIO.PWM(LED_PIN,100)
pi_pwm.start(0)

def distance():
      GPIO.output(PIN_TRIGGER, True)
      
      time.sleep(0.00001)
      GPIO.output(PIN_TRIGGER, False)

      StartTime = time.time()
      StopTime = time.time()

      while GPIO.input(PIN_ECHO) == 0:
            StartTime = time.time()

      while GPIO.input(PIN_ECHO) == 1:
            StopTime = time.time()

      TimeElapsed = StopTime - StartTime

      # multiply with the sonic speed (34300 cm/s)
      # and divide by 2, because there and back
      distance = (TimeElapsed * 34300) / 2

      ## set brightness percentage for LED
      global pwm_percentage
      
      if (distance < 3):
            pwm_percentage = 100
      elif (distance < 7):
            pwm_percentage = 80
      elif (distance < 10):
            pwm_percentage = 60
      elif (distance < 15):
            pwm_percentage = 40
      elif (distance < 40):
            pwm_percentage = 20
      else:
            pwm_percentage = 0
      
      return distance


def led_pwm(duty_cycle):
      global pi_pwm
      pi_pwm.ChangeDutyCycle(duty_cycle) 
      
      

if __name__ == '__main__':
      try:
            while True:
                  dist = distance()
                  print("Measured Distance = %.1f cm" % dist)
                  print("PWM percentage = %s" %pwm_percentage)
                  led_pwm(pwm_percentage)
                  time.sleep(1)

      except KeyboardInterrupt:
            print("Measurement stopped by User")
            GPIO.cleanup()


