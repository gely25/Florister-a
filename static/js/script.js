// Atelier Floral - Designer Logic Integrated with Django
// All dynamic data (FLOWERS, SIZE_PRESETS, CSRF_TOKEN) is injected via the template

if (typeof FLOWERS === 'undefined') {
    const BASE = "fotos sin fondo tallos/";
    var FLOWERS = [
        { id: 'l1', name: 'Anémona', type: 'l', p: 15, img: BASE + "cayena/tallos grandes/frente.png", thumb: BASE + "cayena/sin tallo/up.png" },
        { id: 'l2', name: 'Lirio', type: 'l', p: 14, img: BASE + "lirios/tallo grande/frente.png", thumb: BASE + "lirios/sin tallo/up.png" },
        { id: 'l3', name: 'Girasol', type: 'l', p: 12, img: BASE + "girasoles/tallos grandes/frente.png", thumb: BASE + "girasoles/sin tallo/up.png" },
        { id: 'm1', name: 'Cayena', type: 'm', p: 10, img: BASE + "flor estrella/tallo grande/frente.png", thumb: BASE + "flor estrella/sin tallo/up.png" },
        { id: 'm2', name: 'Fantasía', type: 'm', p: 8, img: BASE + "flores de fantasia/tallos grandes/frente.png", thumb: BASE + "flores de fantasia/sin tallo/up.png" },
        { id: 's1', name: 'Tulipán', type: 's', p: 7, img: BASE + "tulipanes/tallos pequeños/frente.png", thumb: BASE + "tulipanes/sin tallo/up.png" },
        { id: 's2', name: 'Flor Copo', type: 's', p: 6, img: BASE + "flor copo/tallo pequeño/frente.png", thumb: BASE + "flor copo/sin tallo/up.png" },
        { id: 's3', name: 'Normal', type: 's', p: 6, img: BASE + "flores normales/tallos pequeños/frente.png", thumb: BASE + "flores normales/sin tallo/up.png" }
    ];
}

if (typeof SIZE_PRESETS === 'undefined') {
    var SIZE_PRESETS = {
        grande: { l: 3, m: 3, s: 3 },
        mediano: { l: 3, m: 2, s: 3 },
        pequeño: { l: 1, m: 2, s: 2 },
        personalizado: { l: 4, m: 4, s: 4 }
    };
}

const ALL_SLOTS = {
    l: [{ x: 45, y: 55, r: -5, s: 1 }, { x: 55, y: 55, r: 5, s: 1 }, { x: 48, y: 50, r: -2, s: 1.1 }, { x: 52, y: 50, r: 2, s: 1.1 }],
    m: [{ x: 46, y: 62, r: -10, s: 1 }, { x: 50, y: 58, r: 0, s: 1.05 }, { x: 54, y: 62, r: 10, s: 1 }, { x: 44, y: 60, r: 15, s: 0.95 }],
    s: [{ x: 47, y: 65, r: -8, s: 0.85 }, { x: 50, y: 66, r: 0, s: 0.85 }, { x: 53, y: 65, r: 8, s: 0.85 }, { x: 44, y: 67, r: -12, s: 0.8 }]
};

let CONFIG = {
    l: { n: 4, slots: ALL_SLOTS.l },
    m: { n: 3, slots: ALL_SLOTS.m.slice(0, 3) },
    s: { n: 3, slots: ALL_SLOTS.s.slice(0, 3) }
};

let selectedSizeKey = null;
let tier = 'l', total = 0, flowers = [], selected = null, drag = null, sx, sy, isFinal = false;
let states = new Map(), wrapState = { x: 0, y: 0, s: 1 }, dialDragging = false;

function selectSize(key) {
    selectedSizeKey = key;
    document.querySelectorAll('.sz-card').forEach(c => c.classList.remove('selected'));
    const card = document.getElementById('sz-' + key);
    if (card) card.classList.add('selected');
    const confirmBtn = document.getElementById('szConfirmBtn');
    if (confirmBtn) confirmBtn.classList.add('ready');
}

function confirmSize() {
    if (!selectedSizeKey) return;
    const preset = SIZE_PRESETS[selectedSizeKey];
    CONFIG = {
        l: { n: preset.l, slots: ALL_SLOTS.l.slice(0, preset.l) },
        m: { n: preset.m, slots: ALL_SLOTS.m.slice(0, preset.m) },
        s: { n: preset.s, slots: ALL_SLOTS.s.slice(0, preset.s) }
    };
    const ss = document.getElementById('sizeScreen');
    if (ss) {
        ss.classList.add('hide');
        setTimeout(() => { ss.style.display = 'none'; }, 800);
    }
    renderCatalog();
}

