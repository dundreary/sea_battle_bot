// ---- Poker Dice ----
let pdCode = null, pdState = null, pdKept = new Set(), pdSeenScore='', pdOpeningPending = false, pdOppRollSpun = '', pdAnimating = false, _pdResultPopupEl = null;
let pdOpeningTimer = null;
let _pdBotOpening = false;
let _lastPDSig = null, _pdRefreshing = false;

const PD_DOTS = [
 [[1,1]],
 [[0,2],[2,0]],
 [[0,2],[1,1],[2,0]],
 [[0,0],[0,2],[2,0],[2,2]],
 [[0,0],[0,2],[1,1],[2,0],[2,2]],
 [[0,0],[0,2],[1,0],[1,2],[2,0],[2,2]],
];

function pdFaceDotsHtml(v){
 if(!v) return '';
 const dots = PD_DOTS[v-1] || [];
 return dots.map(([r,c]) => `<div class="dot" style="grid-row:${r+1};grid-column:${c+1}"></div>`).join('');
}
function pdDieInner(){
 // 6 stacked faces, values 1..6; only one visible at rest via .pd-faces transform
 let h='<div class="pd-faces">';
 for(let v=1; v<=6; v++) h += `<div class="pd-face" data-v="${v}">${pdFaceDotsHtml(v)}</div>`;
 return h + '</div>';
}

const PD_CATEGORIES = ['ones','twos','threes','fours','fives','sixes','pair','two_pairs','three_of_kind','four_of_kind','full_house','small_straight','large_straight','five_of_kind','chance'];
const PD_CAT_NAMES = {
 ru: ['Единицы','Двойки','Тройки','Четверки','Пятерки','Шестерки','Пара','Две пары','Тройка','Каре','Фулл-хаус','М.стрит','Б.стрит','Покер','Шанс'],
 en: ['Ones','Twos','Threes','Fours','Fives','Sixes','One Pair','Two Pairs','Three of a Kind','Four of a Kind','Full House','S.Strt','L.Strt','Five of a Kind','Chance'],
 uk: ['Очки','Двійки','Трійки','Четвірки',"П'ятірки",'Шістки','Пара','Дві пари','Трійка','Каре','Фулл-хаус','М.стрит','В.стрит','Покер','Шанс'],
};
function catName(id){ const i=PD_CATEGORIES.indexOf(id); return PD_CAT_NAMES[lang]?.[i]||id; }

const PD_HAND_NAMES = {
 'Five of a Kind': {ru:'Покер',uk:'Покер',en:'Five of a Kind'},
 'Four of a Kind': {ru:'Каре',uk:'Каре',en:'Four of a Kind'},
 'Full House': {ru:'Фулл-хаус',uk:'Фулл-хаус',en:'Full House'},
 'Small Straight': {ru:'Малый стрит',uk:'Малий стріт',en:'Small Straight'},
 'Large Straight': {ru:'Большой стрит',uk:'Великий стріт',en:'Large Straight'},
 'Straight': {ru:'Стрит',uk:'Стрит',en:'Straight'},
 'Three of a Kind':{ru:'Тройка',uk:'Трійка',en:'Three of a Kind'},
 'Two Pair': {ru:'Две пары',uk:'Дві пари',en:'Two Pair'},
 'One Pair': {ru:'Пара',uk:'Пара',en:'One Pair'},
};
function pdHandName(name){
 if(!name) return '';
 // Handle 'Nothing (N)'pattern
 if(name.startsWith('Nothing')) return {ru:'Ничего',uk:'Нічого',en:'Nothing'}[lang]||name;
 return PD_HAND_NAMES[name]?.[lang]||name;
}

function showPokerDice(){
 currentGameType='poker_dice'; setHelpVisible(true);
 var lb=$('langBar');if(lb)lb.style.display='none';
 setStripLockVisible(false);
 hideAllGameAreas();
 if($('legend'))$('legend').style.display='none';
 $('header').classList.remove('in-game');
 document.title=t('pdTitle');
 $('gameInfo').textContent='';
 setStatus('');
 $('actions').className='btn-row stack';
 var savedPd = localStorage.getItem('pd_game');
 var hasActiveGame = !!savedPd;
 var resumeHtml = '';
 if(hasActiveGame){
 resumeHtml = `<div class="active-game-row" onclick="resumePd('${savedPd}')">
 <div class="info"><span class="label"> </span><span class="code">${savedPd}</span></div>
 <span class="badge playing"> ${t('continue')||'Продолжить'}</span>
 </div>`;
 }
 $('actions').innerHTML=`
 ${resumeHtml}
 <div class="game-card" aria-label="${t('vsBot')}" onclick="pdStartSolo()" style="margin-bottom:8px">
 <img src="/static/mode-bot.svg" class="card-icon">
 <div class="card-name">${t('vsBot')}</div>
 </div>
 ${!hasActiveGame ? `
 <div class="game-card" aria-label="${t('vsFriend')}" onclick="pdNewMulti()" style="margin-bottom:8px">
 <img src="/static/mode-friend.svg" class="card-icon">
 <div class="card-name">${t('vsFriend')}</div>
 </div>
 ` : ''}
 <button class="btn outline quit-btn" onclick="showMainMenu()">${t('quit')}</button>
 `;
}

async function pdStartSolo(){
 currentGameType=null; setHelpVisible(false);
 currentScreen='poker_dice';
 try{ if(typeof window.Telegram!=='undefined'&& window.Telegram.WebApp && window.Telegram.WebApp.BackButton) window.Telegram.WebApp.BackButton.show(); }catch(e){}
 const res=await api('/api/pd_new_solo',{uid:getUid(), difficulty: getDifficulty()});
 if(res===null){ showRetry(t('error'), ()=>pdStartSolo()); return; }
 if(!res||!res.ok){setStatus(t('error'));return}
 pdCode=res.code;
 _lastPDSig=null;
 localStorage.setItem('pd_game',pdCode);
 const _sb=$('sbOppHistory'); if(_sb) _sb.innerHTML='';
 pdKept = new Set();
 pdOppRollSpun = '';
 pdShowGame(res.state);
}

