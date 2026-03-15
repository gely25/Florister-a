let currentItem = null;
    let currentQty = 1;

    function openDetails(data) {
        currentItem = data;
        currentQty = 1;
        
        document.getElementById('modalName').innerText = data.name;
        document.getElementById('modalPrice').innerText = '$' + data.price;
        document.getElementById('modalDesc').innerText = data.desc || 'Sin descripción disponible.';
        document.getElementById('modalLabel').innerText = data.label;
        document.getElementById('qtyNum').innerText = '1';

        const imgBox = document.getElementById('modalImgBox');
        if (data.img && data.img !== 'None') {
            imgBox.innerHTML = `<img src="${data.img}" alt="${data.name}">`;
        } else {
            imgBox.innerHTML = `<div style="font-size:6rem; opacity:0.1;">💐</div>`;
        }

        // Toggle flow based on type
        if (data.type === 'flower') {
            document.getElementById('orderControls').style.display = 'none';
            document.getElementById('flowerDesignerLink').style.display = 'block';
        } else {
            document.getElementById('orderControls').style.display = 'block';
            document.getElementById('flowerDesignerLink').style.display = 'none';
        }

        document.getElementById('productModal').classList.add('open');
        lucide.createIcons();
    }

    function closeDetails() {
        document.getElementById('productModal').classList.remove('open');
    }

    function updateQty(delta) {
        currentQty = Math.max(1, currentQty + delta);
        document.getElementById('qtyNum').innerText = currentQty;
    }

    document.getElementById('confirmBuyBtn').onclick = async () => {
        const btn = document.getElementById('confirmBuyBtn');
        btn.disabled = true;
        btn.innerHTML = '<i data-lucide="loader"></i> Procesando...';
        lucide.createIcons();

        try {
            const resp = await fetch('/orders/quick-order/', {
                method: 'POST',
                headers: { 
                    'Content-Type': 'application/json',
                    'X-CSRFToken': window.SISART_CONFIG.csrfToken 
                },
                body: JSON.stringify({
                    product_type: currentItem.type,
                    product_id: currentItem.id,
                    quantity: currentQty
                })
            });
            const res = await resp.json();
            if (res.status === 'success') {
                const waNumber = window.SISART_CONFIG.whatsappNumber;
                window.open(`https://wa.me/${waNumber}?text=${encodeURIComponent(res.whatsapp_message)}`, '_blank');
                window.location.href = `/orders/track/${res.tracking_token}/`;
            } else {
                alert('Error: ' + res.error);
                btn.disabled = false;
                btn.innerHTML = '<i data-lucide="message-circle"></i> Confirmar por WhatsApp';
                lucide.createIcons();
            }
        } catch(e) {
            alert('Error de conexión');
            btn.disabled = false;
            btn.innerHTML = '<i data-lucide="message-circle"></i> Confirmar por WhatsApp';
            lucide.createIcons();
        }
    };

    // Filter Logic
    document.querySelectorAll('.nav-btn').forEach(btn => {
        btn.onclick = () => {
            const filter = btn.getAttribute('data-filter');
            document.querySelectorAll('.nav-btn').forEach(b => b.classList.remove('active'));
            btn.classList.add('active');

            document.querySelectorAll('.product-item').forEach(item => {
                if (filter === 'all' || item.getAttribute('data-type') === filter) {
                    item.style.display = 'flex';
                } else {
                    item.style.display = 'none';
                }
            });
        };
    });

    // Close modal on click outside
    document.getElementById('productModal').onclick = (e) => {
        if (e.target.id === 'productModal') closeDetails();
    };