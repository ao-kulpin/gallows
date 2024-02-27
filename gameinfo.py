import gmessage as gm
from aiogram.utils.keyboard import InlineKeyboardMarkup
from aiogram.types import Message, FSInputFile, URLInputFile, BufferedInputFile, InputMediaPhoto
from aiogram.exceptions import TelegramBadRequest
from contextlib import suppress

class GameData:
    def __init__(self, userName: str = "user") -> None:
        self.userName = userName
        self.userData = UserData()
        self.headMsg = MessageHandle()
        self.chatMsg = MessageHandle()

    def setHeadText(self, text: str = ""):                      self.headMsg.gMsg.setText(text)
    def setChatText(self, text: str = ""):                      self.chatMsg.gMsg.setText(text)

    def setHeadPhoto(self, photo: str = ""):                     self.headMsg.gMsg.setPhoto(photo)

    def setChatMarkup(self, markup: InlineKeyboardMarkup = None): self.chatMsg.gMsg.setMarkup(markup)

    async def redrawAll(self, userMsg: Message):
        await self.headMsg.redraw(userMsg)
        await self.chatMsg.redraw(userMsg)

class UserData: pass     

class MessageHandle:
    def __init__(self) -> None:
        self.tMsg = None
        self.gMsg = gm.GMessage()
        self.changeCount = 0
        self.photoCount = 0

    async def redraw(self, userMsg: Message) -> None:
        with suppress(TelegramBadRequest):

            updater = (self.tMsg.edit_media if self.gMsg.getPhoto() else self.tMsg.edit_text)  if self.tMsg else \
                      (userMsg.answer_photo if self.gMsg.getPhoto() else userMsg.answer)
            newMsg:Message = None
        
            if not self.tMsg \
                or self.gMsg.getPhoto() and self.photoCount != self.gMsg.getPhotoCount() \
                or not self.gMsg.getPhoto() and self.changeCount != self.gMsg.getChangeCount():
                # the message is really changed

                updater = (self.tMsg.edit_media if self.gMsg.getPhoto() else self.tMsg.edit_text)  if self.tMsg else \
                          (userMsg.answer_photo if self.gMsg.getPhoto() else userMsg.answer)

                parms = {"parse_mode": "html"}
                if self.gMsg.getPhoto():
                    pf = FSInputFile(self.gMsg.getPhoto())
                    if self.tMsg:
                        parms["media"] = InputMediaPhoto(media=pf)
                    else:
                        parms["photo"] = pf
                        parms["caption"] = self.gMsg.getText()
                else:
                    parms["text"] = self.gMsg.getText()

                if self.gMsg.getMarkup():
                    parms["reply_markup"] = self.gMsg.getMarkup()

                if self.tMsg:
                    await updater(**parms)
                else:
                    newMsg = await updater(**parms)

                if self.gMsg.getPhoto():
                    self.photoCount = self.gMsg.getPhotoCount()

                if not self.gMsg.getPhoto() or not self.tMsg:
                    self.changeCount = self.gMsg.getChangeCount()

            if self.tMsg and self.gMsg.getPhoto() and self.changeCount != self.gMsg.getChangeCount():
                # caption of the photo is changed
                await self.tMsg.edit_caption(caption=self.gMsg.getText(), parse_mode="HTML")
                self.changeCount = self.gMsg.getChangeCount()

            if newMsg:
                self.tMsg = newMsg            



