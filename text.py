userGreet = """

Привет, <i>{userName}</i>!
Не хотите ли сыграть в добрую русскую <b>Виселицу</b>?:
"""

logUserStart = """
{firstName} {lastName} вошел в бот
"""

logBotStart = """
Бот Gallows запущен (загружено {wordCount} слов)
"""

logBotExit = """
Бот Gallows завершен (сигналом {sigNum})
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

botWord = """

Спасибо, <i>{userName}</i>!
Я (бот) обожаю загадывать слова. Если хотите, то можете определить число букв в слове, которое я Вам загадаю:
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

botRandomWord = """
Подбираю милое словцо: {percent}% ...
"""

logBotGuessWord = """
Бот задумал слово {guessedWord}
"""

botGuessStart = """
Я (бот) задумал слово из <b>{wordLen} букв(ы)</b>, см выше.

Какую букву открыть для Вас?:

"""

logUserGuessStart = """
{userName} задумал слов из {wordLen} букв
"""

userGuessFail = """
Чёрт! Опять я лоханулся с буквой <i>{prevChar}</i> и петля затянулась сильнее. 
Но Надежда еще жива!
Моя Надежда связана с <b>буквой <i>{guessedChar}</i></b>
{keyboardHelp}
"""
botGuessFail = """
Увы, <i>{userName}</i>! Я (бот) не смог найти с <b>букву <i>{guessedChar}</i></b> в своем слове. К сожалению, этот выбор \
не приблизил Вашу победу. 

Подумайте лучше, какую букву следут открыть?
"""

userGuessSuccess = """
Ура! Наконец, мне повезло с буквой <i>{prevChar}</i> и дышать стало чуть легче. 
Теперь хочу попробовать <b>букву <i>{guessedChar}</i></b>!
{keyboardHelp}
"""

botGuessSuccess = """
Поздравляю, <i>{userName}</i>!
В моем слове нашлась {charCount} <b>букв(а) <i>{guessedChar}</i></b>
Вы все ближе к Победе!
Какую букву открыть теперь?:
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

botBotWin = """
Дорогой(я) <i>{userName}</i>!
Буквы {guessedChar} также не оказалось в моем слове.
Поэтому Вы, к сожалению, превысили допустимое правилами игры число ошибок (не более {failureNumber}-ти).

Правильный ответ: <b><u>{guessedWord}</u></b>

Буду счастлив принять Ваши Поздравления!

Сыграем еще?
"""

logBotBotWin = """
{userName} не разгадал слово {guessedWord}({resolvedChars})
"""

userUserWin = """
Дорогой(я) <i>{userName}</i>!
Разгадывая Ваше заковыристое слово:

<b><u>{unknownWord}</u></b>

я (бот), к сожалению, превысил допустимое правилами игры число ошибок (не более {failureNumber}-ти).

Поздравляю Вас с блестящей Победой!
Сегодня Вам особенно везет!

Сыграем еще?
"""

botUserWin = """
Великолепно, <i>{userName}</i>!
Вы блестяще разгадали мое слово:

<b><u>{resolvedWord}</u></b>

Я восхищаюсь Вашими Способностями!

Сыграем еще?
"""

logBotUserWin = """
{userName} разгадал слово {guessedWord}
"""


logUserUserWin = """
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
Мои (бота) ошибки (<b>{failedCount}</b>): {failedChars}
Мои (бота) удачи (<b>{successCount}</b>): {successChars}
До Вашей победы: <b>{failureRemain} ошибки(ок)</b>
До моей (бота) победы: <b>{unresolveCount} неразгаданных букв(ы)</b>


"""

botGameState = """
Мое (бота) слово: <b><u>{resolvedChars}</u></b> ({wordLen} букв/ы)
Ваши ошибки (<b>{failedCount}</b>): {failedChars}
Ваши удачи (<b>{successCount}</b>): {successChars}
До Вашей победы: <b>{unresolveCount} неразгаданных букв(ы)</b>
До моей (бота) победы: <b>{failureRemain} ошибки</b>(ок)

"""

gameRules = """
Правила этой детской игры можно освежить <a href='https://ru.wikipedia.org/wiki/%D0%92%D0%B8%D1%81%D0%B5%D0%BB%D0%B8%D1%86%D0%B0_(%D0%B8%D0%B3%D1%80%D0%B0)'>тут</a>
"""





