import data
import filter
import char

class WordSet:
    def __init__(self, wordLen: int) -> None:
        self._wordLen = wordLen
        self._words = data.wordsByLen[wordLen].copy()

    def getSize(self) -> int: return self._words.size 

    def getWords(self) -> list[str]:
        return [data.allRussWords[i] for i in self._words]

    def filter(self, absentChar:str = "", existChar: str = "", resolvedChars: list[str] = None) -> None:   
        filterObj = None
        if absentChar:
            assert resolvedChars == None
            filterObj = filter.AbsentFilter(absentChar)
        elif existChar:
            assert resolvedChars != None
            filterObj = filter.ExistFilter(existChar, resolvedChars)

        assert filterObj != None
        self._words = filterObj.applyToWords(self._words)

        def countMaxChar(self, resolvedChars: list[str]) -> str:
            counter = char.CharCounter()
            counter.countWords(self._words, resolvedChars)
            return counter.getMaxChar()