async function pdNewMulti(){
 currentGameType=null; setHelpVisible(false);
 currentScreen='poker_dice';
 try{ if(typeof window.Telegram!=='undefined'&& window.Telegram.WebApp && window.Telegram.WebApp.BackButton) window.Telegram.WebApp.BackButton.show(); }catch(e){}
 const res=await api('/api/pd_new_multi',{uid:getUid()});
 if(res===null){ showRetry(t('error'), () => pdNewMulti()); return; }
 if(!res.ok){setStatus(t('error'));return}
 pdCode=res.code;
 _lastPDSig=null;
 localStorage.setItem('pd_game',pdCode);
 pdKept = new Set();
 pdOppRollSpun = '';
 pdShowGame(res.state);
 startGamePoll('poker_dice', pdCode, pdRefreshState);
}

async function pdJoin(code){
 const res=await api('/api/pd_join',{uid:getUid(),code:code.toUpperCase()});
 if(res===null){ showRetry(t('error'), () => pdJoin(code)); return; }
 if(!res.ok){setStatus(t('joinError'));return}
 pdCode=code.toUpperCase();
 _lastPDSig=null;
 localStorage.setItem('pd_game',pdCode);
 pdKept = new Set();
 pdOppRollSpun = '';
 pdShowGame(res.state);
 startGamePoll('poker_dice', pdCode, pdRefreshState);
}

async function pdRefreshState(){
 if(!pdCode)return;
 if(_pdRefreshing) return;
 _pdRefreshing=true;
 try{
 const res=await api('/api/pd_state',{uid:getUid(),code:pdCode});
 notePollResult('poker_dice', res!==null);
 if(!res||!res.ok){
 localStorage.removeItem('pd_game');
 pdCode=null;
 stopGamePoll('poker_dice');
 showPokerDice();
 return;
 }
 if(!pdCode)return;
 const st=res.state;
 const sig = JSON.stringify([st.phase, st.dice, st.my_turn, st.rolls_left, st.scored, st.scorecard_all, st.opponent_scorecard_all, st.categories_left, st.turn, st.solo, st.opponent_joined]);
 if(sig===_lastPDSig) return;
 _lastPDSig = sig;
 // Replay the opponent's throws live in the shared dice tray the moment their
 // turn is delivered (only once, guarded inside pdMaybeAnimateOpponent).
 await pdMaybeAnimateOpponent(st, false);
 if(!pdAnimating) await pdShowGame(st);
 } finally {
 _pdRefreshing=false;
 }
}

async function pdShowGame(st){
 pdState = st;
 showIncomingMessages(st.messages);
 hideAllGameAreas();
 $('pdArea').style.display='';
 setThemeSelectorVisibility(false);
 updateSettingsUI();
 $('header').classList.add('in-game');
 document.title=t('pdTitle');
 $('gameInfo').textContent='';

 $('actions').innerHTML = '';
 $('actions').className = 'btn-row';
 $('pdActions').innerHTML = '';
 $('pdActions').style.minHeight = '120px';
 $('pdDice').innerHTML='';
 $('pdDice').style.minHeight = '';
 $('pdScorecardContainer').style.minHeight = '';
 $('pdResult').innerHTML='';
 $('pdOppHistory').innerHTML='';

 if(st.phase==='finished'){
 stopGamePoll('poker_dice');
 localStorage.removeItem('pd_game');
 pdRenderResult(st);
 return;
 }

 const rollDecided = st.my_roll != null && st.opp_roll != null && st.my_roll !== st.opp_roll;
 if(st.phase==='roll'|| (rollDecided && !_rollAckShown[pdCode])){
 if(rollDecided && _rollAckShown[pdCode]){
 closeFirstRollPopup();
 } else {
 $('pdScorecardContainer').innerHTML='';
 $('pdScorecardContainer').style.minHeight='';
 setStatus(''+t('rollTitle'),'');
 // Opening toss renders in the shared popup; the winner is shown there.
 showFirstRollPopup(st, 'pdRollFirst', 'pdRerollFirst', { solo: st.solo, code: pdCode, proceedFn: () => { _lastPDSig = null; pdRefreshState(); } });
 return;
 }
 }
 // Clear kept dice when it's a fresh turn, scored, or no rolls left
 if(!st.dice || st.dice.length === 0 || st.scored || (st.rolls_left === 0 && st.my_turn)){
 pdKept = new Set();
 }

 pdRenderScorecard(st);
 pdRenderDice(st);
 pdRenderActions(st);
 pdRenderInfo(st);
 closeFirstRollPopup();

 // Solo: if it's the bot's turn (e.g. it won the opening toss), run its move.
 // Guarded so a concurrent poll can't double-run it; the finally resets the
 // guard so a failed attempt self-heals on the next poll.
 if(st.phase==='playing'&& st.solo && !st.my_turn && !_pdBotOpening){
 _pdBotOpening = true;
 try { await pdRunBotTurn(); } finally { _pdBotOpening = false; }
 return;
 }
}

