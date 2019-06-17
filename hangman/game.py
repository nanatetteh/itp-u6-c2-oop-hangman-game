from .exceptions import *
import random


class GuessAttempt(object):

    def __init__(self, letter, hit=None, miss=None):
        self.guess = letter
        self.hit = hit
        self.miss = miss

        if self.miss == True and self.hit == True:
            raise InvalidGuessAttempt()

    def is_hit(self):
        if self.hit:
            return True
        return False

    def is_miss(self):
        if self.miss:
            return True
        return False


class GuessWord(object):
    def __init__(self, word):
        if word == '':
            raise InvalidWordException()

        self.answer = word
        self.masked = len(word) * "*"

    # Code to uncover word. takes the masked words and coverts to a list
    # replace the letter at the index where it evaluates true
    def uncover_word(self, letter):

        maskv = list(self.masked)

        for idx, char in enumerate(self.answer):
            if char.lower() == letter.lower():
                maskv[idx] = char.lower()
        str = ''.join(maskv)
        return str

    def perform_attempt(self, letter):
        if len(letter) > 1:
            raise InvalidGuessedLetterException()

        if letter.lower() in self.answer.lower():
            attempt = GuessAttempt(letter, hit=True)
            self.masked = self.uncover_word(letter)
        else:
            attempt = GuessAttempt(letter, miss=True)
        return attempt


class HangmanGame(object): 

    WORD_LIST = ['rmotr', 'python', 'awesome']

    def __init__(self, listword=None, number_of_guesses=5):
        if listword == None:
            listword = self.WORD_LIST

        selectWord = self.select_random_word(listword)
        self.word = GuessWord(selectWord)
        self.remaining_misses = number_of_guesses
        self.previous_guesses = []

    @classmethod
    def select_random_word(cls, listword):
        if len(listword) == 0:
            raise InvalidListOfWordsException()
        return random.choice(listword)

    def guess(self, letter):
        if self.is_won() or self.is_lost():
            raise GameFinishedException()
        self.previous_guesses.append(letter.lower())
        attempt = self.word.perform_attempt(letter)
        if attempt.is_miss():
            self.remaining_misses -= 1
            if self.is_lost():
                raise GameLostException()

        if self.is_won():
            raise GameWonException()

        return attempt
    # The following code block will be the game states that can be invoked
    def is_finished(self):
        if self.is_won() or self.is_lost():
            return True
        return False

    def is_won(self):
        if self.word.answer == self.word.masked:
            return True
        return False

    def is_lost(self):
        if self.remaining_misses < 1:
            return True
        return False
