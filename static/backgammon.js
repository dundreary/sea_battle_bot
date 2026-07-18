// ---- Backgammon ----
let bgCode=null, bgState=null, bgPollTimer=null, bgSeenRoll='';
let bgSelected=null, bgMoveTargets=[], bgVariant='short';

const BG_CHECKER_COLORS = {1:'white',[-1]:'black'};

function showBackgammon(){
  var lb=$('langBar');if(lb)lb.style.display='none';
  hideAllGameAreas();
  if($('legend'))$('legend').style.display='none';
  document.title=t('backgammon');
  $('gameInfo').textContent='';
  setStatus('');
  $('actions').className='btn-row stack';
  var savedBg = localStorage.getItem('bg_game');
  var resumeHtml = '';
  if(savedBg){
    resumeHtml = `<div class="active-game-row" onclick="resumeBg('${savedBg}')">
      <div class="info"><span class="label">🎲 </span><span class="code">${savedBg}</span></div>
      <span class="badge playing">▶ ${t('continue')}</span>
    </div>`;
  }
  $('actions').innerHTML=`
    ${resumeHtml}
    <div class="bg-variant-row">
      <button class="bg-variant-btn ${bgVariant==='short'?'active':''}" onclick="bgSetVariant('short')">${t('bgVariantShort')}</button>
      <button class="bg-variant-btn ${bgVariant==='long'?'active':''}" onclick="bgSetVariant('long')">${t('bgVariantLong')}</button>
    </div>
    <div class="game-card" onclick="bgStartSolo()" style="margin-bottom:8px">
      <img src="/static/mode-bot.svg" class="card-icon">
      <div class="name">${t('bgSolo')}</div>
      <div class="card-desc">${t('withBot')}</div>
    </div>
    ${!savedBg ? `
    <div class="game-card" onclick="bgNewMulti()" style="margin-bottom:8px">
      <img src="/static/mode-friend.svg" class="card-icon">
      <div class="name">${t('bgFriend')}</div>
      <div class="card-desc">${t('withFriend')}</div>
    </div>
    ` : ''}
    <button class="btn outline quit-btn" onclick="showMainMenu()">${t('quit')}</button>
  `;
}

function bgSetVariant(v){
  bgVariant=v;
  showBackgammon();
}

async function bgStartSolo(){
  const res=await api('/api/bg_new_solo',{uid:getUid(), difficulty: 2, variant: bgVariant});
  if(!res||!res.ok){setStatus(t('error'));return}
  bgCode=res.code;
  localStorage.setItem('bg_game',bgCode);
  $('actions').innerHTML='';
  bgShowGame(res.state);
}

async function bgNewMulti(){
  const res=await api('/api/bg_new_multi',{uid:getUid(), variant: bgVariant});
  if(!res||!res.ok){setStatus(t('error'));return}
  bgCode=res.code;
  localStorage.setItem('bg_game',bgCode);
  bgShowGame(res.state);
  bgPoll();
}

async function bgJoin(code){
  const res=await api('/api/bg_join',{uid:getUid(),code:code.toUpperCase()});
  if(!res||!res.ok){setStatus(t('joinError'));return}
  bgCode=code.toUpperCase();
  localStorage.setItem('bg_game',bgCode);
  bgShowGame(res.state);
  bgPoll();
}

function bgPoll(){
  if(bgPollTimer)clearInterval(bgPollTimer);
  bgPollTimer=setInterval(async()=>{
    if(!bgCode){clearInterval(bgPollTimer);bgPollTimer=null;return}
    await bgRefreshState();
  },2000);
}

async function bgRefreshState(){
  if(!bgCode)return;
  const res=await api('/api/bg_state',{uid:getUid(),code:bgCode});
  if(!res||!res.ok){
    localStorage.removeItem('bg_game');
    bgCode=null;
    showBackgammon();
    return;
  }
  if(!bgCode)return;
  const st=res.state;
  // Real-time opponent reveal: when the friend just rolled (their dice are
  // surfaced) and it is now our turn, announce what they threw.
  if(!st.solo && st.last_roller!==st.my_color && st.last_roll && st.last_roll.length && st.turn===st.my_color){
    const key=st.last_roll.join(',')+':'+st.last_roller;
    if(key!==bgSeenRoll){
      bgSeenRoll=key;
      const dice=st.last_roll.map(d=>'⚀⚁⚂⚃⚄⚅'[d-1]||d).join(' ');
      showRevealBanner('🎲 '+{ru:'Соперник выбросил '+dice,uk:'Суперник викидав '+dice,en:'Opponent rolled '+dice}[lang]);
    }
  }
  bgShowGame(res.state);
}

