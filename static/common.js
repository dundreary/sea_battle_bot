const LANG = {
 ru: {
 title: 'МОРСКОЙ БОЙ',
 rules: 'Правила',
 ok: 'OK',
 cancel: 'Отмена',
 startBtn: 'Начать игру',
 vsBot: 'С ботом',
 vsFriend: 'С другом',
 ownBoard: 'ТВОИ КОРАБЛИ',
 oppBoard: 'ДОСКА СОПЕРНИКА',
 legEmpty: 'пусто', legShip: 'корабль', legHit: 'попал', legMiss: 'мимо', legSunk: 'потоплен',
 welcome: 'Добро пожаловать!',
 placing: 'Расстановка — крути, пока не устроит',
 reroll: 'Переставить',
 confirm: 'OK ОК, начинаем!',
 rollTitle: 'Бросьте кубик — кто больше, тот ходит первым',
 rollBtn: 'Бросить кубик',
 rollYou: 'Ваш бросок',
 rollWait: 'Ожидание броска соперника…',
 rollWin: 'Вы ходите первым!',
 rollLose: 'Соперник ходит первым',
 rollTie: 'Ничья — бросайте ещё раз!',
 rollContinue: 'Продолжить',
 rollWon: 'Вы выиграли бросок!',
 rollLost: 'Соперник выиграл бросок',
 rollYouFirst: 'Вы ходите первым',
 rollOppFirst: 'Соперник ходит первым',
 rollWaitOpp: 'Ждём соперника…',
 rollRerolling: 'Переброс…',
 again: 'Ещё раз? Нажми «ОК» когда устроит',
 yourTurn: 'ТВОЙ ХОД!',
 oppTurn: 'ХОД СОПЕРНИКА...',
 message: 'Сообщение',
 messagePrompt: 'Сообщение сопернику (до 280 символов):',
 messageSent: 'Сообщение отправлено OK',
 messageError: 'Не удалось отправить сообщение',
 surrender: 'Сдаться',
 quit: 'Выйти',
 quitConfirm: 'Выйти из игры?',
 hit: 'Попадание!',
 sunk: 'Корабль потоплен!',
 miss: 'Мимо!',
 botHit: 'попал в',
 botSunk: 'потопил',
 botMiss: 'мимо',
 win: 'ПОБЕДА!',
 winDesc: 'Ты потопил все корабли соперника!',
 lose: 'ПОРАЖЕНИЕ',
 loseDesc: 'Все твои корабли потоплены...',
 draw: 'НИЧЬЯ',
 playAgain: 'Играть ещё',
 close: 'Закрыть',
 joinTitle: 'Присоединиться',
 joinBtn: 'Ввести код',
 joinPlaceholder: 'Введи код игры',
 joinError: '! Игра не найдена или уже полная',
 waitOpp: 'Ожидаем соперника...',
 codeShare: 'Код: <b>{}</b> — отправь другу',
 error: '! Ошибка соединения',
 errorShot: '! Сюда уже стреляли',
 gameOver: 'Игра закончилась.',
 gameInfo: '{code} {mode}',
 seaBattle: 'Морской бой',
 selectGame: 'Выбери режим',
 inviteFriend: 'Пригласить друга',
 ckInviteFriend: 'Пригласить друга',
 shareCopied: 'Код скопирован, отправь другу',
 copyCode: 'Нажми, чтобы скопировать код',
 settings: 'Настройки',
 theme: 'Тема',
 language: 'Язык',
 sound: 'Звук',
 vibration: 'Вибрация',
 shipHint: 'Корабли: {0}',
 mine: 'Мина',
 stripMode: 'На раздевание',
 stripTitle: 'Морской бой — На раздевание',
 stripPlace: 'Расставь корабли-одежду',
 stripDesc: 'Корабли могут быть любой формы!',
 stripInfoDesc: 'Фото отправится сопернику только если ты проиграешь.',
 stripLoseTitle: 'Игра окончена!',
 stripLoseDesc: 'Ты проиграл в режиме «На раздевание». Загрузи фото.',
 stripUploadTitle: 'Загрузи фото',
 stripUploadDesc: 'Выбери способ загрузки фото:',
 stripTakePhoto: 'Сделать фото',
 stripChoosePhoto: 'Из галереи',
 stripPhotoSent: 'Фото отправлено победителю OK',
 stripUseStandard: 'Стандартное фото',
 stripSkip: 'Пропустить',
 stripStakeBtn: 'Загрузить фото',
 stripStart: 'Удачи, начинаем',
 stripPlayAgain: 'Отыграться',
 rematchWin: 'Ещё партию',
 rematchLose: 'Отыграться',
 rematchWait: 'Ожидание соперника для реванша...',
 checkers: 'Шашки',
 ckHint: 'Подсказка',
 ckNoMoves: 'Нет ходов',
 backgammon: 'Нарды',
 bgSolo: 'Соло',
 bgRoll: 'Бросить',
 bgWaiting: 'Ожидаем соперника...',
 bgWin: 'Ты победил!',
 bgLose: 'Ты проиграл',
 bgPlayAgain: 'Играть ещё',
 bgYourTurn: 'ТВОЙ ХОД!',
 bgOppTurn: 'ХОД СОПЕРНИКА...',
 stMedium: 'Средне',
 stExpert: 'Эксперт',
 selectDifficulty: 'Выбери сложность',
 pdTitle: 'Покер в кости',
 pdSolo: 'Соло',
 pdRoll: 'Бросить',
 pdScore: 'Закончить',
 pdWaiting: 'Ожидаем соперника...',
 pdYourHand: 'Твоя рука',
 pdOppHand: 'Рука соперника',
 pdWin: 'Ты победил!',
 pdLose: 'Ты проиграл',
 pdDraw: 'Ничья',
 pdPlayAgain: 'Играть ещё',
 pdRollsLeft: 'Бросков: {}',
 pdResult: 'Результат: {}',
 pdPts: 'очк.',
 pdKeep: 'Закрепить',
 pdRound: 'Раунд {}',
 pdResultShort: 'Рез.',
 pdScorecard: 'Табло',
 pdScoreBtn: 'Очки',
 pdOpp: 'Сопер.',
 pdBonus: 'Бонус',
 pdTotal: 'Итого',
 pdChooseCat: 'Выбери категорию',
 pdCategoriesLeft: 'Осталось',
 pdMe: 'Я',
 pdOppMoves: 'Ходы соперника',
 pdThrow: 'Бросок',
 pdKept: 'оставил',
 pdDiscarded: 'сбросил',
 continue: 'Продолжить',
 minimize: 'Свернуть',
 activeGames: 'Активные игры',
 statsMenu: 'Статистика',
 statsTitle: 'Статистика',
 statsWins: 'Победы',
 statsLosses: 'Поражения',
 statsDraws: 'Ничьи',
 statsWinrate: 'Процент побед',
 resetStats: 'Сбросить статистику',
 resetStatsConfirm: 'Сбросить всю статистику? Это действие нельзя отменить.',
 statsTotal: 'Всего игр',
 statsHistory: 'Последние игры',
 statsNoGames: 'Пока нет сыгранных игр',
 statsResWin: 'Победа',
 statsResLoss: 'Поражение',
 statsResDraw: 'Ничья',
 bgVariantShort: 'Короткие',
 bgVariantLong: 'Длинные',
 playerName: 'Ваше имя',
 playerNamePlaceholder: 'Введите имя',
 ariaCell: 'Клетка {{0}}{{1}}',
 ckWhitePiece: 'белая шашка',
 ckBlackPiece: 'чёрная шашка',
 ckWhiteKing: 'белая шашка король',
 ckBlackKing: 'чёрная шашка король',
 ckKing: 'король',
 ckSelect: 'выбрать',
 ckMoveHere: 'ход сюда',
 bgWhiteChecker: 'шашка белых',
 bgBlackChecker: 'шашка чёрных',
 bgPointSelect: 'Пункт {{0}}, выбрать',
 bgPointMove: 'Пункт {{0}}, ход сюда',
 bgBarSelect: 'Бар, выбрать шашку',
 bgBearOff: 'Вывод (off), снять шашку',
 gameSaved: 'Игра сохранится',
 rulesSeaBattle: 'Расставь флот, стреляй по полю противника (A1–J10). Потопи все корабли первым. В соло бот ходит после тебя.',
 rulesPokerDice: '3 броска. Отмечай кости OK, чтобы оставить. Заполни табло категориями (Пары, Стриты, Покер и т.д.), набери больше очков.',
 rulesCheckers: 'Ходи по диагонали, бей прыжком. Дойди до края — станешь дамкой (). Сними все шашки противника.',
 rulesBackgammon: 'Бросай кости и веди шашки от своего края к своему дому, затем снимай (bear-off). Первым сними все — победа.',
 },
 uk: {
 title: 'Морський бій',
 rules: 'Правила',
 ok: 'OK',
 cancel: 'Скасувати',
 startBtn: 'Почати гру',
 vsBot: 'З ботом',
 vsFriend: 'З другом',
 ownBoard: 'ТВОЇ КОРАБЛІ',
 oppBoard: 'ДОШКА СУПЕРНИКА',
 legEmpty: 'порожньо', legShip: 'корабель', legHit: 'влучив', legMiss: 'повз', legSunk: 'потоплено',
 welcome: 'Ласкаво просимо!',
 placing: 'Розстановка — крути, поки не сподобається',
 reroll: 'Переставити',
 confirm: 'OK ОК, починаємо!',
 rollTitle: 'Киньте кубик — хто більше, той ходить першим',
 rollBtn: 'Кинути кубик',
 rollYou: 'Ваш кидок',
 rollWait: 'Очікування кидка суперника…',
 rollWin: 'Ви ходите першим!',
 rollLose: 'Суперник ходить першим',
 rollTie: 'Нічия — киньте ще раз!',
 rollContinue: 'Продовжити',
 rollWon: 'Ви виграли кидок!',
 rollLost: 'Суперник виграв кидок',
 rollYouFirst: 'Ви ходите першим',
 rollOppFirst: 'Суперник ходить першим',
 rollWaitOpp: 'Чекаємо на суперника…',
 rollRerolling: 'Перекинь…',
 again: 'Ще раз? Натисни «ОК» коли влаштує',
 yourTurn: 'ТВІЙ ХІД!',
 oppTurn: 'ХІД СУПЕРНИКА...',
 message: 'Повідомлення',
 messagePrompt: 'Повідомлення супернику (до 280 символів):',
 messageSent: 'Повідомлення надіслано OK',
 messageError: 'Не вдалося надіслати повідомлення',
 surrender: 'Здатися',
 quit: 'Вийти',
 quitConfirm: 'Вийти з гри?',
 hit: 'Влучив!',
 sunk: 'Корабель потоплено!',
 miss: 'Повз!',
 botHit: 'влучив у',
 botSunk: 'потопив',
 botMiss: 'повз',
 win: 'ПЕРЕМОГА!',
 winDesc: 'Ти потопив усі кораблі суперника!',
 lose: 'ПОРАЗКА',
 loseDesc: 'Усі твої кораблі потоплені...',
 draw: 'НІЧИЯ',
 playAgain: 'Грати ще',
 close: 'Закрити',
 joinTitle: 'Приєднатися',
 joinBtn: 'Ввести код',
 joinPlaceholder: 'Введи код гри',
 joinError: '! Гру не знайдено або вже повна',
 waitOpp: 'Чекаємо суперника...',
 codeShare: 'Код: <b>{}</b> — відправ другу',
 error: '! Помилка з\'єднання',
 errorShot: '! Сюди вже стріляли',
 gameOver: 'Гра закінчилась.',
 gameInfo: '{code} {mode}',
 seaBattle: 'Морський бій',
 selectGame: 'Обери режим',
 inviteFriend: 'Запросити друга',
 ckInviteFriend: 'Запросити друга',
 shareCopied: 'Код скопійовано, надішли другу',
 copyCode: 'Натисни, щоб скопіювати код',
 settings: 'Налаштування',
 theme: 'Тема',
 language: 'Мова',
 sound: 'Звук',
 vibration: 'Вібрація',
 shipHint: 'Кораблі: {0}',
 mine: 'Міна',
 stripMode: 'На роздягання',
 stripTitle: 'Морський бій — На роздягання',
 stripPlace: 'Розстав кораблі-одяг',
 stripDesc: 'Кораблі можуть бути будь-якої форми!',
 stripInfoDesc: 'Фото надішлеться супернику тільки якщо ти програєш.',
 stripLoseTitle: 'Гра закінчена!',
 stripLoseDesc: 'Ти програв у режимі «На роздягання». Завантаж фото.',
 stripUploadTitle: 'Завантаж фото',
 stripUploadDesc: 'Обери спосіб завантаження фото:',
 stripTakePhoto: 'Зробити фото',
 stripChoosePhoto: 'З галереї',
 stripPhotoSent: 'Фото надіслано переможцю OK',
 stripUseStandard: 'Стандартне фото',
 stripSkip: 'Пропустити',
 stripStakeBtn: 'Завантажити фото',
 stripStart: 'Удачі, починаємо',
 stripPlayAgain: 'Відігратись',
 rematchWin: 'Ще партію',
 rematchLose: 'Відігратись',
 rematchWait: 'Очікування суперника для реваншу...',
 checkers: 'Шашки',
 ckHint: 'Підказка',
 ckNoMoves: 'Немає ходів',
 backgammon: 'Нарди',
 bgSolo: 'Соло',
 bgRoll: 'Кинути',
 bgWaiting: 'Чекаємо суперника...',
 bgWin: 'Ти переміг!',
 bgLose: 'Ти програв',
 bgPlayAgain: 'Грати ще',
 bgYourTurn: 'ТВІЙ ХІД!',
 bgOppTurn: 'ХІД СУПЕРНИКА...',
 stMedium: 'Середньо',
 stExpert: 'Експерт',
 selectDifficulty: 'Обери складність',
 pdTitle: 'Покер у кості',
 pdSolo: 'Соло',
 pdRoll: 'Кинути',
 pdScore: 'Закінчити',
 pdWaiting: 'Чекаємо суперника...',
 pdYourHand: 'Твоя рука',
 pdOppHand: 'Рука суперника',
 pdWin: 'Ти переміг!',
 pdLose: 'Ти програв',
 pdDraw: 'Нічия',
 pdPlayAgain: 'Грати ще',
 pdRollsLeft: 'Кидків: {}',
 pdResult: 'Результат: {}',
 pdPts: 'очк.',
 pdKeep: 'Закріпити',
 pdRound: 'Раунд {}',
 pdResultShort: 'Рез.',
 pdScorecard: 'Табло',
 pdScoreBtn: 'Очки',
 pdOpp: 'Супер.',
 pdBonus: 'Бонус',
 pdTotal: 'Разом',
 pdChooseCat: 'Обери категорію',
 pdCategoriesLeft: 'Залишилось',
 pdMe: 'Я',
 pdOppMoves: 'Ходи суперника',
 pdThrow: 'Кидок',
 pdKept: 'залишив',
 pdDiscarded: 'скинув',
 continue: 'Продовжити',
 minimize: 'Згорнути',
 activeGames: 'Активні ігри',
 statsMenu: 'Статистика',
 statsTitle: 'Статистика',
 statsWins: 'Перемоги',
 statsLosses: 'Поразки',
 statsDraws: 'Нічиї',
 statsWinrate: 'Відсоток перемог',
 resetStats: 'Скинути статистику',
 resetStatsConfirm: 'Скинути всю статистику? Цю дію не можна скасувати.',
 statsTotal: 'Усього ігор',
 statsHistory: 'Останні ігри',
 statsNoGames: 'Поки що немає зіграних ігор',
 statsResWin: 'Перемога',
 statsResLoss: 'Поразка',
 statsResDraw: 'Нічия',
 bgVariantShort: 'Короткі',
 bgVariantLong: 'Довгі',
 playerName: 'Ваше ім\'я',
 playerNamePlaceholder: 'Введіть ім\'я',
 ariaCell: 'Клітинка {{0}}{{1}}',
 ckWhitePiece: 'біла шашка',
 ckBlackPiece: 'чорна шашка',
 ckWhiteKing: 'біла шашка король',
 ckBlackKing: 'чорна шашка король',
 ckKing: 'король',
 ckSelect: 'вибрати',
 ckMoveHere: 'хід сюда',
 bgWhiteChecker: 'шашка білих',
 bgBlackChecker: 'шашка чорних',
 bgPointSelect: 'Пункт {{0}}, вибрати',
 bgPointMove: 'Пункт {{0}}, хід сюда',
 bgBarSelect: 'Бар, вибрати шашку',
 bgBearOff: 'Вивід (off), зняти шашку',
 gameSaved: 'Гра збережеться',
 rulesSeaBattle: 'Розстав флот, стріляй по полю супротивника (A1–J10). Потопи всі кораблі першим. У соло бот ходить після тебе.',
 rulesPokerDice: '3 кидки. Позначай кістки OK, щоб залишити. Заповни табло категоріями (Пари, Стріті, Покер тощо), набери більше очок.',
 rulesCheckers: 'Ходи по діагоналі, бий стрибком. Дійди до края — станеш дамкою (). Зніми всі шашки супротивника.',
 rulesBackgammon: 'Кидай кістки і веди шашки від свого краю до свого дому, потім знімай (bear-off). Першим зніми всі — перемога.',
 },
 en: {
 title: 'Sea Battle',
 rules: 'Rules',
 ok: 'OK',
 cancel: 'Cancel',
 startBtn: 'Start Game',
 vsBot: 'Vs Bot',
 vsFriend: 'Vs Friend',
 ownBoard: 'YOUR SHIPS',
 oppBoard: 'OPPONENT\'S BOARD',
 legEmpty: 'empty', legShip: 'ship', legHit: 'hit', legMiss: 'miss', legSunk: 'sunk',
 welcome: 'Welcome aboard!',
 placing: 'Place ships — reroll until you like it',
 reroll: 'Reroll',
 confirm: 'OK OK, start!',
 rollTitle: 'Roll a die — higher goes first',
 rollBtn: 'Roll die',
 rollYou: 'Your roll',
 rollWait: 'Waiting for opponent to roll…',
 rollWin: 'You go first!',
 rollLose: 'Opponent goes first',
 rollTie: 'Tie — roll again!',
 rollContinue: 'Continue',
 rollWon: 'You won the roll!',
 rollLost: 'Opponent won the roll',
 rollYouFirst: 'You go first',
 rollOppFirst: 'Opponent goes first',
 rollWaitOpp: 'Waiting for opponent…',
 rollRerolling: 'Rerolling…',
 again: 'Again? Press «OK» when ready',
 yourTurn: 'YOUR TURN!',
 oppTurn: 'OPPONENT\'S TURN...',
 message: 'Message',
 messagePrompt: 'Message to your opponent (up to 280 characters):',
 messageSent: 'Message sent OK',
 messageError: 'Could not send message',
 surrender: 'Surrender',
 quit: 'Quit',
 quitConfirm: 'Leave the game?',
 hit: 'Hit!',
 sunk: 'Ship sunk!',
 miss: 'Miss!',
 botHit: 'hit at',
 botSunk: 'sunk at',
 botMiss: 'missed',
 win: 'VICTORY!',
 winDesc: 'You sank all enemy ships!',
 lose: 'DEFEAT',
 loseDesc: 'All your ships are sunk...',
 draw: 'DRAW',
 playAgain: 'Play again',
 close: 'Close',
 joinTitle: 'Join Game',
 joinBtn: 'Enter Code',
 joinPlaceholder: 'Enter game code',
 joinError: '! Game not found or full',
 waitOpp: 'Waiting for opponent...',
 codeShare: 'Code: <b>{}</b> — send to your friend',
 error: '! Connection error',
 errorShot: '! Already targeted',
 gameOver: 'Game over.',
 gameInfo: '{code} {mode}',
 seaBattle: 'Sea Battle',
 selectGame: 'Select mode',
 inviteFriend: 'Invite friend',
 ckInviteFriend: 'Invite friend',
 shareCopied: 'Code copied, send to friend',
 copyCode: 'Tap to copy code',
 settings: 'Settings',
 theme: 'Theme',
 language: 'Language',
 sound: 'Sound',
 vibration: 'Vibration',
 shipHint: 'Ships: {0}',
 mine: 'Mine',
 stripMode: 'Strip Mode',
 stripTitle: 'Sea Battle — Strip Mode',
 stripPlace: 'Place clothing ships',
 stripDesc: 'Ships can be any shape!',
 stripInfoDesc: 'The photo will be sent to your opponent only if you lose.',
 stripLoseTitle: 'Game Over!',
 stripLoseDesc: 'You lost in Strip Mode. Upload a photo.',
 stripUploadTitle: 'Upload Photo',
 stripUploadDesc: 'Choose how to upload a photo:',
 stripTakePhoto: 'Take Photo',
 stripChoosePhoto: 'From Gallery',
 stripPhotoSent: 'Photo sent to winner OK',
 stripUseStandard: 'Standard Photo',
 stripSkip: 'Skip',
 stripStakeBtn: 'Upload photo',
 stripStart: 'Good luck, let\'s begin',
 stripPlayAgain: 'Redeem',
 rematchWin: 'Another game',
 rematchLose: 'Replay',
 rematchWait: 'Waiting for opponent to rematch...',
 checkers: 'Checkers',
 ckHint: 'Hint',
 ckNoMoves: 'No moves',
 backgammon: 'Backgammon',
 bgSolo: 'Solo',
 bgRoll: 'Roll',
 bgWaiting: 'Waiting for opponent...',
 bgWin: 'You Win!',
 bgLose: 'You Lose',
 bgPlayAgain: 'Play again',
 bgYourTurn: 'YOUR TURN!',
 bgOppTurn: 'OPPONENT\'S TURN...',
 stMedium: 'Medium',
 stExpert: 'Expert',
 selectDifficulty: 'Choose difficulty',
 pdTitle: 'Poker Dice',
 pdSolo: 'Solo',
 pdRoll: 'Roll',
 pdScore: 'Score',
 pdWaiting: 'Waiting for opponent...',
 pdYourHand: 'Your Hand',
 pdOppHand: 'Opponent\'s Hand',
 pdWin: 'You Win!',
 pdLose: 'You Lose',
 pdDraw: 'Draw',
 pdPlayAgain: 'Play again',
 pdRollsLeft: 'Rolls: {}',
 pdResult: 'Result: {}',
 pdPts: 'pts',
 pdKeep: 'Keep',
 pdRound: 'Round {}',
 pdResultShort: 'Res.',
 pdScorecard: 'Scorecard',
 pdScoreBtn: 'Score',
 pdOpp: 'Opp.',
 pdBonus: 'Bonus',
 pdTotal: 'Total',
 pdChooseCat: 'Choose category',
 pdCategoriesLeft: 'Left',
 pdMe: 'Me',
 pdOppMoves: "Opponent's Moves",
 pdThrow: 'Throw',
 pdKept: 'kept',
 pdDiscarded: 'discarded',
 continue: 'Continue',
 minimize: 'Minimize',
 activeGames: 'Active games',
 statsMenu: 'Stats',
 statsTitle: 'Statistics',
 statsWins: 'Wins',
 statsLosses: 'Losses',
 statsDraws: 'Draws',
 statsWinrate: 'Win rate',
 resetStats: 'Reset statistics',
 resetStatsConfirm: 'Reset all statistics? This cannot be undone.',
 statsTotal: 'Total games',
 statsHistory: 'Recent games',
 statsNoGames: 'No games played yet',
 statsResWin: 'Win',
 statsResLoss: 'Loss',
 statsResDraw: 'Draw',
 bgVariantShort: 'Short',
 bgVariantLong: 'Long',
 playerName: 'Your name',
 playerNamePlaceholder: 'Enter your name',
 ariaCell: 'Cell {{0}}{{1}}',
 ckWhitePiece: 'white piece',
 ckBlackPiece: 'black piece',
 ckWhiteKing: 'white king',
 ckBlackKing: 'black king',
 ckKing: 'king',
 ckSelect: 'select',
 ckMoveHere: 'move here',
 bgWhiteChecker: 'white checker',
 bgBlackChecker: 'black checker',
 bgPointSelect: 'Point {{0}}, select',
 bgPointMove: 'Point {{0}}, move here',
 bgBarSelect: 'Bar, select checker',
 bgBearOff: 'Bear off, remove checker',
 gameSaved: 'Game will be saved',
 rulesSeaBattle: 'Deploy your fleet, shoot at the enemy grid (A1–J10). Sink all ships first. In solo the bot moves after you.',
 rulesPokerDice: '3 rolls. Mark dice OK to keep them. Fill the scorecard with categories (Pairs, Straights, Poker, etc.) and score more points.',
 rulesCheckers: 'Move diagonally, capture by jumping. Reach the far row to become a King (). Capture all opponent pieces.',
 rulesBackgammon: 'Roll dice and move checkers from your edge to your home, then bear them off. First to bear off all checkers wins.',
 }
};