function pdRenderScorecard(st){
 const cont = $('pdScorecardContainer');
 cont.innerHTML = '';

 const categoriesLeft = st.categories_left || [];

 const table = document.createElement('table');
 table.className = 'pd-scorecard';
 table.id = 'pdScorecardEl';

 let html = `<tr><th class="cat-name">${t('pdScorecard')||'Табло'}</th><th class="cat-score">${t('pdScoreBtn')||'Очки'}</th><th class="cat-score" style="color:var(--text-hint)">${t('pdOpp')||'Сопер.'}</th></tr>`;

 const sc = st.scorecard || {};
 const oppSc = st.opponent_scorecard || {};
 const scAll = st.scorecard_all || {};
 const oppScAll = st.opponent_scorecard_all || {};

 const renderCat = (catId) => {
 const myVal = scAll[catId];
 const oppVal = oppScAll[catId];
 const canScore = categoriesLeft.includes(catId) && st.my_turn && !st.scored && st.dice && st.dice.length > 0;
 const cls = canScore ? 'available': (myVal !== null ? 'used': '');
 const myDisplay = myVal !== null ? myVal : (canScore ? '-': '');
 const oppDisplay = oppVal !== null ? oppVal : (oppVal === null ? '': oppVal);

 html += `<tr class="${cls}" data-cat="${catId}">`;
 html += `<td class="cat-name">${catName(catId)}</td>`;
 html += `<td class="cat-score">${myDisplay}</td>`;
 html += `<td class="cat-score" style="color:var(--text-hint)">${oppDisplay}</td>`;
 html += `</tr>`;
 };

 // Upper section
 for(let i = 0; i < 6; i++) renderCat(PD_CATEGORIES[i]);

 // Bonus row
 const bonus = st.bonus;
 const upperSum = st.upper_sum || 0;
 html += `<tr class="bonus-row"><td> ${t('pdBonus')||'Бонус'} (>=63=+35)</td><td>${bonus ? '+35': upperSum+'/63'}</td><td style="color:var(--text-hint)">${st.opponent_bonus ? '+35': (st.opponent_upper_sum||0)+'/63'}</td></tr>`;

 // Divider
 html += `<tr class="section-divider"><td colspan="3"></td></tr>`;

 // Lower section
 for(let i = 6; i < PD_CATEGORIES.length; i++) renderCat(PD_CATEGORIES[i]);

 // Total row
 const totalCls = st.total_score > st.opponent_total_score ? 'total-row win': st.total_score < st.opponent_total_score ? 'total-row lose': 'total-row';
 html += `<tr class="${totalCls}"><td>Σ ${t('pdTotal')||'Итого'}</td><td>${st.total_score}</td><td>${st.opponent_total_score}</td></tr>`;

 table.innerHTML = html;
 cont.appendChild(table);

 // Attach click handlers for available categories
 table.querySelectorAll('tr.available').forEach(row => {
 row.addEventListener('click', () => {
 const cat = row.dataset.cat;
 if(cat) pdDoScore(cat);
 });
 });
}

