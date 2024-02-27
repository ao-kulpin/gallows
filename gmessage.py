from aiogram.utils.keyboard import InlineKeyboardMarkup

class GMessage:
        def __init__(self, text: str = "", markup: InlineKeyboardMarkup = None, photo:str =""):
            self._text   = text
            self._markup = markup 
            self._photo  = photo
            self._changeCount = 1
            self._photoCount = 1

        def getText(self)   -> str:                   return self._text            
        def getMarkup(self) -> InlineKeyboardMarkup:  return self._markup
        def getPhoto(self)   -> str:                  return self._photo     

        def getChangeCount(self):                     return    self._changeCount         
        def getPhotoCount(self):                      return    self._photoCount         

        def setText(self, text: str):                      
            self._changeCount += int(self._text != text)
            self._text = text
        def setMarkup(self, markup: InlineKeyboardMarkup): 
            self._markup = markup          
            self._changeCount += 1
        def setPhoto(self, photo: str):                    
            self._photoCount += int(self._photo != photo)
            self._photo  = photo          