const API = window.location.origin;
let state = null, uid = null, gameCode = null, lang = 'ru';
let botUsername = '';

function $(id){return document.getElementById(id)}

function hideAllGameAreas(){
 $('ownBoardWrap').classList.add('hidden');
 $('oppBoardWrap').classList.add('hidden');
 $('pdArea').style.display='none';
 $('ckArea').style.display='none';
 $('bgArea').style.display='none';
 const _sh=$('shipHint'); if(_sh) _sh.innerHTML='';
}

let _snd=localStorage.getItem('sb_snd')!=='0',_vibe=localStorage.getItem('sb_vibe')!=='0';
let _actx=null;
function actx(){if(!_actx)_actx=new(window.AudioContext||window.webkitAudioContext)();return _actx}
function tone(f,d,t='sine',v=0.15){if(!_snd)return;try{const c=actx(),o=c.createOscillator(),g=c.createGain();o.type=t;o.frequency.value=f;g.gain.setValueAtTime(v,c.currentTime);g.gain.exponentialRampToValueAtTime(0.001,c.currentTime+d);o.connect(g).connect(c.destination);o.start();o.stop(c.currentTime+d)}catch(e){}}
function haptic(s){if(!_vibe)return;try{const h=window.Telegram?.WebApp?.HapticFeedback;if(h)h.impactOccurred(s)}catch(e){}}
function hapticN(t){if(!_vibe)return;try{const h=window.Telegram?.WebApp?.HapticFeedback;if(h)h.notificationOccurred(t)}catch(e){}}
function sfxHit(){tone(800,0.08,'square',0.12);haptic('medium')}
function sfxMiss(){tone(200,0.12,'sine',0.08);haptic('light')}
function sfxSunk(){tone(500,0.15,'square',0.1);setTimeout(()=>tone(300,0.15,'square',0.1),100);setTimeout(()=>tone(150,0.2,'square',0.1),200);haptic('heavy')}
function sfxPlace(){tone(400,0.04,'sine',0.06);haptic('light')}
function sfxWin(){tone(523,0.15,'sine',0.1);setTimeout(()=>tone(659,0.15,'sine',0.1),150);setTimeout(()=>tone(784,0.3,'sine',0.1),300);hapticN('success')}
function sfxLose(){tone(400,0.2,'sine',0.08);setTimeout(()=>tone(300,0.2,'sine',0.08),200);setTimeout(()=>tone(200,0.4,'sine',0.08),400);hapticN('error')}
function sfxChime(){tone(1000,0.25,'sine',0.12);haptic('medium')}
function sfxClick(){tone(600,0.02,'sine',0.04);haptic('light')}
function sfxTick(){tone(1200,0.04,'sine',0.06)}
function sfxRoll(){if(!_snd)return;for(let i=0;i<8;i++){const delay=i*70;setTimeout(()=>tone(800+Math.random()*400,0.03,'square',0.04),delay)}}

// ---- AI "thinking" + reveal UX ------------------------------------------------
// In solo games the AI move is computed on the server and returned together with
// the player's own move. To remove the "did I move or is it lagging?" confusion
// we show an explicit "AI is thinking" beat, then reveal what the AI did
// (the dice it threw, the pieces it moved / dice it kept). These helpers are
// also reused to surface an opponent's action the moment a poll delivers it.
function _aiDelay(ms){ return new Promise(r => setTimeout(r, ms)); }
function showRevealBanner(html){
 const b = document.createElement('div');
 b.className = 'ai-reveal-banner';
 b.innerHTML = html;
 document.body.appendChild(b);
 requestAnimationFrame(() => b.classList.add('show'));
 setTimeout(() => { b.classList.remove('show'); setTimeout(() => b.remove(), 400); }, 2400);
}

