import random
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

		display.blit(self.stages[self.fails], (0, 0)) 				# display image
		display_surface.blit(self.text_word, self.rect_word) 		# display word 
		display_surface.blit(self.text_guessed, self.rect_guessed) 	# display guessed letters word 

	def createWord(self):
		""" Creates a text object with the word and guessed letters"""
		show = ""
		for letter in self.word:
			if letter in self.guessed:
				show += letter + " "
			else:
				show += "_ "

		self.text_word = self.font.render(show, True, (0,0,0)) 
		self.rect_word = self.text_word.get_rect(center=(self.size[0] // 2, 3*self.size[1] // 4))

		show = ""
		for letter in self.guessed:
			if letter not in self.word:
				show += letter + " "

		self.text_guessed = self.font.render(show, True, (0,0,0)) 
		self.rect_guessed = self.text_guessed.get_rect(center=(self.size[0] // 2, self.size[1] // 10))

	def checkGuess(self, guess):
		""" Checks if a guess is right or not """

		if guess in self.guessed: #check if the player repeated some letter
			print("You've already said that letter")
			return False

		else:
			self.guessed.append(guess) #will add the letter to the list of letters already guessed
			if guess not in self.word:
				self.fails += 1
				return False

			else:
				return True

	def loadGraphics(self, path="./Games/Images/Hangman"):
		""" Loads the graphics to the game """

		self.stages = []

		for f in os.listdir(path):
			ext = os.path.splitext(f)[1]
			if ext.lower() == ".png":
				self.stages.append(pygame.image.load(os.path.join(path,f)))

if __name__ == "__main__":

	pygame.init() 

	white = (255, 255, 255) 
	black = (0, 0, 0)

	# dimensions
	SIZE = (1400, 800)

	# set dimensions and window name
	display_surface = pygame.display.set_mode((SIZE[0], SIZE[1]))
	pygame.display.set_caption("Project Morse") 

	# create a font object
	font = pygame.font.Font('freesansbold.ttf', 100) 

	text = UI.MorseText(7*SIZE[0] // 8, SIZE[1] // 4, font)

	ser = serial.Serial('COM5', 9600)

	game = Hangman(input("Word: "), font, SIZE)

	while(True):
		for event in pygame.event.get() : 
			if event.type == pygame.QUIT : 

				pygame.quit()
				ser.close()
				quit() 

		if not game.finished:
			if ser.inWaiting():
				letter = ser.read(1).decode()

				print(letter)

				text.updateText(letter)

				game.checkGuess(letter)
				game.displayGame(display_surface)

			if text.changed:
				display_surface.fill(white)
				
				text.display(display_surface)
				game.displayGame(display_surface)

			pygame.display.update()  

	pygame.quit()
	ser.close()