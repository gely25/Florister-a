/* ── HELPER: IMAGEN ERROR ── */
function handleImageError(img) {
  img.style.display = 'none';
}

/* ── UI SETUP ── */
document.addEventListener('DOMContentLoaded', () => {
  // Tabs filtering
  const tabs = document.querySelectorAll('.tab-btn');
  const cards = document.querySelectorAll('#track-ramos .product-card');
  tabs.forEach(t => {
    t.addEventListener('click', () => {
      const cat = t.getAttribute('data-cat');
      tabs.forEach(btn => btn.classList.remove('active'));
      t.classList.add('active');
      
      cards.forEach(card => {
        if (cat === 'all' || card.getAttribute('data-size') === cat) {
          card.style.display = '';
        } else {
          card.style.display = 'none';
        }
      });

      // Show/Hide empty message
      const visibleCards = Array.from(cards).filter(c => c.style.display !== 'none');
      const emptyMsg = document.getElementById('empty-ramos-msg');
      const wrapRamos = document.getElementById('wrap-ramos');
      
      if (visibleCards.length === 0) {
        emptyMsg.style.display = 'block';
        wrapRamos.style.display = 'none';
      } else {
        emptyMsg.style.display = 'none';
        wrapRamos.style.display = 'block';
      }
      
      // Reset scroll and update buttons if it's the ramos track
      const trackRamos = document.getElementById('track-ramos');
      if (trackRamos) {
        trackRamos.scrollLeft = 0;
        // Trigger scroll event to update buttons
        trackRamos.dispatchEvent(new Event('scroll'));
      }
    });
  });

  // Carousels (Only for remaining ones if any, like portfolio)
  function setupCarousel(trackId, prevId, nextId) {
    const track = document.getElementById(trackId);
    const prev = document.getElementById(prevId);
    const next = document.getElementById(nextId);
    if(!track || !prev || !next) return;
    const updateBtns = () => {
      prev.disabled = track.scrollLeft <= 10;
      next.disabled = track.scrollLeft >= (track.scrollWidth - track.clientWidth - 10);
    };
    prev.addEventListener('click', () => { track.scrollBy({ left: -260, behavior: 'smooth' }); setTimeout(updateBtns, 350); });
    next.addEventListener('click', () => { track.scrollBy({ left: 260, behavior: 'smooth' }); setTimeout(updateBtns, 350); });
    track.addEventListener('scroll', updateBtns, { passive: true });
    window.addEventListener('resize', updateBtns);
    setTimeout(updateBtns, 100);
  }

  setupCarousel('track-ramos', 'prev-ramos', 'next-ramos');
  setupCarousel('track-portfolio', 'prev-portfolio', 'next-portfolio');
});

/* ── BANNER ANIMATION ── */
/* ── BANNER ANIMATION (Sequential Logic from index.html) ── */
let bIndex = 0;
const totalB = 4;
const focusColors = ['#f0a8b0', '#b0d0a0', '#e0c080', '#c0a0e0'];

const FALL_DURATION   = 850;
const PETAL_GAP       = 1600;
const PAUSE_AFTER_ALL = 600;
const GROW_STAGGER    = 150;
const GROW_DURATION   = 520;

const PETAL_DIRS = ['Top', 'Right', 'Bottom', 'Left'];
const PETAL_IDLE_TRANSFORMS = [
  'rotate(0deg)', 'rotate(90deg)', 'rotate(180deg)', 'rotate(270deg)'
];

let activeBannerTimers = [];
const scheduleBanner = (fn, delay) => { 
  const id = setTimeout(fn, delay); 
  activeBannerTimers.push(id); 
};
const clearBannerTimers = () => { 
  activeBannerTimers.forEach(clearTimeout); 
  activeBannerTimers = []; 
};

function updateBannerUI(idx) {
  const btrackL = document.getElementById('btrack-left');
  const btrackR = document.getElementById('btrack-right');
  const bdotsL = document.querySelectorAll('#bdots-left .bside-dot');
  const bdotsR = document.querySelectorAll('#bdots-right .bside-dot');
  if (!btrackL || !btrackR) return;

  btrackL.style.transform = `translateX(-${idx * 220}px)`;
  btrackR.style.transform = `translateX(-${idx * 220}px)`;
  bdotsL.forEach((d, i) => d.classList.toggle('active', i === idx));
  bdotsR.forEach((d, i) => d.classList.toggle('active', i === idx));
}