// Small, non-blocking "AI is thinking" overlay for games that compute the bot's
// move on the server (Checkers / Backgammon). pointer-events:none so it never
// intercepts taps on the board. Always paired with hideAiThinking() in a
// finally block so it clears even on error.
let _aiThinkEl = null;
function showAiThinking(msg){
 hideAiThinking();
 const o = document.createElement('div');
 o.className = 'ai-think-overlay';
 o.innerHTML = `<div class="ai-think-box"> ${msg || {ru:'Думает…',uk:'Думає…',en:'Thinking…'}[lang]}</div>`;
 document.body.appendChild(o);
 _aiThinkEl = o;
}
function hideAiThinking(){
 if(_aiThinkEl){ _aiThinkEl.remove(); _aiThinkEl = null; }
}

function toggleSnd(){_snd=!_snd;localStorage.setItem('sb_snd',_snd?'1':'0');updateSettingsUI()}
function toggleVibe(){_vibe=!_vibe;localStorage.setItem('sb_vibe',_vibe?'1':'0');updateSettingsUI()}
function updateSettingsUI(){
 const sndBtn=document.getElementById('sndBtn');
 const vibeBtn=document.getElementById('vibeBtn');
 const sndBtnPd=document.getElementById('sndBtnPd');
 const vibeBtnPd=document.getElementById('vibeBtnPd');
 const sndBtnCk=document.getElementById('sndBtnCk');
 const vibeBtnCk=document.getElementById('vibeBtnCk');
 const chk = on => on ? 'OK': '';
 const sndIcon=chk(_snd), vibeIcon=chk(_vibe);
 if(sndBtn)sndBtn.textContent=sndIcon;
 if(vibeBtn)vibeBtn.textContent=vibeIcon;
 if(sndBtnPd)sndBtnPd.textContent=sndIcon;
 if(vibeBtnPd)vibeBtnPd.textContent=vibeIcon;
 if(sndBtnCk)sndBtnCk.textContent=sndIcon;
 if(vibeBtnCk)vibeBtnCk.textContent=vibeIcon;
}
function setThemeSelectorVisibility(visible){
 const el=$('themeSelector'); if(!el)return;
 el.style.display=visible?'flex':'none';
}

function setTheme(themeName){
 const validThemes = ['ocean', 'forest'];
 if(!validThemes.includes(themeName)) return;

 document.documentElement.className = 'palette-'+ themeName;
 localStorage.setItem('sb_theme', themeName);

 const btns = document.querySelectorAll('.theme-btn');
 btns.forEach(btn => {
 btn.classList.remove('active');
 if(btn.dataset.theme === themeName) btn.classList.add('active');
 });
}

function initTheme(){
 const saved = localStorage.getItem('sb_theme') || 'ocean';
 setTheme(saved);
}

function showSettings(){
 document.querySelectorAll('.overlay').forEach(o=>o.remove()); // clear stray modal if a nav happens while one is open
 setStripLockVisible(false);
 currentGameType=null; setHelpVisible(false);
 currentScreen='settings';
 try{ if(typeof window.Telegram!=='undefined'&& window.Telegram.WebApp && window.Telegram.WebApp.BackButton) window.Telegram.WebApp.BackButton.show(); }catch(e){}
 const existing=$('settingsOverlay');
 if(existing){existing.remove()}
 const o=document.createElement('div');o.className='overlay';o.id='settingsOverlay';
 const curTheme = document.documentElement.className.indexOf('forest')>=0 ? 'forest': 'ocean';
 const chk = on => on ? 'OK': '';
 const AR = `role="button" tabindex="0" onkeydown="if(event.key==='Enter'||event.key===''){event.preventDefault();this.click()}"`;
 o.innerHTML=`
 <div class="modal settings-compact">
 <h2> ${t('settings')}</h2>

 <div class="sett-sec">${t('theme')}</div>
 <div class="sett-chips">
 <button class="sett-chip ${curTheme==='ocean'?'on':''}" ${AR} onclick="setTheme('ocean');showSettings()"> Ocean</button>
 <button class="sett-chip ${curTheme==='forest'?'on':''}" ${AR} onclick="setTheme('forest');showSettings()"> Forest</button>
 </div>

 <div class="sett-sec">${t('sound')} / ${t('vibration')}</div>
 <div class="sett-chips">
 <button class="sett-chip ${_snd?'on':''}" ${AR} onclick="toggleSnd();showSettings()"> ${t('sound')}</button>
 <button class="sett-chip ${_vibe?'on':''}" ${AR} onclick="toggleVibe();showSettings()"> ${t('vibration')}</button>
 </div>

 <div class="sett-sec">${t('selectDifficulty')}</div>
 <div class="sett-chips">
 <button class="sett-chip ${gameDifficulty===2?'on':''}" ${AR} onclick="setDifficulty(2);showSettings()"> ${t('stMedium')}</button>
 <button class="sett-chip ${gameDifficulty===4?'on':''}" ${AR} onclick="setDifficulty(4);showSettings()"> ${t('stExpert')}</button>
 </div>

 <div class="sett-sec">${t('language')}</div>
 <div class="sett-chips">
 <button class="sett-chip ${lang==='ru'?'on':''}" ${AR} onclick="setLang('ru');showSettings()">RU RU</button>
 <button class="sett-chip ${lang==='uk'?'on':''}" ${AR} onclick="setLang('uk');showSettings()">UA UA</button>
 <button class="sett-chip ${lang==='en'?'on':''}" ${AR} onclick="setLang('en');showSettings()">EN EN</button>
 </div>
 <div class="sett-name-row">
 <span class="sett-sec" style="padding:0"> ${t('playerName')||'Ваше имя'}</span>
 <input id="nameInput" class="sett-input" maxlength="24" value="${getPlayerName().replace(/"/g,'&quot;')}" oninput="savePlayerName(this.value)" placeholder="${t('playerNamePlaceholder')||'Введите имя'}" />
 </div>
 <button class="btn outline settings-close" onclick="this.closest('.overlay').remove()">${t('close')}</button>
 </div>`;
 document.body.appendChild(o);
}

function detectLang(){
 try{
 const tg = window.Telegram.WebApp.initDataUnsafe?.user?.language_code || 'ru';
 if(tg.startsWith('uk'))return 'uk';
 }catch(e){}
 const nav = (navigator.language || '').slice(0,2);
 if(nav==='uk')return'uk';
 if(nav==='en')return'en';
 try{var s=localStorage.getItem('sb_lang');if(s)return s}catch(e){}
 return 'ru';
}

function t(key, ...args){
 let s = LANG[lang][key] || LANG.ru[key] || key;
 if(args.length){
 s = s.replace(/\{\{(\d+)\}\}/g, (m,i)=> (args[+i]!==undefined?args[+i]:m))
 .replace(/\{(\d+)\}/g, (m,i)=> (args[+i]!==undefined?args[+i]:m));
 }
 return s;
}

function setLang(l){
 lang = l;
 try{localStorage.setItem('sb_lang', l)}catch(e){}
 document.querySelectorAll('.lang-btn').forEach(b => b.classList.toggle('active', b.dataset.lang === l));
 applyLang();
 if(state) updateUI();
}

function applyLang(){
 $('lblOwn').textContent = t('ownBoard');
 $('lblOpp').textContent = t('oppBoard');
 if(!state && !gameCode) showMenu();
 else document.title=t('title')
}

function initTG(){
 try{
 const tg = window.Telegram && window.Telegram.WebApp ? window.Telegram.WebApp : null;
 if(!tg) return;
 tg.ready(); tg.expand();
 if(typeof tg.BackButton !== 'undefined'&& tg.BackButton){
 try{ tg.BackButton.onClick(()=>{ if(typeof window.__sbBack === 'function') window.__sbBack(); }); }catch(e){}
 }
 }catch(e){}
}
// Browsers (and especially Telegram's WebView) suspend the AudioContext until
// a user gesture occurs. Resume it once, on the first pointer interaction, so
// SFX are not silently dropped after a navigation/refresh.
document.addEventListener('pointerdown', function(){ try{ const a=actx(); if(a&&a.resume) a.resume(); }catch(e){} }, {once:true});
function getUid(){
 if(uid)return uid;
 try{uid=window.Telegram.WebApp.initDataUnsafe?.user?.id||localStorage.getItem('sb_uid')||Date.now()}catch(e){uid=localStorage.getItem('sb_uid')||Date.now()}
 localStorage.setItem('sb_uid',uid);
 return uid
}

function setStatus(text,cls=''){const s=$('status');s.innerHTML=text;s.className='status'+(cls?' '+cls:'')}

let gameMessageQueue=[];
function showIncomingMessages(messages){
 if(Array.isArray(messages)&&messages.length) gameMessageQueue.push(...messages);
 if(document.querySelector('.game-message-overlay')||!gameMessageQueue.length)return;
 const text=gameMessageQueue.shift();
 const o=document.createElement('div');
 o.className='overlay game-message-overlay';
 const modal=document.createElement('div');
 modal.className='modal';
 const title=document.createElement('h2'); title.textContent=''+t('message');
 const body=document.createElement('p'); body.style.whiteSpace='pre-wrap'; body.textContent=text;
 const close=document.createElement('button'); close.className='btn primary'; close.style.width='100%'; close.textContent='OK';
 close.onclick=()=>{o.remove();showIncomingMessages([])};
 modal.append(title,body,close); o.appendChild(modal); document.body.appendChild(o);
}

// ---- In-app confirm/prompt (replace native browser dialogs) ----------------
function confirmDialog(title, message, onYes, yesLabel, noLabel){
 yesLabel = yesLabel || t('ok');
 noLabel = noLabel || t('cancel');
 const o=document.createElement('div'); o.className='overlay';
 o.innerHTML=`<div class="modal"><h2>${title}</h2><p>${message}</p>
 <button class="btn success" style="width:100%;margin:6px 0" id="cdYes">${yesLabel}</button>
 <button class="btn outline" style="width:100%;margin:6px 0" id="cdNo">${noLabel}</button></div>`;
 document.body.appendChild(o);
 const yesBtn=o.querySelector('#cdYes');
 const noBtn=o.querySelector('#cdNo');
 yesBtn.onclick=()=>{ o.remove(); onYes(); };
 noBtn.onclick=()=>{ o.remove(); };
 yesBtn.focus();
 o.addEventListener('keydown',(e)=>{
 if(e.key==='Escape'){ e.preventDefault(); o.remove(); return; }
 if(e.key==='Tab'){
 const f=[yesBtn,noBtn], first=f[0], last=f[f.length-1];
 if(e.shiftKey && document.activeElement===first){ e.preventDefault(); last.focus(); }
 else if(!e.shiftKey && document.activeElement===last){ e.preventDefault(); first.focus(); }
 }
 });
}

function promptDialog(title, placeholder, onDone){
 const o=document.createElement('div'); o.className='overlay';
 o.innerHTML=`<div class="modal"><h2>${title}</h2>
 <input id="pdInput" class="sett-input" maxlength="64" placeholder="${placeholder}">
 <button class="btn success" style="width:100%;margin:6px 0" id="pdOk">OK</button>
 <button class="btn outline" style="width:100%;margin:6px 0" id="pdNo">${t('cancel')}</button></div>`;
 document.body.appendChild(o);
 const inp=o.querySelector('#pdInput');
 const okBtn=o.querySelector('#pdOk');
 const noBtn=o.querySelector('#pdNo');
 inp.focus();
 const done=()=>{ const v=inp.value.trim(); o.remove(); if(v) onDone(v); };
 okBtn.onclick=done;
 noBtn.onclick=()=>{ o.remove(); };
 inp.addEventListener('keydown',e=>{ if(e.key==='Enter') done(); });
 o.addEventListener('keydown',(e)=>{
 if(e.key==='Escape'){ e.preventDefault(); o.remove(); return; }
 if(e.key==='Tab'){
 const f=[inp,okBtn,noBtn], first=f[0], last=f[f.length-1];
 if(e.shiftKey && document.activeElement===first){ e.preventDefault(); last.focus(); }
 else if(!e.shiftKey && document.activeElement===last){ e.preventDefault(); first.focus(); }
 }
 });
}

// Retry helper for network failures after api()'s internal retry has been
// exhausted. Renders a small tappable "" in the status line; clicking it
// re-runs the failed action (e.g. a shot) without losing game state.
let _retryFn=null;
function showRetry(msg, fn){
 _retryFn=fn;
 setStatus(`${msg} <span id="retryBtn" style="display:inline-block;margin-left:8px;padding:4px 10px;border:1px solid var(--accent-primary);border-radius:6px;cursor:pointer"></span>`,'battle');
 const b=document.getElementById('retryBtn'); if(b) b.onclick=()=>{ if(_retryFn) _retryFn(); };
}

// Localized reassurance shown on the "minimize" (Свернуть) button: the game
// is only minimized, not ended, so progress is saved.
function minimizeTitle(){ return {ru:'Игра сохранится',uk:'Гру збережено',en:'Game will be saved'}[lang]||'Game will be saved'; }

async function api(method,data,_isRetry){
 try{
 data = data || {};
 data.lang = lang;
 try{ data.init_data = window.Telegram.WebApp.initData || ''; }catch(e){ data.init_data = ''; }
 const ctrl = new AbortController();
 const to = setTimeout(()=>ctrl.abort(), 8000);
 let r;
 try{
 r = await fetch(API+method,{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify(data),signal:ctrl.signal});
 } finally { clearTimeout(to); }
 return await r.json();
 }catch(e){
 if(!_isRetry){ await new Promise(res=>setTimeout(res,800)); return api(method,data,true); }
 return null;
 }
}

async function fetchBotInfo(retries=10){
 try {
 const res = await api('/api/bot_info', {});
 if(res && res.ok && res.bot_username){
 botUsername = res.bot_username;
 } else if(retries > 0) {
 await new Promise(r => setTimeout(r, 500));
 return fetchBotInfo(retries - 1);
 }
 } catch(e){}
}

