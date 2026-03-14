async function updateStatus() {
        const status = document.getElementById('statusSelect').value;
        const formData = new FormData();
        formData.append('status', status);
        formData.append('csrfmiddlewaretoken', '{{ csrf_token }}');

        try {
            const res = await fetch("{% url 'orders:update_status' order.id %}", {
                method: 'POST',
                body: formData
            });
            const data = await res.json();
            if (data.status === 'success') {
                alert('Estado actualizado correctamente.');
                window.location.reload();
            } else {
                alert('Error: ' + data.error);
            }
        } catch(e) {
            alert('Error de conexión');
        }
    }