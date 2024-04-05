import numpy as np
import numpy.typing as npt

allRussWords: npt.ArrayLike = None
wordLenMax = 100
wordLenMin = 2
failureNumber = 6
wordsByLen = npt.ArrayLike = None
startUserWordLen = 6
startBotWordLen  = 7
botWordLenMin = 4
botWordLenMax = 11

botWordProbeNumber = 200

placeholder = "\uFFFD"

failurePhotos = ("error0.jpg", "error1.jpg", "error2.jpg", 
                 "error3.jpg", "error4.jpg", "error5.jpg", "error6.jpg")

def getRussWord(i: int) -> str: return allRussWords[i]