function renderBoard(boardEl,grid,isOpponent,gameOver, shipsData, isStrip){
 boardEl.setAttribute('role','grid');
 const EMPTY=0,SHIP=1,HIT=2,MISS=3,SUNK=4,DEAD=5,MINE=6,MINE_HIT=7;
 const COLS='ABCDEFGHIJ';
 // Screen-reader labels for each cell, kept in the currently selected UI
 // language. Purely additive (aria-label + keyboard activation for
 // shootable cells) -- doesn't change the existing visual/click behaviour.
 const STATE_LABEL=({
 ru:{empty:'пусто',ship:'корабль',hit:'попадание',miss:'мимо',sunk:'потоплен',mine:'мина'},
 uk:{empty:'порожньо',ship:'корабель',hit:'влучання',miss:'повз',sunk:'потоплено',mine:'міна'},
 en:{empty:'empty',ship:'ship',hit:'hit',miss:'miss',sunk:'sunk',mine:'mine'},
 })[lang] || {empty:'empty',ship:'ship',hit:'hit',miss:'miss',sunk:'sunk',mine:'mine'};

 // Build the 100 cell nodes exactly once so DOM identity (and therefore
 // keyboard focus) is preserved across re-renders -- this is the A11Y-2 fix
 // and also avoids a full reflow on every poll refresh.
 if(boardEl.childElementCount !== 100){
 boardEl.innerHTML='';
 for(let r=0;r<10;r++)for(let c=0;c<10;c++){
 const cell=document.createElement('div');
 cell.className='cell';
 cell.dataset.r=r;
 cell.dataset.c=c;
 boardEl.appendChild(cell);
 }
 }

 const cells = boardEl.children;
 for(let i=0;i<100;i++){
 const cell=cells[i];
 const r=+cell.dataset.r, c=+cell.dataset.c;
 const v=grid[i];
 cell.className='cell';
 cell.textContent='';
 let sw=STATE_LABEL.empty;
 if(v===EMPTY||v===SHIP||v===MINE){cell.classList.add('empty');if(v===SHIP){cell.classList.add(isStrip?'strip-ship':'ship');sw=STATE_LABEL.ship;if(isOpponent&&gameOver)cell.classList.add('enemy-reveal')}else if(v===MINE){cell.classList.add('mine');sw=STATE_LABEL.mine;if(isOpponent&&gameOver)cell.classList.add('enemy-reveal')}}
 else if(v===HIT){cell.classList.add('hit');cell.textContent='X';sw=STATE_LABEL.hit}
 else if(v===MINE_HIT){cell.classList.add('mine');sw=STATE_LABEL.mine;if(isOpponent&&gameOver)cell.classList.add('enemy-reveal')}
 else if(v===MISS){cell.classList.add('miss');cell.textContent='·';sw=STATE_LABEL.miss}
 else if(v===SUNK){cell.classList.add('sunk');cell.textContent='X';sw=STATE_LABEL.sunk}
 else if(v===DEAD){cell.classList.add('dead');cell.textContent='·'}
 else cell.classList.add('empty');
 // Highlight the opponent's most recent shot on the HUMAN's OWN board
 // (bot_shots land on ownBoard), analogous to the Checkers/Backgammon
 // "last move" flashes. Cleared automatically on the next render because
 // we reset className at the top of the loop.
 if(!isOpponent && state && state._lastOppShot && state._lastOppShot.r===r && state._lastOppShot.c===c){
 cell.classList.add('enemy-last');
 }
 cell.setAttribute('aria-label', COLS[c]+(r+1)+': '+sw);
 const shootable = isOpponent&&!gameOver&&(v===EMPTY||v===SHIP);
 if(shootable){
 cell.classList.add('shootable');
 cell.setAttribute('role','button');
 cell.tabIndex=0;
 if(!cell._wired){
 cell.onclick=()=>handleShot(+cell.dataset.r,+cell.dataset.c);
 cell.onkeydown=(e)=>{ if(e.key==='Enter'||e.key===''){ e.preventDefault(); handleShot(+cell.dataset.r,+cell.dataset.c); } };
 cell._wired=true;
 }
 }else{
 cell.classList.remove('shootable');
 cell.removeAttribute('role');
 cell.tabIndex=-1;
 cell.onclick=null;
 cell.onkeydown=null;
 cell._wired=false;
 }
 }
}

async function refreshState(){
 if(!gameCode)return;
 if(_sbRefreshing)return; // a previous poll is still in flight; skip
 _sbRefreshing=true;
 try{
 const res=await api('/api/state',{uid:getUid(),code:gameCode});
 if(res === null){
 // transient network failure (api already retried once) — keep the saved game,
 // just tell the user we're reconnecting; the poll will retry.
 notePollResult('sea_battle', false);
 setStatus({ru:'Переподключение…',uk:'Перепідключення…',en:'Reconnecting…'}[lang], '');
 return;
 }
 if(!res.ok){
 localStorage.removeItem('sb_game');
 setStatus(t('gameOver'));
 $('actions').className='btn-row';
 $('actions').innerHTML=`<button class="btn primary" onclick="startSolo()">${t('startBtn')}</button>`;
 return;
 }
 notePollResult('sea_battle', true);
 if(!gameCode)return;
 state=res.state;
 // Dedup idle polls: only re-render when something actually changed.
 const sig = JSON.stringify([state.own,state.opp,state.turn,state.phase,state.my_roll,state.opp_roll,state.all_sunk,state.my_all_sunk,state.ready,state.solo]);
 if(sig===_lastSBSig) return; // idle poll: nothing changed, skip full re-render
 _lastSBSig = sig;
 updateUI();
 } finally {
 _sbRefreshing=false;
 }
}

// ---- Opening dice roll (multiplayer: decides who moves first) --------------
// Redesigned: both dice (mine + opponent's) are visible together from the
// moment the roll phase starts, in a single "Roll" screen, instead of the
// old flow where the opponent's die only appeared after they'd already
// rolled. A tie shows an explicit "Reroll" button (see reroll_first on the
// server) rather than silently auto-clearing and hoping the player notices.
const DIE_PIPS = {
 1: [[50,50]],
 2: [[28,28],[72,72]],
 3: [[28,28],[50,50],[72,72]],
 4: [[28,28],[28,72],[72,28],[72,72]],
 5: [[28,28],[28,72],[50,50],[72,28],[72,72]],
 6: [[28,28],[28,50],[28,72],[72,28],[72,50],[72,72]],
};
function diceFace(n){ return (n>=1&&n<=6) ? String(n) : '?'; }

function _dieSvg(n, extraClass){
 const pips = DIE_PIPS[n] || [];
 const dots = pips.map(([x,y]) => `<circle cx="${x}" cy="${y}" r="9"></circle>`).join('');
 return `<div class="roll-die3d${extraClass ? ' '+extraClass : ''}"><svg viewBox="0 0 100 100">${dots}</svg></div>`;
}

// ---- Opening roll MODAL POPUP --------------------------------------------
// Replaces the inline firstRollHTML rendering. Shows BOTH dice (yours +
// opponent's) in a centered modal and owns the whole opening-roll flow: the
// PvP "waiting for opponent" transition, the tie auto-reroll, and the
// decisive "Continue" step. It is idempotent: if the overlay already exists
// its inner content is re-rendered from the new state so polling refreshes
// update it instead of stacking duplicate popups.
let _rollPopupEl = null;
let _rollPopupCode = null;
let _rollPopupProceed = null;
const _rollPopupClosed = {}; // code -> true once the PvP "waiting" popup closed
const _rollAutoRerollCount = {}; // code -> auto-reroll attempts so far (cap)
const _rollPopupIntroDone = {}; // code -> true after first board reveal delay
let _rollWaitScheduled = false;
let _rollWaitTimer = null;
let _rollRerollScheduled = false;
let _rollRerollTimer = null;
let _rollProceedScheduled = false;
let _rollProceedTimer = null;

function _rollPopupInner(st, rollFn, rerollFn, o){
 const solo = o.solo;
 const label = (txt, sub)=>`<div class="roll-die-label">${txt}${sub?`<span>${sub}</span>`:''}</div>`;
 const mySide = (n, waiting)=>`<div class="roll-die-col">${_dieSvg(n||1, waiting?'roll-die-pending':'')}${label(t('rollYou'))}</div>`;
 const oppSide = (n, waiting)=>`<div class="roll-die-col">${_dieSvg(n||1, waiting?'roll-die-pending':'')}${label('')}</div>`;
 const dieRow = `<div class="roll-die-row">${mySide(st.my_roll, st.my_roll==null)}<div class="roll-vs">VS</div>${oppSide(st.opp_roll, st.opp_roll==null)}</div>`;

 // Each branch fills titleSlot (top, fixed height) and footSlot (bottom, fixed height).
 // The dice row is always rendered in the middle fixed slot -> constant vertical position.
 let titleSlot = '';
 let footSlot = '';

 if(st.my_roll==null && st.opp_roll==null){
 titleSlot = `<div class="roll-title">${t('rollTitle')}</div>`;
 footSlot = `<button class="btn primary roll-cta" id="rollBtn" onclick="window['${rollFn}']()">${t('rollBtn')}</button>`;
 }
 else if(!solo && st.my_roll!=null && st.opp_roll==null){
 footSlot = `<div class="roll-wait">${t('rollWaitOpp')}</div><button class="btn outline roll-cta" id="closeRollBtn" onclick="__rollPopupCloseWait()">${t('close')}</button>`;
 }
 else if(st.my_roll!=null && st.opp_roll!=null && st.my_roll===st.opp_roll){
 const count = o.code ? (_rollAutoRerollCount[o.code]||0) : 0;
 if(count >= 6){
 footSlot = `<div class="roll-result roll-tie">${t('rollTie')}</div><button class="btn primary roll-cta" id="rerollBtn" onclick="window['${rerollFn}']()"> ${t('reroll')}</button>`;
 } else {
 footSlot = `<div class="roll-result roll-tie">${t('rollRerolling')}</div>`;
 }
 }
 else if(st.my_roll==null && st.opp_roll!=null){
 titleSlot = `<div class="roll-title">${t('rollTitle')}</div>`;
 footSlot = `<button class="btn primary roll-cta" id="rollBtn" onclick="window['${rollFn}']()">${t('rollBtn')}</button>`;
 }
 else {
 // Decisive: both rolled, different -> winner line in the foot slot, no title.
 const won = st.my_roll > st.opp_roll;
 footSlot = `<div class="roll-result ${won?'roll-win':'roll-lose'}">${won ? t('rollYouFirst') : t('rollOppFirst')}</div>`;
 }

 return `<div class="roll-stage">
 <div class="roll-title-slot">${titleSlot}</div>
 ${dieRow}
 <div class="roll-foot-slot">${footSlot}</div>
 </div>`;
}

// Called from each game's roll-phase block. Idempotent: reuses the existing
// overlay element (re-rendering its content from the new state) instead of
// stacking popups on every polling refresh.
function showFirstRollPopup(st, rollFn, rerollFn, opts){
 opts = opts || {};
 const code = opts.code || st.code || '';
 const solo = !!opts.solo;
 const proceedFn = (typeof opts.proceedFn === 'function') ? opts.proceedFn : null;

 const myRolled = st.my_roll != null;
 const oppRolled = st.opp_roll != null;
 const tie = myRolled && oppRolled && st.my_roll === st.opp_roll;
 const waiting = !solo && myRolled && !oppRolled;
 const decisive = myRolled && oppRolled && !tie;

 // Fresh roll (nothing thrown yet) -> (re)arm per-code guards for this game.
 if(st.my_roll==null && st.opp_roll==null){
 _rollPopupClosed[code] = false;
 _rollAutoRerollCount[code] = 0;
 }

 // PvP waiting guard: once closed (auto or manually) polling must not reopen.
 if(waiting && _rollPopupClosed[code]){
 return;
 }

 if(!_rollPopupEl || !_rollPopupEl.isConnected){
 _rollPopupEl = document.createElement('div');
 _rollPopupEl.className = 'overlay';
 _rollPopupEl.id = 'firstRollPopupOverlay';
 _rollPopupEl.setAttribute('role','dialog');
 _rollPopupEl.setAttribute('aria-modal','true');
 _rollPopupEl._onKey = (e)=>{
 if(e.key === 'Escape'){
 const s = _rollPopupEl && _rollPopupEl._st;
 const wait = !!(s && !s.solo && s.my_roll != null && s.opp_roll == null);
 if(wait) __rollPopupCloseWait();
 }
 };
 document.addEventListener('keydown', _rollPopupEl._onKey);
 document.body.appendChild(_rollPopupEl);
 }
 _rollPopupEl._st = st;
 // Only clear a pending proceed timer when switching to a DIFFERENT game's
 // popup. For the same code re-rendering the same decisive state (normal
 // polling), we must NOT clear it, or the auto-start would never fire.
 if(code !== _rollPopupCode && _rollProceedTimer){
 clearTimeout(_rollProceedTimer);
 _rollProceedTimer = null;
 _rollProceedScheduled = false;
 }
 _rollPopupCode = code;
 _rollPopupProceed = proceedFn;
 _rollPopupEl.innerHTML = `<div class="modal roll-popup">${_rollPopupInner(st, rollFn, rerollFn, {solo, code})}</div>`;

 // Focus the primary action for keyboard users.
 const focusBtn = _rollPopupEl.querySelector('#rollBtn, #closeRollBtn');
 if(focusBtn) focusBtn.focus();

 // PvP waiting -> auto-close after a short beat (a Close button is offered).
 if(waiting){
 if(!_rollWaitScheduled){
 _rollWaitScheduled = true;
 _rollWaitTimer = setTimeout(()=>{
 _rollWaitScheduled = false;
 if(code) _rollPopupClosed[code] = true;
 closeFirstRollPopup();
 }, 1500);
 }
 } else {
 if(_rollWaitTimer){ clearTimeout(_rollWaitTimer); _rollWaitTimer = null; }
 _rollWaitScheduled = false;
 }

 // Auto-reroll on a tie when both sides have already rolled. Capped per code.
 if(tie){
 const count = _rollAutoRerollCount[code] || 0;
 if(count < 6 && !_rollRerollScheduled){
 _rollRerollScheduled = true;
 const codeAtSchedule = code;
 const fn = rerollFn;
 _rollRerollTimer = setTimeout(()=>{
 _rollRerollScheduled = false;
 _rollAutoRerollCount[codeAtSchedule] = (_rollAutoRerollCount[codeAtSchedule]||0) + 1;
 if(typeof window[fn] === 'function') window[fn]();
 }, 900);
 }
 } else {
 if(_rollRerollTimer){ clearTimeout(_rollRerollTimer); _rollRerollTimer = null; }
 _rollRerollScheduled = false;
 }

 // Decisive (both rolled, not a tie) and a proceed callback is provided:
 // auto-advance after a short beat so the game starts on its own (matching the
 // Poker/Checkers/Backgammon behaviour). No manual "Continue" button is shown
 // for any game -- the roll popup is purely informational and the game starts
 // itself. The timer is armed once per (code, decisive-resolution) and is NOT
 // cleared by re-entrant polling renders (only on a code change), so it always
 // fires even if refreshState re-enters this popup several times beforehand.
 if(decisive && proceedFn && !_rollProceedScheduled){
 _rollProceedScheduled = true;
 _rollProceedTimer = setTimeout(()=>{
 _rollProceedScheduled = false;
 if(_rollPopupCode === code) __rollPopupContinue();
 _rollProceedTimer = null;
 }, 1500);
 }
}