function getSmartWrapBounds() {
    const stage = document.getElementById('stage');
    if (!stage) return { minS: 0.8, maxS: 1.2, centerOffsetX: 0 };
    const stageW = stage.offsetWidth;
    const WRAP_BASE_W = 460;
    if (flowers.length === 0) return { minS: 0.80, maxS: 1.10, centerOffsetX: 0 };
    const stageRect = stage.getBoundingClientRect();
    let minLeft = Infinity, maxRight = -Infinity;
    let sumCX = 0;
    flowers.forEach(f => {
        const rect = f.el.getBoundingClientRect();
        const flLeft = rect.left - stageRect.left;
        const flRight = rect.right - stageRect.left;
        const flCX = (rect.left + rect.right) / 2 - stageRect.left;
        if (flLeft < minLeft) minLeft = flLeft;
        if (flRight > maxRight) maxRight = flRight;
        sumCX += flCX;
    });
    const spreadPx = maxRight - minLeft;
    const centerOffsetX = ((sumCX / flowers.length) - (stageW / 2)) * 0.45;
    return {
        minS: Math.max(0.78, Math.min(1.05, (spreadPx + 100) / WRAP_BASE_W)),
        maxS: Math.min(1.30, stageW / WRAP_BASE_W * 1.15),
        centerOffsetX
    };
}

function applySmartWrap(autoCenter = true) {
    const { minS, maxS, centerOffsetX } = getSmartWrapBounds();
    const slider = document.getElementById('wScale');
    if (slider) {
        slider.min = minS.toFixed(2);
        slider.max = maxS.toFixed(2);
        wrapState.s = Math.max(minS, Math.min(maxS, wrapState.s));
        slider.value = wrapState.s;
    }
    const valText = document.getElementById('wScaleValText');
    if (valText) valText.innerText = wrapState.s.toFixed(1) + 'x';
    document.querySelectorAll('.wrap-part').forEach(w => w.style.setProperty('--tw', wrapState.s));
    if (autoCenter && flowers.length > 0 && Math.abs(wrapState.x) < 40) {
        wrapState.x = centerOffsetX;
        document.querySelectorAll('.wrap-part').forEach(w => {
            w.style.setProperty('--tx', wrapState.x + 'px');
            w.style.setProperty('--ty', wrapState.y + 'px');
        });
    }
}

function renderCatalog() {
    const list = document.getElementById('flist'); if (!list) return;
    const tierFlows = FLOWERS.filter(f => f.type === tier);
    const fullCount = flowers.filter(f => f.tier === tier).length;
    const maxForTier = SIZE_PRESETS[selectedSizeKey] ? SIZE_PRESETS[selectedSizeKey][tier] : CONFIG[tier].n;
    const isFull = fullCount >= maxForTier;

    // To prevent "click-through" bugs on mobile where destroying the tapped DOM element 
    // causes the click to hit the element underneath it (e.g. the 'Ramo' tab), 
    // we only build the DOM if it's empty or from a different tier.
    if (list.dataset.renderedTier !== tier) {
        list.innerHTML = '';
        list.dataset.renderedTier = tier;
        tierFlows.forEach(f => {
            const d = document.createElement('div'); d.className = `fcard ${isFull ? 'locked' : ''}`;
            d.onclick = (e) => {
                if (e) { e.preventDefault(); e.stopPropagation(); }
                // Live check fullCount when clicked
                const curFull = flowers.filter(fl => fl.tier === tier).length;
                const curMax = SIZE_PRESETS[selectedSizeKey] ? SIZE_PRESETS[selectedSizeKey][tier] : CONFIG[tier].n;
                if (curFull < curMax) add(f);
            };
            d.innerHTML = `<img src="${f.thumb}" class="fcard-img" onerror="if(!this.dataset.tried){this.dataset.tried=true; this.src=this.src.replace('.webp','.png');}else{this.src='https://placehold.co/100x100?text=Error'; this.onerror=null;}"><div><div class="fname">${f.name}</div></div><div class="fprice">$${f.p}</div>`;
            list.appendChild(d);
        });
    } else {
        // Just update lock state
        document.querySelectorAll('#flist .fcard').forEach(d => {
            if (isFull) d.classList.add('locked');
            else d.classList.remove('locked');
        });
    }
}

