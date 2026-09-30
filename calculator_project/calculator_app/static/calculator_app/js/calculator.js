document.addEventListener('DOMContentLoaded', function() {
    const input = document.getElementById('expression-input');
    const buttons = document.querySelectorAll('.btn-num, .btn-operator');
    const clearBtn = document.getElementById('clear-btn');
    const form = document.querySelector('.calculator-form');
    
    // Add click events to number and operator buttons
    buttons.forEach(button => {
        button.addEventListener('click', function(e) {
            e.preventDefault();
            const value = this.dataset.value;
            if (value !== undefined) {
                // Append value to input
                input.value += value;
                input.focus();
            }
        });
    });
    
    // Clear button
    if (clearBtn) {
        clearBtn.addEventListener('click', function(e) {
            e.preventDefault();
            input.value = '';
            input.focus();
        });
    }
    
    // Keyboard support
    input.addEventListener('keydown', function(e) {
        // Allow Enter key to submit
        if (e.key === 'Enter') {
            e.preventDefault();
            form.submit();
        }
        
        // Allow Escape key to clear
        if (e.key === 'Escape') {
            e.preventDefault();
            input.value = '';
        }
    });
    
    // Auto-focus on input
    input.focus();
    
    // Highlight input on focus
    input.addEventListener('focus', function() {
        this.select();
    });
    
    // Add some useful keyboard shortcuts
    document.addEventListener('keydown', function(e) {
        // Focus input when typing numbers or operators
        const key = e.key;
        if (/^[0-9+\-*/.()%]$/.test(key) && document.activeElement !== input) {
            e.preventDefault();
            input.value += key;
            input.focus();
        }
    });
});