function closeFirstRollPopup(){
 if(_rollWaitTimer){ clearTimeout(_rollWaitTimer); _rollWaitTimer = null; }
 if(_rollRerollTimer){ clearTimeout(_rollRerollTimer); _rollRerollTimer = null; }
 if(_rollProceedTimer){ clearTimeout(_rollProceedTimer); _rollProceedTimer = null; }
 _rollWaitScheduled = false;
 _rollRerollScheduled = false;
 _rollProceedScheduled = false;
 if(_rollPopupEl){
 if(_rollPopupEl._onKey) document.removeEventListener('keydown', _rollPopupEl._onKey);
 _rollPopupEl.remove();
 _rollPopupEl = null;
 }
 _rollPopupCode = null;
 _rollPopupProceed = null;
}

// Continue button: mark the roll acknowledged (so it never reappears), close
// the popup, then run the game's proceed callback (e.g. ackRoll / refresh).
function __rollPopupContinue(){
 const code = _rollPopupCode;
 if(code) _rollAckShown[code] = true;
 const fn = _rollPopupProceed;
 closeFirstRollPopup();
 if(typeof fn === 'function') fn();
}

// PvP waiting "Close": remember that we already showed the waiting popup for
// this code so polling does not reopen it.
function __rollPopupCloseWait(){
 const code = _rollPopupCode;
 if(code) _rollPopupClosed[code] = true;
 closeFirstRollPopup();
}

// One-shot guard keyed by game code: mark the first-roll popup acknowledged
// so polling does not reopen it.
const _rollAckShown = {};
const _sbAutoAck = {};

async function doFirstRoll(endpoint, codeVal, refreshFn, afterRoll){
 const btn = document.getElementById('rollBtn');
 if(btn) btn.disabled = true;
 const spinEls = Array.from(document.querySelectorAll('#firstRollPopupOverlay .roll-die3d'));
 spinEls.forEach(d => { d.classList.remove('roll-die-pending'); d.classList.add('roll-die-spinning'); });
 try{ sfxRoll(); }catch(e){}
 const res = await api(endpoint, {uid:getUid(), code:codeVal});
 spinEls.forEach(d => d.classList.remove('roll-die-spinning'));
 if(res===null){ showRetry(t('error'), ()=>rollFirst()); return; }
 await refreshFn();
 if(res && res.roll_resolved){ _rollAckShown[codeVal] = true; }
 if(res && res.needs_bot_turn && typeof afterRoll === 'function'){ afterRoll(res); }
}

async function doRerollFirst(endpoint, codeVal, refreshFn, afterRoll){
 const btn = document.getElementById('rerollBtn');
 if(btn) btn.disabled = true;
 const spinEls = Array.from(document.querySelectorAll('#firstRollPopupOverlay .roll-die3d'));
 spinEls.forEach(d => { d.classList.add('roll-die-spinning'); });
 try{ sfxClick(); }catch(e){}
 const res = await api(endpoint, {uid:getUid(), code:codeVal});
 spinEls.forEach(d => d.classList.remove('roll-die-spinning'));
 if(res===null){ showRetry(t('error'), ()=>rerollFirst()); return; }
 await refreshFn();
 if(res && res.roll_resolved){ _rollAckShown[codeVal] = true; }
 if(res && res.needs_bot_turn && typeof afterRoll === 'function'){ afterRoll(res); }
}

function rollFirst(){ return doFirstRoll('/api/roll_first', gameCode, refreshState); }
function rerollFirst(){ return doRerollFirst('/api/reroll_first', gameCode, refreshState); }
async function ackRoll(){
 if(!state) return;
 _rollAckShown[gameCode] = true;
 // In solo, if the bot won the opening roll it owes its first shot. Take it
 // now (the dice-result screen has already been shown to the human).
 if(state.solo && state.phase==='playing'&& state.turn===2){
 const res = await api('/api/bot_opening_shot', {uid:getUid(), code:gameCode});
 if(res && res.ok){
 if(res.state){ state = res.state; updateUI(); }
 const bs = res.bot_shots;
 if(bs && bs.length){
 sbRenderOppHistory(bs);
 const last = bs[bs.length-1];
 if(state) state._lastOppShot = {r:last.r, c:last.c};
 }
 if(state.all_sunk||state.my_all_sunk){
 if(!document.querySelector('.overlay')){
 showResult(state.all_sunk ? '': '', state.all_sunk ? t('win') : t('lose'), state.all_sunk ? t('winDesc') : t('loseDesc'), state.strip);
 }
 return;
 }
 return;
 }
 }
 if(state && state.phase==='playing'){ updateUI(); }
 else { await refreshState(); }
}
function ckRollFirst(){ return doFirstRoll('/api/checkers_roll_first', ckCode, ckRefreshState, ckAfterOpeningRoll); }
function ckRerollFirst(){ return doRerollFirst('/api/checkers_reroll_first', ckCode, ckRefreshState); }
function ckAfterOpeningRoll(res){
 if(res && res.needs_bot_turn) ckRunBotTurn();
}
function pdRollFirst(){ pdOppRollSpun=''; return doFirstRoll('/api/pd_roll_first', pdCode, pdRefreshState, pdAfterOpeningRoll); }
function pdRerollFirst(){ pdOppRollSpun=''; return doRerollFirst('/api/pd_reroll_first', pdCode, pdRefreshState, pdAfterOpeningRoll); }
function bgRollFirst(){ return doFirstRoll('/api/bg_roll_first', bgCode, bgRefreshState); }
function bgRerollFirst(){ return doRerollFirst('/api/bg_reroll_first', bgCode, bgRefreshState); }

function updateUI(){
 if(!state)return;
 const s=state;
 // A round that left the 'finished'phase means the rematch (if any) has
 // started, so stop treating the game as pending a rematch.
 if(s.phase!=='finished') rematchPending=false;
 showIncomingMessages(s.messages);
 const gameOver=s.all_sunk||s.my_all_sunk;
 const isPlacing = s.phase==='placing'||s.phase==='placing1'||s.phase==='placing2';
 $('pdArea').style.display='none';
 $('ckArea').style.display='none';
 $('ownBoardWrap').classList.remove('hidden');
 $('oppBoardWrap').classList.remove('hidden');
 renderBoard($('ownBoard'),s.own,false,gameOver,s.own_ships,s.strip);
 renderBoard($('oppBoard'),s.opp,true,gameOver,null,s.strip);

 $('gameInfo').textContent = '';
 $('header').classList.add('in-game');
 document.title = s.strip ? t('stripTitle') : t('title');

 const ownEl=$('ownBoard'), oppEl=$('oppBoard');
 ownEl.classList.remove('my-turn');
 oppEl.classList.remove('my-turn');
 if(s.my_turn){
 oppEl.classList.add('my-turn');
 }else{
 ownEl.classList.add('my-turn');
 }

 if(gameOver){
 if(rematchPending){
 // A rematch on the same code is in progress: keep polling and wait for
 // the opponent (or the server) to restart the round. No result overlay.
 setStatus(t('rematchWait'), 'battle');
 return;
 }
 if(s.all_sunk && s.strip && !s.opp_stake && !s.strip_photo){
 setStatus('' + {ru:'Ожидание фото...',uk:'Очікування фото...',en:'Waiting for photo...'}[lang], 'battle');
 if(!_stripPhotoWaitTimer){
 _stripPhotoWaitTimer = setTimeout(() => {
 _stripPhotoWaitTimer = null;
 stopGamePoll('sea_battle');
 localStorage.removeItem('sb_game');
 showResult('',t('win'),{ru:'Соперник не отправил фото',uk:'Суперник не надіслав фото',en:'Opponent did not send a photo'}[lang], true);
 }, 60000);
 }
 return;
 }
 stopGamePoll('sea_battle');
 const won = s.all_sunk;
 const resultTitle = won ? t('win') : t('lose');
 const resultDesc = won ? t('winDesc') : t('loseDesc');
 // At game over the opponent board reveals the full enemy layout. Relabel
 // it so the loser understands these are the opponent's ships they missed.
 $('lblOpp').textContent = won
 ? {ru:'Флот соперника потоплен',uk:'Флот суперника потоплено',en:" Opponent's fleet sunk"}[lang]
 : {ru:'Корабли соперника',uk:'Кораблі суперника',en:" Opponent's ships"}[lang];
 setStatus(`${resultTitle} ${resultDesc}`, 'battle');
 $('actions').className = 'btn-col';
 $('actions').innerHTML = `<div class="result-notice ${won ? 'win': 'lose'}">${resultTitle}<br><span style="font-size:13px;font-weight:400">${resultDesc}</span></div>`;
 if(!rematchPending) localStorage.removeItem('sb_game');
 $('app').insertBefore($('status'), $('app').firstChild);
 if(won)showResult('',resultTitle,resultDesc,s.strip);
 else if(s.my_all_sunk)showResult('',resultTitle,resultDesc,s.strip);
 return;
 }

 if(s.phase==='placing'||s.phase==='placing1'||s.phase==='placing2'){
 $('header').classList.add('in-game');
 ownEl.classList.remove('my-turn');
 oppEl.classList.remove('my-turn');
 $('app').insertBefore($('status'), $('app').firstChild);
 const alreadyConfirmed = s.ready && s.pnum && s.ready[s.pnum];
 const c = s.code;
 // During ship placement only the player's own board is shown (clean,
 // focused). The opponent board appears later, at the dice-roll step.
 $('oppBoardWrap').classList.add('hidden');
 $('actions').className = 'btn-col';
 if(alreadyConfirmed && !s.solo){
 setStatus(` <b>${c}</b> — ${t('waitOpp')} OK`, '');
 $('status').style.cursor='pointer';
 $('status').title=t('copyCode');
 $('status').onclick=()=>navigator.clipboard.writeText(c).then(()=>setStatus('OK '+c+''+{ru:'скопирован',uk:'скопійовано',en:'copied'}[lang],''));
 $('actions').innerHTML=`
 <button class="btn success" disabled style="opacity:0.5;cursor:default">OK ${t('confirm')}</button>
 ${s.pnum === 1 ? `<button class="btn primary" onclick="shareGame()"> ${t('inviteFriend')}</button>` : ''}
 <button class="btn outline" onclick="leaveGame(true)">${s.solo ? t('quit') : t('surrender')}</button>
 <button class="btn outline" onclick="leaveGame()" title="${minimizeTitle()}">${t('minimize')}</button>
 `;
 }else{
 if(!s.solo){
 setStatus(` <b>${c}</b> — ${t('waitOpp')}`, '');
 $('status').style.cursor='pointer';
 $('status').title=t('copyCode');
 $('status').onclick=()=>navigator.clipboard.writeText(c).then(()=>setStatus('OK '+c+''+{ru:'скопирован',uk:'скопійовано',en:'copied'}[lang],''));
 }else{
 setStatus(s.strip ? t('stripPlace') : t('placing'),'');
 $('status').style.cursor='';
 $('status').onclick=null;
 }
 // In strip mode each player must commit a stake photo before
 // starting. The main action button doubles as the upload step:
 // it shows the "upload photo" label until a stake photo exists,
 // then switches to the normal start label once it's uploaded.
 const needStake = s.strip && !s.strip_stake;
 const startBtnClass = needStake ? 'btn strip-btn': 'btn primary';
 const startOnclick = needStake ? 'showStripInfoOverlay()': 'confirmPlace()';
 const startLabel = needStake ? t('stripStakeBtn') : (s.strip ? t('stripStart') : t('confirm'));
 $('actions').innerHTML=`
 <button class="btn success" onclick="autoPlace()">${t('reroll')}</button>
 ${!s.solo && s.pnum === 1 ? `<button class="btn primary" onclick="shareGame()"> ${t('inviteFriend')}</button>` : ''}
 <button class="${startBtnClass}" onclick="${startOnclick}">${startLabel}</button>
 ${!s.solo ? `<button class="btn outline" onclick="leaveGame(true)">${t('surrender')}</button>` : ''}
 ${!s.solo ? `<button class="btn outline" onclick="leaveGame()" title="${minimizeTitle()}">${t('minimize')}</button>` : ''}
 `;
 }
 setThemeSelectorVisibility(false);
 delete _rollAckShown[gameCode];
 delete _sbAutoAck[gameCode];
 return;
 }

 // Route to the roll screen purely by phase. Note: my_roll/opp_roll stay
 // populated on the backend even after phase flips to 'playing'(kept
 // around because the opening-roll winner is shown inside the shared
 // #firstRollPopupOverlay, with no separate post-popup banner), so they must
 // NOT be part of this check -- doing so used to make this screen (and its
 // "Continue" button) re-render forever after a decisive roll, since
 // refreshing state would always find the same still-set, still-decisive
 // my_roll/opp_roll and show the roll screen again instead of the board.
 const rollDecided = s.my_roll != null && s.opp_roll != null && s.my_roll !== s.opp_roll;
 if(s.phase==='roll'|| (rollDecided && !_rollAckShown[gameCode])){
 if(rollDecided && _rollAckShown[gameCode]){
 // Already acknowledged (user clicked Continue): drop the popup and let
 // the playing render below take over (board).
 closeFirstRollPopup();
 } else {
 ownEl.classList.remove('my-turn');
 oppEl.classList.remove('my-turn');
 $('app').insertBefore($('status'), $('app').firstChild);
 // Reveal the opponent board with a soft fade/slide as the roll begins.
 const ow = $('oppBoardWrap');
 ow.classList.remove('hidden');
 ow.style.opacity = '0';
 ow.style.transform = 'translateY(12px)';
 requestAnimationFrame(() => requestAnimationFrame(() => {
 ow.style.opacity = '';
 ow.style.transform = '';
 }));
 setStatus(''+t('rollTitle'),'');
 // The popup now owns the opening-roll result. Continue runs ackRoll (which handles the solo
 // bot opening shot and the _rollAckShown guard).
 showFirstRollPopup(s, 'rollFirst', 'rerollFirst', { solo: s.solo, code: gameCode, proceedFn: () => ackRoll() });
 $('actions').className='btn-col';
 $('actions').innerHTML = `<button class="btn outline" onclick="leaveGame(true)">${s.solo ? t('quit') : t('surrender')}</button>`;
 setThemeSelectorVisibility(false);
 return;
 }
 }

 $('oppBoardWrap').classList.remove('hidden');
 closeFirstRollPopup();
 updateSettingsUI();
 $('ownBoardWrap').after($('status'));

 if(s.my_turn){
 setStatus(t('yourTurn'),'battle');
 $('actions').className='btn-col';
 $('actions').innerHTML=`
 ${s.solo
 ? `<div class="btn-row" style="margin-top:8px"><button class="btn outline" onclick="leaveGame(true)">${t('quit')}</button><button class="btn outline" onclick="leaveGame()" title="${minimizeTitle()}">${t('minimize')}</button></div>`
 : `<div class="btn-row"><button class="btn outline" onclick="sendOpponentMessage()">${t('message')}</button><button class="btn outline" onclick="leaveGame(true)">${t('surrender')}</button></div>
 <button class="btn outline" onclick="leaveGame()" title="${minimizeTitle()}">${t('minimize')}</button>`}
 `;
 }else{
 setStatus(t('oppTurn'),'');
 $('actions').className='btn-col';
 $('actions').innerHTML=`
 ${s.solo
 ? `<div class="btn-row" style="margin-top:8px"><button class="btn outline" onclick="leaveGame(true)">${t('quit')}</button><button class="btn outline" onclick="leaveGame()" title="${minimizeTitle()}">${t('minimize')}</button></div>`
 : `<div class="btn-row"><button class="btn outline" onclick="sendOpponentMessage()">${t('message')}</button><button class="btn outline" onclick="leaveGame(true)">${t('surrender')}</button></div>
 <button class="btn outline" onclick="leaveGame()" title="${minimizeTitle()}">${t('minimize')}</button>`}
 `;
 }
}