function add(f) {
    const c = flowers.filter(fl => fl.tier === tier).length;
    const isCustom = selectedSizeKey === 'personalizado';
    const maxForTier = SIZE_PRESETS[selectedSizeKey] ? SIZE_PRESETS[selectedSizeKey][tier] : CONFIG[tier].n;
    if (c >= maxForTier) return; // Respect max limit for all sizes including personalizado

    // Fallback slot if predefined slots are exhausted
    let slot = CONFIG[tier].slots[c];
    if (!slot) {
        // Random slight jitter around center for extra flowers
        slot = {
            x: 50 + (Math.random() * 10 - 5),
            y: tier === 'l' ? 53 : tier === 'm' ? 60 : 66,
            r: Math.random() * 20 - 10,
            s: tier === 'l' ? 1.1 : tier === 'm' ? 0.85 : 0.55
        };
    }

    const flowersArea = document.getElementById('flowers');
    if (!flowersArea) return;

    const cont = document.createElement('div'); cont.className = 'pfl-container';
    cont.style.left = `${slot.x}%`; cont.style.top = `${slot.y}%`;
    const tierSize = tier === 'l' ? { w: '200px', baseS: 1.10 } : tier === 'm' ? { w: '200px', baseS: 0.85 } : { w: '200px', baseS: 0.55 };
    cont.style.width = tierSize.w; cont.style.height = tierSize.w;
    const ring = document.createElement('div'); ring.className = 'rotation-ring';
    ring.innerHTML = `<div class="rotation-handle"><svg viewBox="0 0 12 12"><path d="M6 1.5 A4.5 4.5 0 0 1 10.5 6" fill="none" stroke="currentColor" stroke-width="1.5"/></svg></div>`;
    const badge = document.createElement('div'); badge.className = 'angle-badge'; badge.innerText = '0°';
    const img = document.createElement('img');
    // Using thumbnail for instant feedback, then asynchronously swap to full
    img.src = f.thumb || f.img;
    img.className = 'pfl';
    img.decoding = 'async';
    img.onerror = function () {
        if (!this.dataset.tried) { this.dataset.tried = true; this.src = this.src.replace('.webp', '.png'); }
        else { this.src = 'https://placehold.co/400x600?text=Error'; this.onerror = null; }
    };
    if (f.thumb && f.img && f.thumb !== f.img) {
        const full = new Image();
        full.decoding = 'async';
        full.onload = function() { img.src = f.img; };
        full.onerror = function() { /* keep thumb */ };
        full.src = f.img;
    }
    cont.appendChild(ring); cont.appendChild(badge); cont.appendChild(img);
    flowersArea.appendChild(cont);
    const obj = { el: cont, tier, data: f, x: 0, y: 0, s: isCustom ? slot.s : tierSize.baseS, r: 0, baseR: slot.r };
    flowers.push(obj); states.set(cont, obj); total += f.p;
    cont.style.setProperty('--sx', '-200px'); cont.style.setProperty('--sy', '200px');
    cont.style.setProperty('--s', slot.s); cont.style.setProperty('--r', slot.r + 'deg');
    cont.style.animation = 'fly 0.5s ease-out forwards';
    setTimeout(() => { 
        cont.style.animation = 'none';
        transform(obj); 
        
        // On mobile, if catalog is open, do not trigger the full select() because it opens the controls drawer and hides the catalog
        const cat = document.querySelector('.catalog');
        if (window.innerWidth <= 768 && cat && cat.classList.contains('mob-visible')) {
            if (selected) selected.classList.remove('selected');
            selected = cont; 
            selected.classList.add('selected');
        } else {
            select(cont); 
        }
        
        applySmartWrap(true);
        // Brief touch hint on first flower
        const th = document.getElementById('touchHint');
        if (flowers.length === 1 && th && window.innerWidth <= 768) {
            setTimeout(() => { th.classList.add('show'); setTimeout(() => th.classList.remove('show'), 3500); }, 400);
        }
    }, 550);
    updateUI();
}

function select(cont) {
    if (selected) selected.classList.remove('selected');
    selected = cont; selected.classList.add('selected');
    const fEdit = document.getElementById('fEdit');
    const wEdit = document.getElementById('wEdit');
    if (cont.classList.contains('wrap-part')) {
        if (wEdit) wEdit.style.display = 'block';
        if (fEdit) fEdit.style.display = 'none';
        applySmartWrap(false);
    } else {
        if (fEdit) fEdit.style.display = 'block';
        if (wEdit) wEdit.style.display = 'none';
        const s = states.get(cont);
        const limits = getLogicalLimits(s.tier);
        const fScale = document.getElementById('fScale');
        if (fScale) { fScale.min = limits.minS; fScale.max = limits.maxS; fScale.value = s.s; }
        const scaleValText = document.getElementById('scaleValText');
        if (scaleValText) scaleValText.innerText = s.s.toFixed(1) + 'x';
        const fRot = document.getElementById('fRot');
        if (fRot) fRot.value = s.r;
        const rotValText = document.getElementById('rotValText');
        if (rotValText) rotValText.innerText = Math.round(s.r) + '°';
        const adjTitle = document.getElementById('adjTitle');
        if (adjTitle) adjTitle.innerText = 'Flor: ' + s.data.name;
        updateRotationUI(s.r);
    }
    const controls = document.getElementById('controls');
    if (controls) controls.classList.add('show');
}

function deselectAll() {
    if (selected) selected.classList.remove('selected');
    selected = null;
    const controls = document.getElementById('controls');
    if (controls) controls.classList.remove('show');
}

function toggleMinimize() {
    const controls = document.getElementById('controls');
    if (controls) controls.classList.toggle('minimized');
}

function getLogicalLimits(t) {
    const BASE_LIMITS = { l: { min: 1.00, max: 1.60 }, m: { min: 0.75, max: 0.95 }, s: { min: 0.45, max: 0.70 } };
    let minS = BASE_LIMITS[t].min, maxS = BASE_LIMITS[t].max;
    const scales = { l: [], m: [], s: [] };
    flowers.forEach(f => scales[f.tier].push(f.s));
    const getMax = arr => arr.length ? Math.max(...arr) : null;
    const getMin = arr => arr.length ? Math.min(...arr) : null;

    // Jerarquía de escala: Grandes > Medianas > Pequeñas
    if (t === 'l') {
        const maxM = getMax(scales.m);
        if (maxM !== null) minS = Math.max(minS, maxM + 0.05);
    }
    else if (t === 'm') {
        const minL = getMin(scales.l);
        if (minL !== null) maxS = Math.min(maxS, minL - 0.05);
        const maxSm = getMax(scales.s);
        if (maxSm !== null) minS = Math.max(minS, maxSm + 0.05);
    }
    else if (t === 's') {
        const minM = getMin(scales.m);
        if (minM !== null) maxS = Math.min(maxS, minM - 0.05);
    }

    if (minS >= maxS - 0.05) minS = Math.max(BASE_LIMITS[t].min, maxS - 0.1);
    return { minS: +minS.toFixed(2), maxS: +maxS.toFixed(2) };
}

