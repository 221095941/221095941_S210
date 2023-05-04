from kivy.app import App
from kivy.uix.widget import Widget
from kivy.properties import ObjectProperty
from kivy.lang import Builder
from kivy.clock import Clock


import RPi.GPIO as GPIO
from time import sleep


# Raspberry Pi Setup
GPIO.setmode(GPIO.BOARD)

ledPin = 19

GPIO.setup(ledPin,GPIO.OUT)



# Morse Code Functions

MORSE_CODE_DICT = {'A': '.-', 
        'B': '-...', 
        'C': '-.-.', 
        'D': '-..', 
        'E': '.', 
        'F': '..-.', 
        'G': '--.', 
        'H': '....', 
        'I': '..', 
        'J': '.---', 
        'K': '-.-', 
        'L': '.-..', 
        'M': '--', 
        'N': '-.', 
        'O': '---', 
        'P': '.--.', 
        'Q': '--.-', 
        'R': '.-.', 
        'S': '...', 
        'T': '-', 
        'U': '..-', 
        'V': '...-', 
        'W': '.--', 
        'X': '-..-', 
        'Y': '-.--', 
        'Z': '--..'}


def dot():
   GPIO.output(ledPin,1)
   sleep(0.5)
   GPIO.output(ledPin,0)
   sleep(0.5)

def dash():
   GPIO.output(ledPin,1)
   sleep(1)
   GPIO.output(ledPin,0)
   sleep(0.5)

def nextLetter():
   GPIO.output(ledPin,0)
   sleep(2)


def morse_code(word):
	word = word.upper()
	for letter in word:
		morse_letter_code = MORSE_CODE_DICT.get(letter)
		for c in morse_letter_code:
			if c == ".":
				dot()
			elif c == "-":
				dash()
			else:
				print("Unexpected Error")
		nextLetter()
	print("Word Finished")


Builder.load_file('MyLayout.kv')

class MyLayout(Widget):
	def press(self):

		word = self.ids.word_input.text
		
		# Update the label
		word = word.strip()
		if len(word) < 13:
			self.ids.word_label.text = f'Entered word: {word}'
			morse_code(word)
		else:
			self.ids.word_label.text = 'Your word is invalid'

		# Clear input box
		self.ids.word_input.text = ''

class MyApp(App):
	def build(self):	
		return MyLayout()


 

if __name__ == '__main__':
	MyApp().run()