function pdRenderDice(st){
 const cont=$('pdDice');
 cont.innerHTML='';
 const dice=st.dice||[];
 const diceTotal = values => values.reduce((total, value) => total + value, 0);
 // We no longer statically replay the opponent's last roll at the start of
 // the player's turn; the throw animation already reveals it. So showOpp is
 // disabled and the player simply sees their own (empty) tray.
 const showOpp = st.my_turn && (!st.dice || st.dice.length === 0);

 if(st.my_turn || showOpp){
 let labelColor = 'var(--accent-primary)';
 let labelText = '';
 if(showOpp){
 labelColor = 'var(--color-hit)';
 labelText = st.opponent_scored_category ? `${t('pdOppHand')}: ${catName(st.opponent_scored_category)} — ${st.opponent_scored_points} ${t('pdPts')}` : t('pdOppHand');
 } else {
 labelText = st.hand_name ? `${t('pdYourHand')}: ${pdHandName(st.hand_name)} (${diceTotal(dice)} ${t('pdPts')})` : t('pdYourHand');
 }
 const label = document.createElement('div');
 label.style.cssText = 'width:100%;text-align:center;font-size:13px;color:'+labelColor+';font-weight:600;margin-bottom:6px;margin-top:10px';
 label.textContent = labelText;
 cont.appendChild(label);

 const showDice = showOpp ? (st.opponent_dice||[]) : dice;
 for(let i=0;i<5;i++){
 const die=document.createElement('div');
 die.className='pd-dot-die';
 if(showOpp) die.style.cursor='default';
 const val = showDice[i] || 0;
 die.innerHTML = pdDieInner();
 const f = die.querySelector('.pd-faces');
 if(f){ f.style.opacity = val ? '1': '0'; f.style.transform = 'translateY(-'+ ((val?val-1:0)*100/6) + '%)'; }
 die.dataset.idx=i;
 if(st.my_turn && !showOpp && !st.scored && st.rolls_left>0){
 if(pdKept.has(i)) die.classList.add('kept');
 die.onclick=()=>pdToggleKeep(i);
 }
 cont.appendChild(die);
 }
 } else if(st.solo){
  // Solo bot turn: show empty dice tray instead of fake all-ones.
  const label = document.createElement('div');
  label.style.cssText = 'width:100%;text-align:center;font-size:13px;color:var(--accent-primary);font-weight:600;margin-bottom:6px;margin-top:10px';
  label.textContent = '' + t('pdOppHand');
  cont.appendChild(label);
  for(let i=0;i<5;i++){
   const die=document.createElement('div');
   die.className='pd-dot-die';
   die.style.cursor='default';
   die.innerHTML = pdDieInner();
   const f = die.querySelector('.pd-faces');
   if(f){ f.style.opacity = '0'; f.style.transform = 'translateY(0%)'; }
   cont.appendChild(die);
  }
 } else {
 // Multiplayer: the opponent's current dice are live, show them.
 const label = document.createElement('div');
 label.style.cssText = 'width:100%;text-align:center;font-size:13px;color:var(--accent-primary);font-weight:600;margin-bottom:6px;margin-top:10px';
 if(st.opponent_hand_name){
 label.textContent = `${t('pdOppHand')}: ${pdHandName(st.opponent_hand_name)} (${diceTotal(dice)} ${t('pdPts')})`;
 } else {
 label.textContent = t('pdOppHand');
 }
 cont.appendChild(label);

 for(let i=0;i<5;i++){
 const die=document.createElement('div');
 die.className='pd-dot-die';
 die.style.cursor='default';

 const val = dice[i] || 0;
 die.innerHTML = pdDieInner();
 const f = die.querySelector('.pd-faces');
 if(f){ f.style.opacity = val ? '1': '0'; f.style.transform = 'translateY(-'+ ((val?val-1:0)*100/6) + '%)'; }
 cont.appendChild(die);
 }
 }

 }

 // Play back the opponent's (or AI's) full turn in the SINGLE shared dice
 // tray: the dice spin on the first throw, the kept dice are highlighted and
 // the discarded ones spin again in place, up to the third throw. No separate
 // / duplicated "opponent table" — everything happens in #pdDice.

 async function pdMaybeAnimateOpponent(st, skipFirstRoll = false){
 const hist = st.opponent_roll_history || [];
 if(!hist.length) return false;
 const key = hist.map(h => (h.dice||[]).join(',')).join('|') + ':'+ (st.opponent_scored_category || '');
 if(pdSeenScore === key) return false;
 pdSeenScore = key;

 // Intentionally do NOT re-render the scorecard here. The table already
 // shows the running totals from the previous turn (rendered by pdShowGame
 // before this animation); the bot's new score is revealed only by the
 // pdShowGame call that follows the animation, so the dice spin to their
 // result before the table updates.
 await pdAnimateBotTurn(hist, st.opponent_scored_category, st.opponent_scored_points, st, skipFirstRoll);
 return true;
 }

 async function pdAnimateBotTurn(history, cat, pts, st, skipFirstRoll = false){
 if(pdAnimating) return;
 pdAnimating = true;
 const myCode = pdCode;
 stopGamePoll('poker_dice');
 const savedKept = pdKept;
 pdKept = new Set();

 const cont = $('pdDice');
 cont.style.minHeight = '';
 cont.innerHTML = '';
 const label = document.createElement('div');
 label.style.cssText = 'width:100%;text-align:center;font-size:13px;color:var(--color-hit);font-weight:600;margin-bottom:6px;margin-top:6px;min-height:20px';
 cont.appendChild(label);

 const diceEls = [];
 for(let i = 0; i < 5; i++){
 const die = document.createElement('div');
 die.className = 'pd-dot-die';
 die.style.cursor = 'default';
 die.dataset.idx = i;
 die.innerHTML = pdDieInner();
 cont.appendChild(die);
 diceEls.push(die);
 }

 // Pin the container height AFTER the label and dice are laid out (and the
 // label has a stable min-height), via min-height — NOT a fixed height — so
 // the dice row stays vertically stable even when a longer localized label
 // (uk/en) replaces the text mid-animation. Measuring after building the
 // children captures the real, final layout height.
 cont.style.minHeight = cont.offsetHeight + 'px';

 const setDie = (el, val, snap=false) => {
 const f = el.querySelector('.pd-faces');
 if(f){
 if(snap) f.style.transition = 'none';
 f.style.opacity = val ? '1': '0';
 f.style.transform = 'translateY(-'+ ((val?val-1:0)*100/6) + '%)';
 if(snap) { void f.offsetWidth; f.style.transition = ''; }
 } else {
 // Fallback: (shouldn't happen) rebuild the faces stack, then land it.
 el.innerHTML = pdDieInner();
 const nf = el.querySelector('.pd-faces');
 if(nf){ 
 if(snap) nf.style.transition = 'none';
 nf.style.opacity = val ? '1': '0'; 
 nf.style.transform = 'translateY(-'+ ((val?val-1:0)*100/6) + '%)'; 
 if(snap) { void nf.offsetWidth; nf.style.transition = ''; }
 }
 }
 };

 try {
 if (skipFirstRoll && history.length > 0) {
 const entry = history[0];
 label.textContent = `${t('pdThrow')} 1`;
 for(let i = 0; i < 5; i++) setDie(diceEls[i], entry.dice ? (entry.dice[i] || 0) : 0, true);
 }

 for(let h = skipFirstRoll ? 1 : 0; h < history.length; h++){
 const entry = history[h] || {};
 const kept = entry.kept || [];
 const rerolled = entry.rerolled || [];
 const isFirst = h === 0;
 label.textContent = isFirst
 ? `${t('pdThrow')} 1`
 : `${t('pdThrow')} ${h + 1} · ${t('pdKept')} ${kept.length}, ${t('pdDiscarded')} ${rerolled.length}`;

 if(!isFirst) {
 // Pause to "think" about what to keep
 await _aiDelay(600);
 for(let i = 0; i < 5; i++){
 if(kept.includes(i)) diceEls[i].classList.add('kept');
 else diceEls[i].classList.remove('kept');
 }
 // Pause to show the kept selection before rolling
 await _aiDelay(600);
 } else {
 for(let i = 0; i < 5; i++) diceEls[i].classList.remove('kept');
 }

 sfxRoll();
 const spinEls = isFirst ? diceEls : rerolled.map(i => diceEls[i]);
 for(const el of spinEls) el.classList.add('rolling');
 await _aiDelay(1600);
 for(const el of spinEls) el.classList.remove('rolling');
 // Set the final faces once, after the rotation ends.
 for(let i = 0; i < 5; i++) setDie(diceEls[i], entry.dice ? (entry.dice[i] || 0) : 0);
 await _aiDelay(400);
 }

 // If the bot stopped before using all 3 rolls, it means it decided to keep all 5 dice.
 // Highlight them so the user understands why the bot isn't rerolling!
 if (history.length < 3) {
 await _aiDelay(600);
 for(let i = 0; i < 5; i++) diceEls[i].classList.add('kept');
 await _aiDelay(600);
 }

 // Brief "thinking" beat before revealing the bot's chosen category.
 await _aiDelay(800);

 const catNameStr = cat ? catName(cat) : '';
 label.textContent = cat
 ? `${t('pdOppHand')}: ${catNameStr} — ${pts || 0} ${t('pdPts')}`
 : t('pdOppHand');
 
 if (cat) {
 const row = document.querySelector(`#pdScorecardEl tr[data-cat="${cat}"]`);
 if (row) {
 row.style.transition = '';
 row.style.backgroundColor = 'var(--accent-primary)';
 await _aiDelay(150);
 row.style.backgroundColor = '';
 await _aiDelay(150);
 row.style.backgroundColor = 'var(--accent-primary)';
 await _aiDelay(150);
 
 const oppCell = row.querySelectorAll('.cat-score')[1];
 if (oppCell) {
 oppCell.textContent = pts !== undefined ? pts : '';
 oppCell.style.color = 'var(--bg-main)';
 oppCell.style.fontWeight = 'bold';
 }
 await _aiDelay(1000);
 row.style.backgroundColor = '';
 if (oppCell) {
 oppCell.style.color = '';
 oppCell.style.fontWeight = '';
 }
 }
 }
 } finally {
 // Release the pinned height now that the final layout is settled so the
 // container can size naturally for the human's turn.
 cont.style.minHeight = '';
 pdKept = savedKept;
 pdAnimating = false;
 if(pdCode !== myCode) return;
 pdShowGame(st);
 startGamePoll('poker_dice', pdCode, pdRefreshState);
 }
 }


 function pdToggleKeep(idx){
 if(pdKept.has(idx)) pdKept.delete(idx);
 else pdKept.add(idx);
 sfxClick();
 const dice=$('pdDice').children;
 for(let i=0;i<dice.length;i++){
 const dieIdx = parseInt(dice[i].dataset.idx);
 if(pdKept.has(dieIdx)) dice[i].classList.add('kept');
 else dice[i].classList.remove('kept');
 }
}