async function bgShowGame(st, keepSelection=false){
  bgState=st;
  showIncomingMessages(st.messages);
  if(!keepSelection){
    bgSelected=null;
    bgMoveTargets=[];
  }
  hideAllGameAreas();
  $('bgArea').style.display='';
  setThemeSelectorVisibility(false);
  $('header').classList.add('in-game');
  document.title=t('backgammon');
  $('gameInfo').textContent='';
  $('actions').innerHTML='';
  $('actions').className='btn-row';
  $('bgActions').innerHTML='';

  if(st.phase==='roll'){
    armRollBanner(bgCode);
    $('bgBoard').innerHTML='';
    setStatus('🎲 '+t('rollTitle'),'');
    const el=$('bgActions');
    el.className='btn-col';
    el.innerHTML = firstRollHTML(st, 'bgRollFirst', 'bgRerollFirst') +
      `<button class="btn danger" onclick="bgSurrender()">${t('surrender')}</button>`;
    return;
  }

  if(st.phase==='playing' && st.solo && !st.my_turn && !window._bgBotOpening){
    window._bgBotOpening = true;
    try{
      setStatus('♟ '+{ru:'ХОД СОПЕРНИКА...',uk:'ХІД СУПЕРНИКА...',en:"OPPONENT'S TURN..."}[lang],'');
      await bgRunBotTurn();
    }finally{
      window._bgBotOpening = false;
    }
    return;
  }

  bgRenderBoard(st);
  showRollWinnerBanner(st, bgCode);
  if(st.phase==='finished'){
    if(bgPollTimer){clearInterval(bgPollTimer);bgPollTimer=null}
    localStorage.removeItem('bg_game');
    const won = st.winner === st.you;
    const icon=won?'🏆':'💔';
    const title=won?t('bgWin'):t('bgLose');
    const desc=t('backgammon');
    showResult(icon,title,desc,false,'bgStartSolo()',t('bgPlayAgain'));
    const el=$('bgActions');
    el.className='btn-col';
    el.innerHTML=`
      <button class="btn success" onclick="bgStartSolo()">${t('bgPlayAgain')}</button>
      <button class="btn outline" onclick="showBackgammon()">${t('close')}</button>
    `;
    return;
  }
  bgRenderDice(st);
  bgRenderActions(st);
}

