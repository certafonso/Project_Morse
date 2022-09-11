"""
A simple UI that just shows the letter inputed by user on the screen
Usage: python UI.py [COM port]
"""

import serial
import pygame
import json

with open("./Games/Morse.json") as f:
	morse_dict = json.load(f)

class MorseText():
	def __init__(self, x, y, font):
		self.letter = ""
		self.morse = ""

		self.changed = True
		self.font = font
		self.color = (0, 0, 0)
		self.x = x
		self.y = y

	def changeColor(self, color):
		""" Changes the color of the text """
		self.color = color

	def updateText(self, letter):
		""" Updates the text objects to a letter """
		
		self.letter = letter
		self.morse = morse_dict[letter]
		self.changed = True

	def display(self, display_surface):
		""" Displays the letter on screen """

		print(self.y, self.font.size(self.letter))

		self.text_letter = self.font.render(self.letter, True, self.color) 
		self.rect_letter = self.text_letter.get_rect(center=(self.x, self.y - self.font.size(self.letter)[1]//2))
		display_surface.blit(self.text_letter, self.rect_letter) 
		
		self.text_morse = self.font.render(self.morse, True, self.color)
		self.rect_morse = self.text_morse.get_rect(center=(self.x, self.y + self.font.size(self.morse)[1]//5))
		display_surface.blit(self.text_morse, self.rect_morse)

		self.changed = False


def main():
	from sys import argv

	# Checks for the correct number of arguments
	if len(argv) < 2:
		print("Wrong number of arguments. Usage: python UI.py [COM port]")
		return

	# Initialise pygame and some colors
	pygame.init() 
	white = (255, 255, 255) 
	black = (0, 0, 0)

	# Set dimensions of the display
	SIZE = (500, 500)
	display_surface = pygame.display.set_mode((SIZE[0], SIZE[1]))

	# Set window name
	pygame.display.set_caption("Project Morse") 

	# Create a font object
	font = pygame.font.Font('freesansbold.ttf', SIZE[0] // 2) 

	# Create a MorseText object to display the guesses
	text = MorseText(SIZE[0] // 2, SIZE[1] // 2, font)

	# Initialise serial connection
	ser = serial.Serial(argv[1], 9600)

	# Game loop
	running = True
	while(running):

		# get serial
		if ser.inWaiting():
			word = ser.read(1)

			text.updateText(word.decode())
	
		for event in pygame.event.get() : 
			if event.type == pygame.QUIT : 

				pygame.quit()
				ser.close()
				return

		if text.changed:
			display_surface.fill(white)
			
			text.display(display_surface)

		pygame.display.update()  

if __name__ == "__main__":
	main()