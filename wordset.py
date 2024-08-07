import numpy as np
import numpy.typing as npt

import math

import data
from data import placeholder
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
    resolvedChars: list[str] = [placeholder] * wordLen
    ws = WordSet(wordLen)
    failCount: int = 0
    while placeholder in resolvedChars:
        guessedChar: str = ws.countMaxChar(resolvedChars)
        if guessedChar in word:
            # successful guess
            for i in range(wordLen): # update resolvedChars
                if word[i] == guessedChar:
                    assert resolvedChars[i] == placeholder
                    resolvedChars[i] = guessedChar

            ws.filter(existChar=guessedChar, resolvedChars=resolvedChars)
        else:
            # failed guess
            failCount += 1
            ws.filter(absentChar=guessedChar)      

    return failCount

fullWordList = None

class WordStore:
    def __init__(self) -> None:
        self._store = {}
    def add(self, word: str, complexity: int) -> None:
        self._store.update({word: complexity})
    def has(self, word: str) -> bool:
        return self._store.get(word) != None

prevFinds = WordStore()        

async def findRandomComplexWord(wordLen, showProgress) -> str:
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
    prevComplexWord = ""
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
            if prevFinds.has(word) :
                prevComplexWord = word
            else:
                complexWord = word

    print(f"\n *** findRandomComplexWord->{complexWord}/{prevComplexWord}({maxComplexity})")

    if complexWord == "":
        return prevComplexWord
    else:
        prevFinds.add(complexWord, maxComplexity)
        return complexWord

async def chooseComplexWord(wordLen) -> str:
    global fullWordList
    words = None
    if wordLen == None:
        if fullWordList == None:
            fullWordList = range(len(data.allRussWords))
        words = fullWordList
    else:
        words = data.wordsByLen[wordLen]

    wordsSize: int = len(words)  
    pos0 = wordsSize * data.complexWordZone
    pos = math.floor(pos0 + (wordsSize - pos0) * np.random.random_sample())
    wi = words[pos]

    complexWord = data.getRussWord(wi)
    wc = data.getComplexity(wi)

    print(f"\n *** chooseComplexWord->{complexWord}(complexity={wc})")

    return complexWord