function petalFalling(i) {
  const el = document.getElementById('fcP' + i);
  if(!el) return;
  el.style.animation = `petalFall${PETAL_DIRS[i]} ${FALL_DURATION}ms cubic-bezier(0.4,0,0.85,1) forwards`;
}

function petalFallen(i) {
  const el = document.getElementById('fcP' + i);
  if(!el) return;
  el.style.animation = 'none';
  el.style.opacity = '0';
  void el.offsetWidth;
}

function petalGrowing(i) {
  const el = document.getElementById('fcP' + i);
  if(!el) return;
  el.style.animation = 'none';
  el.style.opacity = '0';
  void el.offsetWidth;
  el.style.animation = `petalGrow${PETAL_DIRS[i]} ${GROW_DURATION}ms cubic-bezier(0.34,1.56,0.64,1) forwards`;
}

function petalIdle(i) {
  const el = document.getElementById('fcP' + i);
  if(!el) return;
  el.style.animation = 'none';
  el.style.opacity = '1';
  el.style.transform = PETAL_IDLE_TRANSFORMS[i];
  void el.offsetWidth;
}

function runBannerCycle() {
  clearBannerTimers();
  const fcCenter = document.querySelector('#fc-flower circle');

  // Phase 1 - Petals fall one by one, advance carousel exactly at the same time
  for (let i = 0; i < 4; i++) {
    const t = i * PETAL_GAP;
    scheduleBanner(() => {
      petalFalling(i);
      bIndex = (i + 1) < totalB ? i + 1 : 0;
      updateBannerUI(bIndex);
    }, t);
    scheduleBanner(() => {
      petalFallen(i);
    }, t + FALL_DURATION);
  }

  // Phase 2 - Regrow staggered
  const regrowStart = 4 * PETAL_GAP + FALL_DURATION + PAUSE_AFTER_ALL;
  for (let i = 0; i < 4; i++) {
    scheduleBanner(() => petalGrowing(i), regrowStart + i * GROW_STAGGER);
    scheduleBanner(() => petalIdle(i), regrowStart + i * GROW_STAGGER + GROW_DURATION);
  }

  // Phase 3 - Loop
  const totalCycle = regrowStart + 4 * GROW_STAGGER + GROW_DURATION + 700;
  scheduleBanner(runBannerCycle, totalCycle);
}

// Start cycle
scheduleBanner(runBannerCycle, 600);

document.addEventListener('DOMContentLoaded', () => {
  // Helpers
  const setupDots = (selector, callback) => {
    document.querySelectorAll(selector).forEach((dot, idx) => {
      dot.addEventListener('click', () => {
        callback(idx);
      });
    });
  };

  const jumpToBannerIndex = (idx) => {
    clearBannerTimers();
    bIndex = idx;
    updateBannerUI(bIndex);
    
    // Reset flower
    for(let i=0; i<4; i++) {
        petalIdle(i);
    }
    
    // Restart cycle after a delay
    scheduleBanner(runBannerCycle, 5000);
  };

  setupDots('#bdots-left .bside-dot', jumpToBannerIndex);
  setupDots('#bdots-right .bside-dot', jumpToBannerIndex);

  // ── HERO CAROUSEL ──
  const heroSlides = [
    {
      title: 'Detalles que<br>duran para siempre',
      sub: 'Ramos únicos, arreglos personalizados y flores frescas seleccionadas para cada momento especial.'
    },
    {
      title: 'Ramos con<br>Alma y Corazón',
      sub: 'Creamos experiencias florales diseñadas a tu medida con la frescura de lo natural.'
    },
    {
      title: 'Momentos para<br>el Recuerdo',
      sub: 'Sorprende a quienes más quieres con detalles que expresan todo lo que sientes.'
    }
  ];

  let hIndex = 0;
  const hDots = document.querySelectorAll('.hero-dot');
  const hTitle = document.querySelector('.hero-title');
  const hSub = document.querySelector('.hero-sub');
  let hInterval = setInterval(nextHero, 5000);

  function goToHero(idx) {
    hIndex = idx;
    
    // Animate out
    hTitle.style.opacity = '0';
    hTitle.style.transform = 'translateY(10px)';
    hSub.style.opacity = '0';
    hSub.style.transform = 'translateY(10px)';
    
    setTimeout(() => {
      hTitle.innerHTML = heroSlides[hIndex].title;
      hSub.textContent = heroSlides[hIndex].sub;
      
      // Animate in
      hTitle.style.opacity = '1';
      hTitle.style.transform = 'translateY(0)';
      hSub.style.opacity = '1';
      hSub.style.transform = 'translateY(0)';
      
      hDots.forEach((d, i) => d.classList.toggle('active', i === hIndex));
    }, 400);
  }

  function nextHero() {
    goToHero((hIndex + 1) % heroSlides.length);
  }

  hDots.forEach((dot, i) => {
    dot.addEventListener('click', () => {
      clearInterval(hInterval);
      goToHero(i);
      hInterval = setInterval(nextHero, 5000);
    });
  });
});