function checkPositionConstraints(s, dy) {
    const currentTop = s.el.offsetTop + s.y;
    const tops = { l: [], m: [], s: [] };
    flowers.forEach(f => { if (f.el !== s.el) tops[f.tier].push(f.el.offsetTop + f.y); });
    const getMinTop = arr => arr.length ? Math.min(...arr) : null;
    const getMaxTop = arr => arr.length ? Math.max(...arr) : null;

    // Las flores grandes (l) no pueden bajar más que las medianas (m)
    if (s.tier === 'l') {
        const minM = getMinTop(tops.m);
        if (minM !== null && currentTop + dy > minM - 15) return false;
    }
    // Las medianas (m) deben estar entre las grandes y las pequeñas
    else if (s.tier === 'm') {
        const maxL = getMaxTop(tops.l);
        const minS = getMinTop(tops.s);
        if (maxL !== null && currentTop + dy < maxL + 15) return false;
        if (minS !== null && currentTop + dy > minS - 15) return false;
    }
    // Las pequeñas (s) no pueden subir más que las medianas (m)
    else if (s.tier === 's') {
        const maxM = getMaxTop(tops.m);
        if (maxM !== null && currentTop + dy < maxM + 15) return false;
    }
    return true;
}

function transform(s) {
    const limits = getLogicalLimits(s.tier);
    s.s = Math.max(limits.minS, Math.min(limits.maxS, s.s));
    s.el.style.transform = `translate(-50%,-50%) translate(${s.x}px, ${s.y}px) scale(${s.s}) rotate(${s.baseR + s.r}deg)`;
    const badge = s.el.querySelector('.angle-badge');
    if (badge) badge.innerText = Math.round(s.r) + '°';
    s.el.style.setProperty('--ring-rot', `${s.r}deg`);
}

function applyAngle(s, a, snap = true) {
    const SNAPS = [0, 45, 90, 135, 180, -45, -90, -135, -180];
    if (snap) { for (let sn of SNAPS) { if (Math.abs(a - sn) < 8) { a = sn; break; } } }
    s.r = a; transform(s); updateRotationUI(a);
}

function updateRotationUI(a) {
    const dial = document.getElementById('dial'); if (dial) dial.style.transform = `rotate(${a}deg)`;
    const rotSlider = document.getElementById('fRot'); if (rotSlider) rotSlider.value = Math.max(-180, Math.min(180, a));
    const rotValText = document.getElementById('rotValText'); if (rotValText) rotValText.innerText = Math.round(a) + '°';
    updateArc(a);
}

function updateArc(a) {
    const arcFill = document.getElementById('arcFill'); const needle = document.getElementById('arcNeedle');
    if (!arcFill || !needle) return;
    const r = 70; const clamped = Math.max(-90, Math.min(90, a));
    const rad = (clamped - 90) * Math.PI / 180;
    const x = r * Math.cos(rad); const y = 70 + r * Math.sin(rad);
    if (Math.abs(clamped) > 1) { arcFill.setAttribute('d', `M 0 0 A 70 70 0 0 ${clamped > 0 ? 1 : 0} ${x} ${y}`); needle.setAttribute('x2', x); needle.setAttribute('y2', y); needle.setAttribute('opacity', 0.8); }
    else { arcFill.setAttribute('d', ''); needle.setAttribute('opacity', 0); }
}

function updateUI() {
    const pval = document.getElementById('pval');
    if (pval) pval.innerText = `$${total.toFixed(2)}`;

    const sum = document.getElementById('sum');
    if (!sum) return;
    sum.innerHTML = '';

    // Group flowers by name
    const counts = {};
    const icons = {};
    flowers.forEach(f => {
        const name = (f.data.name || "Flor").trim();
        counts[name] = (counts[name] || 0) + 1;
        icons[name] = f.data.thumb;
    });

    Object.keys(counts).forEach(name => {
        const d = document.createElement('div');
        d.className = 'ri';
        const displayCount = counts[name] > 1 ? `: ${counts[name]}` : '';
        d.innerHTML = `<img src="${icons[name]}" onerror="if(!this.dataset.tried){this.dataset.tried=true; this.src=this.src.replace('.webp','.png');}else{this.src='https://placehold.co/100x100?text=Error'; this.onerror=null;}"><span>${name}${displayCount}</span>`;
        sum.appendChild(d);
    });

    const nextBtn = document.getElementById('nextBtn');
    if (nextBtn) {
        const isCustom = selectedSizeKey === 'personalizado';
        const maxForTierUI = SIZE_PRESETS[selectedSizeKey] ? SIZE_PRESETS[selectedSizeKey][tier] : CONFIG[tier].n;
        const currentCount = flowers.filter(f => f.tier === tier).length;
        const isFull = currentCount >= maxForTierUI;
        const hasAtLeastOne = currentCount >= 1;

        if (isFull || (isCustom && hasAtLeastOne)) {
            nextBtn.classList.add('on');
            nextBtn.style.pointerEvents = 'auto';
            nextBtn.style.opacity = '1';
        } else {
            nextBtn.classList.remove('on');
        }
    }
    renderCatalog();
}

