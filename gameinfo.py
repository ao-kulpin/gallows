import gmessage as gm
from aiogram.utils.keyboard import InlineKeyboardMarkup
from aiogram.types import Message

class GameData:
    def __init__(self, userName: str = "user") -> None:
        self.userName = userName
        self.userData = UserData()
        self.headGMsg = gm.GMessage()
        self.chatGMsg = gm.GMessage()
        self.headTMsg = None
        self.chatTMsg = None

    def setHeadText(self, text: str = ""):                      self.headGMsg.setText(text)
    def setChatText(self, text: str = ""):                      self.chatGMsg.setText(text)

    def setHeadPhoto(self, photo: str = ""):                     self.headGMsg.setPhoto(photo)

    def setChatMarkup(self, markup: InlineKeyboardMarkup = None): self.chatGMsg.setMarkup(markup)

    async def redrawAll(self, userMsg: Message):
        if self.chatTMsg == None:
            self.chatTMsg = await userMsg.answer(text=self.chatGMsg.getText(), 
                                           reply_markup=self.chatGMsg.getMarkup(), 
                                           parse_mode="html")
        else:
            await self.chatTMsg.edit_text(text=self.chatGMsg.getText(), 
                                           reply_markup=self.chatGMsg.getMarkup(), 
                                           parse_mode="html")
class UserData: pass        