import gmessage as gm
from aiogram.utils.keyboard import InlineKeyboardMarkup
from aiogram.types import Message, FSInputFile, URLInputFile, BufferedInputFile, InputMediaPhoto


class GameData:
    def __init__(self, userName: str = "user") -> None:
        self.userName = userName
        self.userData = UserData()
        self.headGMsg = gm.GMessage()
        self.chatGMsg = gm.GMessage()
        self.headTMsg = None
        self.chatTMsg = None
        self.capCount = 0 #############################

    def setHeadText(self, text: str = ""):                      self.headGMsg.setText(text)
    def setChatText(self, text: str = ""):                      self.chatGMsg.setText(text)

    def setHeadPhoto(self, photo: str = ""):                     self.headGMsg.setPhoto(photo)

    def setChatMarkup(self, markup: InlineKeyboardMarkup = None): self.chatGMsg.setMarkup(markup)

    async def redrawMsg(self, userMsg: Message, tMsg: Message, gMsg: gm.GMessage) -> Message:
        updater = (tMsg.edit_media if gMsg.getPhoto() else tMsg.edit_text)  if tMsg else \
                  (userMsg.answer_photo  if gMsg.getPhoto() else userMsg.answer)
        parms = {"parse_mode": "html"}

        if gMsg.getPhoto():
            pf = FSInputFile(gMsg.getPhoto())
            if tMsg:
                parms["media"] = InputMediaPhoto(media=pf)
            else:
                parms["photo"] = pf
                parms["caption"] = gMsg.getText()
        else:
            parms["text"] = gMsg.getText()

        if gMsg.getMarkup():
            parms["reply_markup"] = gMsg.getMarkup()

        res = await updater(**parms) if not tMsg or not gMsg.getPhoto() else tMsg

        if tMsg and gMsg.getPhoto():
            await tMsg.edit_caption(caption=gMsg.getText() + str(self.capCount), parse_mode="HTML")
            self.capCount += 1

        return tMsg if tMsg else res

    async def redrawAll(self, userMsg: Message):
        self.headTMsg = await self.redrawMsg(userMsg, self.headTMsg, self.headGMsg)
        self.chatTMsg = await self.redrawMsg(userMsg, self.chatTMsg, self.chatGMsg)

class UserData: pass        