function step() {
    if (tier === 'l') { tier = 'm'; document.getElementById('s1').classList.remove('active'); document.getElementById('s2').classList.add('active'); }
    else if (tier === 'm') { tier = 's'; document.getElementById('s2').classList.remove('active'); document.getElementById('s3').classList.add('active'); }
    else { document.getElementById('finishBtn').style.display = 'block'; document.getElementById('nextBtn').style.display = 'none'; return; }
    const nextBtn = document.getElementById('nextBtn');
    if (nextBtn) nextBtn.classList.remove('on');
    renderCatalog();
}

function stepRot(delta) { if (!selected || !states.has(selected)) return; const s = states.get(selected); applyAngle(s, Math.max(-180, Math.min(180, s.r + delta)), false); }
function applyQuickRot(delta) { if (!selected || !states.has(selected)) return; const s = states.get(selected); applyAngle(s, s.r + delta, false); }
function resetSelected() { if (!selected || !states.has(selected)) return; const s = states.get(selected); s.x = 0; s.y = 0; s.s = 1; s.r = 0; if (document.getElementById('fScale')) document.getElementById('fScale').value = 1; if (document.getElementById('scaleValText')) document.getElementById('scaleValText').innerText = '1.0x'; if (document.getElementById('fRot')) document.getElementById('fRot').value = 0; if (document.getElementById('rotValText')) document.getElementById('rotValText').innerText = '0°'; transform(s); updateRotationUI(0); }
function setWrapColor(color, el) { document.querySelectorAll('.wrap-part').forEach(w => { w.style.setProperty('--wc', color); }); document.querySelectorAll('.color-swatch').forEach(s => s.classList.remove('active')); if (el) el.classList.add('active'); }
function removeSelected() { if (!selected || !states.has(selected)) return; const s = states.get(selected); total -= s.data.p; flowers = flowers.filter(f => f.el !== selected); states.delete(selected); selected.remove(); selected = null; const controls = document.getElementById('controls'); if (controls) controls.classList.remove('show'); updateUI(); }

function clearBouquet() {
    if (flowers.length === 0) return;
    const modal = document.getElementById('clearModal');
    if (modal) modal.style.display = 'flex';
}
window.clearBouquet = clearBouquet;

function hideClearModal() {
    const modal = document.getElementById('clearModal');
    if (modal) modal.style.display = 'none';
}
window.hideClearModal = hideClearModal;

function confirmClearBouquet() {
    hideClearModal();
    // Clear data
    flowers = [];
    states.clear();
    total = 0;

    // Clear DOM
    const flowersArea = document.getElementById('flowers');
    if (flowersArea) flowersArea.innerHTML = '';

    // Reset steps
    tier = 'l';
    document.querySelectorAll('.si').forEach(s => s.classList.remove('active'));
    const s1 = document.getElementById('s1');
    if (s1) s1.classList.add('active');

    // Reset Buttons UI
    const finishBtn = document.getElementById('finishBtn');
    if (finishBtn) finishBtn.style.display = 'none';
    const nextBtn = document.getElementById('nextBtn');
    if (nextBtn) nextBtn.style.display = 'block';

    deselectAll();
    updateUI();
    applySmartWrap(true);
}
window.confirmClearBouquet = confirmClearBouquet;

let isProcessing = false;

function finishOrder() {
    if (isProcessing) return;

    // Validation for 'Personalizado' size
    if (selectedSizeKey === 'personalizado') {
        const counts = { l: 0, m: 0, s: 0 };
        flowers.forEach(f => {
            counts[f.tier]++;
        });

        // Condition: 1 Large OR 2 Medium OR 3 Small
        const isValid = counts.l >= 1 || counts.m >= 2 || counts.s >= 3;

        if (!isValid) {
            alert('Para un Ramo Personalizado, debes incluir al menos:\n- 1 flor Grande\n- O 2 flores Medianas\n- O 3 flores Pequeñas\n\n¡Agrega un poco más para continuar!');
            return;
        }
    }

    if (selected) { selected.classList.remove('selected'); selected = null; }
    const controls = document.getElementById('controls');
    if (controls) controls.classList.remove('show');

    const finishBtn = document.getElementById('finishBtn');

    if (typeof IS_AUTHENTICATED !== 'undefined' && IS_AUTHENTICATED) {
        // Authenticated: lock button and process immediately
        if (finishBtn) {
            finishBtn.innerText = 'PROCESANDO...';
            finishBtn.style.opacity = '0.7';
            finishBtn.style.pointerEvents = 'none';
        }
        isProcessing = true;
        processOrder(false);
    } else {
        // Guest: just open the modal, don't lock the button yet
        isProcessing = false;
        document.getElementById('checkoutModal').style.display = 'flex';
        document.getElementById('modalButtons').style.display = 'flex';
        document.getElementById('guestForm').style.display = 'none';
        const guestNameEl = document.getElementById('guestName');
        if (guestNameEl) guestNameEl.value = '';
        const guestPhoneEl = document.getElementById('guestPhone');
        if (guestPhoneEl) guestPhoneEl.value = '';
    }
}
window.finishOrder = finishOrder;

