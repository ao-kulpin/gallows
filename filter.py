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

class ExistFilter(Filter):
    def __init__(self, existChar: str, resolvedChars: list[str]):
        assert len(existChar) == 1
        self.existChar = existChar 
        self.resolvedChars = resolvedChars
        self.loopRange = range(len(resolvedChars))

    def applyToWord(self, word: str) -> bool:
        assert len(word) == len(self.resolvedChars)
        for i in self.loopRange:
            if (self.existChar == word[i]) != (self.existChar == self.resolvedChars[i]):
                ###print(f"filter({word}, {self.existChar}, {self.resolvedChars}, {i})->false")
                return False
        ###print(f"filter({word}, {self.resolvedChars})->true")
        return True       

class AbsentFilter(Filter):
    def __init__(self, absentChar: str):
        assert len(absentChar) == 1
        self.absentChar = absentChar 

    def applyToWord(self, word: str) -> bool:
        return -1 == word.find(self.absentChar)
    