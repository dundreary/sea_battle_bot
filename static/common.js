const LANG = {
  ru: {
    title: '⚓ МОРСКОЙ БОЙ',
    startBtn: '🎮 Начать игру',
    ownBoard: '🚢 ТВОИ КОРАБЛИ',
    oppBoard: '🎯 ДОСКА СОПЕРНИКА',
    legEmpty: 'пусто', legShip: 'корабль', legHit: 'попал', legMiss: 'мимо', legSunk: 'потоплен',
    welcome: '🔱 Добро пожаловать!',
    placing: '🚢 Расстановка — крути, пока не устроит',
    reroll: '🔀 Переставить',
    confirm: '✅ ОК, начинаем!',
    rollTitle: 'Бросьте кубик — кто больше, тот ходит первым',
    rollBtn: 'Бросить кубик',
    rollYou: 'Ваш бросок',
    rollWait: 'Ожидание броска соперника…',
    rollWin: '🎉 Вы ходите первым!',
    rollLose: 'Соперник ходит первым',
    rollTie: '🤝 Ничья — бросайте ещё раз!',
    rollContinue: 'Продолжить',
    rollWon: '🎉 Вы выиграли бросок!',
    rollLost: 'Соперник выиграл бросок',
    rollYouFirst: 'Вы ходите первым',
    rollOppFirst: 'Соперник ходит первым',
    again: '🔄 Ещё раз? Нажми «ОК» когда устроит',
    yourTurn: '⚓ ТВОЙ ХОД!',
    oppTurn: '⏳ ХОД СОПЕРНИКА...',
    message: 'Сообщение',
    messagePrompt: 'Сообщение сопернику (до 280 символов):',
    messageSent: 'Сообщение отправлено ✅',
    messageError: 'Не удалось отправить сообщение',
    surrender: 'Сдаться',
    quit: '🚪 Выйти',
    quitConfirm: 'Выйти из игры?',
    hit: '🔥 Попадание!',
    sunk: '💀 Корабль потоплен!',
    miss: '💨 Мимо!',
    botHit: 'попал в',
    botSunk: 'потопил',
    botMiss: 'мимо',
    win: '🏆 ПОБЕДА!',
    winDesc: 'Ты потопил все корабли соперника!',
    lose: '💔 ПОРАЖЕНИЕ',
    loseDesc: 'Все твои корабли потоплены...',
    playAgain: '🔄 Играть ещё',
    close: '🚪 Закрыть',
    withBot: '· с ботом',
    withFriend: '· с другом',
    vsBot: 'С ботом',
    vsFriend: 'С другом',
    joinTitle: 'Присоединиться',
    joinBtn: 'Ввести код',
    joinPlaceholder: 'Введи код игры',
    joinError: '⚠️ Игра не найдена или уже полная',
    waitOpp: '⏳ Ожидаем соперника...',
    codeShare: '📤 Код: <b>{}</b> — отправь другу',
    error: '⚠️ Ошибка соединения',
    errorShot: '⚠️ Сюда уже стреляли',
    gameOver: '🔱 Игра закончилась.',
    gameInfo: '{code} {mode}',
    seaBattle: 'Морской бой',
    selectGame: 'Выбери режим',
    inviteFriend: 'Пригласить друга',
    ckInviteFriend: 'Пригласить друга',
    shareCopied: 'Код скопирован, отправь другу',
    copyCode: 'Нажми, чтобы скопировать код',
    settings: 'Настройки',
    sound: 'Звук',
    vibration: 'Вибрация',
    shipHint: '🚢 Корабли: {0}',
    mine: '💣 Мина',
    stripMode: 'На раздевание',
    stripTitle: '👗 Морской бой — На раздевание',
    stripPlace: '👗 Расставь корабли-одежду',
    stripDesc: 'Корабли могут быть любой формы!',
    stripInfoDesc: 'Фото отправится сопернику только если ты проиграешь.',
    stripLoseTitle: '👗 Игра окончена!',
    stripLoseDesc: 'Ты проиграл в режиме «На раздевание». Загрузи фото.',
    stripUploadTitle: '📸 Загрузи фото',
    stripUploadDesc: 'Выбери способ загрузки фото:',
    stripTakePhoto: '📷 Сделать фото',
    stripChoosePhoto: '🖼 Из галереи',
    stripPhotoSent: 'Фото отправлено победителю ✅',
    stripUseStandard: '🎭 Стандартное фото',
    stripSkip: '⏭ Пропустить',
    stripStakeBtn: '📸 Загрузить фото',
    stripStart: '🍀 Удачи, начинаем',
    stripPlayAgain: '💪 Отыграться',
    rematchWin: '🎉 Ещё партию',
    rematchLose: '💪 Отыграться',
    rematchWait: '⏳ Ожидание соперника для реванша...',
    checkers: 'Шашки',
    ckHint: '💡 Подсказка',
    ckNoMoves: 'Нет ходов',
    backgammon: 'Нарды',
    bgSolo: '🕹️ Соло',
    bgFriend: '👤 С другом',
    bgRoll: '🎲 Бросить',
    bgWaiting: '⏳ Ожидаем соперника...',
    bgWin: '🏆 Ты победил!',
    bgLose: '💔 Ты проиграл',
    bgPlayAgain: '🔄 Играть ещё',
    bgYourTurn: '♟ ТВОЙ ХОД!',
    bgOppTurn: '♟ ХОД СОПЕРНИКА...',
    stEasy: 'Легко',
    stMedium: 'Средне',
    stHard: 'Сложно',
    stExpert: 'Эксперт',
    selectDifficulty: 'Выбери сложность',
    pdTitle: 'Покер в кости',
    pdSolo: '🕹️ Соло',
    pdFriend: '👤 С другом',
    pdRoll: '🎲 Бросить',
    pdScore: '📊 Закончить',
    pdWaiting: '⏳ Ожидаем соперника...',
    pdYourHand: 'Твоя рука',
    pdOppHand: 'Рука соперника',
    pdWin: '🏆 Ты победил!',
    pdLose: '💔 Ты проиграл',
    pdDraw: '🤝 Ничья',
    pdPlayAgain: '🔄 Играть ещё',
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
    continue: '▶ Продолжить',
    minimize: 'Свернуть',
    activeGames: '▶ Активные игры',
    statsMenu: '📊 Статистика',
    statsTitle: 'Статистика',
    statsWins: 'Победы',
    statsLosses: 'Поражения',
    statsDraws: 'Ничьи',
    statsWinrate: 'Процент побед',
    statsTotal: 'Всего игр',
    statsHistory: 'Последние игры',
    statsNoGames: 'Пока нет сыгранных игр',
    statsResWin: 'Победа',
    statsResLoss: 'Поражение',
    statsResDraw: 'Ничья',
    bgVariantShort: 'Короткие',
    bgVariantLong: 'Длинные',
  },
  uk: {
    title: 'Морський бій',
    startBtn: '🎮 Почати гру',
    ownBoard: '🚢 ТВОЇ КОРАБЛІ',
    oppBoard: '🎯 ДОШКА СУПЕРНИКА',
    legEmpty: 'порожньо', legShip: 'корабель', legHit: 'влучив', legMiss: 'повз', legSunk: 'потоплено',
    welcome: '🔱 Ласкаво просимо!',
    placing: '🚢 Розстановка — крути, поки не сподобається',
    reroll: '🔀 Переставити',
    confirm: '✅ ОК, починаємо!',
    rollTitle: 'Киньте кубик — хто більше, той ходить першим',
    rollBtn: 'Кинути кубик',
    rollYou: 'Ваш кидок',
    rollWait: 'Очікування кидка суперника…',
    rollWin: '🎉 Ви ходите першим!',
    rollLose: 'Суперник ходить першим',
    rollTie: '🤝 Нічия — киньте ще раз!',
    rollContinue: 'Продовжити',
    rollWon: '🎉 Ви виграли кидок!',
    rollLost: 'Суперник виграв кидок',
    rollYouFirst: 'Ви ходите першим',
    rollOppFirst: 'Суперник ходить першим',
    again: '🔄 Ще раз? Натисни «ОК» коли влаштує',
    yourTurn: '⚓ ТВІЙ ХІД!',
    oppTurn: '⏳ ХІД СУПЕРНИКА...',
    message: 'Повідомлення',
    messagePrompt: 'Повідомлення супернику (до 280 символів):',
    messageSent: 'Повідомлення надіслано ✅',
    messageError: 'Не вдалося надіслати повідомлення',
    surrender: 'Здатися',
    quit: '🚪 Вийти',
    quitConfirm: 'Вийти з гри?',
    hit: '🔥 Влучив!',
    sunk: '💀 Корабель потоплено!',
    miss: '💨 Повз!',
    botHit: 'влучив у',
    botSunk: 'потопив',
    botMiss: 'повз',
    win: '🏆 ПЕРЕМОГА!',
    winDesc: 'Ти потопив усі кораблі суперника!',
    lose: '💔 ПОРАЗКА',
    loseDesc: 'Усі твої кораблі потоплені...',
    playAgain: '🔄 Грати ще',
    close: '🚪 Закрити',
    withBot: '· з ботом',
    withFriend: '· з другом',
    vsBot: 'З ботом',
    vsFriend: 'З другом',
    joinTitle: 'Приєднатися',
    joinBtn: 'Ввести код',
    joinPlaceholder: 'Введи код гри',
    joinError: '⚠️ Гру не знайдено або вже повна',
    waitOpp: '⏳ Чекаємо суперника...',
    codeShare: '📤 Код: <b>{}</b> — відправ другу',
    error: '⚠️ Помилка з\'єднання',
    errorShot: '⚠️ Сюди вже стріляли',
    gameOver: '🔱 Гра закінчилась.',
    gameInfo: '{code} {mode}',
    seaBattle: 'Морський бій',
    selectGame: 'Обери режим',
    inviteFriend: 'Запросити друга',
    ckInviteFriend: 'Запросити друга',
    shareCopied: 'Код скопійовано, надішли другу',
    copyCode: 'Натисни, щоб скопіювати код',
    settings: 'Налаштування',
    sound: 'Звук',
    vibration: 'Вібрація',
    shipHint: '🚢 Кораблі: {0}',
    mine: '💣 Міна',
    stripMode: 'На роздягання',
    stripTitle: '👗 Морський бій — На роздягання',
    stripPlace: '👗 Розстав кораблі-одяг',
    stripDesc: 'Кораблі можуть бути будь-якої форми!',
    stripInfoDesc: 'Фото надішлеться супернику тільки якщо ти програєш.',
    stripLoseTitle: '👗 Гра закінчена!',
    stripLoseDesc: 'Ти програв у режимі «На роздягання». Завантаж фото.',
    stripUploadTitle: '📸 Завантаж фото',
    stripUploadDesc: 'Обери спосіб завантаження фото:',
    stripTakePhoto: '📷 Зробити фото',
    stripChoosePhoto: '🖼 З галереї',
    stripPhotoSent: 'Фото надіслано переможцю ✅',
    stripUseStandard: '🎭 Стандартне фото',
    stripSkip: '⏭ Пропустити',
    stripStakeBtn: '📸 Завантажити фото',
    stripStart: '🍀 Удачі, починаємо',
    stripPlayAgain: '💪 Відігратись',
    rematchWin: '🎉 Ще партію',
    rematchLose: '💪 Відігратись',
    rematchWait: '⏳ Очікування суперника для реваншу...',
    checkers: 'Шашки',
    ckHint: '💡 Підказка',
    ckNoMoves: 'Немає ходів',
    backgammon: 'Нарди',
    bgSolo: '🕹️ Соло',
    bgFriend: '👤 З другом',
    bgRoll: '🎲 Кинути',
    bgWaiting: '⏳ Чекаємо суперника...',
    bgWin: '🏆 Ти переміг!',
    bgLose: '💔 Ти програв',
    bgPlayAgain: '🔄 Грати ще',
    bgYourTurn: '♟ ТВІЙ ХІД!',
    bgOppTurn: '♟ ХІД СУПЕРНИКА...',
    stEasy: 'Легко',
    stMedium: 'Середньо',
    stHard: 'Складно',
    stExpert: 'Експерт',
    selectDifficulty: 'Обери складність',
    pdTitle: 'Покер у кості',
    pdSolo: '🕹️ Соло',
    pdFriend: '👤 З другом',
    pdRoll: '🎲 Кинути',
    pdScore: '📊 Закінчити',
    pdWaiting: '⏳ Чекаємо суперника...',
    pdYourHand: 'Твоя рука',
    pdOppHand: 'Рука суперника',
    pdWin: '🏆 Ти переміг!',
    pdLose: '💔 Ти програв',
    pdDraw: '🤝 Нічия',
    pdPlayAgain: '🔄 Грати ще',
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
    continue: '▶ Продовжити',
    minimize: 'Згорнути',
    activeGames: '▶ Активні ігри',
    statsMenu: '📊 Статистика',
    statsTitle: 'Статистика',
    statsWins: 'Перемоги',
    statsLosses: 'Поразки',
    statsDraws: 'Нічиї',
    statsWinrate: 'Відсоток перемог',
    statsTotal: 'Усього ігор',
    statsHistory: 'Останні ігри',
    statsNoGames: 'Поки що немає зіграних ігор',
    statsResWin: 'Перемога',
    statsResLoss: 'Поразка',
    statsResDraw: 'Нічия',
    bgVariantShort: 'Короткі',
    bgVariantLong: 'Довгі',
  },
  en: {
    title: 'Sea Battle',
    startBtn: '🎮 Start Game',
    ownBoard: '🚢 YOUR SHIPS',
    oppBoard: '🎯 OPPONENT\'S BOARD',
    legEmpty: 'empty', legShip: 'ship', legHit: 'hit', legMiss: 'miss', legSunk: 'sunk',
    welcome: '🔱 Welcome aboard!',
    placing: '🚢 Place ships — reroll until you like it',
    reroll: '🔀 Reroll',
    confirm: '✅ OK, start!',
    rollTitle: 'Roll a die — higher goes first',
    rollBtn: 'Roll die',
    rollYou: 'Your roll',
    rollWait: 'Waiting for opponent to roll…',
    rollWin: '🎉 You go first!',
    rollLose: 'Opponent goes first',
    rollTie: '🤝 Tie — roll again!',
    rollContinue: 'Continue',
    rollWon: '🎉 You won the roll!',
    rollLost: 'Opponent won the roll',
    rollYouFirst: 'You go first',
    rollOppFirst: 'Opponent goes first',
    again: '🔄 Again? Press «OK» when ready',
    yourTurn: '⚓ YOUR TURN!',
    oppTurn: '⏳ OPPONENT\'S TURN...',
    message: 'Message',
    messagePrompt: 'Message to your opponent (up to 280 characters):',
    messageSent: 'Message sent ✅',
    messageError: 'Could not send message',
    surrender: 'Surrender',
    quit: '🚪 Quit',
    quitConfirm: 'Leave the game?',
    hit: '🔥 Hit!',
    sunk: '💀 Ship sunk!',
    miss: '💨 Miss!',
    botHit: 'hit at',
    botSunk: 'sunk at',
    botMiss: 'missed',
    win: '🏆 VICTORY!',
    winDesc: 'You sank all enemy ships!',
    lose: '💔 DEFEAT',
    loseDesc: 'All your ships are sunk...',
    playAgain: '🔄 Play again',
    close: '🚪 Close',
    withBot: '· vs bot',
    withFriend: '· vs friend',
    vsBot: 'vs Bot',
    vsFriend: 'vs Friend',
    joinTitle: 'Join Game',
    joinBtn: 'Enter Code',
    joinPlaceholder: 'Enter game code',
    joinError: '⚠️ Game not found or full',
    waitOpp: '⏳ Waiting for opponent...',
    codeShare: '📤 Code: <b>{}</b> — send to your friend',
    error: '⚠️ Connection error',
    errorShot: '⚠️ Already targeted',
    gameOver: '🔱 Game over.',
    gameInfo: '{code} {mode}',
    seaBattle: 'Sea Battle',
    selectGame: 'Select mode',
    inviteFriend: 'Invite friend',
    ckInviteFriend: 'Invite friend',
    shareCopied: 'Code copied, send to friend',
    copyCode: 'Tap to copy code',
    settings: 'Settings',
    sound: 'Sound',
    vibration: 'Vibration',
    shipHint: '🚢 Ships: {0}',
    mine: '💣 Mine',
    stripMode: 'Strip Mode',
    stripTitle: '👗 Sea Battle — Strip Mode',
    stripPlace: '👗 Place clothing ships',
    stripDesc: 'Ships can be any shape!',
    stripInfoDesc: 'The photo will be sent to your opponent only if you lose.',
    stripLoseTitle: '👗 Game Over!',
    stripLoseDesc: 'You lost in Strip Mode. Upload a photo.',
    stripUploadTitle: '📸 Upload Photo',
    stripUploadDesc: 'Choose how to upload a photo:',
    stripTakePhoto: '📷 Take Photo',
    stripChoosePhoto: '🖼 From Gallery',
    stripPhotoSent: 'Photo sent to winner ✅',
    stripUseStandard: '🎭 Standard Photo',
    stripSkip: '⏭ Skip',
    stripStakeBtn: '📸 Upload photo',
    stripStart: '🍀 Good luck, let\'s begin',
    stripPlayAgain: '💪 Redeem',
    rematchWin: '🎉 Another game',
    rematchLose: '💪 Replay',
    rematchWait: '⏳ Waiting for opponent to rematch...',
    checkers: 'Checkers',
    ckHint: '💡 Hint',
    ckNoMoves: 'No moves',
    backgammon: 'Backgammon',
    bgSolo: '🕹️ Solo',
    bgFriend: '👤 With Friend',
    bgRoll: '🎲 Roll',
    bgWaiting: '⏳ Waiting for opponent...',
    bgWin: '🏆 You Win!',
    bgLose: '💔 You Lose',
    bgPlayAgain: '🔄 Play again',
    bgYourTurn: '♟ YOUR TURN!',
    bgOppTurn: '♟ OPPONENT\'S TURN...',
    stEasy: 'Easy',
    stMedium: 'Medium',
    stHard: 'Hard',
    stExpert: 'Expert',
    selectDifficulty: 'Choose difficulty',
    pdTitle: 'Poker Dice',
    pdSolo: '🕹️ Solo',
    pdFriend: '👤 With Friend',
    pdRoll: '🎲 Roll',
    pdScore: '📊 Score',
    pdWaiting: '⏳ Waiting for opponent...',
    pdYourHand: 'Your Hand',
    pdOppHand: 'Opponent\'s Hand',
    pdWin: '🏆 You Win!',
    pdLose: '💔 You Lose',
    pdDraw: '🤝 Draw',
    pdPlayAgain: '🔄 Play again',
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
    continue: '▶ Continue',
    minimize: 'Minimize',
    activeGames: '▶ Active games',
    statsMenu: '📊 Stats',
    statsTitle: 'Statistics',
    statsWins: 'Wins',
    statsLosses: 'Losses',
    statsDraws: 'Draws',
    statsWinrate: 'Win rate',
    statsTotal: 'Total games',
    statsHistory: 'Recent games',
    statsNoGames: 'No games played yet',
    statsResWin: 'Win',
    statsResLoss: 'Loss',
    statsResDraw: 'Draw',
    bgVariantShort: 'Short',
    bgVariantLong: 'Long',
  }
};