function showGuestForm() {
    document.getElementById('modalButtons').style.display = 'none';
    document.getElementById('guestForm').style.display = 'block';
}
window.showGuestForm = showGuestForm;

function hideCheckoutModal() {
    document.getElementById('checkoutModal').style.display = 'none';
    // Restore finish button in case user cancels
    isProcessing = false;
    const finishBtn = document.getElementById('finishBtn');
    if (finishBtn) {
        finishBtn.innerText = 'FINALIZAR DISEÑO ✓';
        finishBtn.style.opacity = '1';
        finishBtn.style.pointerEvents = 'auto';
    }
}
window.hideCheckoutModal = hideCheckoutModal;

async function processOrder(isGuest, viaWhatsapp = false) {
    let guestData = null;
    if (isGuest) {
        const name = document.getElementById('guestName').value.trim();
        if (!name) {
            alert('Por favor indica tu nombre.');
            return;
        }
        guestData = { name, email: null, phone: 'N/A' };
        const btn = document.getElementById('btnProcessGuest');
        btn.innerText = 'Procesando...';
        btn.disabled = true;
        const btnSys = document.getElementById('btnProcessGuestSystem');
        if (btnSys) btnSys.disabled = true;
    }

    isFinal = true;
    hideCheckoutModal();

    // Compute absolute visual center position as % of stage area for server-side image generation
    const stageEl2 = document.getElementById('stage');
    const stageRect2 = stageEl2 ? stageEl2.getBoundingClientRect() : { left: 0, top: 0, width: 400, height: 600 };
    const flowersData = flowers.map(f => {
        const contRect = f.el.getBoundingClientRect();
        const cx_pct = ((contRect.left + contRect.width / 2) - stageRect2.left) / stageRect2.width * 100;
        const cy_pct = ((contRect.top + contRect.height / 2) - stageRect2.top) / stageRect2.height * 100;
        return {
            flower_id: f.data.id,
            x: Math.round(cx_pct * 10) / 10,
            y: Math.round(cy_pct * 10) / 10,
            scale: f.s,
            rotation: f.r
        };
    });

    // Wrap Data
    const wrapPart = document.querySelector('.wrap-part');
    const wrapColor = wrapPart ? (getComputedStyle(wrapPart).getPropertyValue('--wc').trim() || '#e8dfcc') : '#e8dfcc';

    const orderData = {
        size_id: selectedSizeKey,
        flowers: flowersData,
        wrap_data: {
            color: wrapColor,
            scale: wrapState.s,
            x: wrapState.x,
            y: wrapState.y
        },
        coupon_code: null,
        guest_data: guestData
    };

    try {
        const response = await fetch('/orders/create/', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': CSRF_TOKEN
            },
            body: JSON.stringify(orderData)
        });
        const result = await response.json();

        if (result.status === 'success') {
            document.getElementById('finalView').innerHTML = document.getElementById('stage').innerHTML;
            document.getElementById('doneOv').classList.add('show');

            setTimeout(() => {
                if (!IS_AUTHENTICATED) {
                    if (result.whatsapp_message) {
                        // The service returns raw text, we encode it here for guests
                        const waNumber = '593985991149';
                        window.location.href = `https://wa.me/${waNumber}?text=${encodeURIComponent(result.whatsapp_message)}`;
                    } else {
                        window.location.href = `/orders/track/${result.tracking_token || 'guest'}/`;
                    }
                } else {
                    // Authenticated users go to their history
                    window.location.href = '/orders/history/';
                }
            }, 2000);
        } else {
            alert('Error al crear el pedido: ' + result.error);
            isFinal = false;
            isProcessing = false;
            const finishBtn = document.getElementById('finishBtn');
            if (finishBtn) {
                finishBtn.innerText = 'FINALIZAR DISEÑO ✓';
                finishBtn.style.opacity = '1';
                finishBtn.style.pointerEvents = 'auto';
            }
        }
    } catch (e) {
        console.error(e);
        alert('Ocurrió un error de conexión.');
        isFinal = false;
        isProcessing = false;
        const finishBtn = document.getElementById('finishBtn');
        if (finishBtn) {
            finishBtn.innerText = 'FINALIZAR DISEÑO ✓';
            finishBtn.style.opacity = '1';
            finishBtn.style.pointerEvents = 'auto';
        }
    }

    if (isGuest) {
        const btn = document.getElementById('btnProcessGuest');
        btn.innerText = 'Enviar Pedido (WhatsApp)';
        btn.disabled = false;
        const btnSys = document.getElementById('btnProcessGuestSystem');
        if (btnSys) btnSys.disabled = false;
    }
}
window.processOrder = processOrder;

