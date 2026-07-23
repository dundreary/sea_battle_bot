// ---- Checkers ----
let ckState=null, ckCode=null, ckSelected=null, ckSeenMove='', ckHint=null;

const CK_PIECE_NAMES={0:'.',1:'w',2:'b',3:'W',4:'B'};
let _lastCKSig=null, _ckRefreshing=false, _lastCKBoardSig=null;

function showCheckers(){
 currentGameType='checkers'; setHelpVisible(true);
 var lb=$('langBar');if(lb)lb.style.display='none';
 setStripLockVisible(false);
 hideAllGameAreas();
 if($('legend'))$('legend').style.display='none';
 $('header').classList.remove('in-game');
 document.title=t('checkers');
 $('gameInfo').textContent='';
 setStatus('');
 $('actions').className='btn-row stack';
 var savedCk = localStorage.getItem('ck_game');
 var resumeHtml = '';
 if(savedCk){
 resumeHtml = `<div class="active-game-row" onclick="resumeCk('${savedCk}')">
 <div class="info"><span class="label"> </span><span class="code">${savedCk}</span></div>
 <span class="badge playing"> ${t('continue')}</span>
 </div>`;
 }
 $('actions').innerHTML=`
 ${resumeHtml}
 <div class="game-card" aria-label="${t('vsBot')}" onclick="ckStartSolo()" style="margin-bottom:8px">
 <img src="/static/mode-bot.svg" class="card-icon">
 <div class="card-name">${t('vsBot')}</div>
 </div>
 ${!savedCk ? `
 <div class="game-card" aria-label="${t('vsFriend')}" onclick="ckNewMulti()" style="margin-bottom:8px">
 <img src="/static/mode-friend.svg" class="card-icon">
 <div class="card-name">${t('vsFriend')}</div>
 </div>
 ` : ''}
 <button class="btn outline quit-btn" onclick="showMainMenu()">${t('quit')}</button>
 `;
}

async function ckStartSolo(){
 currentGameType=null; setHelpVisible(false);
 currentScreen='checkers';
 try{ if(typeof window.Telegram!=='undefined'&& window.Telegram.WebApp && window.Telegram.WebApp.BackButton) window.Telegram.WebApp.BackButton.show(); }catch(e){}
 const res=await api('/api/checkers_new_solo',{uid:getUid(), difficulty: getDifficulty()});
 if(res===null){ showRetry(t('error'), ()=>ckStartSolo()); return; }
 if(!res||!res.ok){setStatus(t('error'));return}
 ckCode=res.code;
 _lastCKSig=null; _lastCKBoardSig=null;
 localStorage.setItem('ck_game',ckCode);
 const _sb=$('sbOppHistory'); if(_sb) _sb.innerHTML='';
 ckShowGame(res.state);
 startGamePoll('checkers', ckCode, ckRefreshState);
}

async function ckNewMulti(){
 currentGameType=null; setHelpVisible(false);
 currentScreen='checkers';
 try{ if(typeof window.Telegram!=='undefined'&& window.Telegram.WebApp && window.Telegram.WebApp.BackButton) window.Telegram.WebApp.BackButton.show(); }catch(e){}
 const res=await api('/api/checkers_new_multi',{uid:getUid()});
 if(res===null){ showRetry(t('error'), () => ckNewMulti()); return; }
 if(!res.ok){setStatus(t('error'));return}
 ckCode=res.code;
 _lastCKSig=null; _lastCKBoardSig=null;
 localStorage.setItem('ck_game',ckCode);
 ckShowGame(res.state);
 startGamePoll('checkers', ckCode, ckRefreshState);
}

async function ckJoin(code){
 const res=await api('/api/checkers_join',{uid:getUid(),code:code.toUpperCase()});
 if(res===null){ showRetry(t('error'), () => ckJoin(code)); return; }
 if(!res.ok){setStatus(t('joinError'));return}
 ckCode=code.toUpperCase();
 _lastCKSig=null; _lastCKBoardSig=null;
 localStorage.setItem('ck_game',ckCode);
 ckShowGame(res.state);
 startGamePoll('checkers', ckCode, ckRefreshState);
}

