import numpy as np

import math

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
    
def getWordComplexity(word: str) -> int:
    wordLen: int = len(word)
    resolvedChars: list[str] = ["?"] * wordLen
    ws = WordSet(wordLen)
    failCount: int = 0
    while "?" in resolvedChars:
        guessedChar: str = ws.countMaxChar(resolvedChars)
        if guessedChar in word:
            # successful guess
            for i in range(wordLen): # update resolvedChars
                if word[i] == guessedChar:
                    assert resolvedChars[i] == "?"
                    resolvedChars[i] = guessedChar

            ws.filter(existChar=guessedChar, resolvedChars=resolvedChars)
        else:
            # failed guess
            failCount += 1
            ws.filter(absentChar=guessedChar)      

    return failCount

fullWordList = None

async def findRandomComplexWord(wordLen, showProgress) ->str:
    global fullWordList
    words = None
    if wordLen == None:
        if fullWordList == None:
            fullWordList = range(len(data.allRussWords))
        words = fullWordList
    else:
        words = data.wordsByLen[wordLen]

    wordsSize: int = len(words)  

    maxComplexity: int = -1
    complexWord: str = ""
    percent: int = -1
    for i in range(data.botWordProbeNumber):
        newPercent = math.floor(100 * i / data.botWordProbeNumber)
        if newPercent != percent:
            percent = newPercent
            await showProgress(percent)
        word:str = data.getRussWord(words[math.floor(wordsSize * np.random.random_sample())])
        comlexity: int = getWordComplexity(word)
        if comlexity > maxComplexity \
            or comlexity == maxComplexity and np.random.random_sample() > 0.5:
                                              # randomization of the choice 
            maxComplexity = comlexity
            complexWord = word

    print(f"\n *** findRandomComplexWord->{complexWord}({maxComplexity})")

    return complexWord


