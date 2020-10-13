import random
import serial

class Hangman():
    def __init__(self, word):
        self.word = word
        self.guessed = []
        self.fails = 0

        self.displayGame()

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

    def displayGame(self):
        """ Creates visual representation of current game """
        show = ""
        for letter in self.word:
            if letter in self.guessed:
                show += letter + " "
            else:
                show += "_ "

        print(show, self.fails)       

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


if __name__ == "__main__":
    game = Hangman(input("Word: "))

    ser = serial.Serial('COM5', 9600)

    while(not game.finished):
        if ser.inWaiting():
            word = ser.read(1).decode()

            print(word)

            game.checkGuess(word)
            game.displayGame()