async function ckRefreshState(){
 if(!ckCode)return;
 if(_ckRefreshing) return;
 _ckRefreshing=true;
 try{
 const res=await api('/api/checkers_state',{uid:getUid(),code:ckCode});
 notePollResult('checkers', res!==null);
 if(!res||!res.ok){
 localStorage.removeItem('ck_game');
 ckCode=null;
 stopGamePoll('checkers');
 showCheckers();
 return;
 }
 if(!ckCode)return;
 const st=res.state;
 // Real-time opponent reveal: when the friend just moved and it is now
 // our turn, announce their move (their last move is highlighted too).
 if(!st.solo && st.last_move && st.turn===st.my_color){
 const m=st.last_move;
 const key=m[0].join(',')+'->'+m[1][m[1].length-1].join(',');
 if(key!==ckSeenMove){
 ckSeenMove=key;
 showRevealBanner(''+{ru:'Ход соперника',uk:'Хід суперника',en:"Opponent's move"}[lang]);
 }
 }
 const sig = JSON.stringify([st.phase, st.board, st.turn, st.my_color, st.my_turn, st.solo, st.opponent_joined, st.winner, st.last_move]);
 if(sig===_lastCKSig) return;
 _lastCKSig = sig;
 ckShowGame(res.state);
 } finally {
 _ckRefreshing=false;
 }
}

async function ckShowGame(st){
 ckState=st;
 showIncomingMessages(st.messages);
 ckSelected=null;
 ckHint=null;
 // Only hide/show areas when ckArea isn't already visible.  The previous
 // code called hideAllGameAreas() (which sets ckArea.style.display='none')
 // and then immediately set it back to '' on EVERY call — including every
 // poll and every turn change.  That display:none → display:'' toggle
 // triggers a layout reflow and is a major cause of the board "jumping".
 if($('ckArea').style.display === 'none'){
 hideAllGameAreas();
 $('ckArea').style.display='';
 }else{
 // ckArea is already visible — just make sure no other game area is.
 $('ownBoardWrap').classList.add('hidden');
 $('oppBoardWrap').classList.add('hidden');
 $('pdArea').style.display='none';
 $('bgArea').style.display='none';
 const _sh=$('shipHint'); if(_sh) _sh.innerHTML='';
 }
 setThemeSelectorVisibility(false);
 $('header').classList.add('in-game');
 document.title=t('checkers');
 $('gameInfo').textContent='';
 $('actions').innerHTML='';
 $('actions').className='btn-row';
 // Only re-render the board when the board-relevant state actually changed.
 // This avoids unnecessary DOM work (and the visual "jump") when ckShowGame
 // is called multiple times with the same board — e.g. ckCellClick calls
 // ckShowGame twice (player_state + state) and the bot-opening path may
 // trigger an extra render.  Reusing cells in ckRenderBoard already prevents
 // a full reflow, but skipping the call entirely is even cheaper.
 // Board rendering: cell reuse prevents reflow, so we can safely render
 // on every poll without the performance/visible-jump penalty.
 // The only guard we keep is to skip if ckArea isn't visible.
 ckRenderBoard(st);
 // Hide the board behind the overlay during the roll phase (like Sea Battle)
 // so the centered popup doesn't appear to shift against the board.
 const _ckb=document.getElementById('ckBoard');
 if(_ckb) _ckb.style.visibility = (st.phase==='roll') ? 'hidden': '';
 if(st.phase==='finished'){
 stopGamePoll('checkers');
 localStorage.removeItem('ck_game');
 let icon, title, desc;
 if(st.draw){
 icon=''; title=t('draw')||'НИЧЬЯ';
 }else{
 const won = st.winner === st.my_color;
 icon = won ? '': '';
 title = won ? t('win') : t('lose');
 }
 desc = t('checkers');
 showResult(icon,title,desc,false,'ckStartSolo()',t('playAgain'));
 const el=$('ckActions');
 el.className='btn-col';
 el.innerHTML=`
 <button class="btn success" onclick="ckStartSolo()">${t('playAgain')}</button>
 <button class="btn outline" onclick="showCheckers()">${t('close')}</button>
 `;
 return;
 }
 const el=$('ckActions');
 el.className='btn-col';
 let html='';
 const rollDecided = st.my_roll != null && st.opp_roll != null && st.my_roll !== st.opp_roll;
 if(st.phase==='roll'|| (rollDecided && !_rollAckShown[ckCode])){
 if(rollDecided && _rollAckShown[ckCode]){
 closeFirstRollPopup();
 } else {
 setStatus(''+t('rollTitle'),'');
 // Opening toss now renders in the modal popup; surrender stays reachable
 // outside it. The popup re-renders idempotently on each poll.
 showFirstRollPopup(st, 'ckRollFirst', 'ckRerollFirst', { solo: st.solo, code: ckCode, proceedFn: () => { _lastCKSig = null; ckRefreshState(); } });
 el.innerHTML = `<button class="btn outline" onclick="ckSurrender()">${st.solo ? t('quit') : t('surrender')}</button>`;
 return;
 }
 }
 closeFirstRollPopup();
 if(st.phase==='playing'&& st.solo && !st.my_turn && !_ckBotOpening){
 _ckBotOpening = true;
 try{
 setStatus(''+{ru:'ХОД СОПЕРНИКА...',uk:'ХІД СУПЕРНИКА...',en:"OPPONENT'S TURN..."}[lang],'');
 await ckRunBotTurn();
 }finally{
 _ckBotOpening = false;
 }
 return;
 }
 if(st.my_turn){
 setStatus(''+{ru:'ТВОЙ ХОД!',uk:'ТВІЙ ХІД!',en:'YOUR TURN!'}[lang],'battle');
 const inviteBtn=st.solo||st.opponent_joined?'':`<button class="btn primary" onclick="shareCkGame()"> ${t('ckInviteFriend')}</button>`;
 if(inviteBtn){
 html+=`<div class="btn-row">${inviteBtn}</div>`;
 }
 }else{
 setStatus(''+{ru:'ХОД СОПЕРНИКА...',uk:'ХІД СУПЕРНИКА...',en:"OPPONENT'S TURN..."}[lang],'');
 }
 html+=`<div class="btn-row"><button class="btn success" onclick="ckGetHint()" ${st.my_turn?'':'disabled style="opacity:0.45;cursor:default"'}> ${t('ckHint')}</button></div>`;
 if(!st.solo){
 html+=`<div class="btn-row" style="margin-top:8px">
 <button class="btn outline" onclick="sendOpponentMessage('checkers',ckCode,ckState)">${t('message')}</button>
 <button class="btn outline" onclick="leaveCkGame()">${t('minimize')}</button>
 </div>
 <button class="btn outline" onclick="ckSurrender()">${t('surrender')}</button>`;
 }else{
 html+=`<div class="btn-row" style="margin-top:8px">
 <button class="btn outline" onclick="ckSurrender()">${t('quit')}</button>
 <button class="btn outline" onclick="leaveCkGame()" title="${t('gameSaved')}">${t('minimize')}</button>
 </div>`;
 }
 el.innerHTML=html;
 if(!st.solo){
 $('status').style.cursor='pointer';
 $('status').title=t('copyCode');
 $('status').onclick=()=>navigator.clipboard.writeText(st.code).then(()=>setStatus('OK '+t('shareCopied'),''));
 }
}