// Initialization and Event Listeners
document.addEventListener('DOMContentLoaded', () => {
    // Prevent long-press context menu on all images in the designer (mobile)
    document.addEventListener('contextmenu', e => {
        if (e.target.tagName === 'IMG' || e.target.closest('.pfl-container') || e.target.closest('.stage-outer')) {
            e.preventDefault();
        }
    });

    // ── RANGE SLIDER PROTECTION ──────────────────────────────────────────────
    // Stop the global startDrag touchstart/touchmove from ever reaching form
    // inputs. This allows input[type=range] (wrap size slider) to work on mobile.
    document.querySelectorAll('#controls input, #controls select').forEach(input => {
        input.addEventListener('touchstart', e => e.stopPropagation(), { passive: false });
        input.addEventListener('touchmove',  e => e.stopPropagation(), { passive: false });
    });
    // Also protect dynamically-added inputs via delegation on #controls
    const controlsEl = document.getElementById('controls');
    if (controlsEl) {
        controlsEl.addEventListener('touchstart', e => {
            if (e.target.tagName === 'INPUT' || e.target.tagName === 'SELECT') {
                e.stopPropagation();
            }
        }, { passive: false, capture: true });
        controlsEl.addEventListener('touchmove', e => {
            if (e.target.tagName === 'INPUT' || e.target.tagName === 'SELECT') {
                e.stopPropagation();
            }
        }, { passive: false, capture: true });
    }

    const stage = document.getElementById('stage');
    if (stage) {
        stage.addEventListener('wheel', e => {
            if (!selected) return; e.preventDefault();
            if (selected.classList.contains('wrap-part')) { const { minS, maxS } = getSmartWrapBounds(); wrapState.s = Math.max(minS, Math.min(maxS, wrapState.s + (e.deltaY > 0 ? -0.03 : 0.03))); if (document.getElementById('wScale')) document.getElementById('wScale').value = wrapState.s; if (document.getElementById('wScaleValText')) document.getElementById('wScaleValText').innerText = wrapState.s.toFixed(1) + 'x'; document.querySelectorAll('.wrap-part').forEach(w => w.style.setProperty('--tw', wrapState.s)); }
            else { const s = states.get(selected); s.s = Math.max(0.3, Math.min(2, s.s + (e.deltaY > 0 ? -0.05 : 0.05))); if (document.getElementById('fScale')) document.getElementById('fScale').value = s.s; transform(s); if (document.getElementById('scaleValText')) document.getElementById('scaleValText').innerText = s.s.toFixed(1) + 'x'; }
        }, { passive: false });
    }

    const dial = document.getElementById('dial');
    if (dial) {
        const startDial = e => {
            if (!selected || !states.has(selected)) return;
            dialDragging = true; e.stopPropagation();
            if (e.cancelable) e.preventDefault();
            const move = me => {
                const mev = me.touches ? me.touches[0] : me;
                const s = states.get(selected); const rect = dial.getBoundingClientRect();
                const cx = rect.left + rect.width / 2; const cy = rect.top + rect.height / 2;
                applyAngle(s, Math.atan2(mev.clientY - cy, mev.clientX - cx) * 180 / Math.PI + 90);
            };
            const up = () => { 
                dialDragging = false; 
                document.removeEventListener('mousemove', move); document.removeEventListener('mouseup', up); 
                document.removeEventListener('touchmove', move); document.removeEventListener('touchend', up); 
            };
            document.addEventListener('mousemove', move, {passive: false}); document.addEventListener('mouseup', up);
            document.addEventListener('touchmove', move, {passive: false}); document.addEventListener('touchend', up);
        };
        dial.addEventListener('mousedown', startDial);
        dial.addEventListener('touchstart', startDial, {passive: false});
    }

    const fScale = document.getElementById('fScale'); if (fScale) fScale.oninput = e => { if (!selected || !states.has(selected)) return; const s = states.get(selected); s.s = parseFloat(e.target.value); if (document.getElementById('scaleValText')) document.getElementById('scaleValText').innerText = s.s.toFixed(1) + 'x'; transform(s); };
    const fRot = document.getElementById('fRot'); if (fRot) fRot.oninput = e => { if (!selected || !states.has(selected)) return; applyAngle(states.get(selected), parseFloat(e.target.value), false); };
    const wScale = document.getElementById('wScale'); 
    if (wScale) {
        wScale.oninput = e => { 
            const { minS, maxS } = getSmartWrapBounds(); 
            wrapState.s = Math.max(minS, Math.min(maxS, parseFloat(e.target.value))); 
            e.target.value = wrapState.s; 
            if (document.getElementById('wScaleValText')) document.getElementById('wScaleValText').innerText = wrapState.s.toFixed(1) + 'x'; 
            document.querySelectorAll('.wrap-part').forEach(w => w.style.setProperty('--tw', wrapState.s)); 
        };
        // Redundant touch protection for mobile wrapper
        wScale.addEventListener('touchstart', e => { e.stopPropagation(); }, {passive: false, capture: true});
        wScale.addEventListener('touchmove', e => { e.stopPropagation(); }, {passive: false, capture: true});
        wScale.addEventListener('mousedown', e => { e.stopPropagation(); });
    }

    const startDrag = (e) => {
        if (isFinal) return;
        const evt = e.touches ? e.touches[0] : e;
        // On mobile, .pfl-container has pointer-events: auto, so target may be container itself
        const target = e.target.closest('.pfl-container') || e.target.closest('.wrap-part');
        if (!target && !e.target.closest('#controls') && !e.target.closest('.fcard') && !e.target.closest('.mob-tab-bar') && !e.target.closest('.right-panel') && !e.target.closest('.catalog')) { deselectAll(); return; }
        if (!target) return;
        // Only process if target has state (is a flower container) or is wrap
        if (!target.classList.contains('wrap-part') && !states.has(target)) return;
        
        const th = document.getElementById('touchHint');
        if (th) th.classList.remove('show');

        const isHandle = e.target.closest('.rotation-handle');
        drag = isHandle ? { type: 'rotate', el: target } : { type: 'move', el: target };
        select(target); sx = evt.clientX; sy = evt.clientY;
        const onMove = me => {
            if (!drag) return;
            const mev = me.touches ? me.touches[0] : me;
            if (drag.type === 'move') {
                const dx = mev.clientX - sx; const dy = mev.clientY - sy;
                if (drag.el.classList.contains('wrap-part')) {
                    // Movement disabled for wrapping per user request
                    return;
                } else {
                    const s = states.get(drag.el);
                    const rect = document.getElementById('stage').getBoundingClientRect();
                    const minX = -rect.width / 2 + 30; const maxX = rect.width / 2 - 30;
                    const minY = -s.el.offsetTop + 30; const maxY = (rect.height - s.el.offsetTop) - 30;
                    const newX = s.x + dx; const newY = s.y + dy;
                    s.x = Math.max(minX, Math.min(maxX, newX)); sx = mev.clientX;
                    if (newY >= minY && newY <= maxY && checkPositionConstraints(s, dy)) { s.y = newY; sy = mev.clientY; }
                    transform(s);
                }
            } else if (drag.type === 'rotate') {
                const s = states.get(drag.el); const rect = drag.el.getBoundingClientRect();
                const cx = rect.left + rect.width / 2; const cy = rect.top + rect.height / 2;
                applyAngle(s, Math.atan2(mev.clientY - cy, mev.clientX - cx) * 180 / Math.PI + 90, false);
            }
            if (e.touches) me.preventDefault();
        };
        const onEnd = () => { 
            drag = null; 
            document.removeEventListener('mousemove', onMove); document.removeEventListener('mouseup', onEnd); 
            document.removeEventListener('touchmove', onMove); document.removeEventListener('touchend', onEnd); 
        };
        document.addEventListener('mousemove', onMove, {passive: false}); document.addEventListener('mouseup', onEnd);
        document.addEventListener('touchmove', onMove, {passive: false}); document.addEventListener('touchend', onEnd);
        if (!e.touches && e.cancelable) e.preventDefault();
    };

    document.addEventListener('mousedown', startDrag);
    document.addEventListener('touchstart', startDrag, {passive: false});

    const controls = document.getElementById('controls');
    const controlsHeader = document.getElementById('controlsHeader');
    if (controls && controlsHeader) {
        let dc = false, ox, oy;
        const startControlDrag = e => {
            if (e.target.closest('.adj-btn')) return;
            const evt = e.touches ? e.touches[0] : e;
            dc = true; ox = evt.clientX - controls.offsetLeft; oy = evt.clientY - controls.offsetTop;
            controls.style.transition = 'none'; 
            if (e.cancelable) e.preventDefault();
        };
        const moveControl = e => {
            if (!dc) return;
            const evt = e.touches ? e.touches[0] : e;
            controls.style.left = (evt.clientX - ox) + 'px';
            controls.style.top = (evt.clientY - oy) + 'px';
            controls.style.right = 'auto';
        };
        const endControlDrag = () => { if (dc) { dc = false; controls.style.transition = 'opacity 0.3s, transform 0.3s'; } };
        
        controlsHeader.addEventListener('mousedown', startControlDrag);
        controlsHeader.addEventListener('touchstart', startControlDrag, {passive: false});
        document.addEventListener('mousemove', moveControl, {passive: false});
        document.addEventListener('touchmove', moveControl, {passive: false});
        document.addEventListener('mouseup', endControlDrag);
        document.addEventListener('touchend', endControlDrag);
    }

    renderCatalog();
});

