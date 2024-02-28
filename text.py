userGreet = """

Привет, <i>{userName}</i>!
Не хотите ли сыграть в добрую русскую <b>Виселицу</b>?:
"""

logUserStart = """
{firstName} {lastName} вошел в бот
"""

choiseActor = """
Спасибо, <i>{userName}</i>, за Правильный выбор!
Определите пож-та кто загадает слово:
"""

userAway = """

Мне очень жаль, <i>{userName}</i>, что сегодня у Вас нет настроения побольше пообщаться со мной
Но я навсегда запомнил нашу Прекрасную Игру и нетерпением жду Новых Встреч с Вами!
"""

logUserAway = """
{userName} вышел из бота
"""

userWord = """

Спасибо, <i>{userName}</i>!
Определите пож-та число букв в Вашем слове:
"""

userGuessStart = """

Итак, в Вашем слове <b>{wordLen} букв(ы)</b>.
Отличный выбор! Попробую поугадывать...
Как насчет <b>буквы <i>{guessedChar}</i></b>?
{keyboardHelp}
"""
logUserGuessStart = """
{userName} задумал слов из {wordLen} букв
"""

userGuessFail = """
Чёрт! Опять я лоханулся с буквой <i>{prevChar}</i> и петля затянулась сильнее. 
Но Надежда еще жива!
Эта Надежда связана с <b>буквой <i>{guessedChar}</i></b>
{keyboardHelp}
"""

userGuessSuccess = """
Ура! Наконец мне повезло с буквой <i>{prevChar}</i> и дышать стало чуть легче. 
Давайте теперь попробуем <b>букву <i>{guessedChar}</i></b>
{keyboardHelp}
"""

userKeyboardHelp = """
Пож-та кликните мышкой (пальцем) над всеми ячейками (ниже) в которых есть буква <b><i>{guessedChar}</i></b>
Если Вы случайно открыли букву в неверной ячейке, то можете снова закрыть ее с помощью повторного клика по ней.
После того как Вы откроете все <i>{guessedChar}</i> (если они есть), нажмите кнопочку ниже, что таких букв (больше) нет.
"""


userBotWin = """
Дорогой(я) <i>{userName}</i>!
Похоже я, наконец, разгадал Ваше слово:

<b><u>{resolvedWord}</u></b>

К счастью, это произошло до полного затягивания петли на моей тонкой шее (осталось еще {failureRemain} ошибки/ок).

Буду счастлив принять Ваши Поздравления!

Сыграем еще?
"""

logUserBotWin = """
Бот разгадал слово {resolvedWord} (от {userName})
"""

userWin = """
Дорогой(я) <i>{userName}</i>!
Разгадывая Ваше заковыристое слово:

<b><u>{unknownWord}</u></b>

я, к сожалению, превысил допустимое правилами игры число ошибок (не более {failureNumber}-ти).

Поздравляю Вас с блестящей Победой!
Сегодня Вам особенно везет!

Сыграем еще?
"""

logUserWin = """
{userName} выиграл со словом {unknownWord}
"""

userUnknownWord = """
Дорогой(я) <i>{userName}</i>!
Сегодня у меня сильно болит голова и я не могу вспомнить ни одного слова такими буквами:

<b><u>{unknownWord}</u></b>

Вы блестяще знаете Русский Язык.
Поздравляю Вас с чистой Победой!

Сыграем еще?
"""

logUserUnknownWord = """
{userName} задал НЕИЗВЕСТНОЕ слово {unknownWord}
"""

userGameState = """
Ваше слово: <b><u>{resolvedChars}</u></b> ({wordLen} букв/ы)
Мои ошибки ({failedCount}): {failedChars}
Мои удачи ({successCount}): {successChars}
До Вашей победы еще: <b>{failureRemain} ошибки</b>(ок)


"""