function ariaCellLabel(r,c,piece,isSrc){
 let label = t('ariaCell', String.fromCharCode(65+c), (8-r));
 if(piece){
 label += ', '+ (piece===1||piece===3 ? t('ckWhitePiece') : t('ckBlackPiece')) + (piece===3||piece===4 ? ''+t('ckKing') : '');
 }
 if(isSrc){
 label += ', '+t('ckSelect');
 }else{
 label += ', '+t('ckMoveHere');
 }
 return label;
}

function ckRenderBoard(st){
 const board=$('ckBoard');
 const grid=st.board;
 // BLACK viewer sits on the opposite side: rotate the board 180° so their
 // pieces appear at the bottom. 63 - idx is the mirrored (7-r, 7-c) cell.
 const flip = st.my_color === 2;
 const toCan = (i)=> flip ? 63 - i : i;
 const highlighted=new Set((st.highlighted_cells||[]).map(([r,c])=>toCan(r*8+c)));
 const lastMove=st.last_move;
 const lastCells=new Set();
 const ckDests=ckComputeDests(st, ckSelected);
 if(lastMove){
 lastCells.add(toCan(lastMove[0][0]*8+lastMove[0][1]));
 for(const s of lastMove[1])lastCells.add(toCan(s[0]*8+s[1]));
 }
 // Reuse existing cell elements instead of clearing innerHTML and rebuilding
 // all 64 from scratch.  Destroying/recreating the cells on every poll causes
 // the board to "jump" (a full reflow + repaint) whenever the turn changes.
 // By updating cells in place the board stays visually anchored.
 const existing=board.children;
 let idx=0;
 for(let r=0;r<8;r++){
 for(let c=0;c<8;c++){
 let cell=existing[idx];
 if(!cell){
 cell=document.createElement('div');
 board.appendChild(cell);
 }
 // Reset every mutable property so stale state from a previous render
 // (classes, handlers, aria, inline styles) never leaks into this cell.
 cell.className='ck-cell';
 cell.innerHTML='';
 cell.onclick=null;
 cell.onkeydown=null;
 cell.style.cursor='';
 cell.removeAttribute('role');
 cell.removeAttribute('aria-label');
 cell.removeAttribute('tabindex');
 const isDark=(r+c)%2===1;
 cell.classList.add(isDark?'dark':'light');
 const visIdx=r*8+c;
 const canIdx=toCan(visIdx);
 const piece=grid[canIdx];
 if(ckSelected&&toCan(ckSelected[0]*8+ckSelected[1])===canIdx)cell.classList.add('selected');
 if(isDark&&piece!==0){
 const el=document.createElement('div');
 const color=piece===1||piece===3?'white':'black';
 const isKing=piece===3||piece===4;
 el.className='ck-piece '+color+(isKing?'king':'');
 if(lastCells.has(canIdx))el.classList.add('last-move');
 el.setAttribute('role','img');
 el.setAttribute('aria-label', piece===1||piece===3 ? t('ckWhitePiece')+(isKing?''+t('ckKing'):'') : t('ckBlackPiece')+(isKing?''+t('ckKing'):''));
 cell.appendChild(el);
 }
 if(isDark&&st.my_turn&&highlighted.has(visIdx)){
 cell.classList.add('highlight-src');
 cell.style.cursor='pointer';
 cell.onclick=()=>ckCellClick(r,c);
 cell.setAttribute('role','button');
 cell.tabIndex = 0;
 cell.setAttribute('aria-label', ariaCellLabel(r,c, piece, true));
 cell.onkeydown = (e)=>{ if(e.key==='Enter'||e.key===''){ e.preventDefault(); ckCellClick(r,c); } };
 }
 if(isDark&&ckDests&&ckDests.has(visIdx)){
 cell.classList.add('highlight-dest');
 cell.style.cursor='pointer';
 cell.onclick=()=>ckCellClick(r,c);
 cell.setAttribute('role','button');
 cell.tabIndex = 0;
 cell.setAttribute('aria-label', ariaCellLabel(r,c, piece, false));
 cell.onkeydown = (e)=>{ if(e.key==='Enter'||e.key===''){ e.preventDefault(); ckCellClick(r,c); } };
 }
 if(ckHint){
 if(ckHint[0]===r && ckHint[1]===c) cell.classList.add('highlight-src');
 if(ckHint[2]===r && ckHint[3]===c) cell.classList.add('highlight-capture');
 }
 idx++;
 }
 }
 // Remove any surplus cells (shouldn't happen for a fixed 8×8 board, but
 // keeps the DOM clean if the board size ever changes).
 while(board.children.length>idx){
 board.removeChild(board.children[board.children.length-1]);
 }
 // Keep the board-signature in sync even when ckRenderBoard is called
 // directly (e.g. from ckCellClick on select/deselect), so the guard in
 // ckShowGame doesn't skip a render that's actually needed.
 _lastCKBoardSig = st.board.join(',') + '|' + st.turn + '|' + (st.last_move ? JSON.stringify(st.last_move) : '');
}

