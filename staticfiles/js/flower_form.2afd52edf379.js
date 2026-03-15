function stepPrice(btn, amount) {
        const wrapper = btn.closest('.custom-number-input');
        const input = wrapper.querySelector('input[type="number"]');
        
        // Handle comma as decimal separator
        let currentString = input.value.replace(',', '.');
        let val = parseFloat(currentString) || 0;
        
        val += amount;
        if (val < 0) val = 0;
        
        // Always strictly 2 decimal places
        input.value = val.toFixed(2);
    }
    
    // Auto-format on blur
    document.addEventListener('DOMContentLoaded', () => {
        document.querySelectorAll('.custom-number-input input[type="number"]').forEach(input => {
            input.addEventListener('blur', function() {
                let val = parseFloat(this.value.replace(',', '.')) || 0;
                this.value = val.toFixed(2);
            });
        });
    });