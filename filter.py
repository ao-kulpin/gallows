import numpy as np
import numpy.typing as npt

import data

class Filter:
    def applyToWord(self, word: str) -> bool:
        pass

    def applyToWords(self, words: npt.ArrayLike) -> npt.ArrayLike:
        res = np.zeros(words.size, dtype=int)
        resCount = 0
        for wi in words:
            if self.applyToWord(data.allRussWords[wi]):
                res[resCount] = wi
                resCount += 1
        res.resize(resCount)
        return res                

class CharFilter(Filter):
    def __init__(self, guessedChar: str, resolvedChars: list[str]):
        assert len(guessedChar) == 1
        self.guessedChar = guessedChar 
        self.resolvedChars = resolvedChars
        self.loopRange = range(len(resolvedChars))

    def applyToWord(self, word: str) -> bool:
        assert len(word) == len(self.resolvedChars)
        for i in self.loopRange:
            if (self.guessedChar == word[i]) != (self.guessedChar == self.resolvedChars[i]):
                ###print(f"filter({word}, {self.guessedChar}, {self.resolvedChars}, {i})->false")
                return False
        ###print(f"filter({word}, {self.resolvedChars})->true")
        return True       

class NoCharFilter(Filter):
    def __init__(self, guessedChar: str):
        assert len(guessedChar) == 1
        self.guessedChar = guessedChar 

    def applyToWord(self, word: str) -> bool:
        return -1 == word.find(self.guessedChar)
    