async function startSolo(){
 setStripLockVisible(false);
 currentGameType=null; setHelpVisible(false);
 const res=await api('/api/new_solo',{uid:getUid(), difficulty: gameDifficulty});
 if(res===null){ showRetry(t('error'), ()=>startSolo()); return; }
 if(!res||!res.ok){setStatus(t('error'));return}
 gameCode=res.code;
 if(state) state._lastOppShot=null;
 localStorage.setItem('sb_game',gameCode);
 const _sb=$('sbOppHistory'); if(_sb) _sb.innerHTML='';
 $('actions').innerHTML='';
 await refreshState();
}

function compressImage(dataUrl, maxW=800, quality=0.7){
 return new Promise(resolve => {
 const img = new Image();
 img.onload = () => {
 try {
 const c = document.createElement('canvas');
 let w = img.width, h = img.height;
 if(w > maxW || h > maxW){
 const ratio = Math.min(maxW/w, maxW/h);
 w = Math.round(w * ratio);
 h = Math.round(h * ratio);
 }
 c.width = w; c.height = h;
 const ctx = c.getContext('2d');
 ctx.drawImage(img, 0, 0, w, h);
 resolve(c.toDataURL('image/jpeg', quality));
 } catch(e){ resolve(dataUrl); }
 };
 // If the image cannot be decoded (e.g. an unsupported format like
 // HEIC), never leave the promise hanging — fall back to the raw
 // data URL so the upload can still proceed.
 img.onerror = () => resolve(dataUrl);
 img.src = dataUrl;
 });
}

function showLoadingOverlay(msg){
 const existing = document.querySelector('.loading-overlay');
 if(existing) existing.remove();
 const o = document.createElement('div');
 o.className = 'loading-overlay';
 o.innerHTML = `<div class="modal"><div class="spinner"></div><p>${msg || ''}</p></div>`;
 document.body.appendChild(o);
}

function hideLoadingOverlay(){
 const o = document.querySelector('.loading-overlay');
 if(o) o.remove();
}

const STRIP_LOADING_MSGS = {
 ru: { camera: 'Подготовка камеры...', process: 'Обработка фото...', create: 'Создание игры...', send: 'Отправка фото...'},
 uk: { camera: 'Підготовка камери...', process: 'Обробка фото...', create: 'Створення гри...', send: 'Надсилання фото...'},
 en: { camera: 'Preparing camera...', process: 'Processing photo...', create: 'Creating game...', send: 'Sending photo...'},
};

function showStripInfoOverlay(){
 const o = document.createElement('div');
 o.className = 'overlay';
 o.innerHTML = `
 <div class="modal">
 <p>${t('stripInfoDesc')}</p>
 <button class="btn strip-btn" style="width:100%;margin:4px 0" onclick="this.closest('.overlay').remove();captureAndUploadStake()">${t('stripStakeBtn')}</button>
 <button class="btn outline" style="width:100%;margin:4px 0" onclick="this.closest('.overlay').remove()">${t('close')}</button>
 </div>`;
 document.body.appendChild(o);
}

// Opens the camera/file picker and resolves with a compressed
// data-URL, or null if the user cancels.
function captureStripPhoto(){
 return new Promise((resolve) => {
 const input = document.createElement('input');
 input.type = 'file';
 input.accept = 'image/*';
 input.capture = 'environment';
 // `resolved` guards against the classic race in Telegram's WebView (most
 // visible on Android): the window can regain focus *before* the file
 // input's change event actually lands, especially for camera captures
 // that need a moment to encode the photo. The old code started a 600ms
 // "did they cancel?" timer on focus and called resolve(null) if change
 // hadn't fired yet -- but a Promise only resolves once, so if change
 // fired a moment later it was silently dropped and the upload never
 // happened (yet nothing told the user it failed). Now the timer is only
 // a *fallback* for a genuine cancel, it's much longer, and both paths
 // check `resolved` first so whichever settles first wins cleanly.
 let resolved = false;
 let opened = false;
 const finish = (value) => {
 if(resolved) return;
 resolved = true;
 window.removeEventListener('focus', onFocus);
 window.removeEventListener('blur', onBlur);
 resolve(value);
 };
 const onBlur = () => { opened = true; };
 const onFocus = () => {
 // Only treat a focus as "returned from the picker" if the picker
 // actually opened first (window blurred). Some browsers fire a stray
 // focus when the camera is launched, which must be ignored.
 if(!opened) return;
 // Give the file 'change'event a generous window to land before
 // deciding the user cancelled -- camera capture in particular can take
 // a couple seconds to hand the photo back on slower devices.
 setTimeout(() => finish(null), 2000);
 };
 window.addEventListener('blur', onBlur);
 window.addEventListener('focus', onFocus);
 input.onchange = async (e) => {
 const file = e.target.files[0];
 if(!file){finish(null);return}
 const reader = new FileReader();
 reader.onerror = () => finish(null);
 reader.onload = async (ev) => { finish(await compressImage(ev.target.result)); };
 reader.readAsDataURL(file);
 };
 input.click();
 });
}

// Captures a "stake" photo and uploads it before the game starts.
async function captureAndUploadStake(){
 const data = await captureStripPhoto();
 if(!data) return;
 showLoadingOverlay(STRIP_LOADING_MSGS[lang].send);
 const res = await api('/api/upload_stake',{uid:getUid(),code:gameCode,photo:data,lang:lang});
 hideLoadingOverlay();
 if(!(res&&res.ok)){ setStatus(t('error')); return; }
 // Flip the stake flag immediately so the action button switches to
 // "start" right away, independent of poll/refresh timing. The server
 // stays the source of truth via refreshState below.
 if(state){ state.strip_stake = true; updateUI(); }
 await refreshState();
}

async function newMulti(strip=false){
 setStripLockVisible(false);
 currentGameType=null; setHelpVisible(false);
 const res=await api('/api/new_multi',{uid:getUid(),strip:strip});
 if(res===null){ showRetry(t('error'), ()=>newMulti()); return; }
 if(!res||!res.ok){setStatus(t('error'));return}
 gameCode=res.code;
 localStorage.setItem('sb_game',gameCode);
 setStatus('', '');
 await refreshState();
 startGamePoll('sea_battle', gameCode, refreshState);
}

function shareGame(){
 if(!gameCode) return;
 copyToClipboard(gameCode, {ru:'Код скопирован OK',uk:'Код скопійовано OK',en:'Code copied OK'}[lang]);
 try{Telegram.WebApp.openTelegramLink(`https://t.me/share/url?url=${encodeURIComponent(gameCode)}`)}catch(e){}
}

function copyToClipboard(text, msg){
 if(navigator.clipboard){
 navigator.clipboard.writeText(text).then(()=>{
 if(msg) setStatus('OK '+ msg, '');
 }).catch(()=>{ if(msg) setStatus('OK '+ msg, ''); });
 } else if(msg) {
 setStatus('OK '+ msg, '');
 }
}

async function joinByCode(code){
 const resolveRes = await api('/api/resolve_code', {code});
 if(resolveRes===null){
 showRetry(t('error'), ()=>joinByCode(code));
 return;
 }
 if(!resolveRes || !resolveRes.ok){
 setStatus(t('joinError'), '');
 return;
 }
 const gameType = resolveRes.game;
 if(gameType === 'sea_battle'){
 const res = await api('/api/join', {uid: getUid(), code});
 if(res===null){ showRetry(t('error'), ()=>joinByCode(code)); return; }
 if(!res || !res.ok){ setStatus(t('joinError')); return; }
 gameCode = code;
 if(state) state._lastOppShot=null;
 localStorage.setItem('sb_game', code);
 $('actions').innerHTML = '';
 await refreshState();
 startGamePoll('sea_battle', code, refreshState);
 } else if(gameType === 'poker_dice'){
 const res = await api('/api/pd_join', {uid: getUid(), code});
 if(res===null){ showRetry(t('error'), ()=>joinByCode(code)); return; }
 if(!res || !res.ok){ setStatus(t('joinError')); return; }
 pdCode = code;
 localStorage.setItem('pd_game', code);
 $('actions').innerHTML = '';
 pdShowGame(res.state);
 startGamePoll('poker_dice', code, pdRefreshState);
 } else if(gameType === 'checkers'){
 const res = await api('/api/checkers_join', {uid: getUid(), code});
 if(res===null){ showRetry(t('error'), ()=>joinByCode(code)); return; }
 if(!res || !res.ok){ setStatus(t('joinError')); return; }
 ckCode = code;
 localStorage.setItem('ck_game', code);
 $('actions').innerHTML = '';
 ckShowGame(res.state);
 startGamePoll('checkers', code, ckRefreshState);
 } else if(gameType === 'backgammon'){
 const res = await api('/api/bg_join', {uid: getUid(), code});
 if(res===null){ showRetry(t('error'), ()=>joinByCode(code)); return; }
 if(!res || !res.ok){ setStatus(t('joinError')); return; }
 bgCode = code;
 localStorage.setItem('bg_game', code);
 $('actions').innerHTML = '';
 bgShowGame(res.state);
 startGamePoll('backgammon', code, bgRefreshState);
 }
}

async function universalJoinGame(){
 promptDialog(t('joinTitle'), t('joinPlaceholder'), (code)=>{
 if(code) joinByCode(code.toUpperCase());
 });
}

const _polls = {};
let _pollFailStreak = {};
let _pollInterval = {};
let _pollMeta = {};
let _connDotEl = null;

// (Re)start a type's poll interval at a specific delay. The captured `code`
// and `refreshFn` come from the arguments so a restarted interval uses the
// latest known code/meta.
function _restartPoll(type, code, refreshFn, iv){
 if(_polls[type]) clearInterval(_polls[type]);
 _pollInterval[type] = iv;
 _polls[type] = setInterval(async () => {
 if(!code){ stopGamePoll(type); return; }
 await refreshFn();
 }, iv);
}

function startGamePoll(type, code, refreshFn){
 stopGamePoll(type);
 _pollMeta[type] = { code, refreshFn };
 _restartPoll(type, code, refreshFn, _pollInterval[type] || 2000);
}
function stopGamePoll(type){
 if(_polls[type]){ clearInterval(_polls[type]); delete _polls[type]; }
 delete _pollMeta[type];
 delete _pollInterval[type];
 delete _pollFailStreak[type];
}
function stopAllPolls(){ for(const k in _polls) stopGamePoll(k); }

// Pause/resume all active game polls when the tab/WebApp becomes hidden or
// visible again. Clearing the interval while hidden avoids wasted requests (and
// the exponential backoff that kicks in after 3+ failures). On resume we
// restart each poll safely (startGamePoll stop+restarts) and force a single
// refresh so the UI is immediately up to date.
function pauseAllPolls(){
 for(const type in _pollMeta){
 if(_polls[type]){ clearInterval(_polls[type]); delete _polls[type]; }
 }
}
function resumeAllPolls(){
 for(const type in _pollMeta){
 const meta = _pollMeta[type];
 if(!meta) continue;
 startGamePoll(type, meta.code, meta.refreshFn);
 try{ meta.refreshFn(); }catch(e){}
 }
}

function currentCodeFor(t){ return _pollMeta[t] ? _pollMeta[t].code : null; }
function currentRefreshFor(t){ return _pollMeta[t] ? _pollMeta[t].refreshFn : null; }

