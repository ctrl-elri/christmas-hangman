# 291632, Ella Rinnemaa, ella.rinnemaa@tuni.fi, skaalautuva versio
#
# Program: A word guessing game similar to Hangman.
#
# How to play: The player can try ten times to guess the letters which
# the word consists of by clicking the letter buttons in the GUI.
# If the player gets a letter correctly the button will turn green and
# the placement of the guessed letter in the word will appear on
# the screen. If the guess is wrong, the button will turn red and the player
# loses one try. The player cannot guess the same letter twice.
#
# If the player guesses all the letters in the word, they win a round.
# If they run out of tries, they lose the game.
#
# The game counts how many words the player has guessed correctly.
# One can win the game by guessing all the words (14) correctly.

from tkinter import *
import random

ALPHABET = ["A", "B", "C", "D", "E", "F", "G", "H", "I", "J", "K", "L", "M",
            "N", "O", "P", "Q", "R", "S", "T", "U", "V", "W", "X", "Y", "Z"]

ANSWERS = ["SANTA", "SNOWMAN", "CHIMNEY", "DECEMBER", "GINGERBREAD", "GRINCH",
           "NUTCRACKER", "ORNAMENTS", "JINGLE", "MISTLETOE", "REINDEER",
           "GIFT", "CAROLS", "CHRISTMAS"]


