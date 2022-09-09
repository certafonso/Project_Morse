"""
A simple hangman game that receives guesses via serial connection.
Usage: python hangman.py [COM port] [word]
"""


import serial
import UI
import pygame
import os, os.path

class Hangman():
	def __init__(self, word, font, size):
		self.word = word
		self.guessed = []
		self.fails = 0

		self.font = font
		self.size = size
		self.loadGraphics()

	@property
	def lost(self):
		""" Check if the player lost """
		return self.fails > 5

	@property
	def won(self):
		""" Check if the player won """
		for letter in self.word:
			if letter not in self.guessed:
				return False

		return True

	@property
	def finished(self):
		""" Checks if game finished or not """
		return self.won or self.lost

	def displayGame(self, display):
		""" Creates visual representation of current game """

		self.createWord()

		# Display the image, word and failed guesses
		display.blit(self.stages[self.fails], (0, 0))
		display.blit(self.text_word, self.rect_word)
		display.blit(self.text_guessed, self.rect_guessed)

	def createWord(self):
		""" Creates a text object with the word and guessed letters"""
		show = ""

		# For each letter in the word check if it was guessed
		for letter in self.word:
			if letter in self.guessed:
				show += letter + " "
			else:
				show += "_ "

		# Pygame text with the word
		self.text_word = self.font.render(show, True, (0,0,0)) 
		self.rect_word = self.text_word.get_rect(center=(self.size[0] // 2, 3*self.size[1] // 4))

		# Get the wrong guesses
		show = ""
		for letter in self.guessed:
			if letter not in self.word:
				show += letter + " "

		# Pygame text with the wrong guesses
		self.text_guessed = self.font.render(show, True, (0,0,0)) 
		self.rect_guessed = self.text_guessed.get_rect(center=(self.size[0] // 2, self.size[1] // 10))

	def checkGuess(self, guess):
		""" Checks if a guess is right or not """

		# Check if the player repeated some letter
		if guess in self.guessed:
			print("You've already said that letter")
			return False

		else:
			# Add the letter to the list of letters already guessed
			self.guessed.append(guess)

			if guess not in self.word:
				self.fails += 1
				return False

			else:
				return True

	def loadGraphics(self, path="./Games/Images/Hangman"):
		""" Loads the graphics to the game """

		self.stages = []

		# Search for all images in the respective folder and load them
		for f in os.listdir(path):
			ext = os.path.splitext(f)[1]
			if ext.lower() == ".png":
				self.stages.append(pygame.image.load(os.path.join(path,f)))

def main():
	from sys import argv

	# Checks for the correct number of arguments
	if len(argv) < 3:
		print("Wrong number of arguments. Usage: python hangman.py [COM port] [word]")
		return

	# Initialise pygame and some colors
	pygame.init() 
	white = (255, 255, 255) 
	black = (0, 0, 0)

	# Set dimensions of the display
	SIZE = (1400, 800)
	display_surface = pygame.display.set_mode((SIZE[0], SIZE[1]))

	# Set window name
	pygame.display.set_caption("Project Morse") 

	# Create a font object
	font = pygame.font.Font('freesansbold.ttf', 100) 

	# Create a MorseText object to display the guesses
	text = UI.MorseText(7*SIZE[0] // 8, SIZE[1] // 4, font)

	# Initialise serial connection
	ser = serial.Serial('COM5', 9600)

	# Initialise the game
	game = Hangman(argv[2], font, SIZE)

	# Game loop
	running = True
	while(running):

		# Check for pygame events (doesn't expect any)
		for event in pygame.event.get() : 
			if event.type == pygame.QUIT : 

				running = False

		if not game.finished:
			# Verify for new guesses, if there is one, update the text
			if ser.inWaiting():
				letter = ser.read(1).decode()

				print(letter)

				text.updateText(letter)

				game.checkGuess(letter)
				game.displayGame(display_surface)

			# If the text changed, clean the screen and print the new one
			if text.changed:
				display_surface.fill(white)
				
				text.display(display_surface)
				game.displayGame(display_surface)

			# Update the display
			pygame.display.update()  

	pygame.quit()
	ser.close()

if __name__ == "__main__":
	main()