// Reflect connectivity in the header dot. ok=true -> green, ok=false -> red.
function setConnDot(ok){
 if(!_connDotEl) _connDotEl = document.getElementById('connDot');
 if(_connDotEl){
 _connDotEl.textContent = ok ? '': '';
 _connDotEl.classList.toggle('off', !ok);
 }
}

// Track per-type poll outcomes and apply exponential backoff after repeated
// failures (3+ consecutive misses), returning to 2000ms once a poll succeeds.
function notePollResult(type, ok){
 if(ok){
 _pollFailStreak[type] = 0;
 const iv = _pollInterval[type] || 2000;
 if(iv !== 2000 && _pollMeta[type]){
 _restartPoll(type, currentCodeFor(type), currentRefreshFor(type), 2000);
 }
 } else {
 _pollFailStreak[type] = (_pollFailStreak[type] || 0) + 1;
 if(_pollFailStreak[type] >= 3){
 const streak = _pollFailStreak[type] - 3;
 const iv = Math.min(2000 * Math.pow(2, streak), 30000);
 if(_pollMeta[type]) _restartPoll(type, currentCodeFor(type), currentRefreshFor(type), iv);
 }
 }
}

let _lastSBSig=null; // last serialized state signature for poll dedup
let _sbRefreshing=false; // in-flight guard so a slow poll can't overlap
let _sbShooting=false; // in-flight guard so a second /api/shoot can't fire while one is pending
let _stripPhotoWaitTimer=null, _ckBotOpening=false, _bgBotOpening=false;
// True while a rematch on the same code is pending, so the finished-game
// cleanup (stop polling / drop saved code) is skipped until the new round
// actually starts.
let rematchPending=false;

function showMainMenu(){
 document.querySelectorAll('.overlay').forEach(o=>o.remove()); // clear stray modal if a nav happens while one is open
 closeFirstRollPopup();
 currentGameType=null; setHelpVisible(false);
 currentScreen='menu';
 try{ if(typeof window.Telegram!=='undefined'&& window.Telegram.WebApp && window.Telegram.WebApp.BackButton) window.Telegram.WebApp.BackButton.hide(); }catch(e){}
 stripUnlocked=false; _stripTaps=0;
 setStripLockVisible(false);
 delete _rollAckShown[gameCode];
 $('ownBoardWrap').classList.add('hidden');
 $('oppBoardWrap').classList.add('hidden');
 gameCode=null;state=null;
 pdCode=null;pdState=null;
 ckCode=null;ckState=null;
 bgCode=null;bgState=null;
 const sbOpp=$('sbOppHistory'); if(sbOpp) sbOpp.innerHTML='';
 bgCode=null;bgState=null;
 stopAllPolls();
 // Note: saved game codes (sb_game/pd_game/ck_game) are intentionally
 // NOT cleared here anymore — quitting a game only minimizes it, so it must
 // stay resumable from the active-games bar below.
 setThemeSelectorVisibility(false);
 $('pdArea').style.display='none';
 $('ckArea').style.display='none';
 document.title = t('seaBattle');
 $('gameInfo').textContent='';
 renderPlayerName();
 $('header').classList.remove('in-game');
 document.querySelectorAll('.board').forEach(b => b.classList.remove('my-turn'));
 $('app').insertBefore($('status'), $('app').firstChild);
 setStatus('');
 var lb=$('langBar');if(lb)lb.style.display='flex';
 $('actions').className='btn-row stack';
 const AR = `role="button" tabindex="0" onkeydown="if(event.key==='Enter'||event.key===''){event.preventDefault();this.click()}"`;
 $('actions').innerHTML=`
 <div id="activeGamesContainer"></div>
 <div class="game-grid">
 <div class="game-card" ${AR} aria-label="${t('seaBattle')}" onclick="showSeaBattleMenu()" style="margin-bottom:8px">
 <img src="/static/sb-navy.svg" class="card-icon" alt="">
 <div class="name" style="color:var(--accent-primary)">${t('seaBattle')}</div>
 </div>
 <div class="game-card" ${AR} aria-label="${t('pdTitle')}" onclick="showPokerDice()" style="margin-bottom:8px">
 <img src="/static/pd-green.svg" class="card-icon" alt="">
 <div class="name" style="color:#ff9800">${t('pdTitle')}</div>
 </div>
 <div class="game-card" ${AR} aria-label="${t('checkers')}" onclick="showCheckers()" style="margin-bottom:8px">
 <img src="/static/checkers-icon.svg" class="card-icon" alt="">
 <div class="name" style="color:#D4A96A">${t('checkers')}</div>
 </div>
 <div class="game-card" ${AR} aria-label="${t('backgammon')}" onclick="showBackgammon()" style="margin-bottom:8px">
 <img src="/static/backgammon-icon.svg" class="card-icon" alt="">
 <div class="name" style="color:#8B5C2A">${t('backgammon')}</div>
 </div>
 <div class="game-card game-card-wide" ${AR} aria-label="${t('joinTitle')}" onclick="universalJoinGame()" style="margin-bottom:8px">
 <img src="/static/mode-join.svg" class="card-icon" alt="">
 <div class="name" style="color:var(--accent-primary)">${t('joinTitle')}</div>
 </div>
 </div>
 `;
 fetchActiveGames();
}

function showMenu(){ showMainMenu(); }

function showHelp(){
 let game=currentGameType;
 let body;
 currentScreen='help';
 try{ if(typeof window.Telegram!=='undefined'&& window.Telegram.WebApp && window.Telegram.WebApp.BackButton) window.Telegram.WebApp.BackButton.show(); }catch(e){}
 if(!game){
 body={ru:'Откройте игру, чтобы увидеть правила',uk:'Відкрийте гру, щоб побачити правила',en:'Open a game to see the rules'}[lang];
 } else if(game==='sea_battle'){
 body=t('rulesSeaBattle');
 } else if(game==='poker_dice'){
 body=t('rulesPokerDice');
 } else if(game==='checkers'){
 body=t('rulesCheckers');
 } else {
 body=t('rulesBackgammon');
 }
 const o=document.createElement('div'); o.className='overlay';
 o.innerHTML=`<div class="modal"><h2>? ${t('rules')}</h2><p style="white-space:pre-line">${body}</p>
 <button class="btn primary" style="width:100%;margin:6px 0" id="helpClose">${t('close')||'Закрыть'}</button></div>`;
 document.body.appendChild(o);
 const cb=o.querySelector('#helpClose');
 cb.focus();
 cb.onclick=()=>o.remove();
 o.addEventListener('keydown',(e)=>{
 if(e.key==='Escape'){ e.preventDefault(); o.remove(); return; }
 if(e.key==='Tab'){
 const f=[cb], first=f[0], last=f[f.length-1];
 if(e.shiftKey && document.activeElement===first){ e.preventDefault(); last.focus(); }
 else if(!e.shiftKey && document.activeElement===last){ e.preventDefault(); first.focus(); }
 }
 });
}

// ---- Player stats (winrate + recent match history) -------------------------
const STATS_GAME_LABEL = {sea_battle:'seaBattle', poker_dice:'pdTitle', checkers:'checkers', backgammon:'backgammon'};
const STATS_GAME_ICON = {sea_battle:'', poker_dice:'', checkers:'', backgammon:''};
const STATS_RESULT_LABEL = {win:'statsResWin', loss:'statsResLoss', draw:'statsResDraw'};

async function showStats(){
 document.querySelectorAll('.overlay').forEach(o=>o.remove()); // clear stray modal if a nav happens while one is open
 currentGameType=null; setHelpVisible(false);
 currentScreen='stats';
 try{ if(typeof window.Telegram!=='undefined'&& window.Telegram.WebApp && window.Telegram.WebApp.BackButton) window.Telegram.WebApp.BackButton.show(); }catch(e){}
 var lb=$('langBar');if(lb)lb.style.display='none';
 setStripLockVisible(false);
 hideAllGameAreas();
 document.title = t('statsTitle');
 setStatus('' + t('statsTitle'));
 $('gameInfo').textContent='';
 $('header').classList.remove('in-game');
 $('app').insertBefore($('status'), $('app').firstChild);
 $('actions').className='btn-col';
 $('actions').innerHTML = `<div class="stats-loading"></div>`;
 const res = await api('/api/stats', {uid:getUid()});
 if(res===null){
 showRetry(t('error'), ()=>showStats());
 return;
 }
 if(!res || !res.ok){
 setStatus(t('error'));
 $('actions').innerHTML = `<button class="btn outline quit-btn" onclick="showMainMenu()">${t('quit')}</button>`;
 return;
 }
 renderStats(res.stats);
}

function renderStats(st){
 const winrateStr = st.winrate==null ? '—': st.winrate+'%';
 let html = `
 <div class="stats-summary">
 <div class="stats-big">${winrateStr}</div>
 <div class="stats-big-label">${t('statsWinrate')}</div>
 <div class="stats-row">
 <div class="stats-cell win"><b>${st.wins}</b><span>${t('statsWins')}</span></div>
 <div class="stats-cell loss"><b>${st.losses}</b><span>${t('statsLosses')}</span></div>
 <div class="stats-cell draw"><b>${st.draws}</b><span>${t('statsDraws')}</span></div>
 </div>
 <div class="stats-total">${t('statsTotal')}: ${st.total}</div>
 </div>`;
 html += `<h3 class="stats-hist-title">${t('statsHistory')}</h3>`;
 if(!st.history || !st.history.length){
 html += `<div class="stats-empty">${t('statsNoGames')}</div>`;
 } else {
 html += '<div class="stats-history">';
 for(const h of st.history.slice(0,20)){
 const icon = STATS_GAME_ICON[h.game] || '';
 const gname = t(STATS_GAME_LABEL[h.game] || h.game);
 const resLabel = t(STATS_RESULT_LABEL[h.result] || h.result);
 html += `<div class="stats-hist-row ${h.result}"><span class="stats-hist-icon">${icon}</span><span class="stats-hist-name">${gname}</span><span class="stats-hist-result ${h.result}">${resLabel}</span></div>`;
 }
 html += '</div>';
 }
 html += `<button class="btn danger" style="margin-top:12px" onclick="resetStats()"> ${t('resetStats') || 'Reset statistics'}</button>`;
 html += `<button class="btn outline quit-btn" style="margin-top:12px" onclick="showMainMenu()">${t('quit')}</button>`;
 $('actions').innerHTML = html;
}

function resetStats(){
 confirmDialog(t('resetStats'), t('resetStatsConfirm'), ()=>{
 api('/api/reset_stats', {uid:getUid()}).then(res=>{
 if(res && res.ok){ renderStats(res.stats); }
 else { alert('Failed to reset statistics.'); }
 }).catch(()=>alert('Failed to reset statistics.'));
 }, t('resetStats'), t('cancel'));
 return;
}

let gameDifficulty = 4;
(function(){ const d = localStorage.getItem('sb_diff'); if(d==='2'||d==='4') gameDifficulty = +d; })();
function getDifficulty(){ return gameDifficulty===2 ? 2 : 4; }
function setDifficulty(v){ gameDifficulty = (v===2?2:4); try{localStorage.setItem('sb_diff', String(gameDifficulty));}catch(e){} }
let stripUnlocked=false; let _stripTaps=0, _stripLastTap=0;

let playerName = localStorage.getItem('sb_name') || '';
function getPlayerName(){
 if(playerName) return playerName;
 try{ const fn = window.Telegram?.WebApp?.initDataUnsafe?.user?.first_name; if(fn) return fn; }catch(e){}
 return '';
}
function renderPlayerName(){
 // player name hidden
}
function savePlayerName(v){
 playerName = (v||'').trim().slice(0,24);
 try{ localStorage.setItem('sb_name', playerName); }catch(e){}
 renderPlayerName();
}

function showSeaBattleMenu(){
 currentGameType='sea_battle'; setHelpVisible(true);
 currentScreen='sea_battle';
 try{ if(typeof window.Telegram!=='undefined'&& window.Telegram.WebApp && window.Telegram.WebApp.BackButton) window.Telegram.WebApp.BackButton.show(); }catch(e){}
 const AR = `role="button" tabindex="0" onkeydown="if(event.key==='Enter'||event.key===''){event.preventDefault();this.click()}"`;
 var lb=$('langBar');if(lb)lb.style.display='none';
 setStripLockVisible(true);
 stripUnlocked=false; _stripTaps=0;
 const lb2=document.getElementById('stripLockBtn'); if(lb2){lb2.classList.remove('strip-unlocked');}
 const sc=document.getElementById('stripCard'); if(sc)sc.style.display='none';
 hideAllGameAreas();
 document.title = t('seaBattle');
 setStatus('');
 $('gameInfo').textContent='';
 $('header').classList.remove('in-game');
 $('app').insertBefore($('status'), $('app').firstChild);
 $('actions').className='btn-row stack';
 $('actions').innerHTML=`
 <div class="game-card" ${AR} aria-label="${t('vsBot')}" onclick="startSolo()" style="margin-bottom:8px">
 <img src="/static/mode-bot.svg" class="card-icon" alt="">
 <div class="card-name">${t('vsBot')}</div>
 </div>
 <div class="game-card" ${AR} aria-label="${t('vsFriend')}" onclick="chooseMultiMode()" style="margin-bottom:8px">
 <img src="/static/mode-friend.svg" class="card-icon" alt="">
 <div class="card-name">${t('vsFriend')}</div>
 </div>
 <div class="game-card" ${AR} aria-label="${t('stripMode')}" onclick="newMulti(true)" id="stripCard" style="display:none;margin-bottom:8px">
 <img src="/static/mode-shirt.svg" class="card-icon" alt="">
 <div class="name">${t('stripMode')}</div>
 <div class="card-desc">${t('stripDesc')}</div>
 </div>
 <button class="btn outline quit-btn" onclick="showMainMenu()">${t('quit')}</button>
 `;
 fetchActiveGames();
}

function tapStripLock(){
 const now=Date.now();
 if(now-_stripLastTap>1800)_stripTaps=0; // reset if gap between taps > 1.8s (not "normal pace")
 _stripLastTap=now; _stripTaps++;
 const btn=document.getElementById('stripLockBtn');
 if(_stripTaps>=5){
 stripUnlocked=true; _stripTaps=0;
 if(btn){ btn.classList.add('strip-unlocked'); btn.title='Разблокировано'; }
 const c=document.getElementById('stripCard'); if(c)c.style.display='';
 } else if(btn){
 btn.classList.remove('strip-unlocked');
 }
}

