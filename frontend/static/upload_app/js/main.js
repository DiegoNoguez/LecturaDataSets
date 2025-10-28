// ✅ FRONTEND: JavaScript puro para interactividad

document.addEventListener('DOMContentLoaded', function() {
    initializeApp();
});

function initializeApp() {
    initializeFileInput();
    initializeFormValidation();
}

function initializeFileInput() {
    const fileInput = document.getElementById('datasetFile');
    const fileInfo = document.getElementById('fileInfo');
    const submitBtn = document.getElementById('submitBtn');
    
    if (fileInput && fileInfo) {
        fileInput.addEventListener('change', function(e) {
            const file = e.target.files[0];
            if (file) {
                const fileSize = formatFileSize(file.size);
                fileInfo.innerHTML = `
                    <strong>📄 ${file.name}</strong>
                    <br>
                    <small>Tamaño: ${fileSize} | Tipo: ${file.type || 'No especificado'}</small>
                `;
                
                // Validar tipo de archivo
                const fileName = file.name.toLowerCase();
                if (!fileName.endsWith('.txt') && !fileName.endsWith('.arff')) {
                    showError('Solo se permiten archivos .txt o .arff');
                    submitBtn.disabled = true;
                } else {
                    hideError();
                    submitBtn.disabled = false;
                }
            } else {
                fileInfo.textContent = 'No se ha seleccionado ningún archivo';
                submitBtn.disabled = false;
            }
        });
    }
}

function initializeFormValidation() {
    const form = document.getElementById('uploadForm');
    if (form) {
        form.addEventListener('submit', function(e) {
            const fileInput = document.getElementById('datasetFile');
            const file = fileInput.files[0];
            
            if (!file) {
                e.preventDefault();
                showError('Por favor, selecciona un archivo');
                return;
            }
            
            // Mostrar loading
            const submitBtn = document.querySelector('.submit-btn');
            if (submitBtn) {
                submitBtn.innerHTML = '⏳ Procesando...';
                submitBtn.disabled = true;
            }
        });
    }
}

function formatFileSize(bytes) {
    if (bytes === 0) return '0 Bytes';
    const k = 1024;
    const sizes = ['Bytes', 'KB', 'MB', 'GB'];
    const i = Math.floor(Math.log(bytes) / Math.log(k));
    return parseFloat((bytes / Math.pow(k, i)).toFixed(2)) + ' ' + sizes[i];
}

function showError(message) {
    // Buscar o crear elemento de error
    let errorElement = document.querySelector('.error-message');
    if (!errorElement) {
        errorElement = document.createElement('div');
        errorElement.className = 'error-message';
        const form = document.querySelector('.upload-form');
        if (form) {
            form.parentNode.insertBefore(errorElement, form);
        }
    }
    
    errorElement.innerHTML = `<span class="error-icon">⚠️</span> ${message}`;
    errorElement.style.display = 'block';
}

function hideError() {
    const errorElement = document.querySelector('.error-message');
    if (errorElement) {
        errorElement.style.display = 'none';
    }
}

// Efectos visuales adicionales
document.addEventListener('DOMContentLoaded', function() {
    // Animación de entrada para las tarjetas
    const cards = document.querySelectorAll('.info-card, .upload-section, .results-card');
    cards.forEach((card, index) => {
        card.style.opacity = '0';
        card.style.transform = 'translateY(20px)';
        
        setTimeout(() => {
            card.style.transition = 'all 0.5s ease';
            card.style.opacity = '1';
            card.style.transform = 'translateY(0)';
        }, index * 100);
    });
});