function ckComputeDests(st, sel){
 if(!sel||!st||!st.valid_dests)return null;
 const flip = st.my_color === 2;
 const visIdx=sel[0]*8+sel[1];
 const canIdx = flip ? 63 - visIdx : visIdx;
 const arr=st.valid_dests[canIdx];
 if(!arr)return null;
 return new Set(flip ? arr.map(i=>63-i) : arr);
}

async function ckCellClick(r,c){
 if(!ckState||!ckState.my_turn)return;
 const flip = ckState.my_color === 2;
 if(ckSelected){
 const sr=ckSelected[0],sc=ckSelected[1];
 if(sr===r&&sc===c){ckSelected=null;ckRenderBoard(ckState);return}
 let csr=sr, csc=sc, cr=r, cc=c;
 if(flip){ csr=7-sr; csc=7-sc; cr=7-r; cc=7-c; }
 const res=await api('/api/checkers_move',{uid:getUid(),code:ckCode,start_r:csr,start_c:csc,end_r:cr,end_c:cc});
 if(res===null){ showRetry(t('error'), () => ckCellClick(r,c)); return; }
 if(!res.ok){setStatus(res?.error==='illegal_move'?{ru:'Нелегальный ход',uk:'Нелегальний хід',en:'Illegal move'}[lang]:t('error'),'') ;ckSelected=null;ckRenderBoard(ckState);return}
 sfxHit();
 // Render your move immediately so the checker slides into place first --
 // this used to be delayed behind the AI's own move computation. The AI's
 // move is now a separate follow-up step (see ckRunBotTurn), triggered
 // right after this paints, instead of arriving bundled in this response.
 if(res.player_state) ckShowGame(res.player_state);
 ckShowGame(res.state);
 // ckShowGame(res.player_state) may have already entered the bot-opening
 // path (which calls ckRunBotTurn internally).  Guard against a duplicate
 // call here — without this the bot turn fires twice, causing an extra
 // board re-render and a visible "jump".
 if(res.needs_bot_turn && !_ckBotOpening) await ckRunBotTurn();
 return;
 }
 let pr=r, pc=c;
 if(flip){ pr=7-r; pc=7-c; }
 const piece=ckState.board[pr*8+pc];
 if(piece===0)return;
 const color=piece===1||piece===3?1:2;
 if(color!==ckState.turn)return;
 ckSelected=[r,c];
 ckHint=null;
 ckRenderBoard(ckState);
}

