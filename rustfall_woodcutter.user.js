// ==UserScript==
// @name         Rustfall – Otomatik Ağaç Kesici v3
// @namespace    http://tampermonkey.net/
// @version      3.0
// @description  Colyseus state hook ile ağaç otomasyonu
// @author       Antigravity
// @match        https://rustfall.world/*
// @match        https://*.rustfall.world/*
// @grant        none
// @run-at       document-start
// ==/UserScript==

(function () {
  'use strict';

  console.log('%c[🪓 WoodBot v3] Script yüklendi!', 'color:#69f0ae;font-weight:bold;font-size:14px');

  // ─────────────────────────────────────────
  //  CONFIG
  // ─────────────────────────────────────────
  const CFG = {
    clickInterval: 2000,   // Tıklamalar arası ms
    scanInterval:  500,    // State tarama sıklığı
  };

  let running   = false;
  let timer     = null;
  let scanTimer = null;
  let clickCount = 0;
  let gameRoom  = null;    // Colyseus room referansı
  let gameState = null;    // Colyseus room.state
  let panel, statusEl, countEl, infoEl;

  // ─────────────────────────────────────────
  //  PANEL
  // ─────────────────────────────────────────
  function buildPanel() {
    if (document.getElementById('rf-v3-panel')) return;

    panel = document.createElement('div');
    panel.id = 'rf-v3-panel';
    panel.style.cssText = [
      'position:fixed', 'top:10px', 'right:10px',
      'z-index:2147483647',
      'background:rgba(5,10,5,0.95)',
      'border:2px solid #4caf50',
      'border-radius:12px',
      'padding:12px 15px',
      'font-family:monospace',
      'font-size:12px',
      'color:#c8e6c9',
      'min-width:220px',
      'box-shadow:0 0 30px rgba(76,175,80,0.6)',
      'user-select:none',
      'pointer-events:all',
    ].join(';');

    panel.innerHTML = `
<div style="font-size:14px;font-weight:bold;color:#69f0ae;margin-bottom:8px;border-bottom:1px solid #1b5e20;padding-bottom:6px">
  🪓 WoodBot v3
</div>
<div id="rfv3-status"  style="color:#aed581;margin-bottom:4px">⏸ Bekliyor</div>
<div id="rfv3-count"   style="color:#558b2f;margin-bottom:4px">Kesilen: 0</div>
<div id="rfv3-info"    style="color:#555;font-size:10px;margin-bottom:10px">State: taranıyor...</div>
<div style="display:flex;gap:8px;margin-bottom:8px">
  <button id="rfv3-start" style="flex:1;padding:6px;background:#2e7d32;border:none;border-radius:6px;color:#fff;cursor:pointer;font-weight:bold;font-family:monospace">▶ BAŞLAT</button>
  <button id="rfv3-stop"  style="flex:1;padding:6px;background:#b71c1c;border:none;border-radius:6px;color:#fff;cursor:pointer;font-family:monospace">■ DUR</button>
</div>
<div style="font-size:10px;color:#37474f;line-height:1.6">
  <b style="color:#2e7d32">Alt+W</b> Başlat/Durdur<br>
  Karakter ağaçların yanında olsun!
</div>
    `.trim();

    document.body.appendChild(panel);
    statusEl = document.getElementById('rfv3-status');
    countEl  = document.getElementById('rfv3-count');
    infoEl   = document.getElementById('rfv3-info');

    document.getElementById('rfv3-start').onclick = startBot;
    document.getElementById('rfv3-stop').onclick  = stopBot;

    // Sürükleme
    let drag = false, ox = 0, oy = 0;
    panel.addEventListener('mousedown', e => {
      if (e.target.tagName === 'BUTTON') return;
      drag = true;
      const r = panel.getBoundingClientRect();
      ox = e.clientX - r.left; oy = e.clientY - r.top;
    });
    document.addEventListener('mousemove', e => {
      if (!drag) return;
      panel.style.left  = (e.clientX - ox) + 'px';
      panel.style.top   = (e.clientY - oy) + 'px';
      panel.style.right = 'auto';
    });
    document.addEventListener('mouseup', () => { drag = false; });

    console.log('[🪓 WoodBot v3] Panel oluşturuldu ✓');
  }

  const setStatus = (msg, col = '#aed581') => {
    if (statusEl) { statusEl.textContent = msg; statusEl.style.color = col; }
    console.log('[🪓 WoodBot v3]', msg);
  };

  // ─────────────────────────────────────────
  //  COLYSEUS HOOKİ
  //  Colyseus Client'ı yakalayıp room.joinOrCreate
  //  ve room.join metodlarını hook'luyoruz
  // ─────────────────────────────────────────
  function hookColyseus() {
    // window üzerinde Colyseus client'ı ara
    const scanWindow = () => {
      // Tüm window property'leri tara
      for (const key of Object.keys(window)) {
        try {
          const val = window[key];
          if (!val || typeof val !== 'object') continue;

          // Colyseus client mi?
          if (typeof val.joinOrCreate === 'function' || typeof val.join === 'function') {
            console.log('[🪓 WoodBot v3] Colyseus client bulundu! Key:', key, val);
            if (infoEl) infoEl.textContent = `Colyseus: ${key} ✓`;
            hookColyseusClient(val);
            return true;
          }

          // Room nesnesi mi?
          if (val.state && typeof val.send === 'function') {
            console.log('[🪓 WoodBot v3] Colyseus Room bulundu! Key:', key);
            setRoom(val);
            return true;
          }
        } catch(e) {}
      }
      return false;
    };

    if (!scanWindow()) {
      let attempts = 0;
      const t = setInterval(() => {
        attempts++;
        if (scanWindow() || attempts > 60) clearInterval(t);
      }, 1000);
    }
  }

  function hookColyseusClient(client) {
    const origJoin = client.joinOrCreate || client.join;
    const methods  = ['joinOrCreate', 'join', 'reconnect', 'joinById'];

    methods.forEach(m => {
      if (typeof client[m] !== 'function') return;
      const original = client[m].bind(client);
      client[m] = async function(...args) {
        const room = await original(...args);
        console.log('[🪓 WoodBot v3] Room yakalandı:', m, room);
        setRoom(room);
        return room;
      };
    });
  }

  function setRoom(room) {
    gameRoom  = room;
    gameState = room.state;
    console.log('[🪓 WoodBot v3] Game state:', gameState);
    console.log('[🪓 WoodBot v3] State keys:', gameState ? Object.keys(gameState) : 'null');

    if (infoEl) {
      const keys = gameState ? Object.keys(gameState).join(', ') : 'yok';
      infoEl.textContent = `State: ${keys.slice(0,40)}`;
    }
  }

  // ─────────────────────────────────────────
  //  CANVAS TIKLAMA (3 farklı yöntem)
  // ─────────────────────────────────────────
  function getCanvas() {
    const all = [...document.querySelectorAll('canvas')];
    return all.sort((a, b) => b.width * b.height - a.width * a.height)[0] || null;
  }

  function sendClick(x, y) {
    // x, y = ekran koordinatları (clientX/clientY)
    const canvas = getCanvas();
    if (!canvas) return false;

    const target = document.elementFromPoint(x, y) || canvas;
    const opts = {
      bubbles: true, cancelable: true, view: window,
      clientX: x, clientY: y,
      screenX: x + window.screenX, screenY: y + window.screenY,
      button: 0, buttons: 1,
    };

    ['pointerdown','mousedown','pointerup','mouseup','click'].forEach(type => {
      target.dispatchEvent(new MouseEvent(type, {
        ...opts,
        buttons: type.includes('down') ? 1 : 0,
      }));
    });

    console.log('[🪓 WoodBot v3] Tıklandı →', x, y);
    return true;
  }

  // ─────────────────────────────────────────
  //  GAME STATE'DEN AĞAÇ BULMA
  // ─────────────────────────────────────────
  function findTreesInState() {
    if (!gameState) return [];

    const trees = [];
    const scan = (obj, depth = 0) => {
      if (depth > 4 || !obj || typeof obj !== 'object') return;
      for (const key of Object.keys(obj)) {
        try {
          const val = obj[key];
          const keyL = key.toLowerCase();
          // Ağaç / kaynak objeleri genelde "tree", "resource", "entity" vb.
          if (keyL.includes('tree') || keyL.includes('wood') || keyL.includes('resource')) {
            console.log('[🪓 WoodBot v3] Ağaç kaynağı bulundu:', key, val);
            if (val && typeof val === 'object') {
              // Map/Array ise her elemanı ekle
              if (typeof val.forEach === 'function') {
                val.forEach(item => { if (item && item.x !== undefined) trees.push(item); });
              } else if (val.x !== undefined) {
                trees.push(val);
              }
            }
          }
          if (typeof val === 'object' && val !== null) scan(val, depth + 1);
        } catch(e) {}
      }
    };

    scan(gameState);
    return trees;
  }

  // ─────────────────────────────────────────
  //  OYUN KOORDİNATI → EKRAN KOORDİNATI
  // ─────────────────────────────────────────
  function worldToScreen(worldX, worldY) {
    // Three.js kamera ile projeksiyon yapmamız lazım
    // Önce deneme: pencere ortası + offset
    const canvas = getCanvas();
    if (!canvas) return null;
    const rect = canvas.getBoundingClientRect();

    // Eğer oyun Three.js kullanıyorsa kamera matrisine ihtiyacımız var
    // Bunu window.game veya benzeri global'dan almaya çalışıyoruz
    const camera = findThreeCamera();
    if (camera) {
      // Three.js Vector3 ile projeksiyon
      try {
        const THREE = findThree();
        if (THREE) {
          const vec = new THREE.Vector3(worldX, 0, worldY);
          vec.project(camera);
          const sx = (vec.x  + 1) / 2 * rect.width  + rect.left;
          const sy = (-vec.y + 1) / 2 * rect.height + rect.top;
          return { x: sx, y: sy };
        }
      } catch(e) {}
    }

    // Fallback: canvas merkezi kullan
    return { x: rect.left + rect.width / 2, y: rect.top + rect.height / 2 };
  }

  function findThree() {
    for (const k of Object.keys(window)) {
      try {
        const v = window[k];
        if (v && v.WebGLRenderer && v.PerspectiveCamera) return v;
      } catch(e) {}
    }
    return null;
  }

  function findThreeCamera() {
    for (const k of Object.keys(window)) {
      try {
        const v = window[k];
        if (!v || typeof v !== 'object') continue;
        if (v.isPerspectiveCamera || v.isOrthographicCamera) return v;
        // Nested
        for (const k2 of Object.keys(v)) {
          const v2 = v[k2];
          if (v2 && (v2.isPerspectiveCamera || v2.isOrthographicCamera)) return v2;
        }
      } catch(e) {}
    }
    return null;
  }

  // ─────────────────────────────────────────
  //  COLYSEUS MESAJ GÖNDERME (en temiz yol!)
  // ─────────────────────────────────────────
  function sendGameMessage(type, data) {
    if (!gameRoom) return false;
    try {
      gameRoom.send(type, data);
      console.log('[🪓 WoodBot v3] Mesaj gönderildi:', type, data);
      return true;
    } catch(e) {
      console.log('[🪓 WoodBot v3] Mesaj hatası:', e);
      return false;
    }
  }

  // ─────────────────────────────────────────
  //  GRID TIKLA (state yoksa fallback)
  //  Ekranı grid'e böl, sırayla her karenin
  //  ortasına tıkla (ağaçlar orada olabilir)
  // ─────────────────────────────────────────
  const gridPositions = [];
  let gridIdx = 0;

  function buildGrid() {
    const canvas = getCanvas();
    if (!canvas) return;
    const rect = canvas.getBoundingClientRect();
    gridPositions.length = 0;

    // Merkezi etrafında bir çember oluştur
    const cx = rect.left + rect.width  * 0.5;
    const cy = rect.top  + rect.height * 0.52;

    // 12 nokta, 3 farklı yarıçap
    const radii = [80, 150, 220];
    radii.forEach(r => {
      for (let a = 0; a < 360; a += 30) {
        const rad = (a * Math.PI) / 180;
        gridPositions.push({
          x: cx + Math.cos(rad) * r,
          y: cy + Math.sin(rad) * r,
        });
      }
    });

    console.log('[🪓 WoodBot v3] Grid hazırlandı:', gridPositions.length, 'nokta');
  }

  // ─────────────────────────────────────────
  //  ANA BOT DÖNGÜSÜ
  // ─────────────────────────────────────────
  function botTick() {
    if (!running) return;

    // Önce Colyseus message dene
    const trees = findTreesInState();
    if (trees.length > 0) {
      const tree = trees[0];
      console.log('[🪓 WoodBot v3] Ağaç bulundu state\'de:', tree);

      // Önce game message ile dene
      const sent = sendGameMessage('interact', { id: tree.id || tree.entityId })
               || sendGameMessage('chop',     { id: tree.id || tree.entityId })
               || sendGameMessage('action',   { target: tree.id, type: 'chop' });

      if (!sent) {
        // Ekran koordinatına çevir ve tıkla
        const screen = worldToScreen(tree.x, tree.y);
        if (screen) sendClick(screen.x, screen.y);
      }
    } else {
      // Fallback: grid tıklama
      if (gridPositions.length === 0) buildGrid();
      if (gridPositions.length > 0) {
        const pos = gridPositions[gridIdx % gridPositions.length];
        gridIdx++;
        sendClick(pos.x, pos.y);
        setStatus(`🔄 Grid[${gridIdx}] tıklandı`, '#ffb74d');
      }
    }

    clickCount++;
    if (countEl) countEl.textContent = `Tıklama: ${clickCount}`;

    timer = setTimeout(botTick, CFG.clickInterval);
  }

  // ─────────────────────────────────────────
  //  BAŞLAT / DURDUR
  // ─────────────────────────────────────────
  function startBot() {
    if (running) return;
    running = true;
    buildGrid();
    setStatus('▶ Çalışıyor...', '#69f0ae');
    botTick();
  }

  function stopBot() {
    running = false;
    clearTimeout(timer);
    setStatus('⏸ Durduruldu', '#ef9a9a');
  }

  // ─────────────────────────────────────────
  //  KLAVYE
  // ─────────────────────────────────────────
  document.addEventListener('keydown', e => {
    if (e.altKey && e.key.toLowerCase() === 'w') {
      if (running) stopBot(); else startBot();
    }
    // Alt+I = state dump
    if (e.altKey && e.key.toLowerCase() === 'i') {
      console.log('[🪓 WoodBot v3] === DURUM RAPORU ===');
      console.log('Room:', gameRoom);
      console.log('State:', gameState);
      console.log('State keys:', gameState ? Object.keys(gameState) : 'yok');
      console.log('Trees:', findTreesInState());
      console.log('Canvas:', getCanvas());
      alert('[WoodBot] Konsola bakın! (F12 → Console)');
    }
  });

  // ─────────────────────────────────────────
  //  BAŞLANGIÇ
  // ─────────────────────────────────────────
  function init() {
    console.log('[🪓 WoodBot v3] init() çalıştı ✓');
    buildPanel();
    hookColyseus();
    setStatus('⏸ Hazır — Başlat\'a bas', '#aed581');
  }

  // document-start'ta başlıyoruz, body henüz yok olabilir
  if (document.body) {
    init();
  } else {
    const obs = new MutationObserver(() => {
      if (document.body) { obs.disconnect(); init(); }
    });
    obs.observe(document.documentElement, { childList: true });
  }

})();
