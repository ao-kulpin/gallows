from datetime import datetime
import data

logHandle = None

def put(s: str) -> None:
    global logHandle
    if logHandle == None:
        logHandle = open(data.logFileName, "at", encoding='utf-8')

    text = f"\n***** {datetime.now()}\n{s}\n"         
    print(text)
    logHandle.write(convertForLog(text))
    close() # ?????

def close() -> None:
    global logHandle
    if logHandle != None:
        logHandle.close()
        logHandle = None

def convertForLog(s: str) -> str:
    return s.replace(data.placeholder, data.textPlaceholder)        