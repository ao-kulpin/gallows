import numpy as np
import numpy.typing as npt
import data

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
        #print(f"countChar({c})->{count}")
        if count > self._maxCount \
            or count == self._maxCount and np.random.random_sample() > 0.5:
                                        # randomization of _maxChar          
            self._maxCount = count
            self._maxChar = c

    def countWord(self, word: str, resolvedChars : list[str]) -> None:
        #print(f"countWord({word} {resolvedChars})")
        assert len(word) == len(resolvedChars)
        for i in range(len(word)):
            if resolvedChars[i] == "?":
                ch: str = word[i]
                if word.find(ch) == i: # ignore duplicates 
                    self.countChar(ch) 

    def countWords(self, words: npt.ArrayLike, resolvedChars : list[str]) -> None:
        print(f"data.allRussWords:{type(data.allRussWords)}")
        for wi in words:
            self.countWord(data.allRussWords[wi], resolvedChars)

    def getMaxChar(self): return self._maxChar            

