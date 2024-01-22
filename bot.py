import asyncio
import numpy as np
import numpy.typing as npt

from aiogram import Bot, Dispatcher, types, F
from aiogram.exceptions import TelegramBadRequest
from aiogram.filters import Command
from aiogram.filters.callback_data import CallbackData
from aiogram.utils.keyboard import ReplyKeyboardBuilder, InlineKeyboardBuilder
from aiogram.types import FSInputFile, URLInputFile, BufferedInputFile, InputMediaPhoto

RussNounsFN = "russian_nouns.txt"

allRussWords: npt.ArrayLike = None
wordLenMax = 100
wordsByLen = npt.ArrayLike = None


# Start the bot
async def main():
    global allRussWords
    print("Bot Gallows starting...")
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
    wordLens = np.zeros(wordLenMax + 1, dtype=int)
    for line in allLines:
        word = line[:-1].upper()
        ### print(f"word:{word}")
        allRussWords[wordCount] = word
        lw = len(word)
        wordLens[lw] +=1
        if actualLenMax < lw: actualLenMax = lw
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

    ### for wli in range(wordsByLen.size):
    ###    print(f"wli({wli}:{wordsByLen[wli].size})->{[allRussWords[i] for i in wordsByLen[wli]]}")
    
    ### for i in range(wordLenMax):    
    ###  print(f"{i}: {wordLens[i]}")  

    print(f"{str(allRussWords.size)} words are loaded")

if __name__ == "__main__":
    asyncio.run(main())