class Hangman:

    def __init__(self):
        self.__main = Tk()
        self.__main.title("Hangman")

        self.__guess_count = 10  # Counts the times the player can guess.
        self.__letterLabels = []  # The labels of letters in the correct word.
        self.__guessed_words_total = 0  # Counts the words the player has guessed correctly.
        self.__correct_answer = None  # The hidden word.
        self.__guessed_words = []  # The words the player has guessed correctly.

        # Setting the image -options.
        self.__tree_pic = PhotoImage(file="tree.gif")
        self.__santa_pic = PhotoImage(file="santa.gif")
        self.__grinch_pic = PhotoImage(file="grinch.gif")
        self.__picLabel = Label(self.__main, image=self.__tree_pic)

        # Setting default image (didn't appear without this code).
        self.__picLabel.image = self.__tree_pic
        self.__picLabel.grid(row=8, column=0, rowspan=6)

        # Creating the player's controllers; the alphabet buttons.
        self.__letterButtons = []
        n = 0
        for i in range(len(ALPHABET)):
            new_button = Button(self.__main, text=ALPHABET[i],
                                font=("Fixedsys", 15),
                                background="gold",
                                foreground="black",
                                command=lambda x=i: self.guess(x),
                                borderwidth=2, relief=RIDGE)
            new_button.grid(row=9, column=2 + n)
            self.__letterButtons.append(new_button)
            n += 1

        # Creating the rest of the buttons in the GUI.

        # Player uses to guess another word; button starts a new round.
        self.__guessButton = Button(self.__main, text="Guess again",
                                    font=("Fixedsys", 12), background="green",
                                    command=self.initialize_game)
        self.__guessButton.grid(row=0, column=len(ALPHABET) + 2, sticky=E)

        # Button starts a new game.
        Button(self.__main, text="Start a new game", font=("Fixedsys", 12),
               background="pink", command=self.new_game). \
            grid(row=12, column=len(ALPHABET) + 2, sticky=E)

        # Button ends the game.
        Button(self.__main, text="Stop playing", font=("Fixedsys", 12),
               background="blue",
               command=self.__main.destroy) \
            .grid(row=14, column=len(ALPHABET) + 2, sticky=E)

        # Creating the labels in the GUI.
        self.__game_situationLabel1 = Label(self.__main,
                                            text="You have {:2d} tries to "
                                                 "guess "
                                                 "the word.".format(
                                                self.__guess_count))
        self.__game_situationLabel1.grid(row=0, column=0, rowspan=2,
                                         sticky=N + S)

        self.__guessesLabel = Label(self.__main,
                                    text="Words guessed correctly: "
                                         + str(self.__guessed_words_total),
                                    font=("Fixedsys", 12))
        self.__guessesLabel.grid(row=5, column=len(ALPHABET) + 2, sticky=E)
        self.__game_situationLabel2 = Label(self.__main, text="The theme is "
                                                              "Christmas.",
                                            font=("Fixedsys", 16))
        self.__game_situationLabel2.grid(row=3, column=0, rowspan=2,
                                         sticky=N + S)
        self.__game_situationLabel3 = Label(self.__main, text="Good luck!",
                                            font=(
                                                "Fixedsys", 18, "bold italic"))
        self.__game_situationLabel3.grid(row=6, column=0, rowspan=2,
                                         sticky=N + S)

        # Starting the game.
        self.initialize_game()

    def initialize_game(self):
        """
        Method starts a new round: sets the values of variables to default and
        updates labels. Draws the hidden word.
        """

        self.__guess_count = 10

        # Labels are updated.
        self.update_tries_left()
        self.update_labels()

        # The old labels are removed.
        for old_label in self.__letterLabels:
            old_label.destroy()

        # The answer is randomly chosen.
        random.shuffle(ANSWERS)
        self.__correct_answer = list(ANSWERS[0])

        # Making sure the chosen word hasn't already been guessed.
        while self.__correct_answer in self.__guessed_words:
            random.shuffle(ANSWERS)
            self.__correct_answer = list(ANSWERS[0])

        # Creating the labels for the the letters which the answer consists of,
        # and setting the text to default (meaning the letters are "hidden").
        self.__letterLabels = []
        n = 0
        for letter in range(len(self.__correct_answer)):
            letterLabel = Label(self.__main, text="_", background="white",
                                borderwidth=2, relief=RAISED)
            letterLabel.grid(row=7, column=10 + n, sticky=E + W)
            n += 1
            self.__letterLabels.append(letterLabel)

        # The alphabet buttons are set to default.
        for button in self.__letterButtons:
            button.configure(background="gold", state=NORMAL)

    def update_tries_left(self):
        """
        Method updates the amount of times the player can try
        to guess the letters.
        """
        self.__game_situationLabel1.configure(
            text="You have {:2d} tries to guess "
                 "the word.".format(self.__guess_count), font=("Fixedsys", 16))

    def update_labels(self):
        """
        Method sets the labels to default. Needed after a round ends.
        """
        self.__game_situationLabel2.configure(text="The theme is Christmas.",
                                              foreground="black")
        self.__game_situationLabel3.configure(text="Good luck!")
        self.__picLabel.configure(image=self.__tree_pic)

    def update_guesses(self):
        """
        Method updates the amount of correctly guessed words.
        Needed after a round ends.
        """
        self.__guessesLabel.configure(text="Words guessed correctly: "
                                           + str(self.__guessed_words_total))

    def check_win(self):
        """
        Method checks to see if the player has won the round.
        """
        guessed_letters = []  # The letters guessed correctly.

        # If the word isn't hidden, the player has guessed it, and it's
        # added to the list.
        for label in self.__letterLabels:
            if label["text"] != "_":
                guessed_letters.append(label)

        if len(guessed_letters) == len(self.__letterLabels):

            # One is added to the amount of words the player has
            # guessed correctly.
            self.__guessed_words_total += 1
            self.update_guesses()

            # Method is called to check if the player has guessed all the words
            # in ANSWERS.
            if not self.check_guesses_total():

                # If the player hasn't won the game,
                # labels are set to message that the player has won the round.
                self.__picLabel.configure(image=self.__santa_pic)
                self.__game_situationLabel1.configure(text="")
                self.__game_situationLabel2.configure(
                    text="Correct! Guess another?",
                    foreground="green")
                self.__game_situationLabel3.configure(text="")

                # The guessed word is added to the list of guessed words.
                self.__guessed_words.append(self.__correct_answer)

    def check_guesses_total(self):
        """
        Method checks if the player has guessed all the words in ANSWERS and
        consequently won the whole game.
        """

        # If the player wins, the labels' texts and image are edited and
        # the guess -button is disabled.
        # If they don't, nothing in the GUI is changed.

        if int(self.__guessed_words_total) == len(ANSWERS):

            self.__picLabel.configure(image=self.__santa_pic)
            self.__game_situationLabel1.configure(text="")
            self.__game_situationLabel2.configure(
                text="Congratulations! You've guessed all words!",
                foreground="green")
            self.__game_situationLabel3.configure(text="")

            self.__guessButton.configure(state=DISABLED)
            return True

        elif self.__guessed_words_total != len(ANSWERS):
            return False

    def end_game(self):
        """
        Method ends the round.
        """

        # The answer is revealed.
        for i in range(len(self.__correct_answer)):
            self.__letterLabels[i].configure(text=self.__correct_answer[i])

        # The controllers are disabled.
        for button in self.__letterButtons:
            button.configure(background="red", state=DISABLED)

        # The labels' texts and image are edited.
        self.__game_situationLabel1.configure(text="")
        self.__game_situationLabel2.configure(text="Incorrect. Try again?",
                                              foreground="red")
        self.__game_situationLabel3.configure(text="")
        self.__picLabel.configure(image=self.__grinch_pic)

        # The player has to start a new game.
        self.__guessButton.configure(state=DISABLED)

    def new_game(self):
        """
        Method starts a new game; sets all game variables to default.
        """
        self.__guessed_words_total = 0
        self.__guessed_words = []

        self.initialize_game()
        self.update_guesses()

    def guess(self, letter_num):
        """
        Method controls the guessing of the letters.
        """

        # To guess, the player must have more than zero tries left.
        if self.__guess_count > 0:

            # If the text in the pressed button is one of the letters in
            # the answer, the player has guessed the letter correctly.
            if self.__letterButtons[letter_num]["text"] in \
                    self.__correct_answer:

                for i in range(len(self.__correct_answer)):

                    # The placement/s of the correctly guessed letter in
                    # the word is/are revealed by changing the label text.
                    if self.__letterButtons[letter_num]["text"] == \
                            self.__correct_answer[i]:

                        self.__letterLabels[i].configure(
                            text=self.__letterButtons[letter_num]["text"])
                        self.__letterButtons[letter_num].configure(
                            state=DISABLED, background="green")

                        # Method to check if the round has been won.
                        self.check_win()

            # If the pressed button's text isn't one of the letters
            # in the answer, the button is disabled and the player loses a try.
            elif self.__letterButtons[letter_num]["text"] not in \
                    self.__correct_answer:
                self.__letterButtons[letter_num].configure(state=DISABLED,
                                                           background="red")
                self.__guess_count -= 1
                self.update_tries_left()

                if self.__guess_count == 0:
                    # Method to check if the round has been lost.
                    self.end_game()

    def start(self):
        self.__main.mainloop()


def main():
    root = Hangman()
    root.start()


main()