function pdDiceDotsHtml(dice){
 let h='<div class="pd-dice" style="margin:8px auto;opacity:0.75;pointer-events:none;width:100%;justify-content:center">';
 for(let i=0;i<5;i++){
 const val = (dice&&dice[i]) || 0;
 let dots='';
 if(val){
 const d=PD_DOTS[val-1]||[];
 for(const[r,c]of d) dots+=`<div class="dot" style="grid-row:${r+1};grid-column:${c+1}"></div>`;
 }
 h+=`<div class="pd-dot-die" style="cursor:default">${dots}</div>`;
 }
 return h+'</div>';
}

function pdRenderActions(st){
 $('actions').innerHTML = '';
 $('actions').className = 'btn-row';
 const el = $('pdActions');
 el.className = 'btn-col';
 let html = '';

 // Roll button — ALWAYS visible. Active only on your turn (before scoring,
 // with rolls left and an opponent present); disabled otherwise, e.g. while
 // it's the opponent's turn.
 const canRoll = st.my_turn && !st.scored && st.rolls_left > 0;
 const waitingForOpponent = !st.solo && !st.opponent_joined;
 const rollDisabled = !canRoll || waitingForOpponent;
 const rollCount = st.my_turn ? ` (${st.rolls_left})` : '';
 html += `<button class="btn success" onclick="pdDoRoll()" ${rollDisabled?'disabled style="opacity:0.5"':''}>${t('pdRoll')}${rollCount}</button>`;

 // Show invite button only if opponent hasn't joined yet
 if(st.my_turn && !st.scored && !st.solo && !st.opponent_joined){
 html += `<button class="btn primary" onclick="sharePdGame()"> ${t('inviteFriend')}</button>`;
 }
 // Messaging is available only in a multiplayer game.
 if(!st.solo){
 html += `<div class="btn-row" style="margin-top:8px">
 <button class="btn outline" onclick="sendOpponentMessage('poker_dice',pdCode,pdState)">${t('message')}</button>
 <button class="btn outline" onclick="leavePdGame()">${t('minimize')}</button>
 </div>`;
 html += `<button class="btn outline" onclick="pdSurrender()">${t('surrender')}</button>`;
 }else{
 html += `<div class="btn-row" style="margin-top:8px">
 <button class="btn outline" onclick="pdSurrender()">${t('quit')}</button>
 <button class="btn outline" onclick="leavePdGame()" title="${t('gameSaved')}">${t('minimize')}</button>
 </div>`;
 }

 el.innerHTML = html;
}

function pdRenderInfo(st){
 if(st.phase === 'finished'){
 pdRenderResult(st);
 return;
 }

 const info = $('pdResult');

 // The top status bar is intentionally left empty in poker dice — the
 // "waiting for opponent" hint is not shown there anymore.
 setStatus('', '');

 info.innerHTML = '';
}

async function pdDoRoll(){
 if(!pdState)return;
 if(pdAnimating)return;
 sfxRoll();
 const keep=Array.from(pdKept);
 const start=Date.now();
 const MIN_ANIM=950;

 const cont=$('pdDice');
 const diceEls=[];
 for(let i=0;i<cont.children.length;i++){
 const child=cont.children[i];
 if(child.dataset.idx!==undefined) diceEls.push(child);
 }
 for(const el of diceEls){
 if(!keep.includes(parseInt(el.dataset.idx))) el.classList.add('rolling');
 }

 const res=await api('/api/pd_roll',{uid:getUid(),code:pdCode,keep:keep});
 const elapsed=Date.now()-start;
 const remain=Math.max(0,MIN_ANIM-elapsed);
 if(res===null){
 for(const el of diceEls) el.classList.remove('rolling');
 showRetry(t('error'), () => pdDoRoll());
 return;
 }
 if(!res.ok){
 for(const el of diceEls) el.classList.remove('rolling');
 setStatus(t('error'));
 return;
 }

 await new Promise(r=>setTimeout(r,remain));
 for(const el of diceEls) el.classList.remove('rolling');

 const finalDice = (res.state && res.state.dice) || [];
 for(let i=0;i<diceEls.length;i++){
 const el=diceEls[i];
 const val=finalDice[i]||0;
 const f = el.querySelector('.pd-faces');
 if(f){ f.style.opacity = val ? '1':'0'; f.style.transform = 'translateY(-'+ ((val?val-1:0)*100/6) + '%)'; }
 }

 pdShowGame(res.state);
}

