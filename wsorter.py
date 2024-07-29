import sys
import math
import io

import data
import wordset

import numpy as np
import numpy.typing as npt

class ComplexWord:
    def __init__(self, complexity: int, word: str) -> None:
        self._complexity = complexity
        self._word = word

def putComplexWords(complexWords: list[ComplexWord], outFN: str) -> None:    
    handle = io.open(outFN, "wt", encoding='utf-8')
    if handle == None:
        print(f"Can't create {outFN}")
        return
    
    for cw in complexWords:
        handle.write(f"{cw._complexity} {cw._word}\n")

    handle.close()    

def main():
    if len(sys.argv) != 3:
        print("Error: no arguments (<input file> <output file>)")
        return
    
    data.loadDictionary(sys.argv[1])

    words = data.allRussWords

    if len(words) <= 0:
        print ("Can't read input file")
        return
    
    wcount = len(words)
    
    print(f"{wcount} words are loaded: {words}")

    complexWords = [None] * wcount # complexity of words

    for iw in range(wcount):
        w = words[iw]
        wc = wordset.getWordComplexity(w)
        complexWords[iw] = ComplexWord(wc, w)
        print(f"{iw} of {wcount} ({math.floor((iw + 1) * 100 / wcount)}%) {w}->{wc}")

    print("\nSorting complexities/words...")

    complexWords.sort(key = lambda cw: str(cw._complexity).zfill(3) + cw._word)

    print("Sorted\n")

    putComplexWords(complexWords, sys.argv[2])

    return

    compWords = [0] * wcount # complexity of words

if __name__ == "__main__":
    main()