const API = window.location.origin;
let state = null, uid = null, gameCode = null, lang = 'ru';
let botUsername = '';

function $(id){return document.getElementById(id)}

function hideAllGameAreas(){
  $('ownBoardWrap').style.display='none';
  $('oppBoardWrap').style.display='none';
  $('pdArea').style.display='none';
  $('ckArea').style.display='none';
  $('bgArea').style.display='none';
  $('shipHint').innerHTML = '';
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

function toggleSnd(){_snd=!_snd;localStorage.setItem('sb_snd',_snd?'1':'0');updateSettingsUI()}
function toggleVibe(){_vibe=!_vibe;localStorage.setItem('sb_vibe',_vibe?'1':'0');updateSettingsUI()}
function updateSettingsUI(){
  const sndBtn=document.getElementById('sndBtn');
  const vibeBtn=document.getElementById('vibeBtn');
  const sndBtnPd=document.getElementById('sndBtnPd');
  const vibeBtnPd=document.getElementById('vibeBtnPd');
  const sndBtnCk=document.getElementById('sndBtnCk');
  const vibeBtnCk=document.getElementById('vibeBtnCk');
  const sndIcon=_snd?'🔊':'🔇';
  const vibeIcon=_vibe?'📳':'📴';
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
  
  document.documentElement.className = 'palette-' + themeName;
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
  const existing=$('settingsOverlay');
  if(existing){existing.remove()}
  const o=document.createElement('div');o.className='overlay';o.id='settingsOverlay';
  const curTheme = document.documentElement.className.indexOf('forest')>=0 ? 'forest' : 'ocean';
  o.innerHTML=`
    <div class="modal">
      <h2>⚙️ ${t('settings')}</h2>
      <div class="sett-row" onclick="setTheme('ocean');showSettings()"><span>🌊 Ocean</span><span class="sett-val">${curTheme==='ocean'?'✅':''}</span></div>
      <div class="sett-row" onclick="setTheme('forest');showSettings()"><span>🌲 Forest</span><span class="sett-val">${curTheme==='forest'?'✅':''}</span></div>
      <div class="sett-row" onclick="toggleSnd();showSettings()"><span>🔊 ${t('sound')}</span><span class="sett-val" id="sndBtn">${_snd?'🔊':'🔇'}</span></div>
      <div class="sett-row" onclick="toggleVibe();showSettings()"><span>📳 ${t('vibration')}</span><span class="sett-val" id="vibeBtn">${_vibe?'📳':'📴'}</span></div>
      <button class="btn outline" style="margin-top:16px" onclick="this.closest('.overlay').remove()">${t('close')}</button>
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
  if(args.length) s = s.replace('{0}', args[0]).replace('{1}', args[1]);
  return s;
}

function setLang(l){
  lang = l;
  try{localStorage.setItem('sb_lang', l)}catch(e){}
  const langMap = {ru:'ru', ua:'uk', en:'en'};
  document.querySelectorAll('.lang-btn').forEach(b => b.classList.toggle('active', (langMap[b.textContent.toLowerCase()]||b.textContent.toLowerCase()) === l));
  applyLang();
  if(state) updateUI();
}

function applyLang(){
  $('lblOwn').textContent = t('ownBoard');
  $('lblOpp').textContent = t('oppBoard');
  if(!state && !gameCode) showMenu();
  else document.title=t('title')
}

function initTG(){try{window.Telegram.WebApp.ready();window.Telegram.WebApp.expand()}catch(e){}}
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
  const title=document.createElement('h2'); title.textContent='💬 '+t('message');
  const body=document.createElement('p'); body.style.whiteSpace='pre-wrap'; body.textContent=text;
  const close=document.createElement('button'); close.className='btn primary'; close.style.width='100%'; close.textContent='OK';
  close.onclick=()=>{o.remove();showIncomingMessages([])};
  modal.append(title,body,close); o.appendChild(modal); document.body.appendChild(o);
}

async function api(method,data,_isRetry){
  try{
    data = data || {};
    data.lang = lang;
    try{ data.init_data = window.Telegram.WebApp.initData || ''; }catch(e){ data.init_data = ''; }
    const r=await fetch(API+method,{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify(data)});
    return await r.json()
  }catch(e){
    // A single quick retry absorbs the brief network blips that are common
    // on mobile (wifi/cell handoff, a momentary drop) instead of surfacing a
    // scary "connection error" for something that would have recovered a
    // second later on its own.
    if(!_isRetry){
      await new Promise(res=>setTimeout(res,800));
      return api(method,data,true);
    }
    setStatus(t('error'));
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
  boardEl.innerHTML='';
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
  for(let r=0;r<10;r++)for(let c=0;c<10;c++){
    const cell=document.createElement('div');
    const v=grid[r*10+c];
    cell.className='cell';
    let stateWord=STATE_LABEL.empty;
    if(v===EMPTY||v===SHIP||v===MINE){cell.classList.add('empty');if(v===SHIP){cell.classList.add(isStrip?'strip-ship':'ship');stateWord=STATE_LABEL.ship;if(isOpponent&&gameOver)cell.classList.add('enemy-reveal')}else if(v===MINE){cell.classList.add('mine');stateWord=STATE_LABEL.mine;if(isOpponent&&gameOver)cell.classList.add('enemy-reveal')}}
    else if(v===HIT){cell.classList.add('hit');cell.textContent='❌';stateWord=STATE_LABEL.hit}
    else if(v===MINE_HIT){cell.classList.add('mine');stateWord=STATE_LABEL.mine;if(isOpponent&&gameOver)cell.classList.add('enemy-reveal')}
    else if(v===MISS){cell.classList.add('miss');cell.textContent='·';stateWord=STATE_LABEL.miss}
    else if(v===SUNK){cell.classList.add('sunk');cell.textContent='✖';stateWord=STATE_LABEL.sunk}
    else if(v===DEAD){cell.classList.add('dead');cell.textContent='·'}
    else cell.classList.add('empty');
    cell.setAttribute('aria-label', COLS[c]+(r+1)+': '+stateWord);
    const shootable = isOpponent&&!gameOver&&(v===EMPTY||v===SHIP);
    if(shootable){
      cell.classList.add('shootable');
      cell.setAttribute('role','button');
      cell.tabIndex=0;
      cell.onclick=()=>handleShot(r,c);
      cell.onkeydown=(e)=>{ if(e.key==='Enter'||e.key===' '){ e.preventDefault(); handleShot(r,c); } };
    }
    boardEl.appendChild(cell);
  }
}

async function refreshState(){
  if(!gameCode)return;
  const res=await api('/api/state',{uid:getUid(),code:gameCode});
  if(!res||!res.ok){
    localStorage.removeItem('sb_game');
    setStatus(t('gameOver'));
    $('actions').className='btn-row';
    $('actions').innerHTML=`<button class="btn primary" onclick="startSolo()">${t('startBtn')}</button>`;
    return
  }
  if(!gameCode)return;
  state=res.state;
  updateUI();
}

function renderShipHint(shipsList, shipsPlaced, isStrip, minePlaced){
  $('shipHint').innerHTML = '';
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
function diceFace(n){ return ['','⚀','⚁','⚂','⚃','⚄','⚅'][n] || '🎲'; }

function _dieSvg(n, extraClass){
  const pips = DIE_PIPS[n] || [];
  const dots = pips.map(([x,y]) => `<circle cx="${x}" cy="${y}" r="9"></circle>`).join('');
  return `<div class="roll-die3d${extraClass ? ' '+extraClass : ''}"><svg viewBox="0 0 100 100">${dots}</svg></div>`;
}

function firstRollHTML(s, rollFn, rerollFn){
  const label = (txt, sub)=>`<div class="roll-die-label">${txt}${sub?`<span>${sub}</span>`:''}</div>`;
  const mySide = (n, waiting)=>`<div class="roll-die-col">${_dieSvg(n||1, waiting?'roll-die-pending':'')}${label(t('rollYou'))}</div>`;
  const oppSide = (n, waiting)=>`<div class="roll-die-col">${_dieSvg(n||1, waiting?'roll-die-pending':'')}${label('🎯')}</div>`;

  if(s.my_roll==null && s.opp_roll==null){
    return `<div class="roll-stage">
      <div class="roll-title">${t('rollTitle')}</div>
      <div class="roll-die-row">${mySide(1,true)}<div class="roll-vs">VS</div>${oppSide(1,true)}</div>
      <button class="btn primary roll-cta" id="rollBtn" onclick="${rollFn}()">🎲 ${t('rollBtn')}</button>
    </div>`;
  }
  if(s.my_roll!=null && s.opp_roll==null){
    return `<div class="roll-stage">
      <div class="roll-die-row">${mySide(s.my_roll,false)}<div class="roll-vs">VS</div>${oppSide(1,true)}</div>
      <div class="roll-wait">${t('rollWait')}</div>
    </div>`;
  }
  if(s.my_roll==null && s.opp_roll!=null){
    return `<div class="roll-stage">
      <div class="roll-title">${t('rollTitle')}</div>
      <div class="roll-die-row">${mySide(1,true)}<div class="roll-vs">VS</div>${oppSide(s.opp_roll,false)}</div>
      <button class="btn primary roll-cta" id="rollBtn" onclick="${rollFn}()">🎲 ${t('rollBtn')}</button>
    </div>`;
  }
  // Both rolled.
  if(s.my_roll === s.opp_roll){
    return `<div class="roll-stage">
      <div class="roll-die-row">${mySide(s.my_roll,false)}<div class="roll-vs">VS</div>${oppSide(s.opp_roll,false)}</div>
      <div class="roll-result roll-tie">${t('rollTie')}</div>
      <button class="btn primary roll-cta" id="rerollBtn" onclick="${rerollFn}()">🔄 ${t('reroll')}</button>
    </div>`;
  }
  const won = s.my_roll > s.opp_roll;
  // Once the dice are decided the roll screen becomes a result screen: both
  // dice plus who moves first, with a Continue button. In solo, if the bot won
  // the opening roll its first shot is taken when the human continues.
  return `<div class="roll-stage">
    <div class="roll-die-row">${mySide(s.my_roll,false)}<div class="roll-vs">VS</div>${oppSide(s.opp_roll,false)}</div>
    <div class="roll-result ${won?'roll-win':'roll-lose'}">${won ? t('rollWin') : t('rollLose')}</div>
    <button class="btn primary roll-cta" id="rollDoneBtn" onclick="ackRoll()">▶ ${t('rollContinue')}</button>
  </div>`;
}

// One-shot guard keyed by game code: the winner banner must appear only once
// when the opening roll resolves, not on every polling refresh afterwards.
const _rollBannerShown = {};
const _rollAckShown = {};

function armRollBanner(code){
  if(code) delete _rollBannerShown[code];
}

// Show a brief, non-blocking banner over the board announcing who won the
// opening dice roll (and therefore moves first). Called from each game's
// render once the board is on screen and both players have rolled a decisive
// value. Relies on my_roll/opp_roll, which the backend keeps sending even in
// the 'playing' phase.
function showRollWinnerBanner(st, code){
  if(!st || st.my_roll == null || st.opp_roll == null || st.my_roll === st.opp_roll) return;
  if(!code || _rollBannerShown[code]) return;
  _rollBannerShown[code] = true;

  const won = st.my_roll > st.opp_roll;
  const myDie  = _dieSvg(st.my_roll,  won ? 'roll-die-win' : '');
  const oppDie = _dieSvg(st.opp_roll, !won ? 'roll-die-win' : '');

  const overlay = document.createElement('div');
  overlay.className = 'roll-winner-overlay';
  overlay.innerHTML = `
    <div class="roll-winner-card ${won ? 'win' : 'lose'}">
      <div class="roll-winner-title">${won ? t('rollWon') : t('rollLost')}</div>
      <div class="roll-die-row">
        <div class="roll-die-col">${myDie}<div class="roll-die-label">${t('rollYou')}</div></div>
        <div class="roll-vs">${st.my_roll} : ${st.opp_roll}</div>
        <div class="roll-die-col">${oppDie}<div class="roll-die-label">🎯</div></div>
      </div>
      <div class="roll-winner-sub">${won ? t('rollYouFirst') : t('rollOppFirst')}</div>
    </div>`;
  document.body.appendChild(overlay);
  setTimeout(() => overlay.classList.add('roll-winner-out'), 2500);
  setTimeout(() => overlay.remove(), 3200);
}

async function doFirstRoll(endpoint, codeVal, refreshFn){
  const btn = document.getElementById('rollBtn');
  if(btn) btn.disabled = true;
  const dieEl = document.querySelector('.roll-die-col:first-child .roll-die3d');
  let anim = null;
  if(dieEl){
    dieEl.classList.add('roll-die-spinning');
    anim = setInterval(()=>{
      const n = 1 + Math.floor(Math.random()*6);
      const pips = DIE_PIPS[n] || [];
      dieEl.querySelector('svg').innerHTML = pips.map(([x,y]) => `<circle cx="${x}" cy="${y}" r="9"></circle>`).join('');
    }, 70);
  }
  try{ sfxRoll(); }catch(e){}
  const res = await api(endpoint, {uid:getUid(), code:codeVal});
  if(anim) clearInterval(anim);
  await refreshFn();
}

async function doRerollFirst(endpoint, codeVal, refreshFn){
  const btn = document.getElementById('rerollBtn');
  if(btn) btn.disabled = true;
  try{ sfxClick(); }catch(e){}
  await api(endpoint, {uid:getUid(), code:codeVal});
  await refreshFn();
}

function rollFirst(){ return doFirstRoll('/api/roll_first', gameCode, refreshState); }
function rerollFirst(){ return doRerollFirst('/api/reroll_first', gameCode, refreshState); }
async function ackRoll(){
  if(!state) return;
  _rollAckShown[gameCode] = true;
  // In solo, if the bot won the opening roll it owes its first shot. Take it
  // now (the dice-result screen has already been shown to the human).
  if(state.solo && state.phase==='playing' && state.turn===2){
    const res = await api('/api/bot_opening_shot', {uid:getUid(), code:gameCode});
    if(res && res.ok){
      if(res.state){ state = res.state; updateUI(); }
      const bs = res.bot_shots;
      if(bs && bs.length){
        const bn='ABCDEFGHIJ';
        let botMsg='🤖 ';
        for(const s of bs){
          if(s.result==='hit')botMsg+=` ${t('botHit')} ${bn[s.c]}${s.r+1}`;
          else if(s.result==='sunk')botMsg+=` ${t('botSunk')} ${bn[s.c]}${s.r+1}`;
          else if(s.result==='mine')botMsg+=` 💣${t('mine')}`;
          else botMsg+=` ${t('botMiss')}`;
        }
        setStatus(botMsg,'');
      }
      if(state.all_sunk||state.my_all_sunk){
        if(!document.querySelector('.overlay')){
          showResult(state.all_sunk ? '🏆' : '💔', state.all_sunk ? t('win') : t('lose'), state.all_sunk ? t('winDesc') : t('loseDesc'), state.strip);
        }
        return;
      }
      return;
    }
  }
  await refreshState();
}
function ckRollFirst(){ return doFirstRoll('/api/checkers_roll_first', ckCode, ckRefreshState); }
function ckRerollFirst(){ return doRerollFirst('/api/checkers_reroll_first', ckCode, ckRefreshState); }
function pdRollFirst(){ return doFirstRoll('/api/pd_roll_first', pdCode, pdRefreshState); }
function pdRerollFirst(){ return doRerollFirst('/api/pd_reroll_first', pdCode, pdRefreshState); }
function bgRollFirst(){ return doFirstRoll('/api/bg_roll_first', bgCode, bgRefreshState); }
function bgRerollFirst(){ return doRerollFirst('/api/bg_reroll_first', bgCode, bgRefreshState); }

function updateUI(){
  if(!state)return;
  const s=state;
  // A round that left the 'finished' phase means the rematch (if any) has
  // started, so stop treating the game as pending a rematch.
  if(s.phase!=='finished') rematchPending=false;
  showIncomingMessages(s.messages);
  const gameOver=s.all_sunk||s.my_all_sunk;
  const isPlacing = s.phase==='placing'||s.phase==='placing1'||s.phase==='placing2';
  $('pdArea').style.display='none';
  $('ckArea').style.display='none';
  $('ownBoardWrap').style.display='block';
  $('oppBoardWrap').style.display='block';
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
      setStatus('⏳ ' + {ru:'Ожидание фото...',uk:'Очікування фото...',en:'Waiting for photo...'}[lang], 'battle');
      if(!window._stripPhotoWaitTimer){
        window._stripPhotoWaitTimer = setTimeout(() => {
          window._stripPhotoWaitTimer = null;
          if(pollTimer){clearInterval(pollTimer);pollTimer=null}
          localStorage.removeItem('sb_game');
          showResult('🏆',t('win'),{ru:'Соперник не отправил фото',uk:'Суперник не надіслав фото',en:'Opponent did not send a photo'}[lang], true);
        }, 60000);
      }
      return;
    }
    if(pollTimer){clearInterval(pollTimer);pollTimer=null}
    const won = s.all_sunk;
    const resultTitle = won ? t('win') : t('lose');
    const resultDesc = won ? t('winDesc') : t('loseDesc');
    // At game over the opponent board reveals the full enemy layout. Relabel
    // it so the loser understands these are the opponent's ships they missed.
    $('lblOpp').textContent = won
      ? {ru:'🚢 Флот соперника потоплен',uk:'🚢 Флот суперника потоплено',en:"🚢 Opponent's fleet sunk"}[lang]
      : {ru:'🚢 Корабли соперника',uk:'🚢 Кораблі суперника',en:"🚢 Opponent's ships"}[lang];
    setStatus(`${resultTitle} ${resultDesc}`, 'battle');
    $('actions').className = 'btn-col';
    $('actions').innerHTML = `<div class="result-notice ${won ? 'win' : 'lose'}">${resultTitle}<br><span style="font-size:13px;font-weight:400">${resultDesc}</span></div>`;
    if(!rematchPending) localStorage.removeItem('sb_game');
    $('app').insertBefore($('status'), $('app').firstChild);
    if(won)showResult('🏆',resultTitle,resultDesc,s.strip);
    else if(s.my_all_sunk)showResult('💔',resultTitle,resultDesc,s.strip);
    return;
  }

  if(s.phase==='placing'||s.phase==='placing1'||s.phase==='placing2'){
    $('header').classList.remove('in-game');
    ownEl.classList.remove('my-turn');
    oppEl.classList.remove('my-turn');
    $('app').insertBefore($('status'), $('app').firstChild);
    renderShipHint(s.ships_list, s.ships_placed, s.strip, s.mine_placed);
    const alreadyConfirmed = s.ready && s.pnum && s.ready[s.pnum];
    const c = s.code;
    $('oppBoardWrap').style.display='none';
    $('actions').className = 'btn-col';
    if(alreadyConfirmed && !s.solo){
      setStatus(`📋 <b>${c}</b> — ${t('waitOpp')} ✅`, '');
      $('status').style.cursor='pointer';
      $('status').title=t('copyCode');
      $('status').onclick=()=>navigator.clipboard.writeText(c).then(()=>setStatus('✅ '+c+' '+{ru:'скопирован',uk:'скопійовано',en:'copied'}[lang],''));
       $('actions').innerHTML=`
        <button class="btn success" disabled style="opacity:0.5;cursor:default">✅ ${t('confirm')}</button>
        ${s.pnum === 1 ? `<button class="btn primary" onclick="shareGame()">📤 ${t('inviteFriend')}</button>` : ''}
         <button class="btn outline danger" onclick="leaveGame(true)">${t('surrender')}</button>
         <button class="btn outline" onclick="leaveGame()">${t('minimize')}</button>
       `;
      }else{
        if(!s.solo){
          setStatus(`📋 <b>${c}</b> — ${t('waitOpp')}`, '');
          $('status').style.cursor='pointer';
          $('status').title=t('copyCode');
          $('status').onclick=()=>navigator.clipboard.writeText(c).then(()=>setStatus('✅ '+c+' '+{ru:'скопирован',uk:'скопійовано',en:'copied'}[lang],''));
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
        const startBtnClass = needStake ? 'btn strip-btn' : 'btn primary';
        const startOnclick = needStake ? 'showStripInfoOverlay()' : 'confirmPlace()';
        const startLabel = needStake ? t('stripStakeBtn') : (s.strip ? t('stripStart') : t('confirm'));
        $('actions').innerHTML=`
          <button class="btn success" onclick="autoPlace()">${t('reroll')}</button>
          ${!s.solo && s.pnum === 1 ? `<button class="btn primary" onclick="shareGame()">📤 ${t('inviteFriend')}</button>` : ''}
           <button class="${startBtnClass}" onclick="${startOnclick}">${startLabel}</button>
           ${!s.solo ? `<button class="btn outline danger" onclick="leaveGame(true)">${t('surrender')}</button>` : ''}
           ${!s.solo ? `<button class="btn outline" onclick="leaveGame()">${t('minimize')}</button>` : ''}
        `;
      }
    setThemeSelectorVisibility(false);
    delete _rollAckShown[gameCode];
    return;
  }
  $('shipHint').innerHTML = '';

  // Route to the roll screen purely by phase. Note: my_roll/opp_roll stay
  // populated on the backend even after phase flips to 'playing' (kept
  // around for a one-shot "you won the roll" banner elsewhere), so they must
  // NOT be part of this check -- doing so used to make this screen (and its
  // "Continue" button) re-render forever after a decisive roll, since
  // refreshing state would always find the same still-set, still-decisive
  // my_roll/opp_roll and show the roll screen again instead of the board.
  const rollDecided = s.my_roll != null && s.opp_roll != null && s.my_roll !== s.opp_roll;
  if(s.phase==='roll' || (rollDecided && !_rollAckShown[gameCode])){
    ownEl.classList.remove('my-turn');
    oppEl.classList.remove('my-turn');
    $('oppBoardWrap').style.display='none';
    $('app').insertBefore($('status'), $('app').firstChild);
    setStatus('🎲 '+t('rollTitle'),'');
    $('actions').className='btn-col';
    $('actions').innerHTML = firstRollHTML(s, 'rollFirst', 'rerollFirst') +
      `<button class="btn danger" onclick="leaveGame(true)">${t('surrender')}</button>`;
    setThemeSelectorVisibility(false);
    return;
  }

  $('oppBoardWrap').style.display='block';
  updateSettingsUI();
  $('ownBoardWrap').after($('status'));

  if(s.my_turn){
    setStatus(t('yourTurn'),'battle');
    $('actions').className='btn-col';
    $('actions').innerHTML=`
      ${s.solo
        ? `<div class="btn-row" style="margin-top:8px"><button class="btn danger" onclick="leaveGame(true)">${t('surrender')}</button><button class="btn outline" onclick="leaveGame()">${t('minimize')}</button></div>`
        : `<div class="btn-row"><button class="btn outline" onclick="sendOpponentMessage()">${t('message')}</button><button class="btn outline" onclick="leaveGame()">${t('minimize')}</button></div>
      <button class="btn danger" onclick="leaveGame(true)">${t('surrender')}</button>`}
    `;
  }else{
    setStatus(t('oppTurn'),'');
    $('actions').className='btn-col';
    $('actions').innerHTML=`
      ${s.solo
        ? `<div class="btn-row" style="margin-top:8px"><button class="btn danger" onclick="leaveGame(true)">${t('surrender')}</button><button class="btn outline" onclick="leaveGame()">${t('minimize')}</button></div>`
        : `<div class="btn-row"><button class="btn outline" onclick="sendOpponentMessage()">${t('message')}</button><button class="btn outline" onclick="leaveGame()">${t('minimize')}</button></div>
      <button class="btn danger" onclick="leaveGame(true)">${t('surrender')}</button>`}
    `;
  }
}

async function startSolo(){
  const res=await api('/api/new_solo',{uid:getUid(), difficulty: gameDifficulty});
  if(!res||!res.ok){setStatus(t('error'));return}
  gameCode=res.code;
  localStorage.setItem('sb_game',gameCode);
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
  ru: { camera: '📸 Подготовка камеры...', process: '⏳ Обработка фото...', create: '⏳ Создание игры...', send: '📤 Отправка фото...' },
  uk: { camera: '📸 Підготовка камери...', process: '⏳ Обробка фото...', create: '⏳ Створення гри...', send: '📤 Надсилання фото...' },
  en: { camera: '📸 Preparing camera...', process: '⏳ Processing photo...', create: '⏳ Creating game...', send: '📤 Sending photo...' },
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
      // Give the file 'change' event a generous window to land before
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
  const res=await api('/api/new_multi',{uid:getUid(),strip:strip});
  if(!res||!res.ok){setStatus(t('error'));return}
  gameCode=res.code;
  localStorage.setItem('sb_game',gameCode);
  setStatus('', '');
  await refreshState();
  pollGame();
}

function shareGame(){
  if(!gameCode) return;
  copyToClipboard(gameCode, {ru:'Код скопирован ✅',uk:'Код скопійовано ✅',en:'Code copied ✅'}[lang]);
  try{Telegram.WebApp.openTelegramLink(`https://t.me/share/url?url=${encodeURIComponent(gameCode)}`)}catch(e){}
}

function copyToClipboard(text, msg){
  if(navigator.clipboard){
    navigator.clipboard.writeText(text).then(()=>{
      if(msg) setStatus('✅ ' + msg, '');
    }).catch(()=>{ if(msg) setStatus('✅ ' + msg, ''); });
  } else if(msg) {
    setStatus('✅ ' + msg, '');
  }
}

async function joinByCode(code){
  const resolveRes = await api('/api/resolve_code', {code});
  if(!resolveRes || !resolveRes.ok){
    setStatus(t('joinError'), '');
    return;
  }
  const gameType = resolveRes.game;
  if(gameType === 'sea_battle'){
    const res = await api('/api/join', {uid: getUid(), code});
    if(!res || !res.ok){ setStatus(t('joinError')); return; }
    gameCode = code;
    localStorage.setItem('sb_game', code);
    $('actions').innerHTML = '';
    await refreshState();
    pollGame();
  } else if(gameType === 'poker_dice'){
    const res = await api('/api/pd_join', {uid: getUid(), code});
    if(!res || !res.ok){ setStatus(t('joinError')); return; }
    pdCode = code;
    localStorage.setItem('pd_game', code);
    $('actions').innerHTML = '';
    pdShowGame(res.state);
    pdPoll();
  } else if(gameType === 'checkers'){
    const res = await api('/api/checkers_join', {uid: getUid(), code});
    if(!res || !res.ok){ setStatus(t('joinError')); return; }
    ckCode = code;
    localStorage.setItem('ck_game', code);
    $('actions').innerHTML = '';
    ckShowGame(res.state);
    ckPoll();
  } else if(gameType === 'backgammon'){
    const res = await api('/api/bg_join', {uid: getUid(), code});
    if(!res || !res.ok){ setStatus(t('joinError')); return; }
    bgCode = code;
    localStorage.setItem('bg_game', code);
    $('actions').innerHTML = '';
    bgShowGame(res.state);
    bgPoll();
  }
}

async function universalJoinGame(){
  const code = prompt(t('joinPlaceholder'));
  if(!code) return;
  await joinByCode(code.toUpperCase());
}

let pollTimer=null;
// True while a rematch on the same code is pending, so the finished-game
// cleanup (stop polling / drop saved code) is skipped until the new round
// actually starts.
let rematchPending=false;

function pollGame(){
  if(pollTimer)clearInterval(pollTimer);
  pollTimer=setInterval(async()=>{
    if(!gameCode){clearInterval(pollTimer);pollTimer=null;return}
    await refreshState();
  },2000);
}

function showMainMenu(){
  stripUnlocked=false;
  delete _rollAckShown[gameCode];
  $('ownBoardWrap').style.display='none';
  $('oppBoardWrap').style.display='none';
  gameCode=null;state=null;
  pdCode=null;pdState=null;
  ckCode=null;ckState=null;
  bgCode=null;bgState=null;
  if(pollTimer){clearInterval(pollTimer);pollTimer=null}
  if(pdPollTimer){clearInterval(pdPollTimer);pdPollTimer=null}
  if(ckPollTimer){clearInterval(ckPollTimer);ckPollTimer=null}
  if(bgPollTimer){clearInterval(bgPollTimer);bgPollTimer=null}
  // Note: saved game codes (sb_game/pd_game/ck_game) are intentionally
  // NOT cleared here anymore — quitting a game only minimizes it, so it must
  // stay resumable from the active-games bar below.
  setThemeSelectorVisibility(false);
  $('pdArea').style.display='none';
  $('ckArea').style.display='none';
  $('shipHint').innerHTML = '';
  document.title = t('seaBattle');
  $('gameInfo').textContent='';
  $('header').classList.remove('in-game');
  document.querySelectorAll('.board').forEach(b => b.classList.remove('my-turn'));
  $('app').insertBefore($('status'), $('app').firstChild);
  setStatus('');
  var lb=$('langBar');if(lb)lb.style.display='flex';
  $('actions').className='btn-row stack';
  $('actions').innerHTML=`
    <div id="activeGamesContainer"></div>
    <div class="game-grid">
      <div class="game-card" onclick="showSeaBattleMenu()" style="margin-bottom:8px">
        <div class="icon">🚢</div>
        <div class="name" style="color:var(--accent-primary)">${t('seaBattle')}</div>
        <div class="card-desc">${t('startBtn')}</div>
      </div>
      <div class="game-card" onclick="showPokerDice()" style="margin-bottom:8px">
        <div class="icon">🃏</div>
        <div class="name" style="color:#ff9800">${t('pdTitle')}</div>
        <div class="card-desc">${t('startBtn')}</div>
      </div>
      <div class="game-card" onclick="showCheckers()" style="margin-bottom:8px">
        <div class="icon">♟️</div>
        <div class="name" style="color:#D4A96A">${t('checkers')}</div>
        <div class="card-desc">${t('startBtn')}</div>
      </div>
      <div class="game-card" onclick="showBackgammon()" style="margin-bottom:8px">
        <div class="icon">🎲</div>
        <div class="name" style="color:#8B5C2A">${t('backgammon')}</div>
        <div class="card-desc">${t('startBtn')}</div>
      </div>
      <div class="game-card game-card-wide" onclick="universalJoinGame()" style="margin-bottom:8px">
        <div class="icon">🔗</div>
        <div class="name" style="color:var(--accent-primary)">${t('joinTitle')}</div>
        <div class="card-desc">${t('joinBtn')}</div>
      </div>
    </div>
  `;
  updateContinueButton();
  fetchActiveGames();
}

function showMenu(){ showMainMenu(); }

// ---- Player stats (winrate + recent match history) -------------------------
const STATS_GAME_LABEL = {sea_battle:'seaBattle', poker_dice:'pdTitle', checkers:'checkers', backgammon:'backgammon'};
const STATS_GAME_ICON = {sea_battle:'🚢', poker_dice:'🃏', checkers:'♟️', backgammon:'🎲'};
const STATS_RESULT_LABEL = {win:'statsResWin', loss:'statsResLoss', draw:'statsResDraw'};

async function showStats(){
  var lb=$('langBar');if(lb)lb.style.display='none';
  hideAllGameAreas();
  document.title = t('statsTitle');
  setStatus('📊 ' + t('statsTitle'));
  $('gameInfo').textContent='';
  $('header').classList.remove('in-game');
  $('app').insertBefore($('status'), $('app').firstChild);
  $('actions').className='btn-col';
  $('actions').innerHTML = `<div class="stats-loading">⏳</div>`;
  const res = await api('/api/stats', {uid:getUid()});
  if(!res || !res.ok){
    setStatus(t('error'));
    $('actions').innerHTML = `<button class="btn outline quit-btn" onclick="showMainMenu()">${t('quit')}</button>`;
    return;
  }
  renderStats(res.stats);
}

function renderStats(st){
  const winrateStr = st.winrate==null ? '—' : st.winrate+'%';
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
      const icon = STATS_GAME_ICON[h.game] || '🎮';
      const gname = t(STATS_GAME_LABEL[h.game] || h.game);
      const resLabel = t(STATS_RESULT_LABEL[h.result] || h.result);
      const vs = h.solo ? t('withBot') : t('withFriend');
      html += `<div class="stats-hist-row ${h.result}"><span class="stats-hist-icon">${icon}</span><span class="stats-hist-name">${gname} <small>${vs}</small></span><span class="stats-hist-result ${h.result}">${resLabel}</span></div>`;
    }
    html += '</div>';
  }
  html += `<button class="btn outline quit-btn" style="margin-top:12px" onclick="showMainMenu()">${t('quit')}</button>`;
  $('actions').innerHTML = html;
}