async function pdDoScore(category){
 if(!pdState || !category) return;
 sfxClick();
 const keep=Array.from(pdKept);
 const res=await api('/api/pd_score',{uid:getUid(),code:pdCode,category:category,keep:keep});
 if(res===null){ showRetry(t('error'), () => pdDoScore(category)); return; }
 if(!res.ok){setStatus(t('error'));return}
 pdKept = new Set();
 // Render the player's own result immediately -- this used to be delayed
 // behind the AI's entire turn (roll/keep/score), which could take a
 // while at Expert difficulty. The AI's turn is now a separate follow-up
 // step (see pdRunBotTurn), triggered right after this paints.
 pdShowGame(res.state);
 if(res.state && res.state.solo && res.state.phase === 'playing'&& res.state.turn === 2){
 await pdRunBotTurn();
 }
}

function _fetchWithTimeout(url, opts, ms){
 return Promise.race([
  api(url, opts),
  new Promise((_, rej)=> setTimeout(()=> rej(new Error('bot_turn_timeout')), ms))
 ]);
}

async function pdRunBotTurn(){
 if(!pdCode) return;
 const myCode = pdCode;
 try {
 pdAnimating = true;
 stopGamePoll('poker_dice');

 const cont = $('pdDice');
 if(!cont) return;
 cont.style.minHeight = cont.offsetHeight + 'px';
 cont.innerHTML = '';

 const label = document.createElement('div');
 label.style.cssText = 'width:100%;text-align:center;font-size:13px;color:var(--color-hit);font-weight:600;margin-bottom:6px;margin-top:6px;min-height:20px';
 cont.appendChild(label);

 const diceEls = [];
 for(let i = 0; i < 5; i++){
 const die = document.createElement('div');
 die.className = 'pd-dot-die';
 die.style.cursor = 'default';
 die.dataset.idx = i;
 die.innerHTML = pdDieInner();
 cont.appendChild(die);
 diceEls.push(die);
 }
 cont.style.minHeight = cont.offsetHeight + 'px';

 const setDie = (el, val, snap=false) => {
 const f = el.querySelector('.pd-faces');
 if(f){ 
 if(snap) f.style.transition = 'none';
 f.style.opacity = val ? '1':'0'; 
 f.style.transform = 'translateY(-'+ ((val?val-1:0)*100/6) + '%)'; 
 if(snap) { void f.offsetWidth; f.style.transition = ''; }
 }
 };

 const genDice = () => [
 Math.floor(Math.random()*6)+1, Math.floor(Math.random()*6)+1,
 Math.floor(Math.random()*6)+1, Math.floor(Math.random()*6)+1,
 Math.floor(Math.random()*6)+1
 ];

 const rollHistory = [];
 let currentDice = genDice();

 // === ROLL 1: animate all 5 dice ===
 label.textContent = `${t('pdThrow')} 1`;
 sfxRoll();
 for(const el of diceEls) el.classList.add('rolling');

 // Start server thinking IN PARALLEL with roll animation
 let keepPromise = _fetchWithTimeout('/api/pd_bot_keep',
   {uid:getUid(), code:pdCode, dice: currentDice, rolls_left: 2}, 20000);

 await _aiDelay(1600);
 for(const el of diceEls) el.classList.remove('rolling');
 for(let i = 0; i < 5; i++) setDie(diceEls[i], currentDice[i], true);
 rollHistory.push({dice: [...currentDice], kept: [], rerolled: [0,1,2,3,4]});

 // Wait for keep decision (may already be done if server was fast)
 let keepRes = await keepPromise;
 if(!keepRes || !keepRes.ok || pdCode !== myCode) return;

 if(!keepRes.all_kept) {
   // Show which dice the bot keeps
   await _aiDelay(400);
   for(let i = 0; i < 5; i++){
     if(keepRes.kept.includes(i)) diceEls[i].classList.add('kept');
     else diceEls[i].classList.remove('kept');
   }
   label.textContent = `${t('pdThrow')} 2 · ${t('pdKept')} ${keepRes.kept.length}, ${t('pdDiscarded')} ${keepRes.rerolled.length}`;
   await _aiDelay(600);

   // === ROLL 2: reroll unkept dice ===
   for(const idx of keepRes.rerolled) currentDice[idx] = Math.floor(Math.random()*6)+1;
   sfxRoll();
   for(const idx of keepRes.rerolled) diceEls[idx].classList.add('rolling');

   // Start server thinking for roll 2 IN PARALLEL
   keepPromise = _fetchWithTimeout('/api/pd_bot_keep',
     {uid:getUid(), code:pdCode, dice: currentDice, rolls_left: 1}, 20000);

   await _aiDelay(1600);
   for(const idx of keepRes.rerolled) diceEls[idx].classList.remove('rolling');
   for(let i = 0; i < 5; i++) {
     diceEls[i].classList.remove('kept');
     setDie(diceEls[i], currentDice[i], true);
   }
   rollHistory.push({dice: [...currentDice], kept: keepRes.kept, rerolled: keepRes.rerolled});

   // Wait for keep decision 2
   const keepRes2 = await keepPromise;
   if(!keepRes2 || !keepRes2.ok || pdCode !== myCode) return;

   if(!keepRes2.all_kept) {
     // Show which dice the bot keeps
     await _aiDelay(400);
     for(let i = 0; i < 5; i++){
       if(keepRes2.kept.includes(i)) diceEls[i].classList.add('kept');
       else diceEls[i].classList.remove('kept');
     }
     label.textContent = `${t('pdThrow')} 3 · ${t('pdKept')} ${keepRes2.kept.length}, ${t('pdDiscarded')} ${keepRes2.rerolled.length}`;
     await _aiDelay(600);

     // === ROLL 3: final reroll ===
     for(const idx of keepRes2.rerolled) currentDice[idx] = Math.floor(Math.random()*6)+1;
     sfxRoll();
     for(const idx of keepRes2.rerolled) diceEls[idx].classList.add('rolling');
     await _aiDelay(1600);
     for(const idx of keepRes2.rerolled) diceEls[idx].classList.remove('rolling');
     for(let i = 0; i < 5; i++){
       diceEls[i].classList.remove('kept');
       setDie(diceEls[i], currentDice[i], true);
     }
     rollHistory.push({dice: [...currentDice], kept: keepRes2.kept, rerolled: keepRes2.rerolled});
   } else {
     // Bot keeps all after roll 2
     await _aiDelay(600);
     for(let i = 0; i < 5; i++) diceEls[i].classList.add('kept');
     await _aiDelay(600);
   }
 } else {
   // Bot keeps all after roll 1
   await _aiDelay(600);
   for(let i = 0; i < 5; i++) diceEls[i].classList.add('kept');
   await _aiDelay(600);
 }

 // === SCORE: server picks category and commits (fast) ===
 await _aiDelay(400);
 const scoreRes = await _fetchWithTimeout('/api/pd_bot_score',
   {uid:getUid(), code:pdCode, roll_history: rollHistory}, 5000);
 if(!scoreRes || !scoreRes.ok || pdCode !== myCode) return;

 const st = scoreRes.state;
 const cat = st.opponent_scored_category;
 const pts = st.opponent_scored_points;

 const catNameStr = cat ? catName(cat) : '';
 label.textContent = cat
   ? `${t('pdOppHand')}: ${catNameStr} — ${pts || 0} ${t('pdPts')}`
   : t('pdOppHand');

 // Blink the scorecard row
 if (cat) {
   pdRenderScorecard(st);
   const row = document.querySelector(`#pdScorecardEl tr[data-cat="${cat}"]`);
   if (row) {
     row.style.transition = '';
     row.style.backgroundColor = 'var(--accent-primary)';
     await _aiDelay(150);
     row.style.backgroundColor = '';
     await _aiDelay(150);
     row.style.backgroundColor = 'var(--accent-primary)';
     await _aiDelay(150);
     const oppCell = row.querySelectorAll('.cat-score')[1];
     if (oppCell) {
       oppCell.textContent = pts !== undefined ? pts : '';
       oppCell.style.color = 'var(--bg-main)';
       oppCell.style.fontWeight = 'bold';
     }
     await _aiDelay(1000);
     row.style.backgroundColor = '';
     if (oppCell) {
       oppCell.style.color = '';
       oppCell.style.fontWeight = '';
     }
   }
 }

 // Mark this turn as seen so pdMaybeAnimateOpponent won't replay it
 const hist = st.opponent_roll_history || [];
 const key = hist.map(h => (h.dice||[]).join(',')).join('|') + ':'+ (st.opponent_scored_category || '');
 pdSeenScore = key;

 cont.style.minHeight = '';
 pdShowGame(st);
 } catch (e) {
 console.error('[pd] bot turn failed', e);
 } finally {
 pdAnimating = false;
 if(pdCode === myCode) startGamePoll('poker_dice', pdCode, pdRefreshState);
 }
}