/* ── PRODUCT DETAIL SECTION ── */
let _pmCurrent = null;
const _mainSections = ['catalogo','wrap-promo-wrap','wrap-fav-wrap','banner','services','about-strip','js-tabs'];

function openProductModal(type, id, name, label, price, imgUrl, desc, stars, stock) {
  _pmCurrent = { type, id, name, price };

  document.getElementById('pdBreadcrumbLabel').textContent = name;
  document.getElementById('pdInfoLabel').textContent = label;
  document.getElementById('pdInfoName').textContent = name;
  document.getElementById('pdInfoPrice').textContent = price;

  // Middle breadcrumb — only for services
  const midEl = document.getElementById('pdBreadcrumbMid');
  const sep2El = document.getElementById('pdSep2');
  if (type === 'service') {
    midEl.textContent = 'Servicios adicionales';
    midEl.style.display = '';
    sep2El.style.display = '';
  } else {
    midEl.style.display = 'none';
    sep2El.style.display = 'none';
  }

  const starsEl = document.getElementById('pdInfoStars');
  if (stars) { starsEl.textContent = stars; starsEl.style.display = ''; }
  else starsEl.style.display = 'none';

  const descEl = document.getElementById('pdInfoDesc');
  if (desc) { descEl.textContent = desc; descEl.style.display = ''; }
  else descEl.style.display = 'none';

  const stockEl = document.getElementById('pdInfoStock');
  const stockNumEl = document.getElementById('pdStockNum');
  if (stock !== '' && stock !== null && stock !== undefined && stock !== '0') {
    stockNumEl.textContent = stock;
    stockEl.style.display = '';
  } else stockEl.style.display = 'none';

  const imgBox = document.getElementById('pdImgBox');
  if (imgUrl) {
    imgBox.innerHTML = `<img src="${imgUrl}" alt="${name}" onerror="this.parentElement.innerHTML='<div class=pd-img-placeholder>💐</div>'">`;
  } else {
    imgBox.innerHTML = '<div class="pd-img-placeholder">💐</div>';
  }

  // Reset qty and hide flow panel
  document.getElementById('pdQtyNum').textContent = '1';
  document.getElementById('pdFlowPanel').style.display = 'none';

  const buyBtn = document.getElementById('pdBuyBtn');
  if (type === 'flower') {
    buyBtn.textContent = '🌹 Diseñar mi ramo';
    buyBtn.onclick = () => { window.location.href = '/bouquet/design/'; };
    document.getElementById('pdQtyRow').style.display = 'none';
  } else {
    buyBtn.textContent = 'Comprar ahora →';
    buyBtn.onclick = showPdFlowPanel;
    document.getElementById('pdQtyRow').style.display = '';
  }

  // Wire guest button each time so qty is current
  document.getElementById('pdFlowGuest').onclick = () => {
    hidePdFlowPanel();
    openGc();
  };

  // Hide main page content, show detail section
  document.querySelectorAll('.tabs-wrap, .section, .banner-wrap, .services-bg, .about-strip').forEach(el => el.style.display = 'none');
  const pdSec = document.getElementById('pdSection');
  pdSec.classList.add('visible');
  window.scrollTo({ top: 0, behavior: 'smooth' });
}

function closePdSection() {
  document.getElementById('pdSection').classList.remove('visible');
  document.querySelectorAll('.tabs-wrap, .section, .banner-wrap, .services-bg, .about-strip').forEach(el => el.style.display = '');
  window.scrollTo({ top: 0, behavior: 'smooth' });
}

let _pdQty = 1;
function pdChangeQty(delta) {
  _pdQty = Math.max(1, _pdQty + delta);
  document.getElementById('pdQtyNum').textContent = _pdQty;
}
function showPdFlowPanel() {
  document.getElementById('pdFlowPanel').style.display = 'block';
  document.getElementById('pdBuyBtn').style.display = 'none';
}
function hidePdFlowPanel() {
  document.getElementById('pdFlowPanel').style.display = 'none';
  document.getElementById('pdBuyBtn').style.display = 'block';
}