window.switchMobTab = function(tab) {
    const catalog = document.querySelector('.catalog');
    const rightPanel = document.querySelector('.right-panel');
    const controls = document.getElementById('controls');
    
    // Backdrops
    const catBackdrop = document.getElementById('mobCatalogBackdrop');
    const sumBackdrop = document.getElementById('mobSummaryBackdrop');
    
    // Tabs
    document.querySelectorAll('.mob-tab-btn').forEach(btn => btn.classList.remove('active'));
    
    // Hide all first
    if (catalog) catalog.classList.remove('mob-visible');
    if (rightPanel) rightPanel.classList.remove('mob-visible');
    if (catBackdrop) catBackdrop.classList.remove('visible');
    if (sumBackdrop) sumBackdrop.classList.remove('visible');
    if (controls && tab !== 'stage') controls.classList.remove('show');
    
    // Show requested
    if (tab === 'catalog') {
        const t = document.getElementById('tabCatalog'); if(t) t.classList.add('active');
        if (catalog) catalog.classList.add('mob-visible');
        if (catBackdrop) catBackdrop.classList.add('visible');
        deselectAll();
    } 
    else if (tab === 'summary') {
        const t = document.getElementById('tabSummary'); if(t) t.classList.add('active');
        if (rightPanel) rightPanel.classList.add('mob-visible');
        if (sumBackdrop) sumBackdrop.classList.add('visible');
        deselectAll();
    }
    else {
        // stage
        const t = document.getElementById('tabStage'); if(t) t.classList.add('active');
    }
};