async function ckRunBotTurn(){
 if(!ckCode) return;
 const myCode = ckCode;
 try {
 // A brief beat before fetching so the player's own move has a moment to
 // register visually, then the AI's move is fetched and rendered.
 await _aiDelay(250);
 const res = await api('/api/checkers_bot_turn', {uid:getUid(), code:ckCode});
 if(!res || !res.ok) return;
 if(!ckCode) return;
 if(ckCode !== myCode) return;
 ckShowGame(res.state);
 } finally {
 hideAiThinking();
 }
}

async function ckGetHint(){
 const res=await api('/api/checkers_hint',{uid:getUid(),code:ckCode});
 if(res===null){ showRetry(t('error'), () => ckGetHint()); return; }
 if(!res.ok){setStatus(t('ckNoMoves'),'');return}
 const h=res.hint;
 const flip = ckState && ckState.my_color === 2;
 let sr=h.start[0], sc=h.start[1], er=h.end[0], ec=h.end[1];
 if(flip){ sr=7-sr; sc=7-sc; er=7-er; ec=7-ec; }
 // Highlight only the suggested move (source in blue, destination in red)
 // instead of selecting the piece, which would also reveal every legal
 // destination and look like several moves at once.
 ckSelected=null;
 ckHint=[sr,sc,er,ec];
 setStatus(''+String.fromCharCode(65+ec)+(8-er),'');
 ckRenderBoard(ckState);
}

function leaveCkGame(){
 stopGamePoll('checkers');
 _ckBotOpening=false;
 // ck_game code stays in localStorage so the main menu's active-games bar can resume it
 ckCode=null;ckState=null;
 $('ckArea').style.display='none';
 showMainMenu();
}

function shareCkGame(){
 if(!ckCode)return;
 copyToClipboard(ckCode,{ru:'Код скопирован OK',uk:'Код скопійовано OK',en:'Code copied OK'}[lang]);
 try{Telegram.WebApp.openTelegramLink(`https://t.me/share/url?url=${encodeURIComponent(ckCode)}`)}catch(e){}
}

function ckSurrender(){
 const msg = {ru:'Сдаться? Игра будет завершена.',uk:'Здатися? Гра буде завершена.',en:'Surrender? The game will end.'}[lang];
 confirmDialog(t('surrender')||'Surrender?', msg, () => {
 stopGamePoll('checkers');
 const code = ckCode;
 ckCode = null; ckState = null;
 $('ckArea').style.display='none';
 localStorage.removeItem('ck_game');
 api('/api/checkers_surrender',{uid:getUid(),code}).then(()=>showMainMenu());
 });
}

