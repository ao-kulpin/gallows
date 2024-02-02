from aiogram.utils.keyboard import InlineKeyboardMarkup

class GMessage:
        def __init__(self, text: str = "", markup: InlineKeyboardMarkup = None):
            self._text = text
            self._markup = markup 

        def getText(self)   -> str:                   return self._text            
        def getMarkup(self) -> InlineKeyboardMarkup:  return self._markup

        def setText(self, text: str):                      self._text   = text          
        def setMarkup(self, markup: InlineKeyboardMarkup): self._markup = markup          

