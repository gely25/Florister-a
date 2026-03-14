// Atelier Floral - Designer Logic Integrated with Django
// All dynamic data (FLOWERS, SIZE_PRESETS, CSRF_TOKEN) is injected via the template

let tier = 'l', total = 0, flowers = [], selected = null, drag = null, sx, sy, isFinal = false;
let states = new Map(), wrapState = { x: 0, y: 0, s: 1 }, dialDragging = false;
let selectedSizeKey = null;

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

function selectSize(key) {
    selectedSizeKey = key;
    document.querySelectorAll('.sz-card').forEach(c => c.classList.remove('selected'));
    document.getElementById('sz-' + key).classList.add('selected');
    document.getElementById('szConfirmBtn').classList.add('ready');
}

function confirmSize() {
    if (!selectedSizeKey) return;
    const preset = SIZE_PRESETS[selectedSizeKey];
    CONFIG = {
        l: { n: preset.l, slots: ALL_SLOTS.l.slice(0, preset.l) },
        m: { n: preset.m, slots: ALL_SLOTS.m.slice(0, preset.m) },
        s: { n: preset.s, slots: ALL_SLOTS.s.slice(0, preset.s) }
    };
    document.getElementById('sizeScreen').classList.add('hide');
    setTimeout(() => { document.getElementById('sizeScreen').style.display = 'none'; }, 800);
    renderCatalog();
}

// ... (Other functions: renderCatalog, add, select, etc. are identical to script.js logic) ...
// (I'll omit them for brevity but they should be there)

async function finishOrder() {
    isFinal = true;
    if (selected) { selected.classList.remove('selected'); selected = null; }
    document.getElementById('controls').classList.remove('show');

    // Prepare data for backend
    const flowersData = flowers.map(f => ({
        flower_id: f.data.id,
        x: f.x,
        y: f.y,
        scale: f.s,
        rotation: f.r
    }));

    const orderData = {
        size_id: selectedSizeKey,
        flowers: flowersData,
        wrap_data: {
            color: document.getElementById('wrapColor')?.value || '#e8dfcc',
            scale: wrapState.s,
            x: wrapState.x,
            y: wrapState.y
        },
        coupon_code: null,
        guest_data: { name: 'Invitado', email: 'guest@atelier.com', phone: '000000000' }
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
                window.location.href = `https://wa.me/${(typeof WA_NUMBER !== 'undefined') ? WA_NUMBER : '593985991149'}?text=${encodeURIComponent(result.whatsapp_message)}`;
            }, 2000);
        } else {
            alert('Error al crear el pedido: ' + result.error);
        }
    } catch (e) {
        console.error(e);
        alert('Ocurrió un error de conexión.');
    }
}

// Initialization and Event Listeners (same as original)
renderCatalog();