function bgRenderBoard(st){
  const cont=$('bgBoard');
  cont.innerHTML='';
  const board=st.board;
  const bar=st.bar||[0,0];
  const off=st.off||[0,0];
  const flip = st.variant === 'long' ? false : (st.my_color === -1);
  const myTurn = st.my_turn;

  // Cells the AI (solo) just moved from / to, so they can be flashed.
  const aiCells = new Set();
  if(st.last_move){
    for(const lm of st.last_move){
      if(lm[0] >= 0) aiCells.add(lm[0]);
      if(lm[1] >= 0) aiCells.add(lm[1]);
    }
  }

  // Build legal moves lookup: from -> Set<to>
  const moveMap = {};
  if(myTurn && st.legal_moves){
    for(const seq of st.legal_moves){
      for(const m of seq){
        const f=m[0], t=m[1];
        if(!moveMap[f]) moveMap[f]=new Set();
        moveMap[f].add(t);
      }
    }
  }

  const wrap=document.createElement('div');
  wrap.className='bg-board-h';

  const MAX_VIS = 5;
  const makeStack = (count, color, idx, isTop) => {
    const stack=document.createElement('div');
    stack.className='bg-stack';
    const vis=Math.min(count, MAX_VIS);
    for(let j=0;j<vis;j++){
      const ch=document.createElement('div');
      ch.className='bg-checker '+BG_CHECKER_COLORS[color];
      if(bgSelected===idx){ ch.classList.add('bg-selected'); }
      if(aiCells.has(idx)){ ch.classList.add('ai-move'); }
      if(myTurn && bgSelected===null && moveMap[idx]){
        ch.style.cursor='pointer';
        ch.onclick=(e)=>{e.stopPropagation();bgSelectSource(idx);};
      }
      if(bgSelected===idx && moveMap[idx] && moveMap[idx].has(-1)){
        ch.style.cursor='pointer';
        ch.onclick=(e)=>{e.stopPropagation();bgDoMove(bgSelected,-1);};
      }
      stack.appendChild(ch);
    }
    if(count>MAX_VIS){
      const pill=document.createElement('div');
      pill.className='bg-count '+BG_CHECKER_COLORS[color];
      pill.textContent='+'+(count-MAX_VIS);
      stack.appendChild(pill);
    }
    return stack;
  };

  const renderRow=(start,end)=>{
    const row=document.createElement('div');
    row.className='bg-row';
    const isTop = start>=12;
    let col=0;
    for(let i=start;i!==end;i+=end>start?1:-1){
      const idx=flip?23-i:i;
      const pt=document.createElement('div');
      // Alternate the two classic triangle colours, offset between the top and
      // bottom rows so the points interlock in a zig-zag like a real board.
      const dark = ((col + (isTop?0:1)) % 2) === 1;
      pt.className='bg-point'+(isTop?' top':'')+(dark? ' alt':'');
      const inner=document.createElement('div');
      inner.className='bg-point-inner';
      const whiteCount = board[idx] > 0 ? board[idx] : 0;
      const blackCount = (st.variant === 'long' && idx === 23)
        ? (st.head_black || 0)
        : (board[idx] < 0 ? -board[idx] : 0);
      const twoColors = whiteCount>0 && blackCount>0;
      if(twoColors){
        // Long narde head: both colours share the point — show two columns.
        inner.classList.add('bg-point-split');
        if(isTop) inner.classList.add('top');
        inner.appendChild(makeStack(whiteCount, 1, idx, isTop));
        inner.appendChild(makeStack(blackCount, -1, idx, isTop));
      } else if(whiteCount>0){
        inner.appendChild(makeStack(whiteCount, 1, idx, isTop));
      } else if(blackCount>0){
        inner.appendChild(makeStack(blackCount, -1, idx, isTop));
      }
      pt.appendChild(inner);
      // Select a source by tapping anywhere on a movable point.
      if(myTurn && bgSelected===null && moveMap[idx]){
        pt.style.cursor='pointer';
        const sel=document.createElement('div');
        sel.style.cssText='position:absolute;inset:0;z-index:1';
        sel.onclick=(e)=>{e.stopPropagation();bgSelectSource(idx);};
        pt.appendChild(sel);
      }
      // Tap a destination point to move there.
      if(myTurn && bgSelected!==null && bgSelected!==idx && moveMap[bgSelected] && moveMap[bgSelected].has(idx)){
        pt.classList.add('bg-target');
        pt.style.cursor='pointer';
        const hitArea=document.createElement('div');
        hitArea.style.cssText='position:absolute;inset:0;z-index:2';
        hitArea.onclick=(e)=>{e.stopPropagation();bgDoMove(bgSelected,idx);};
        pt.appendChild(hitArea);
      }
      row.appendChild(pt);
      col++;
    }
    return row;
  };

  // Left half: top points 12-17, bottom points 11-6
  const leftHalf=document.createElement('div');
  leftHalf.className='bg-half';
  leftHalf.appendChild(renderRow(12,18));
  leftHalf.appendChild(renderRow(11,5));

  // Center bar
  const barCol=document.createElement('div');
  barCol.className='bg-bar-v';
  if(bar[0]>0||bar[1]>0){
    barCol.innerHTML=`<div class="bg-bar-label">BAR</div>`;
    for(let j=0;j<bar[0];j++){
      const ch=document.createElement('div');
      ch.className='bg-checker white';
      if(myTurn && bgSelected===null && moveMap[-1]) ch.style.cursor='pointer';
      if(myTurn && bgSelected===null && moveMap[-1]) ch.onclick=()=>bgSelectSource(-1);
      barCol.appendChild(ch);
    }
    for(let j=0;j<bar[1];j++){
      const ch=document.createElement('div');
      ch.className='bg-checker black';
      barCol.appendChild(ch);
    }
  }

  // Right half: top points 18-23, bottom points 5-0
  const rightHalf=document.createElement('div');
  rightHalf.className='bg-half';
  rightHalf.appendChild(renderRow(18,24));
  rightHalf.appendChild(renderRow(5,-1));

  // Off (bear-off) column on the right
  const offCol=document.createElement('div');
  offCol.className='bg-off-col';
  if(off[0]>0||off[1]>0){
    offCol.innerHTML=`<div>⬜ ${off[0]}</div><div>⬛ ${off[1]}</div>`;
  }
  if(bgSelected!==null && moveMap[bgSelected] && moveMap[bgSelected].has(-1)){
    offCol.classList.add('bg-target');
    offCol.style.cursor='pointer';
    offCol.onclick=(e)=>{e.stopPropagation();bgDoMove(bgSelected,-1);};
  }

  wrap.appendChild(leftHalf);
  wrap.appendChild(barCol);
  wrap.appendChild(rightHalf);
  wrap.appendChild(offCol);

  cont.innerHTML='';
  cont.appendChild(wrap);
  cont.onclick=()=>{
    if(bgSelected!==null){
      bgSelected=null;
      bgMoveTargets=[];
      bgShowGame(bgState);
      setStatus({ru:'Нажми на шашку',uk:'Натисни на шашку',en:'Tap a checker to move'}[lang],'battle');
    }
  };
}