function setStripLockVisible(v){
 const b=document.getElementById('stripLockBtn');
 if(b)b.style.display = v ? '': 'none';
}

// Tracks which game-selection screen the user is currently on (null once a
// game is actually started or on any non-selection screen). Drives the ?
// help button so it only shows on the four selection screens.
let currentGameType = null;
let currentScreen = 'menu';
window.__sbBack = function(){
 if(currentScreen==='menu'){
 try{ if(typeof window.Telegram!=='undefined'&& window.Telegram.WebApp && window.Telegram.WebApp.BackButton) window.Telegram.WebApp.BackButton.hide(); }catch(e){}
 return;
 }
 showMainMenu();
};
function setHelpVisible(v){
 const b=document.getElementById('helpBtn');
 if(b) b.style.display = v ? '': 'none';
}

function chooseMultiMode(){
 setStripLockVisible(false);
 currentGameType=null; setHelpVisible(false);
 newMulti(false);
}

async function autoPlace(){
 const res=await api('/api/place_auto',{uid:getUid(),code:gameCode});
 if(res===null){ showRetry(t('error'), ()=>autoPlace()); return; }
 if(!res||!res.ok)return;
 sfxPlace();
 await refreshState();
 setStatus(t('again'),'');
}

async function confirmPlace(){
 const res=await api('/api/confirm',{uid:getUid(),code:gameCode});
 if(res===null){ showRetry(t('error'), ()=>confirmPlace()); return; }
 if(!res||!res.ok){
 setStatus('! '+ {ru:'Сначала расставь корабли!',uk:'Спочатку розстав кораблі!',en:'Place all ships first!'}[lang],'');
 return;
 }
 sfxClick();
 await refreshState();
}

function sbRenderOppHistory(_bs){
 // bot labels removed
}

async function handleShot(r,c){
 if(!state||!state.my_turn)return;
 if(_sbShooting) return; // block a second shot while one is in flight
 let cell=null, _ab=$('actions');
 try{
 _sbShooting=true;
 if(_ab) _ab.classList.add('actions-disabled');
 cell=document.querySelector('.cell.shootable[data-r="'+r+'"][data-c="'+c+'"]');
 if(cell) cell.classList.add('shooting');
 setStatus({ru:'Ожидание…',uk:'Очікування…',en:'Waiting…'}[lang],'battle');
 const res=await api('/api/shoot',{uid:getUid(),code:gameCode,r,c});
 if(res===null){ showRetry(t('error'), ()=>handleShot(r,c)); return; } // network failure after api's internal retry
 if(!res.ok){ setStatus(t('errorShot')); return; }

 let msg='';
 if(res.result.result==='hit'){msg=t('hit');sfxHit()}
 else if(res.result.result==='sunk'){msg=t('sunk');sfxSunk()}
 else if(res.result.result==='mine'){
 msg= {ru:'МИНА! Твой корабль поврежден!',uk:'МІНА! Твій корабель пошкоджено!',en:'MINE! Your ship is damaged!'}[lang];
 sfxSunk();
 }
 else {msg=t('miss');sfxMiss()}

 const bs=res.result.bot_shots;
 if(bs&&bs.length){
 sbRenderOppHistory(bs);
 const last=bs[bs.length-1];
 if(state) state._lastOppShot={r:last.r,c:last.c};
 }
 // Render the final board from the shot response immediately. This avoids a
 // race with polling and makes the win/loss result appear without delay.
 if(res.state){
 state=res.state;
 updateUI();
 if(state.all_sunk||state.my_all_sunk){
 if(!document.querySelector('.overlay')){
 showResult(state.all_sunk ? '': '', state.all_sunk ? t('win') : t('lose'), state.all_sunk ? t('winDesc') : t('loseDesc'), state.strip);
 }
 return;
 }
 }else{
 await refreshState();
 }
 if(msg)setStatus(msg,'battle');
 } finally {
 _sbShooting=false;
 if(cell) cell.classList.remove('shooting');
 if(_ab) _ab.classList.remove('actions-disabled');
 }
}

async function sendOpponentMessage(game='sea_battle', code=gameCode, gameState=state){
 if(!gameState || gameState.solo || !code)return;
 promptDialog(t('message'), t('messagePrompt'), (message)=>{
 if(!message) return;
 const text = message.trim();
 if(!text)return;
 api('/api/message_opponent',{uid:getUid(),code,message:text,game}).then(res=>{
 setStatus(res && res.ok ? t('messageSent') : t('messageError'), res && res.ok ? '': 'battle');
 });
 });
}

function showResult(icon,title,desc,strip,playAgainFn,playAgainLabel){
 closeFirstRollPopup();
 setStripLockVisible(false);
 currentGameType=null; setHelpVisible(false);
 stripUnlocked=false;
 const o=document.createElement('div');
 o.className='overlay';
 const won = icon==='';
 if(icon==='')sfxWin();else sfxLose();

 if(strip && icon===''){
 // The loser's stake photo was already committed (and
 // delivered to the winner) before the game started.
 o.innerHTML=`
 <div class="modal">
 <div class="result-icon"></div>
 <h2>${title}</h2>
 <p>${desc}</p>
 <button class="btn success" style="margin:4px 0;width:100%" onclick="this.closest('.overlay').remove();requestRematch()"> ${t('rematchLose')}</button>
 <button class="btn outline quit-btn" style="margin:4px 0;width:100%" onclick="this.closest('.overlay').remove();showMenu()">${t('quit')}</button>
 </div>`;
 document.body.appendChild(o);
 return;
 }

 if(strip && icon===''){
 const photo = state && (state.opp_stake || state.strip_photo) ? (state.opp_stake || state.strip_photo) : null;
 o.innerHTML=`
 <div class="modal">
 <div class="result-icon"></div>
 <h2>${title}</h2>
 <p>${desc}</p>
 ${photo ? `<img src="${photo}" style="max-width:90%;max-height:320px;border-radius:8px;margin:12px auto;display:block;object-fit:contain">` : ''}
 <button class="btn success" style="margin-top:8px" onclick="this.closest('.overlay').remove();requestRematch()"> ${t('rematchWin')}</button>
 <button class="btn outline" style="margin-top:8px" onclick="this.closest('.overlay').remove();showMenu()">${t('quit')}</button>
 </div>`;
 document.body.appendChild(o);
 return;
 }

 // Non-strip results (sea battle and the other games that reuse this modal).
 // Sea battle defaults to a same-code rematch; other games pass their own
 // "play again" action so they don't call the sea-battle rematch endpoint.
 const paFn = playAgainFn || 'requestRematch()';
 const paLabel = playAgainLabel || (won ? t('rematchWin') : t('rematchLose'));
 o.innerHTML=`
 <div class="modal">
 <div class="result-icon">${icon}</div>
 <h2>${title}</h2>
 <p>${desc}</p>
 <button class="btn success" style="margin-top:8px" onclick="this.closest('.overlay').remove();${paFn}">${paLabel}</button>
 <button class="btn outline" style="margin-top:8px" onclick="this.closest('.overlay').remove();showMenu()">${t('quit')}</button>
 </div>`;
 document.body.appendChild(o);
}

async function requestRematch(){
 if(rematchPending) return;
 // Both this player and the opponent must opt in; the server restarts the
 // SAME game (same code) once both agree, so nobody re-enters the code.
 const ov = document.querySelector('.overlay');
 if(ov) ov.remove();
 rematchPending = true;
 if(state) state._lastOppShot=null;
 setStatus(t('rematchWait'), 'battle');
 startGamePoll('sea_battle', gameCode, refreshState);
 const r=await api('/api/rematch', {uid:getUid(), code:gameCode});
 if(r===null){ showRetry(t('error'), ()=>requestRematch()); return; }
}

async function leaveGame(surrender){
 closeFirstRollPopup();
 stripUnlocked=false;
 delete _rollAckShown[gameCode];
 if(surrender){
 const msg = {ru:'Сдаться? Игра будет завершена.',uk:'Здатися? Гра буде завершена.',en:'Surrender? The game will end.'}[lang];
 confirmDialog(t('surrender')||'Surrender?', msg, ()=>{
 stopGamePoll('sea_battle');
 const _code = gameCode;
 localStorage.removeItem('sb_game');
 gameCode=null;if(state) state._lastOppShot=null;state=null;
 $('ownBoardWrap').classList.add('hidden');
 $('oppBoardWrap').classList.add('hidden');
 api('/api/surrender',{uid:getUid(),code:_code});
 showMainMenu();
 });
 return;
 }
 // Clear poll timer BEFORE any async operation to prevent refreshState/updateUI from re-showing boards
 stopGamePoll('sea_battle');
 const _code = gameCode;
 if(surrender) localStorage.removeItem('sb_game');
 gameCode=null;if(state) state._lastOppShot=null;state=null;
 // Hide boards BEFORE clearing other game data to ensure UI consistency
 $('ownBoardWrap').classList.add('hidden');
 $('oppBoardWrap').classList.add('hidden');
 if(surrender){
 await api('/api/surrender',{uid:getUid(),code:_code});
 }
 showMainMenu();
}

function showSeaBattle(){ showSeaBattleMenu(); }

async function fetchActiveGames(){
 const cont=$('activeGamesContainer');
 if(!cont)return;
 const res=await api('/api/active_games',{uid:getUid()});
 if(!res||!res.ok||!res.games||!res.games.length){
 cont.innerHTML='';
 return;
 }
 var html='<div class="active-games"><h3>'+t('activeGames')+'</h3>';
 for(const g of res.games){
 const exitBtn='<button class="active-game-exit" title="'+{ru:'Выйти',uk:'Вийти',en:'Exit'}[lang]+'" onclick="event.stopPropagation();abandonGame(\''+g.type+'\',\''+g.code+'\')">x</button>';
 if(g.type==='sea_battle'){
 var badge=g.my_turn?'<span class="badge playing"> '+t('yourTurn')+'</span>':'<span class="badge"> '+{ru:'ожидание...',uk:'очікування...',en:'waiting...'}[lang]+'</span>';
 html+='<div class="active-game-row" onclick="resumeSB(\''+g.code+'\')"><div class="info"><span class="label"> </span><span class="code">'+g.code+'</span></div>'+badge+exitBtn+'</div>';
 }
 else if(g.type==='poker_dice'){
 var badge=g.my_turn?'<span class="badge playing"> '+t('yourTurn')+'</span>':'<span class="badge"> '+{ru:'ожидание...',uk:'очікування...',en:'waiting...'}[lang]+'</span>';
 html+='<div class="active-game-row" onclick="resumePd(\''+g.code+'\')"><div class="info"><span class="label"> </span><span class="code">'+g.code+'</span></div>'+badge+exitBtn+'</div>';
 }
 else if(g.type==='checkers'){
 var badge=g.my_turn?'<span class="badge playing"> '+t('yourTurn')+'</span>':'<span class="badge"> '+{ru:'ожидание...',uk:'очікування...',en:'waiting...'}[lang]+'</span>';
 html+='<div class="active-game-row" onclick="resumeCk(\''+g.code+'\')"><div class="info"><span class="label"> </span><span class="code">'+g.code+'</span></div>'+badge+exitBtn+'</div>';
 }
 else if(g.type==='backgammon'){
 var badge=g.my_turn?'<span class="badge playing"> '+t('bgYourTurn')+'</span>':'<span class="badge"> '+{ru:'ожидание...',uk:'очікування...',en:'waiting...'}[lang]+'</span>';
 html+='<div class="active-game-row" onclick="resumeBg(\''+g.code+'\')"><div class="info"><span class="label"> </span><span class="code">'+g.code+'</span></div>'+badge+exitBtn+'</div>';
 }
 }
 html+='</div>';
 cont.innerHTML=html;
}

async function abandonGame(type, code){
 if(!code) return;
 let endpoint = null;
 if(type==='poker_dice') endpoint='/api/pd_surrender';
 else if(type==='sea_battle') endpoint='/api/surrender';
 else if(type==='checkers') endpoint='/api/checkers_surrender';
 else if(type==='backgammon') endpoint='/api/bg_surrender';
 if(!endpoint) return;
 const key = type==='poker_dice'?'pd_game':type==='sea_battle'?'sb_game':type==='checkers'?'ck_game':'bg_game';
 localStorage.removeItem(key);
 try {
 await api(endpoint, {uid:getUid(), code:code});
 } catch(e) {}
 fetchActiveGames();
}

function resumeSB(code){
 gameCode=code;
 localStorage.setItem('sb_game',code);
 $('actions').innerHTML='';
 refreshState();
 setTimeout(()=>startGamePoll('sea_battle', gameCode, refreshState),500);
}

function resumeCk(code){
 currentGameType=null; setHelpVisible(false); setStripLockVisible(false);
 ckCode=code;
 localStorage.setItem('ck_game',code);
 $('actions').innerHTML='';
 _lastCKSig=null; _lastCKBoardSig=null; currentScreen='checkers';
 // Reset ckArea visibility
 if($('ckArea')) $('ckArea').style.display='';
 // Reset the bot opening flag so the game renders correctly
 _ckBotOpening=false;
 // Do NOT delete _rollAckShown here - the first roll result should only show once
 // If the game is in 'playing' phase, we should see the board, not the popup
 ckRefreshState();
 setTimeout(()=>startGamePoll('checkers', ckCode, ckRefreshState),500);
}

function tryReconnect(){
 showMenu();
 fetchBotInfo().then(() => checkStartParam());
}

async function checkStartParam(){
 try {
 const sp = window.Telegram?.WebApp?.initDataUnsafe?.start_param;
 if(!sp) return;
 await joinByCode(sp.trim().toUpperCase());
 } catch(e){}
}

lang = detectLang();
setLang(lang);
initTheme();
renderPlayerName();
initTG();
tryReconnect();

// Pause polling while the tab/WebApp is hidden; resume (and force a refresh)
// when it becomes visible again. Guarded so we never double-start a poll.
document.addEventListener('visibilitychange', function(){
 if(document.hidden){
 pauseAllPolls();
 } else {
 resumeAllPolls();
 }
});