let gameDifficulty = 4;
let stripUnlocked=false; let _stripTaps=0, _stripLastTap=0;

function showBotDifficulty(){
  var lb=$('langBar');if(lb)lb.style.display='none';
  document.title = t('seaBattle');
  setStatus(t('selectDifficulty'));
  $('gameInfo').textContent='';
  $('shipHint').innerHTML = '';
  $('header').classList.remove('in-game');
  $('app').insertBefore($('status'), $('app').firstChild);
  $('actions').className='btn-row stack';
  $('actions').innerHTML=`
    <button class="btn outline" onclick="startSoloWithDifficulty(1)" style="width:100%">🌟 ${t('stEasy')}</button>
    <button class="btn outline" onclick="startSoloWithDifficulty(2)" style="width:100%">🎯 ${t('stMedium')}</button>
    <button class="btn outline" onclick="startSoloWithDifficulty(3)" style="width:100%">🔥 ${t('stHard')}</button>
    <button class="btn primary" onclick="startSoloWithDifficulty(4)" style="width:100%">💀 ${t('stExpert')}</button>
    <button class="btn outline quit-btn" onclick="showSeaBattleMenu()" style="margin-top:8px">${t('quit')}</button>
  `;
  fetchActiveGames();
}

function startSoloWithDifficulty(diff){
  gameDifficulty = diff;
  startSolo();
}

