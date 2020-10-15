"""
A simple UI that just shows the letter inputed by user on the screen
"""

import serial
import pygame
import json

with open("./Games/Morse.json") as f:
	morse_dict = json.load(f)

class MorseText():
	def __init__(self, x, screen_Y, font):
		self.letter = ""
		self.morse = ""

		self.changed = True
		self.font = font
		self.color = (0, 0, 0)
		self.x = x
		self.screen_Y = screen_Y

	def changeColor(self, color):
		""" Changes the color of the text """
		self.color = color

	def updateText(self, letter):
		""" Updates the text objects to a letter """
		
		self.letter = letter
		self.morse = morse_dict[letter]
		self.changed = True

	def display(self, display_surface):

		self.text_letter = self.font.render(self.letter, True, self.color) 
		self.rect_letter = self.text_letter.get_rect(center=(self.x, self.screen_Y // 3))
		display_surface.blit(self.text_letter, self.rect_letter) 
		
		self.text_morse = self.font.render(self.morse, True, self.color)
		self.rect_morse = self.text_morse.get_rect(center=(self.x, 2 * self.screen_Y // 3))
		display_surface.blit(self.text_morse, self.rect_morse)

		self.changed = False


if __name__ == "__main__":
	ser = serial.Serial('COM5', 9600)

	pygame.init() 

	white = (255, 255, 255) 
	black = (0, 0, 0)
	
	# dimensions
	SIZE = (500, 500)

	# set dimensions and window name
	display_surface = pygame.display.set_mode((SIZE[0], SIZE[1]))
	pygame.display.set_caption("Project Morse") 

	# create a font object
	font = pygame.font.Font('freesansbold.ttf', SIZE[0] // 2) 

	text = MorseText(SIZE[0] // 2, SIZE[1], font)
	
	while True :
		# get serial
		if ser.inWaiting():
			word = ser.read(1)

			text.updateText(word.decode())
	
		for event in pygame.event.get() : 
			if event.type == pygame.QUIT : 

				pygame.quit()
				ser.close()
				quit() 

		if text.changed:
			display_surface.fill(white)
			
			text.display(display_surface)

		pygame.display.update()  
