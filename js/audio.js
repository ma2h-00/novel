/* =========================================================
   audio.js
   外部音源を使わずに、Web Audio API でその場で
   サウンドノベル風の SFX / アンビエント BGM を生成する。
   ========================================================= */

const Audio = (() => {
  let ctx = null;
  let masterGain = null;
  let bgmNodes = [];
  let bgmId = null;
  let muted = false;

  function ensure() {
    if (ctx) return;
    const AC = window.AudioContext || window.webkitAudioContext;
    if (!AC) return;
    ctx = new AC();
    masterGain = ctx.createGain();
    masterGain.gain.value = 0.7;
    masterGain.connect(ctx.destination);
  }

  function resume() {
    ensure();
    if (ctx && ctx.state === 'suspended') ctx.resume();
  }

  function setMuted(v) {
    muted = v;
    if (masterGain) masterGain.gain.value = v ? 0 : 0.7;
  }

  /* ---------- SFX ---------- */
  function blip() {
    ensure(); if (!ctx) return;
    const o = ctx.createOscillator();
    const g = ctx.createGain();
    o.type = 'sine';
    o.frequency.value = 1100;
    o.frequency.linearRampToValueAtTime(1500, ctx.currentTime + 0.05);
    g.gain.value = 0.0001;
    g.gain.exponentialRampToValueAtTime(0.12, ctx.currentTime + 0.005);
    g.gain.exponentialRampToValueAtTime(0.0001, ctx.currentTime + 0.12);
    o.connect(g).connect(masterGain);
    o.start();
    o.stop(ctx.currentTime + 0.13);
  }

  function click() {
    ensure(); if (!ctx) return;
    const o = ctx.createOscillator();
    const g = ctx.createGain();
    o.type = 'square';
    o.frequency.value = 720;
    g.gain.value = 0.0001;
    g.gain.exponentialRampToValueAtTime(0.06, ctx.currentTime + 0.002);
    g.gain.exponentialRampToValueAtTime(0.0001, ctx.currentTime + 0.05);
    o.connect(g).connect(masterGain);
    o.start();
    o.stop(ctx.currentTime + 0.06);
  }

  function sting() {
    // 「ジャン!!」 ── 緊張シーン用
    ensure(); if (!ctx) return;
    const now = ctx.currentTime;
    const o1 = ctx.createOscillator();
    const o2 = ctx.createOscillator();
    const g  = ctx.createGain();
    o1.type = 'sawtooth';
    o2.type = 'sawtooth';
    o1.frequency.value = 90;
    o2.frequency.value = 90 * 1.012;  // beat
    g.gain.value = 0.0001;
    g.gain.exponentialRampToValueAtTime(0.45, now + 0.01);
    g.gain.exponentialRampToValueAtTime(0.0001, now + 1.2);
    o1.connect(g);
    o2.connect(g);
    g.connect(masterGain);
    o1.start(now); o2.start(now);
    o1.stop(now + 1.25); o2.stop(now + 1.25);
  }

  function shock() {
    // 「ドン!!」 ── 死体発見、襲撃
    ensure(); if (!ctx) return;
    const now = ctx.currentTime;
    // ノイズ
    const buf = ctx.createBuffer(1, ctx.sampleRate * 0.6, ctx.sampleRate);
    const d = buf.getChannelData(0);
    for (let i = 0; i < d.length; i++) {
      d[i] = (Math.random() * 2 - 1) * Math.pow(1 - i / d.length, 2);
    }
    const noise = ctx.createBufferSource();
    noise.buffer = buf;
    const ng = ctx.createGain();
    ng.gain.value = 0.5;
    noise.connect(ng).connect(masterGain);
    noise.start(now);

    // 低音ドン
    const o = ctx.createOscillator();
    const g = ctx.createGain();
    o.type = 'sine';
    o.frequency.value = 60;
    o.frequency.exponentialRampToValueAtTime(28, now + 0.5);
    g.gain.value = 0.0001;
    g.gain.exponentialRampToValueAtTime(0.6, now + 0.005);
    g.gain.exponentialRampToValueAtTime(0.0001, now + 0.7);
    o.connect(g).connect(masterGain);
    o.start(now); o.stop(now + 0.75);
  }

  function heartbeat() {
    ensure(); if (!ctx) return;
    const now = ctx.currentTime;
    [0, 0.25].forEach((t) => {
      const o = ctx.createOscillator();
      const g = ctx.createGain();
      o.type = 'sine';
      o.frequency.value = 70;
      g.gain.value = 0.0001;
      g.gain.exponentialRampToValueAtTime(0.4, now + t + 0.005);
      g.gain.exponentialRampToValueAtTime(0.0001, now + t + 0.18);
      o.connect(g).connect(masterGain);
      o.start(now + t); o.stop(now + t + 0.2);
    });
  }

  function paper() {
    // 紙をめくる音っぽいノイズ
    ensure(); if (!ctx) return;
    const now = ctx.currentTime;
    const buf = ctx.createBuffer(1, ctx.sampleRate * 0.25, ctx.sampleRate);
    const d = buf.getChannelData(0);
    for (let i = 0; i < d.length; i++) d[i] = (Math.random() * 2 - 1);
    const noise = ctx.createBufferSource();
    noise.buffer = buf;
    const filt = ctx.createBiquadFilter();
    filt.type = 'highpass';
    filt.frequency.value = 3500;
    const g = ctx.createGain();
    g.gain.value = 0.0001;
    g.gain.exponentialRampToValueAtTime(0.18, now + 0.02);
    g.gain.exponentialRampToValueAtTime(0.0001, now + 0.22);
    noise.connect(filt).connect(g).connect(masterGain);
    noise.start(now);
  }

  function chime() {
    ensure(); if (!ctx) return;
    const now = ctx.currentTime;
    [880, 1320, 1760].forEach((f, i) => {
      const o = ctx.createOscillator();
      const g = ctx.createGain();
      o.type = 'sine';
      o.frequency.value = f;
      g.gain.value = 0.0001;
      g.gain.exponentialRampToValueAtTime(0.15, now + 0.02 + i * 0.08);
      g.gain.exponentialRampToValueAtTime(0.0001, now + 0.08 + i * 0.08 + 0.7);
      o.connect(g).connect(masterGain);
      o.start(now + i * 0.08); o.stop(now + 0.9 + i * 0.08);
    });
  }

  /* ---------- BGM (アンビエント・ループ) ---------- */
  function stopBgm(fade = 1.0) {
    if (!ctx || !bgmNodes.length) { bgmNodes = []; bgmId = null; return; }
    const now = ctx.currentTime;
    bgmNodes.forEach((n) => {
      if (n.gain) {
        try {
          n.gain.gain.cancelScheduledValues(now);
          n.gain.gain.setValueAtTime(n.gain.gain.value, now);
          n.gain.gain.exponentialRampToValueAtTime(0.0001, now + fade);
        } catch (e) {}
      }
    });
    const oldNodes = bgmNodes;
    setTimeout(() => {
      oldNodes.forEach((n) => {
        try { n.osc && n.osc.stop(); } catch (e) {}
        try { n.lfo && n.lfo.stop(); } catch (e) {}
      });
    }, fade * 1000 + 100);
    bgmNodes = [];
    bgmId = null;
  }

  function startBgm(id) {
    ensure(); if (!ctx) return;
    if (bgmId === id) return;
    stopBgm(0.6);
    bgmId = id;

    const now = ctx.currentTime + 0.05;
    const presets = {
      ambient_office: [
        { freq: 55,  type: 'sine',     gain: 0.06,  detune: 0 },
        { freq: 82,  type: 'sine',     gain: 0.04,  detune: -3 },
        { freq: 110, type: 'sine',     gain: 0.02,  detune: 5 },
      ],
      tense: [
        { freq: 45,  type: 'sawtooth', gain: 0.05,  detune: 0,   filter: 250 },
        { freq: 67,  type: 'sawtooth', gain: 0.04,  detune: 7,   filter: 220 },
        { freq: 90,  type: 'sine',     gain: 0.025, detune: 0 },
      ],
      mystery: [
        { freq: 110, type: 'sine',     gain: 0.04,  detune: 0 },
        { freq: 138, type: 'sine',     gain: 0.03,  detune: 5 },
        { freq: 73,  type: 'triangle', gain: 0.04,  detune: -7 },
      ],
      dread: [
        { freq: 33,  type: 'sawtooth', gain: 0.06,  detune: 0,   filter: 180 },
        { freq: 49,  type: 'sawtooth', gain: 0.05,  detune: 3,   filter: 160 },
      ],
      sad: [
        { freq: 196, type: 'sine',     gain: 0.05,  detune: 0 },
        { freq: 233, type: 'sine',     gain: 0.04,  detune: -4 },
        { freq: 98,  type: 'triangle', gain: 0.04,  detune: 0 },
      ],
      hope: [
        { freq: 261, type: 'sine',     gain: 0.04,  detune: 0 },
        { freq: 329, type: 'sine',     gain: 0.04,  detune: 0 },
        { freq: 392, type: 'sine',     gain: 0.03,  detune: 0 },
      ],
      finale: [
        { freq: 55,  type: 'sawtooth', gain: 0.06,  detune: 0,   filter: 280 },
        { freq: 82,  type: 'sawtooth', gain: 0.05,  detune: 7,   filter: 240 },
        { freq: 110, type: 'sine',     gain: 0.04,  detune: 0 },
        { freq: 165, type: 'sine',     gain: 0.025, detune: 0 },
      ],
    };
    const preset = presets[id];
    if (!preset) return;

    preset.forEach((p) => {
      const o = ctx.createOscillator();
      const g = ctx.createGain();
      o.type = p.type;
      o.frequency.value = p.freq;
      o.detune.value = p.detune;
      g.gain.value = 0.0001;
      g.gain.exponentialRampToValueAtTime(p.gain, now + 1.5);
      let last = g;
      if (p.filter) {
        const f = ctx.createBiquadFilter();
        f.type = 'lowpass';
        f.frequency.value = p.filter;
        o.connect(f); f.connect(g);
      } else {
        o.connect(g);
      }
      // LFO で微妙な揺らぎ
      const lfo = ctx.createOscillator();
      const lfoGain = ctx.createGain();
      lfo.frequency.value = 0.13 + Math.random() * 0.2;
      lfoGain.gain.value = 1.5;
      lfo.connect(lfoGain);
      lfoGain.connect(o.detune);
      lfo.start(now);
      g.connect(masterGain);
      o.start(now);
      bgmNodes.push({ osc: o, gain: g, lfo });
    });
  }

  return {
    resume,
    setMuted,
    sfx: { blip, click, sting, shock, heartbeat, paper, chime },
    startBgm,
    stopBgm,
  };
})();
