from aiogram.utils.keyboard import InlineKeyboardMarkup

class GMessage:
        def __init__(self, text: str = "", markup: InlineKeyboardMarkup = None, photo:str =""):
            self._text   = text
            self._markup = markup 
            self._photo  = photo

        def getText(self)   -> str:                   return self._text            
        def getMarkup(self) -> InlineKeyboardMarkup:  return self._markup
        def getPhoto(self)   -> str:                  return self._photo            

        def setText(self, text: str):                      self._text   = text          
        def setMarkup(self, markup: InlineKeyboardMarkup): self._markup = markup          
        def setPhoto(self, photo: str):                    self._photo  = photo          

