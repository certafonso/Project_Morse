import serial
import pygame

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

# create a font object
font = pygame.font.Font('freesansbold.ttf', X // 2) 
  
while True :
	# get serial
	if ser.inWaiting():
		word = ser.read(1)
		type(word)
		print(word)

	# update text
	text = font.render(word, True, black) 
	textRect = text.get_rect()
	textRect.center = (X // 2, Y // 2) 
  
	# show stuff
	display_surface.fill(white)
	display_surface.blit(text, textRect) 

	for event in pygame.event.get() : 
		if event.type == pygame.QUIT : 

			pygame.quit()
			ser.close()
			quit() 

	pygame.display.update()  