function showSeaBattleMenu(){
  var lb=$('langBar');if(lb)lb.style.display='none';
  stripUnlocked=false;
  hideAllGameAreas();
  document.title = t('seaBattle');
  setStatus('');
  $('gameInfo').textContent='';
  $('header').classList.remove('in-game');
  $('app').insertBefore($('status'), $('app').firstChild);
  $('actions').className='btn-row stack';
  $('actions').innerHTML=`
    <div class="game-card" onclick="showBotDifficulty()" style="margin-bottom:8px">
      <img src="/static/mode-bot.svg" class="card-icon">
      <div class="name">${t('vsBot')}</div>
      <div class="card-desc">${t('withBot')}</div>
    </div>
    <div class="game-card" onclick="chooseMultiMode()" style="margin-bottom:8px">
      <img src="/static/mode-friend.svg" class="card-icon">
      <div class="name">${t('vsFriend')}</div>
      <div class="card-desc">${t('withFriend')}</div>
    </div>
    <div class="game-card" onclick="newMulti(true)" id="stripCard" style="display:none;margin-bottom:8px">
      <img src="/static/mode-shirt.svg" class="card-icon">
      <div class="name">${t('stripMode')}</div>
      <div class="card-desc">${t('stripDesc')}</div>
    </div>
    <button class="btn outline quit-btn" onclick="showMainMenu()">${t('quit')}</button>
    <div id="stripUnlockArea" style="height:140px;width:100%;cursor:pointer" onclick="tapStripUnlock()"></div>
  `;
  fetchActiveGames();
}

