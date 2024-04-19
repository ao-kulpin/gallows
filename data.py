import numpy as np
import numpy.typing as npt

RussNounsFN = "russian_nouns_without_filter.txt"  #####"russian_nouns.txt"

allRussWords: npt.ArrayLike = None
wordLenMax = 100
wordLenMin = 2
failureNumber = 6
wordsByLen = npt.ArrayLike = None
startUserWordLen = 6
startBotWordLen  = 9
botWordLenMin = 4
botWordLenMax = 11

botWordProbeNumber = 200

logFileName = "gallows.log"

placeholder     = "\uFFFD"
textPlaceholder = "?"

failurePhotos = ("error0.jpg", "error1.jpg", "error2.jpg", 
                 "error3.jpg", "error4.jpg", "error5.jpg", "error6.jpg")

def loadDictionary() -> None :
    global allRussWords, wordLenMax, wordsByLen
    print("Russian words loading...")
    allLines: list[str]
    try:
        f = open(RussNounsFN, "r", encoding='utf-8')
        allLines = np.array(f.readlines(), str)
        f.close()
    except:
        print(f"Can't load file {RussNounsFN}")
        return
    
    print(f"File {RussNounsFN} is loaded")
    allRussWords = np.empty(allLines.size, dtype=object)
    wordCount = 0
    actualLenMax = 0
    actualLenMin = 100
    wordLens = np.zeros(wordLenMax + 1, dtype=int)
    for line in allLines:
        word = line[:-1].upper()
        ### print(f"word:{word}")
        allRussWords[wordCount] = word
        lw = len(word)
        wordLens[lw] +=1
        if actualLenMax < lw: actualLenMax = lw
        if actualLenMin > lw: actualLenMin = lw
        wordCount += 1
        ### print(f"words: {allRussWords}")        

    wordsByLen = np.empty(actualLenMax + 1, dtype=object)
    for wl in range(actualLenMax + 1):
        wordsByLen[wl] = np.empty(wordLens[wl], dtype=int)

    wordLenCounts = np.zeros(actualLenMax + 1, dtype=int) 

    for wi in range(allRussWords.size):
        wl: int = len(allRussWords[wi])
        ### print(f"wi {wi}/{allRussWords[wi]}")
        wlc: int = wordLenCounts[wl]
        wordsByLen[wl][wlc] = wi
        wordLenCounts[wl] += 1

###    for wli in range(wordsByLen.size):
###        print(f"wli({wli}:{wordsByLen[wli].size})->{[allRussWords[i] for i in wordsByLen[wli]]}")
    
###    for i in range(wordLenMax):    
###      print(f"{i}: {wordLens[i]}")  

def getRussWord(i: int) -> str: return allRussWords[i]