function goToServices() {
  document.getElementById('pdSection').classList.remove('visible');
  document.querySelectorAll('.tabs-wrap, .section, .banner-wrap, .services-bg, .about-strip').forEach(el => el.style.display = '');
  setTimeout(() => {
    const sec = document.getElementById('section-servicios');
    if (sec) sec.scrollIntoView({ behavior: 'smooth', block: 'start' });
  }, 80);
}

/* ── GUEST CHECKOUT ── */
function openGc() {
  if (!_pmCurrent) return;
  document.getElementById('gcProductName').textContent = _pmCurrent.name;
  document.getElementById('gcProductPrice').textContent = _pmCurrent.price;
  document.getElementById('gcName').value = '';
  document.getElementById('gcOverlay').classList.add('open');
}
function closeGc() { document.getElementById('gcOverlay').classList.remove('open'); }
function closeGcIfBackground(e) { if (e.target === document.getElementById('gcOverlay')) closeGc(); }

async function _submitQuickOrder() {
  const name = document.getElementById('gcName').value.trim();
  if (!name) { document.getElementById('gcName').focus(); document.getElementById('gcName').style.borderColor = 'var(--rose)'; return; }

  const waBtn = document.getElementById('gcBtnWa');
  waBtn.disabled = true;
  waBtn.textContent = 'Procesando...';

  try {
    const resp = await fetch('/orders/quick-order/', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json', 'X-CSRFToken': '{{ csrf_token }}' },
      body: JSON.stringify({
        product_type: _pmCurrent.type,
        product_id: _pmCurrent.id,
        quantity: _pdQty,
        guest_data: { name }
      })
    });
    const result = await resp.json();
    if (result.status === 'success') {
      closeGc();
      if (result.whatsapp_message) {
        const waNumber = '{{ whatsapp_number }}';
        window.open(`https://wa.me/${waNumber}?text=${encodeURIComponent(result.whatsapp_message)}`, '_blank');
      }
      setTimeout(() => { window.location.href = `/orders/track/${result.tracking_token}/`; }, 1200);
    } else {
      alert('Error: ' + (result.error || 'No se pudo procesar el pedido.'));
    }
  } catch(e) {
    alert('Error de conexión. Por favor intenta de nuevo.');
  } finally {
    waBtn.disabled = false;
    waBtn.innerHTML = '<svg width="18" height="18" viewBox="0 0 24 24" fill="white"><path d="M17.472 14.382c-.297-.149-1.758-.867-2.03-.967-.273-.099-.471-.148-.67.15-.197.297-.767.966-.94 1.164-.173.199-.347.223-.644.075-.297-.15-1.255-.463-2.39-1.475-.883-.788-1.48-1.761-1.653-2.059-.173-.297-.018-.458.13-.606.134-.133.298-.347.446-.52.149-.174.198-.298.298-.497.099-.198.05-.371-.025-.52-.075-.149-.669-1.612-.916-2.207-.242-.579-.487-.5-.669-.51-.173-.008-.371-.01-.57-.01-.198 0-.52.074-.792.372-.272.297-1.04 1.016-1.04 2.479 0 1.462 1.065 2.875 1.213 3.074.149.198 2.096 3.2 5.077 4.487.709.306 1.262.489 1.694.625.712.227 1.36.195 1.871.118.571-.085 1.758-.719 2.006-1.413.248-.694.248-1.289.173-1.413-.074-.124-.272-.198-.57-.347m-5.421 7.403h-.004a9.87 9.87 0 01-5.031-1.378l-.361-.214-3.741.982.998-3.648-.235-.374a9.86 9.86 0 01-1.51-5.26c.001-5.45 4.436-9.884 9.888-9.884 2.64 0 5.122 1.03 6.988 2.898a9.825 9.825 0 012.893 6.994c-.003 5.45-4.437 9.884-9.885 9.884m8.413-18.297A11.815 11.815 0 0012.05 0C5.495 0 .16 5.335.157 11.892c0 2.096.547 4.142 1.588 5.945L.057 24l6.305-1.654a11.882 11.882 0 005.683 1.448h.005c6.554 0 11.89-5.335 11.893-11.893a11.821 11.821 0 00-3.48-8.413z"/></svg> Enviar pedido por WhatsApp';
  }
}

document.addEventListener('DOMContentLoaded', () => {
  document.getElementById('gcBtnWa').addEventListener('click', () => _submitQuickOrder());
});