function bgRenderDice(st){
  const cont=$('bgActions');
  const dice=st.dice||[];
  if(!dice.length){
    if(st.my_turn && st.phase==='playing' && (st.solo || st.opponent_joined)){
      const rollBtn=document.createElement('button');
      rollBtn.className='btn success';
      rollBtn.style.cssText='width:100%;margin:8px 0';
      rollBtn.textContent='🎲 '+t('bgRoll');
      rollBtn.onclick=()=>bgDoRoll();
      cont.appendChild(rollBtn);
    }
    return;
  }
  if(!st.my_turn) return;
  const diceDiv=document.createElement('div');
  diceDiv.className='bg-dice';
  const used=st.used_dice||0;
  for(let i=0;i<dice.length;i++){
    const die=document.createElement('div');
    die.className='bg-die'+(i<used?' used':'');
    die.textContent=dice[i];
    diceDiv.appendChild(die);
  }
  cont.appendChild(diceDiv);
  if(st.my_turn && bgSelected===null){
    const moveHint=document.createElement('div');
    moveHint.className='bg-info';
    const noMoves = !st.legal_moves || !st.legal_moves.length;
    if(noMoves){
      moveHint.textContent={ru:'Нет доступных ходов',uk:'Немає доступних ходів',en:'No moves available'}[lang];
      const passBtn=document.createElement('button');
      passBtn.className='btn outline';
      passBtn.textContent='⏭ '+{ru:'Пропустить',uk:'Пропустити',en:'Pass'}[lang];
      passBtn.onclick=()=>bgPassTurn();
      cont.appendChild(passBtn);
    } else {
      moveHint.textContent={ru:'Нажми на шашку',uk:'Натисни на шашку',en:'Tap a checker to move'}[lang];
    }
    cont.appendChild(moveHint);
  }
}

function bgRenderActions(st){
  const el=$('bgActions');
  el.className='btn-col';
  let html='';
  if(st.phase==='playing' && !st.solo && !st.opponent_joined){
    setStatus({ru:'🔄 Ожидание друга...',uk:'🔄 Очікування друга...',en:'🔄 Waiting for opponent...'}[lang],'');
  }else if(st.my_turn && st.phase==='playing'){
    setStatus(t('bgYourTurn'),'battle');
    const inviteBtn=st.solo||st.opponent_joined?'':`<button class="btn primary" onclick="shareBgGame()">📤 ${t('inviteFriend')}</button>`;
    if(inviteBtn) html+=`<div class="btn-row">${inviteBtn}</div>`;
  }else if(st.phase==='playing'){
    setStatus(t('bgOppTurn'),'');
  }
  if(!st.solo && st.phase==='playing'){
    html+=`<div class="btn-row" style="margin-top:8px">
      <button class="btn outline" onclick="sendOpponentMessage('backgammon',bgCode,bgState)">${t('message')}</button>
      <button class="btn outline" onclick="leaveBgGame()">${t('minimize')}</button>
    </div>
    <button class="btn danger" onclick="bgSurrender()">${t('surrender')}</button>`;
  }else if(st.phase==='playing'){
    html+=`<div class="btn-row" style="margin-top:8px">
      <button class="btn danger" onclick="bgSurrender()">${t('surrender')}</button>
      <button class="btn outline" onclick="leaveBgGame()">${t('minimize')}</button>
    </div>`;
  }
  el.insertAdjacentHTML('beforeend', html);
}

