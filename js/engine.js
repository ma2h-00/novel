/* =========================================================
   engine.js
   サウンドノベル風アドベンチャーのコアエンジン
   ========================================================= */

(() => {
  'use strict';

  /* ---------- DOM参照 ---------- */
  const $ = (sel) => document.querySelector(sel);
  const titleScreen = $('#title-screen');
  const gameScreen  = $('#game-screen');
  const aboutScreen = $('#about-screen');
  const bgLayer     = $('#bg-layer');
  const bgOverlay   = $('#bg-overlay');
  const textbox     = $('#textbox');
  const namebox     = $('#namebox');
  const textbody    = $('#textbody');
  const nextMarker  = $('#next-marker');
  const choicePane  = $('#choice-pane');
  const chapterBanner = $('#chapter-banner');
  const modal       = $('#modal');
  const modalTitle  = $('#modal-title');
  const modalBody   = $('#modal-body');

  /* ---------- ゲーム状態 ---------- */
  const initialState = () => ({
    sceneId: 'start',
    eventIndex: 0,
    evidence: [],            // 取得済み証拠 ID
    flags: {},               // 任意フラグ
    trust: {                 // -3 〜 +3
      shinohara: 0,
      kuga: 0,
      amamiya: 0,
      shirakawa: 0,
      tachibana: 0,
      kurose: 0,
    },
    chapter: 0,
  });
  let state = initialState();

  /* ---------- 描画ヘルパ ---------- */
  let typeTimer = null;
  let typingActive = false;
  let pendingFinish = null;   // 現在進行中の typewrite() を即時完了する関数
  let waitingForAdvance = false;
  let advanceResolver = null;
  let currentBg = null;

  function setBackground(name) {
    if (!name) return;
    if (currentBg === name) return;
    bgLayer.className = 'bg-layer ' + name;
    currentBg = name;
  }

  function shake() {
    bgLayer.classList.remove('shake');
    void bgLayer.offsetWidth;
    bgLayer.classList.add('shake');
  }

  function flash() {
    const el = document.createElement('div');
    el.className = 'flash';
    gameScreen.appendChild(el);
    setTimeout(() => el.remove(), 600);
  }

  function showChapter(label) {
    return new Promise((resolve) => {
      chapterBanner.textContent = label;
      chapterBanner.classList.add('show');
      setTimeout(() => {
        chapterBanner.classList.remove('show');
        setTimeout(resolve, 700);
      }, 2400);
    });
  }

  function setNameBox(name) {
    namebox.textContent = name || '';
  }

  function showNextMarker(show) {
    if (show) nextMarker.classList.add('show');
    else nextMarker.classList.remove('show');
  }

  /* ---------- タイプライター ---------- */
  function typewrite(text, opts = {}) {
    return new Promise((resolve) => {
      typingActive = true;
      showNextMarker(false);
      textbody.classList.toggle('narration', !!opts.narration);
      textbody.textContent = '';
      let i = 0;
      const speed = opts.fast ? 8 : 28;

      function step() {
        if (!typingActive) return;  // 既に finish 済み
        textbody.textContent = text.slice(0, ++i);
        if (i < text.length) {
          typeTimer = setTimeout(step, speed);
        } else {
          finish();
        }
      }
      function finish() {
        if (!typingActive) return;
        typingActive = false;
        clearTimeout(typeTimer);
        textbody.textContent = text;
        showNextMarker(true);
        pendingFinish = null;
        resolve();
      }
      pendingFinish = finish;
      step();
    });
  }

  function skipTyping() {
    // タイピング中のクリック → 全文表示 + Promise 解決
    if (pendingFinish) pendingFinish();
  }

  /* ---------- ユーザー入力待ち ---------- */
  function waitForAdvance() {
    return new Promise((resolve) => {
      waitingForAdvance = true;
      advanceResolver = () => {
        waitingForAdvance = false;
        advanceResolver = null;
        showNextMarker(false);
        resolve();
      };
    });
  }

  function tryAdvance() {
    if (typingActive) {
      skipTyping();
      return;
    }
    if (waitingForAdvance && advanceResolver) {
      advanceResolver();
    }
  }

  document.addEventListener('keydown', (e) => {
    if (!gameScreen.classList.contains('active')) return;
    if (modal.classList.contains('show')) return;
    if (choicePane.classList.contains('show')) return;
    if (e.key === ' ' || e.key === 'Enter' || e.key === 'ArrowRight') {
      e.preventDefault();
      tryAdvance();
    }
  });
  textbox.addEventListener('click', tryAdvance);

  /* ---------- 証拠 ---------- */
  function addEvidence(id) {
    if (state.evidence.includes(id)) return;
    state.evidence.push(id);
    const def = SCENARIO.evidence[id];
    const el = document.createElement('div');
    el.className = 'evidence-pop';
    el.textContent = '＋ 証拠：' + (def ? def.name : id);
    gameScreen.appendChild(el);
    setTimeout(() => el.remove(), 3300);
    Audio.sfx.chime();
  }

  function hasEvidence(id) {
    return state.evidence.includes(id);
  }

  /* ---------- 信頼度 ---------- */
  function adjustTrust(name, delta) {
    if (state.trust[name] === undefined) return;
    state.trust[name] = Math.max(-3, Math.min(3, state.trust[name] + delta));
  }

  /* ---------- フラグ ---------- */
  function setFlag(k, v = true) { state.flags[k] = v; }
  function flag(k)              { return !!state.flags[k]; }

  /* ---------- 選択肢 ---------- */
  function showChoices(prompt, options) {
    return new Promise((resolve) => {
      choicePane.innerHTML = '';
      if (prompt) {
        const p = document.createElement('div');
        p.className = 'choice-prompt';
        p.textContent = prompt;
        choicePane.appendChild(p);
      }
      options.forEach((opt) => {
        const btn = document.createElement('button');
        btn.className = 'choice-btn';
        btn.textContent = opt.text;
        if (opt.disabled) btn.classList.add('disabled');
        btn.addEventListener('click', () => {
          if (opt.disabled) return;
          Audio.sfx.click();
          choicePane.classList.remove('show');
          resolve(opt);
        });
        choicePane.appendChild(btn);
      });
      choicePane.classList.add('show');
    });
  }

  /* ---------- シーン実行 ---------- */
  let running = false;

  async function run(sceneId) {
    state.sceneId = sceneId;
    state.eventIndex = 0;
    while (true) {
      const scene = SCENARIO.scenes[state.sceneId];
      if (!scene) {
        console.error('Unknown scene:', state.sceneId);
        return;
      }
      const events = scene.events;
      if (state.eventIndex >= events.length) {
        if (scene.next) {
          state.sceneId = scene.next;
          state.eventIndex = 0;
          continue;
        }
        return;
      }
      const ev = events[state.eventIndex++];
      const result = await runEvent(ev);
      if (result && result.jump) {
        state.sceneId = result.jump;
        state.eventIndex = 0;
      }
      if (result && result.stop) return;
    }
  }

  async function runEvent(ev) {
    const t = ev.t;
    switch (t) {
      case 'bg':
        setBackground(ev.v);
        return null;

      case 'bgm':
        if (ev.v === null || ev.v === 'stop') Audio.stopBgm();
        else Audio.startBgm(ev.v);
        return null;

      case 'sfx':
        if (Audio.sfx[ev.v]) Audio.sfx[ev.v]();
        return null;

      case 'shake':
        shake();
        return null;

      case 'flash':
        flash();
        return null;

      case 'chap':
        await showChapter(ev.v);
        return null;

      case 'd':   // 台詞 dialogue
      case 't': {
        setNameBox(ev.n || '');
        await typewrite(ev.v, { fast: ev.fast });
        await waitForAdvance();
        return null;
      }

      case 'n': { // ナレーション
        setNameBox('');
        await typewrite(ev.v, { narration: true, fast: ev.fast });
        await waitForAdvance();
        return null;
      }

      case 'ev':
        addEvidence(ev.v);
        return null;

      case 'set':
        setFlag(ev.k, ev.v === undefined ? true : ev.v);
        return null;

      case 'trust':
        adjustTrust(ev.who, ev.d);
        return null;

      case 'chapter':
        state.chapter = ev.v;
        return null;

      case 'goto':
        return { jump: ev.v };

      case 'if': {
        // 単一条件のみセットすること（後勝ちで上書きされる）
        let ok = false;
        if (ev.flag)        ok = flag(ev.flag) === (ev.eq === undefined ? true : ev.eq);
        if (ev.evidence)    ok = hasEvidence(ev.evidence);
        if (ev.trustGE)     ok = state.trust[ev.trustGE.who] >= ev.trustGE.v;
        if (ev.trustLE)     ok = state.trust[ev.trustLE.who] <= ev.trustLE.v;
        if (ev.allEvidence) ok = ev.allEvidence.every(hasEvidence);
        if (ev.allFlags)    ok = ev.allFlags.every(flag);
        if (ev.someFlags) {
          const c = ev.someFlags.filter(flag).length;
          ok = c >= (ev.min || 1);
        }
        if (ev.evidenceCountGE) ok = state.evidence.length >= ev.evidenceCountGE;
        if (ok) return { jump: ev.then };
        return null;
      }

      case 'choice': {
        const choice = await showChoices(ev.prompt, ev.options);
        if (choice.set) Object.entries(choice.set).forEach(([k, v]) => setFlag(k, v));
        if (choice.trust) Object.entries(choice.trust).forEach(([k, v]) => adjustTrust(k, v));
        if (choice.ev) (Array.isArray(choice.ev) ? choice.ev : [choice.ev]).forEach(addEvidence);
        if (choice.goto) return { jump: choice.goto };
        return null;
      }

      case 'reason': {
        // 推理：与えられた選択肢の中から正解の証拠を選ばせる
        const opts = ev.options.map((o) => ({
          text: o.text + (o.evRequired && !hasEvidence(o.evRequired) ? '　[未取得]' : ''),
          disabled: o.evRequired && !hasEvidence(o.evRequired),
          isCorrect: !!o.correct,
          goto: o.goto,
          set: o.set,
        }));
        const choice = await showChoices(ev.prompt, opts);
        if (choice.set) Object.entries(choice.set).forEach(([k, v]) => setFlag(k, v));
        if (choice.isCorrect) {
          Audio.sfx.chime();
          if (ev.onCorrect) await runEvent(ev.onCorrect);
          if (ev.correctSet) Object.entries(ev.correctSet).forEach(([k, v]) => setFlag(k, v));
          if (ev.correctGoto) return { jump: ev.correctGoto };
        } else {
          Audio.sfx.shock();
          if (ev.onWrong) await runEvent(ev.onWrong);
          if (ev.wrongSet) Object.entries(ev.wrongSet).forEach(([k, v]) => setFlag(k, v));
          if (ev.wrongGoto) return { jump: ev.wrongGoto };
        }
        if (choice.goto) return { jump: choice.goto };
        return null;
      }

      case 'ending':
        await showEnding(ev.v);
        return { stop: true };

      case 'wait':
        await new Promise((r) => setTimeout(r, ev.v || 600));
        return null;
    }
    return null;
  }

  /* ---------- エンディング表示 ---------- */
  async function showEnding(id) {
    const def = SCENARIO.endings[id];
    Audio.stopBgm(2);
    setBackground(def.bg || 'bg-black');
    showNextMarker(false);
    textbox.style.display = 'none';
    const el = document.createElement('div');
    el.className = 'ending-title';
    el.innerHTML =
      `<div class="label">― ENDING ${id} ―</div>` +
      `<div class="name">${def.title}</div>`;
    gameScreen.appendChild(el);
    setTimeout(() => el.classList.add('show'), 50);
    await new Promise((r) => setTimeout(r, 5000));
    el.classList.remove('show');
    await new Promise((r) => setTimeout(r, 1800));
    el.remove();
    textbox.style.display = '';
    // クレジット表示
    setNameBox('');
    await typewrite(def.epilogue || '', { narration: true });
    await waitForAdvance();
    setNameBox('');
    await typewrite(
      'Thank you for playing.\n\n' +
      'レイアウト・オブ・デス ― 白紙の校了日\n' +
      `達成エンディング：${id} 「${def.title}」\n` +
      `収集した証拠：${state.evidence.length} / ${Object.keys(SCENARIO.evidence).length}`,
      { narration: true }
    );
    await waitForAdvance();
    showTitle();
  }

  /* ---------- セーブ / ロード ---------- */
  const SAVE_KEY = 'layout-of-death-save';
  function save() {
    try {
      localStorage.setItem(SAVE_KEY, JSON.stringify(state));
      return true;
    } catch (e) { return false; }
  }
  function loadSave() {
    try {
      const raw = localStorage.getItem(SAVE_KEY);
      if (!raw) return null;
      return JSON.parse(raw);
    } catch (e) { return null; }
  }

  /* ---------- モーダル ---------- */
  function openModal(title, html) {
    modalTitle.textContent = title;
    modalBody.innerHTML = html;
    modal.classList.add('show');
  }
  function closeModal() { modal.classList.remove('show'); }
  $('#modal-close').addEventListener('click', closeModal);
  modal.addEventListener('click', (e) => {
    if (e.target === modal) closeModal();
  });

  $('#btn-evidence').addEventListener('click', () => {
    Audio.sfx.click();
    if (state.evidence.length === 0) {
      openModal('証拠ファイル', '<p class="empty">まだ何も見つけていない。</p>');
      return;
    }
    const html = state.evidence.map((id) => {
      const e = SCENARIO.evidence[id];
      if (!e) return '';
      return `<div class="ev-card">
        <div class="ev-name">${e.name}</div>
        <div class="ev-desc">${e.desc}</div>
      </div>`;
    }).join('');
    openModal('証拠ファイル', html);
  });

  $('#btn-trust').addEventListener('click', () => {
    Audio.sfx.click();
    const labels = {
      shinohara: '篠原 千尋', kuga: '久我 玲司', amamiya: '雨宮 蓮',
      shirakawa: '白河 エリカ', tachibana: '立花 祐介', kurose: '黒瀬 直人',
    };
    const html = Object.entries(state.trust).map(([k, v]) => {
      const pct = ((v + 3) / 6) * 100;
      return `<div class="trust-row">
        <span>${labels[k]}</span>
        <span>
          <span class="trust-bar"><span style="width:${pct}%"></span></span>
        </span>
      </div>`;
    }).join('');
    openModal('人物関係', html);
  });

  $('#btn-save').addEventListener('click', () => {
    Audio.sfx.click();
    if (save()) openModal('セーブ', '<p>進行状況を保存しました。</p>');
    else        openModal('セーブ', '<p>保存に失敗しました。</p>');
  });

  $('#btn-load').addEventListener('click', () => {
    Audio.sfx.click();
    const data = loadSave();
    if (!data) { openModal('ロード', '<p class="empty">セーブデータがありません。</p>'); return; }
    state = data;
    closeModal();
    startGame(state.sceneId);
  });

  $('#btn-title').addEventListener('click', () => {
    Audio.sfx.click();
    showTitle();
  });

  /* ---------- 画面遷移 ---------- */
  function showTitle() {
    Audio.stopBgm(0.6);
    titleScreen.classList.add('active');
    gameScreen.classList.remove('active');
    aboutScreen.classList.remove('active');
    setBackground('bg-black');
    textbox.style.display = '';
    textbody.textContent = '';
    setNameBox('');
  }

  function startGame(sceneId = 'start') {
    Audio.resume();
    titleScreen.classList.remove('active');
    aboutScreen.classList.remove('active');
    gameScreen.classList.add('active');
    state = state || initialState();
    run(sceneId);
  }

  function showAbout() {
    titleScreen.classList.remove('active');
    aboutScreen.classList.add('active');
  }

  /* ---------- タイトル画面のボタン ---------- */
  document.querySelectorAll('[data-action]').forEach((b) => {
    b.addEventListener('click', () => {
      Audio.sfx.click();
      const a = b.dataset.action;
      if (a === 'start') {
        state = initialState();
        startGame('start');
      } else if (a === 'load') {
        const data = loadSave();
        if (!data) {
          alert('セーブデータがありません。');
          return;
        }
        state = data;
        startGame(state.sceneId);
      } else if (a === 'about') {
        showAbout();
      } else if (a === 'back-title') {
        showTitle();
      }
    });
  });

  /* ---------- 初期化 ---------- */
  showTitle();
  // ユーザー初操作で AudioContext を resume
  ['click', 'keydown', 'touchstart'].forEach((evt) =>
    window.addEventListener(evt, () => Audio.resume(), { once: true })
  );

  // デバッグ用にエンジンを公開
  window.__engine = { state: () => state, run, addEvidence, setFlag };
})();