// ── STATIC SERVICES LOGIC ──
function openStaticService(title, description, icon, imageUrl) {
  const iconMap = {
    '🧸': 'https://em-content.zobj.net/source/apple/354/teddy-bear_1f9f8.png',
    '✏️': 'https://em-content.zobj.net/source/apple/354/pencil_270f-fe0f.png',
    '🚚': 'https://em-content.zobj.net/source/apple/354/delivery-truck_1f69a.png',
    '💬': 'https://em-content.zobj.net/source/apple/354/speech-balloon_1f4ac.png'
  };

  let iconHtml = `<span>${icon || '✨'}</span>`;
  if (imageUrl) {
    iconHtml = `<img src="${imageUrl}" style="width:100px;height:100px;object-fit:contain;">`;
  } else if (iconMap[icon]) {
    iconHtml = `<img src="${iconMap[icon]}" style="width:100px;height:100px;object-fit:contain;">`;
  }

  document.getElementById('ssTitle').textContent = title;
  document.getElementById('ssBody').innerHTML = `
    <div style="text-align:center;margin:12px 0 16px;display:flex;justify-content:center;">${iconHtml}</div>
    <div style="margin-bottom:22px">
      <h3 style="font-family:var(--serif);font-size:1.1rem;margin-bottom:8px">Sobre este servicio</h3>
      <p style="font-size:.9rem;color:#555;line-height:1.7;margin:0">${description}</p>
    </div>
    <div style="display:flex;gap:12px;margin-top:4px">
      <button onclick="handleServiceContact('${title.replace(/'/g, "\\'")}')" style="flex:1;padding:12px;border-radius:10px;cursor:pointer;font-family:var(--sans);font-size:.9rem;font-weight:600;background:var(--rose);color:#fff;border:none;display:flex;align-items:center;justify-content:center;gap:8px;">
        <svg width="18" height="18" viewBox="0 0 24 24" fill="white"><path d="M17.472 14.382c-.297-.149-1.758-.867-2.03-.967-.273-.099-.471-.148-.67.15-.197.297-.767.966-.94 1.164-.173.199-.347.223-.644.075-.297-.15-1.255-.463-2.39-1.475-.883-.788-1.48-1.761-1.653-2.059-.173-.297-.018-.458.13-.606.134-.133.298-.347.446-.52.149-.174.198-.298.298-.497.099-.198.05-.371-.025-.52-.075-.149-.669-1.612-.916-2.207-.242-.579-.487-.5-.669-.51-.173-.008-.371-.01-.57-.01-.198 0-.52.074-.792.372-.272.297-1.04 1.016-1.04 2.479 0 1.462 1.065 2.875 1.213 3.074.149.198 2.096 3.2 5.077 4.487.709.306 1.262.489 1.694.625.712.227 1.36.195 1.871.118.571-.085 1.758-.719 2.006-1.413.248-.694.248-1.289.173-1.413-.074-.124-.272-.198-.57-.347m-5.421 7.403h-.004a9.87 9.87 0 01-5.031-1.378l-.361-.214-3.741.982.998-3.648-.235-.374a9.86 9.86 0 01-1.51-5.26c.001-5.45 4.436-9.884 9.888-9.884 2.64 0 5.122 1.03 6.988 2.898a9.825 9.825 0 012.893 6.994c-.003 5.45-4.437 9.884-9.885 9.884m8.413-18.297A11.815 11.815 0 0012.05 0C5.495 0 .16 5.335.157 11.892c0 2.096.547 4.142 1.588 5.945L.057 24l6.305-1.654a11.882 11.882 0 005.683 1.448h.005c6.554 0 11.89-5.335 11.893-11.893a11.821 11.821 0 00-3.48-8.413z"/></svg>
        WhatsApp
      </button>
      <button onclick="closeStaticService()" style="flex:1;padding:12px;border-radius:10px;cursor:pointer;font-family:var(--sans);font-size:.9rem;font-weight:600;background:#fff;color:var(--text);border:1.5px solid var(--border);">Cerrar</button>
    </div>
  `;
  document.getElementById('ssOverlay').classList.add('open');
}

function handleServiceContact(serviceName) {
  const waNumber = '{{ whatsapp_number }}';
  const message = `Hola Sisart! 🌸 Me gustaría obtener más información sobre el servicio: ${serviceName}.`;
  window.open(`https://wa.me/${waNumber}?text=${encodeURIComponent(message)}`, '_blank');
}
function closeStaticService() { document.getElementById('ssOverlay').classList.remove('open'); }
function closeStaticServiceIfBg(e) { if(e.target === document.getElementById('ssOverlay')) closeStaticService(); }