// BotRexy Main JavaScript

// Get CSRF Token from meta tag
const csrfToken = document.querySelector('meta[name="csrf-token"]')?.getAttribute('content');

// Utility function for API calls
async function apiCall(url, method = 'GET', data = null) {
    const headers = {
        'Content-Type': 'application/json'
    };
    
    // Add CSRF token to headers for non-GET requests
    if (method !== 'GET' && csrfToken) {
        headers['X-CSRFToken'] = csrfToken;
    }

    const options = {
        method: method,
        headers: headers
    };
    
    if (data) {
        options.body = JSON.stringify(data);
    }
    
    try {
        const response = await fetch(url, options);
        return await response.json();
    } catch (error) {
        console.error('API call error:', error);
        throw error;
    }
}

// Interceptor global para fetch (para scripts inline que no usan apiCall)
const originalFetch = window.fetch;
window.fetch = async function(url, options = {}) {
    // Si no es GET y no tiene el header CSRF, agregarlo
    if (options.method && options.method.toUpperCase() !== 'GET') {
        options.headers = options.headers || {};
        
        // Manejar Headers object o objeto plano
        if (options.headers instanceof Headers) {
            if (!options.headers.has('X-CSRFToken') && csrfToken) {
                options.headers.append('X-CSRFToken', csrfToken);
            }
        } else {
            if (!options.headers['X-CSRFToken'] && csrfToken) {
                options.headers['X-CSRFToken'] = csrfToken;
            }
        }
    }
    return originalFetch(url, options);
};

// ... (Resto de las funciones: showLoading, hideLoading, showToast, etc. sin cambios) ...

// Show loading spinner
function showLoading(element) {
    const spinner = document.createElement('span');
    spinner.className = 'loading ms-2';
    element.appendChild(spinner);
}

function hideLoading(element) {
    const spinner = element.querySelector('.loading');
    if (spinner) {
        spinner.remove();
    }
}

function showToast(message, type = 'info') {
    let toastContainer = document.getElementById('toastContainer');
    if (!toastContainer) {
        toastContainer = document.createElement('div');
        toastContainer.id = 'toastContainer';
        toastContainer.className = 'position-fixed top-0 end-0 p-3';
        toastContainer.style.zIndex = '9999';
        document.body.appendChild(toastContainer);
    }
    
    const toastId = 'toast-' + Date.now();
    const toastHTML = `
        <div id="${toastId}" class="toast align-items-center text-white bg-${type} border-0" role="alert" aria-live="assertive" aria-atomic="true">
            <div class="d-flex">
                <div class="toast-body">
                    ${message}
                </div>
                <button type="button" class="btn-close btn-close-white me-2 m-auto" data-bs-dismiss="toast" aria-label="Close"></button>
            </div>
        </div>
    `;
    
    toastContainer.insertAdjacentHTML('beforeend', toastHTML);
    const toastElement = document.getElementById(toastId);
    const toast = new bootstrap.Toast(toastElement, { autohide: true, delay: 3000 });
    toast.show();
    
    toastElement.addEventListener('hidden.bs.toast', function () {
        toastElement.remove();
    });
}

function copyToClipboard(text) {
    navigator.clipboard.writeText(text).then(() => {
        showToast('Copiado al portapapeles', 'success');
    }).catch(err => {
        showToast('Error al copiar', 'danger');
    });
}

function formatDate(dateString) {
    const date = new Date(dateString);
    return date.toLocaleDateString('es-ES', {
        year: 'numeric', month: 'long', day: 'numeric', hour: '2-digit', minute: '2-digit'
    });
}

// Export functions
window.BotRexy = {
    apiCall, showLoading, hideLoading, showToast, copyToClipboard, formatDate
};