function tapStripUnlock(){
  const now=Date.now();
  if(now-_stripLastTap>1800)_stripTaps=0;   // reset if gap between taps > 1.8s (not "normal pace")
  _stripLastTap=now; _stripTaps++;
  if(_stripTaps>=10){ stripUnlocked=true; _stripTaps=0; const c=document.getElementById('stripCard'); if(c)c.style.display=''; }
}

function chooseMultiMode(){
  newMulti(false);
}

async function autoPlace(){
  const res=await api('/api/place_auto',{uid:getUid(),code:gameCode});
  if(!res||!res.ok)return;
  sfxPlace();
  await refreshState();
  setStatus(t('again'),'');
}

async function confirmPlace(){
  const res=await api('/api/confirm',{uid:getUid(),code:gameCode});
  if(!res||!res.ok){
    setStatus('⚠️ ' + {ru:'Сначала расставь корабли!',uk:'Спочатку розстав кораблі!',en:'Place all ships first!'}[lang],'');
    return;
  }
  sfxClick();
  await refreshState();
}

async function handleShot(r,c){
  if(!state||!state.my_turn)return;
  const res=await api('/api/shoot',{uid:getUid(),code:gameCode,r,c});
  if(!res||!res.ok){setStatus(t('errorShot'));return}

  let msg='';
  if(res.result.result==='hit'){msg=t('hit');sfxHit()}
  else if(res.result.result==='sunk'){msg=t('sunk');sfxSunk()}
  else if(res.result.result==='mine'){
    msg= {ru:'💣 МИНА! Твой корабль поврежден!',uk:'💣 МІНА! Твій корабель пошкоджено!',en:'💣 MINE! Your ship is damaged!'}[lang];
    sfxSunk();
  }
  else {msg=t('miss');sfxMiss()}

  const bs=res.result.bot_shots;
  let botMsg='';
  if(bs&&bs.length){
    const bn='ABCDEFGHIJ';
    botMsg='🤖 ';
    for(const s of bs){
      if(s.result==='hit')botMsg+=` ${t('botHit')} ${bn[s.c]}${s.r+1}`;
      else if(s.result==='sunk')botMsg+=` ${t('botSunk')} ${bn[s.c]}${s.r+1}`;
      else if(s.result==='mine')botMsg+=` 💣${t('mine')}`;
      else botMsg+=` ${t('botMiss')}`;
    }
    msg+=' '+botMsg;
  }
  // Render the final board from the shot response immediately. This avoids a
  // race with polling and makes the win/loss result appear without delay.
  if(res.state){
    state=res.state;
    updateUI();
    if(state.all_sunk||state.my_all_sunk){
      if(!document.querySelector('.overlay')){
        showResult(state.all_sunk ? '🏆' : '💔', state.all_sunk ? t('win') : t('lose'), state.all_sunk ? t('winDesc') : t('loseDesc'), state.strip);
      }
      return;
    }
  }else{
    await refreshState();
  }
  if(msg)setStatus(msg,'battle');
}

