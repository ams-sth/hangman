import random
import string
import nltk
from nltk.corpus import brown

try:
    nltk.data.find('corpora/brown')
except LookupError:
    nltk.download('brown', quiet=True)

class HangmanLogic:
    def __init__(self, level="basic", dictionary_path="data/dictionary.txt"):
        try:
            with open(dictionary_path, "r") as f:
                self.word_list = [line.strip().upper() for line in f if line.strip()]
        except FileNotFoundError:
            raise FileNotFoundError("Dictionary file not found. Provide a valid path.")

        if not self.word_list:
            raise ValueError("Dictionary file is empty.")

        self.level = level

        if self.level == "intermediate":
            self.phrase_list = self.generate_random_phrases()
        else:
            self.phrase_list = []

        self.score = 0
        self.reset()

    def generate_random_phrases(self):
        phrases = []
        for sentence in brown.sents():
            phrase = " ".join(sentence).upper()
            
            # ← Only allow letters and spaces, no "(2)" nonsense
            if not all(c.isalpha() or c == " " for c in phrase):
                continue
                
            if 2 <= len(phrase.split()) <= 5:
                phrases.append(phrase)
            
            if len(phrases) >= 100:
                break
        return phrases

    def reset(self):
        if self.level == "basic":
            self.hidden_word = random.choice(self.word_list)
        else:
            self.hidden_word = random.choice(self.phrase_list)

        self.current_display_word = ["_" if c != " " else " " for c in self.hidden_word]
        self.tries = 6 if self.level == "basic" else 4
        self.game_over = False
        self.guessed_letters = set()

    @property
    def guess_word(self):
        return self.current_display_word

    def guess(self, letter):
        if self.game_over:
            return None

        if not letter or len(letter) != 1 or letter.upper() not in string.ascii_uppercase:
            return "invalid"

        letter = letter.upper()
        if letter in self.guessed_letters:
            return "already"

        self.guessed_letters.add(letter)

        if letter in self.hidden_word:
            for i, c in enumerate(self.hidden_word):
                if c == letter:
                    self.current_display_word[i] = letter
                    self.score += 1
            if "_" not in self.current_display_word:
                self.game_over = True
                return "win"
            return "correct"
        else:
            self.tries -= 1
            if self.tries <= 0:
                self.game_over = True
                return "lose"
            return "wrong"
        
    def timeout(self):
        self.tries -= 1
        if self.tries <= 0:
            self.game_over = True
            return "lose"
        return "continue"