async function bgDoRoll(){
  sfxRoll();
  const res=await api('/api/bg_roll',{uid:getUid(),code:bgCode});
  if(!res||!res.ok){setStatus(t('error'));return}
  bgShowGame(res.state);
}

async function bgSelectSource(idx){
  if(bgSelected===idx){
    bgSelected=null;
    bgMoveTargets=[];
    bgShowGame(bgState);
    setStatus({ru:'Нажми на шашку',uk:'Натисни на шашку',en:'Tap a checker to move'}[lang],'battle');
    return;
  }
  bgSelected=idx;
  bgMoveTargets=[];
  if(bgState && bgState.legal_moves){
    for(const seq of bgState.legal_moves){
      for(const m of seq){
        if(m[0]===idx && !bgMoveTargets.includes(m[1])) bgMoveTargets.push(m[1]);
      }
    }
  }
  // Re-render with visual feedback, preserving the current selection
  bgShowGame(bgState, true);
  setStatus('🎯 '+(bgMoveTargets.length ? {ru:'Выбери пункт назначения',uk:'Обери пункт призначення',en:'Choose destination'}[lang] : {ru:'Нет ходов этой шашкой',uk:'Немає ходів цією шашкою',en:'No moves for this checker'}[lang]),'battle');
}

async function bgDoMove(from,to){
  bgSelected=null;
  const res=await api('/api/bg_move',{uid:getUid(),code:bgCode,from,to:to>=0?to:null});
  if(!res||!res.ok){setStatus(t('error'));return}
  sfxHit();
  // Render your own move immediately -- the AI's turn (roll + all die moves)
  // is now a separate follow-up step (see bgRunBotTurn), triggered right
  // after this paints, instead of being computed synchronously here.
  bgShowGame(res.state);
  if(res.needs_bot_turn) await bgRunBotTurn();
}

async function bgRunBotTurn(){
  if(!bgCode) return;
  await _aiDelay(250);
  const res = await api('/api/bg_bot_turn', {uid:getUid(), code:bgCode});
  if(!res || !res.ok) return;
  if(!bgCode) return;
  bgShowGame(res.state);
}

async function bgPassTurn(){
  const res=await api('/api/bg_move',{uid:getUid(),code:bgCode,from:-1,to:-1});
  if(!res||!res.ok){setStatus(t('error'));return}
  bgSelected=null;
  bgShowGame(res.state);
  if(res.needs_bot_turn) await bgRunBotTurn();
}

function leaveBgGame(){
  if(bgPollTimer){clearInterval(bgPollTimer);bgPollTimer=null}
  bgCode=null; bgState=null;
  $('bgArea').style.display='none';
  showMainMenu();
}

function shareBgGame(){
  if(!bgCode)return;
  copyToClipboard(bgCode,{ru:'Код скопирован ✅',uk:'Код скопійовано ✅',en:'Code copied ✅'}[lang]);
  try{Telegram.WebApp.openTelegramLink(`https://t.me/share/url?url=${encodeURIComponent(bgCode)}`)}catch(e){}
}

async function bgSurrender(){
  var msg = {ru:'Сдаться? Игра будет завершена.',uk:'Здатися? Гра буде завершена.',en:'Surrender? The game will end.'}[lang];
  if(!confirm(msg)) return;
  if(bgPollTimer){clearInterval(bgPollTimer);bgPollTimer=null}
  const code = bgCode;
  bgCode=null;bgState=null;
  $('bgArea').style.display='none';
  localStorage.removeItem('bg_game');
  await api('/api/bg_surrender',{uid:getUid(),code});
  showMainMenu();
}

function resumeBg(code){
  bgCode=code;
  localStorage.setItem('bg_game',code);
  $('actions').innerHTML='';
  bgRefreshState();
  bgPoll();
}