// Called by doFirstRoll/doRerollFirst when the opening-roll response says the
// bot won the toss and owes its first move. A short delay lets the popup show
// the winner before the bot's opening animation starts. Also sets _pdBotOpening
// so the auto-proceed path (pdShowGame -> line 218) skips the redundant trigger.
function pdAfterOpeningRoll(){
 if(pdOpeningPending) return;
 pdOpeningPending = true;
 const myCode = pdCode;
 pdOpeningTimer = setTimeout(async () => {
 pdOpeningPending = false;
 if(pdCode !== myCode) return;
 
 _rollAckShown[pdCode] = true;
 closeFirstRollPopup();
 if (pdState) {
 pdRenderScorecard(pdState);
 pdRenderDice(pdState);
 pdRenderActions(pdState);
 pdRenderInfo(pdState);
 }

 _pdBotOpening = true;
 try { await pdRunBotTurn(); } finally { _pdBotOpening = false; }
 }, 700);
}

function pdRenderResult(st){
 const div=$('pdResult');
 // Clear other pd areas so only result is visible, collapse min-heights
 $('pdScorecardContainer').innerHTML = '';
 $('pdScorecardContainer').style.minHeight = '0';
 $('pdDice').innerHTML = '';
 $('pdDice').style.minHeight = '0';
 $('pdActions').innerHTML = '';
 $('pdActions').style.minHeight = '0';
 $('actions').innerHTML = '';
 $('actions').className = 'btn-row';

 let html = '';

 // Win/lose status
 if(st.winner===st.you_id){
 setStatus(t('pdWin'),'battle');
 sfxWin();
 }else if(st.winner===0||(st.solo&&st.winner===0)){
 setStatus(t('pdLose'),'');
 sfxLose();
 }else if(st.winner===-1){
 setStatus(t('pdDraw'),'');
 }

 // Scorecard final table — rendered inside a modal popup (see showPdResultPopup)
 html += '<table class="pd-scorecard" style="margin:8px auto;max-width:340px">';
 html += `<tr><th class="cat-name"></th><th class="cat-score"> ${t('pdMe')||'Я'}</th><th class="cat-score"> ${t('pdOpp')||'Сопер.'}</th></tr>`;

 const sc = st.scorecard_all || {};
 const oppSc = st.opponent_scorecard_all || {};

 const renderCat = (catId) => {
 const myVal = sc[catId];
 const oppVal = oppSc[catId];
 html += `<tr><td class="cat-name"> ${catName(catId)}</td><td class="cat-score">${myVal !== null ? myVal : '-'}</td><td class="cat-score" style="color:var(--text-hint)">${oppVal !== null ? oppVal : '-'}</td></tr>`;
 };

 for(let i = 0; i < 6; i++) renderCat(PD_CATEGORIES[i]);
 const bonus = st.bonus;
 html += `<tr class="bonus-row"><td> ${t('pdBonus')||'Бонус'} (>=63)</td><td>${bonus ? '+35': '0'}</td><td style="color:var(--text-hint)">${st.opponent_bonus ? '+35': '0'}</td></tr>`;
 html += `<tr class="section-divider"><td colspan="3"></td></tr>`;
 for(let i = 6; i < PD_CATEGORIES.length; i++) renderCat(PD_CATEGORIES[i]);

 const totalCls = st.total_score > st.opponent_total_score ? 'total-row win': st.total_score < st.opponent_total_score ? 'total-row lose': 'total-row';
 html += `<tr class="${totalCls}"><td>Σ ${t('pdTotal')||'Итого'}</td><td>${st.total_score}</td><td>${st.opponent_total_score}</td></tr>`;
 html += '</table>';

 // Action buttons right below the table
 const playAgainFn = st.solo ? 'pdStartSolo()': 'pdNewMulti()';
 html += `<div class="btn-col" style="margin-top:12px">
 <button class="btn success" onclick="${playAgainFn}"> ${t('pdPlayAgain')}</button>
 <button class="btn outline" onclick="showMenu()">${t('quit')}</button>
 </div>`;

 div.innerHTML = html;

 // Show the result table in a modal popup instead of inline
 showPdResultPopup(st, html);

 // Clear saved game on finish so it doesn't show in menu
 if(pdCode) localStorage.removeItem('pd_game');
}

