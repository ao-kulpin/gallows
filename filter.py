import numpy as np
import numpy.typing as npt

import data

class Filter:
    def applyToWord(self, word: str) -> bool:
        pass

    def applyToWords(self, words: npt.ArrayLike) -> npt.ArrayLike
        res = np.zeros(words.size, dtype=int)
        resCount = 0
        for wi in words:
            if self.applyToWord(data.allRussWords[wi]):
                res[resCount] = wi
                resCount += 1
        res.resize(resCount)
        return res                

class NoCharFilter(Filter):
    def __init__(self, noChar: str):
        assert len(noChar) == 1
        self.noChar = NoChar 

    def applyToWord(self, word: str) -> bool:
        return -1 == word.find(self.noChar)
    