async function sendOpponentMessage(game='sea_battle', code=gameCode, gameState=state){
  if(!gameState || gameState.solo || !code)return;
  const message = window.prompt(t('messagePrompt'));
  if(message === null)return;
  const text = message.trim();
  if(!text)return;
  const res = await api('/api/message_opponent',{uid:getUid(),code,message:text,game});
  setStatus(res && res.ok ? t('messageSent') : t('messageError'), res && res.ok ? '' : 'battle');
}

function showResult(icon,title,desc,strip,playAgainFn,playAgainLabel){
  stripUnlocked=false;
  const o=document.createElement('div');
  o.className='overlay';
  const won = icon==='🏆';
  if(icon==='🏆')sfxWin();else sfxLose();
  
  if(strip && icon==='💔'){
    // The loser's stake photo was already committed (and
    // delivered to the winner) before the game started.
    o.innerHTML=`
      <div class="modal">
        <div class="result-icon">💔</div>
        <h2>${title}</h2>
        <p>${desc}</p>
        <button class="btn success" style="margin:4px 0;width:100%" onclick="this.closest('.overlay').remove();requestRematch()">💪 ${t('rematchLose')}</button>
        <button class="btn outline quit-btn" style="margin:4px 0;width:100%" onclick="this.closest('.overlay').remove();showMenu()">${t('quit')}</button>
      </div>`;
    document.body.appendChild(o);
    return;
  }
  
  if(strip && icon==='🏆'){
    const photo = state && (state.opp_stake || state.strip_photo) ? (state.opp_stake || state.strip_photo) : null;
    o.innerHTML=`
      <div class="modal">
        <div class="result-icon">🏆</div>
        <h2>${title}</h2>
        <p>${desc}</p>
        ${photo ? `<img src="${photo}" style="max-width:90%;max-height:320px;border-radius:8px;margin:12px auto;display:block;object-fit:contain">` : ''}
        <button class="btn success" style="margin-top:8px" onclick="this.closest('.overlay').remove();requestRematch()">🎉 ${t('rematchWin')}</button>
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
  // Both this player and the opponent must opt in; the server restarts the
  // SAME game (same code) once both agree, so nobody re-enters the code.
  const ov = document.querySelector('.overlay');
  if(ov) ov.remove();
  rematchPending = true;
  setStatus(t('rematchWait'), 'battle');
  if(!pollTimer){ pollTimer = setInterval(refreshState, 2000); }
  try { await api('/api/rematch', {uid:getUid(), code:gameCode}); } catch(e){}
}

async function leaveGame(surrender){
  stripUnlocked=false;
  delete _rollAckShown[gameCode];
  if(surrender){
    var msg = {ru:'Сдаться? Игра будет завершена.',uk:'Здатися? Гра буде завершена.',en:'Surrender? The game will end.'}[lang];
    if(!confirm(msg))return;
  }
  // Clear poll timer BEFORE any async operation to prevent refreshState/updateUI from re-showing boards
  if(pollTimer){clearInterval(pollTimer);pollTimer=null}
  const _code = gameCode;
  if(surrender) localStorage.removeItem('sb_game');
  gameCode=null;state=null;
  // Hide boards BEFORE clearing other game data to ensure UI consistency
  $('ownBoardWrap').style.display='none';
  $('oppBoardWrap').style.display='none';
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
    if(g.type==='sea_battle'){
      var badge=g.my_turn?'<span class="badge playing">🚢 '+t('yourTurn')+'</span>':'<span class="badge">🚢 '+{ru:'ожидание...',uk:'очікування...',en:'waiting...'}[lang]+'</span>';
      html+='<div class="active-game-row" onclick="resumeSB(\''+g.code+'\')"><div class="info"><span class="label">🚢 </span><span class="code">'+g.code+'</span></div>'+badge+'</div>';
    }
    else if(g.type==='poker_dice'){
      var badge=g.my_turn?'<span class="badge playing">🃏 '+t('yourTurn')+'</span>':'<span class="badge">🃏 '+{ru:'ожидание...',uk:'очікування...',en:'waiting...'}[lang]+'</span>';
      html+='<div class="active-game-row" onclick="resumePd(\''+g.code+'\')"><div class="info"><span class="label">🃏 </span><span class="code">'+g.code+'</span></div>'+badge+'</div>';
    }
    else if(g.type==='checkers'){
      var badge=g.my_turn?'<span class="badge playing">♟️ '+t('yourTurn')+'</span>':'<span class="badge">♟️ '+{ru:'ожидание...',uk:'очікування...',en:'waiting...'}[lang]+'</span>';
      html+='<div class="active-game-row" onclick="resumeCk(\''+g.code+'\')"><div class="info"><span class="label">♟️ </span><span class="code">'+g.code+'</span></div>'+badge+'</div>';
    }
    else if(g.type==='backgammon'){
      var badge=g.my_turn?'<span class="badge playing">🎲 '+t('bgYourTurn')+'</span>':'<span class="badge">🎲 '+{ru:'ожидание...',uk:'очікування...',en:'waiting...'}[lang]+'</span>';
      html+='<div class="active-game-row" onclick="resumeBg(\''+g.code+'\')"><div class="info"><span class="label">🎲 </span><span class="code">'+g.code+'</span></div>'+badge+'</div>';
    }
  }
  html+='</div>';
  cont.innerHTML=html;
}

function resumeSB(code){
  gameCode=code;
  localStorage.setItem('sb_game',code);
  $('actions').innerHTML='';
  refreshState();
  setTimeout(pollGame,500);
}

function resumeCk(code){
  ckCode=code;
  localStorage.setItem('ck_game',code);
  $('actions').innerHTML='';
  ckRefreshState();
  ckPoll();
}

function tryReconnect(){
  showMenu();
  fetchBotInfo().then(() => checkStartParam());
}

function continueGame(){
  const saved=localStorage.getItem('sb_game');
  if(saved){
    gameCode=saved;
      $('actions').innerHTML='';
    refreshState();
    setTimeout(pollGame,500);
  }
}

function updateContinueButton(){
  const btn=$('continueBtn');
  if(btn) btn.style.display='none';
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
initTG();
tryReconnect();