// Show the final scorecard in a modal popup (overlay + .modal), matching the
// project's existing popup style (.overlay / .modal from common.js).
function showPdResultPopup(st, tableHtml){
 // Remove any existing result popup
 if(_pdResultPopupEl){ _pdResultPopupEl.remove(); _pdResultPopupEl=null; }
 const playAgainFn = st.solo ? 'pdStartSolo()': 'pdNewMulti()';
 const popup = document.createElement('div');
 popup.className = 'overlay';
 popup.id = 'pdResultPopup';
 popup.setAttribute('role','dialog');
 popup.setAttribute('aria-modal','true');
 popup._onKey = (e)=>{ if(e.key==='Escape') closePdResultPopup(); };
 document.addEventListener('keydown', popup._onKey);
 popup.innerHTML = `
  <div class="modal" style="max-width:340px;text-align:center">
   <h2>${st.winner===st.you_id ? (t('pdWin')||'Победа!') : st.winner===-1 ? (t('pdDraw')||'Ничья') : (t('pdLose')||'Поражение')}</h2>
   ${tableHtml}
   <div class="btn-row" style="margin-top:12px;gap:8px">
    <button class="btn success" onclick="${playAgainFn}"> ${t('pdPlayAgain')}</button>
    <button class="btn outline" onclick="closePdResultPopup()">${t('quit')}</button>
   </div>
  </div>
 `;
 document.body.appendChild(popup);
 _pdResultPopupEl = popup;
}

function closePdResultPopup(){
 if(_pdResultPopupEl){
  document.removeEventListener('keydown', _pdResultPopupEl._onKey);
  _pdResultPopupEl.remove();
  _pdResultPopupEl=null;
 }
 // Return to main menu after closing the popup
 $('pdArea').style.display='none';
 showMainMenu();
}

function leavePdGame(){
 stopGamePoll('poker_dice');
 if(pdOpeningTimer){clearTimeout(pdOpeningTimer);pdOpeningTimer=null;}
 pdAnimating=false;
 // pd_game code stays in localStorage so the main menu's active-games bar can resume it
 pdCode=null; pdState=null;
 $('pdArea').style.display='none';
 showMainMenu();
}

async function pdSurrender(){
 const msg = {ru:'Сдаться? Игра будет завершена.',uk:'Здатися? Гра буде завершена.',en:'Surrender? The game will end.'}[lang];
 confirmDialog(t('surrender')||'Surrender?', msg, async () => {
 const res=await api('/api/pd_surrender',{uid:getUid(),code:pdCode});
 if(!res||!res.ok){setStatus(t('error'));return}
 localStorage.removeItem('pd_game');
 pdShowGame(res.state);
 });
}

function sharePdGame(){
 if(!pdCode)return;
 copyToClipboard(pdCode,{ru:'Код скопирован OK',uk:'Код скопійовано OK',en:'Code copied OK'}[lang]);
 try{Telegram.WebApp.openTelegramLink(`https://t.me/share/url?url=${encodeURIComponent(pdCode)}`)}catch(e){}
}

function resumePd(code){
 currentGameType=null; setHelpVisible(false); setStripLockVisible(false);
 pdCode=code;
 _lastPDSig=null;
 localStorage.setItem('pd_game',code);
 pdKept = new Set();
 $('actions').innerHTML='';
 pdRefreshState();
 startGamePoll('poker_dice', pdCode, pdRefreshState);
}

