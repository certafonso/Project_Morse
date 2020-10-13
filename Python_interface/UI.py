"""
A simple UI that just shows the letter inputed by user on the screen
"""

import serial
import pygame
import json

with open("./Python_interface/Morse.json") as f:
	morse_dict = json.load(f)

ser = serial.Serial('COM5', 9600)

pygame.init() 

white = (255, 255, 255) 
black = (0, 0, 0)
  
# dimensions
X = 500
Y = 500

# set dimensions and window name
display_surface = pygame.display.set_mode((X, Y))
pygame.display.set_caption("Project Morse") 

word = ""
word2 = ""

# create a font object
font = pygame.font.Font('freesansbold.ttf', X // 2) 
  
while True :
	# get serial
	if ser.inWaiting():
		word = ser.read(1)

		try:
			word2 = morse_dict[word.decode()]
		except: pass

	display_surface.fill(white)

	# update text
	text = font.render(word, True, black) 
	textRect = text.get_rect(center=(X // 2, Y // 3))
	display_surface.blit(text, textRect) 

	# update text
	text2 = font.render(word2, True, black)
	textRect2 = text2.get_rect(center=(X // 2, 2 * Y // 3))
	display_surface.blit(text2, textRect2) 
  
	for event in pygame.event.get() : 
		if event.type == pygame.QUIT : 

			pygame.quit()
			ser.close()
			quit() 

	pygame.display.update()  