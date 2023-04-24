import RPi.GPIO as GPIO
import time
from kivy.app import App
from kivy.uix.widget import Widget
from kivy.lang import Builder
from kivy.core.window import Window


GPIO.setmode(GPIO.BOARD)
GPIO.setup(19,GPIO.OUT)
GPIO.setup(23,GPIO.OUT)
GPIO.setup(29,GPIO.OUT)


# Load design file
Builder.load_file('LEDs.kv')

# List of LEDs and colors
leds = [[19,"Red"], [23,"Blue"], [29,"Green"]]

# Loop over all pins and turn on/off depedning on arg

# Turn off all pins and end the program

def quitter(string):
	if string == "Quit":
		app.stop()

def LED_Swtich(color, led_list):
	i = 0
	while i < len(led_list):
		if led_list[i][1] == color:
			GPIO.output(led_list[i][0], GPIO.HIGH)
			i = i + 1
		else:
			GPIO.output(led_list[i][0], GPIO.LOW)
			i = i + 1
	quitter(color)


class MyLayout(Widget):
	checks = []
	def checkbox_click(self, instance, value, LED):
		if value == True:
			MyLayout.checks.append(LED)
			led = ''
			for x in MyLayout.checks:
				led = f'{led} {x}'
			self.ids.output_label.text = f'You Selected: {led}'
			led = led.strip()
			LED_Swtich(led,leds)
		else:
			MyLayout.checks.remove(LED)
			led = ''
			for x in MyLayout.checks:
				led = f'{led} {x}'
			self.ids.output_label.text = f'You Selected: {led}'
			led = led.strip()

class LEDApp(App):
	def build(self):
		return MyLayout()

if __name__ == '__main__':
	LEDApp().run()


