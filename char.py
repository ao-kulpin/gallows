import numpy as np
import numpy.typing as npt
from bot import allRussWords

allChars = "АБВГДЕЁЖЗИЙКЛМНОПРСТУФХЦЧШЩЪЫЬЭЮЯ-"

class CharCounter:
    def __init__(self) -> None:
        self._counts = {}
        for c in allChars:
            self._counts[c] = 0
        self._maxCount = 0
        self._maxChar = allChars[0]

    def countChar(self, c: str) -> None:
        assert len(c) == 1
        count = self._counts[c] + 1
        self._counts[c] = count
        if count > self._maxCount:
            self._maxCount = count
            self._maxChar = c

    def countWord(self, word: str, resolvedChars : list[str]) -> None:
        assert len(word) == len(resolvedChars)
        for i in range(len(word)):
            if resolvedChars[i] == "?":
                self.countChar(word[i])

    def coutWords(self, words: npt.ArrayLike, resolvedChars : list[str]) -> None:
        print(f"allRussWords:{type(allRussWords)}")
        for wi in words:
            self.countWord(allRussWords[wi], resolvedChars)

    def getMaxChar(self): self._maxChar            

