/**
 * Theme Toggle - Dark Mode Controller
 * Maneja el cambio entre modo claro y oscuro
 */

(function() {
    'use strict';
    
    // Obtener tema guardado o usar preferencia del sistema
    function getInitialTheme() {
        const savedTheme = localStorage.getItem('theme');
        if (savedTheme) {
            return savedTheme;
        }
        
        // Verificar preferencia del sistema
        if (window.matchMedia && window.matchMedia('(prefers-color-scheme: dark)').matches) {
            return 'dark';
        }
        
        return 'light';
    }
    
    // Aplicar tema
    function applyTheme(theme) {
        document.documentElement.setAttribute('data-theme', theme);
        localStorage.setItem('theme', theme);
        
        // Actualizar icono del botón
        const themeToggle = document.getElementById('themeToggle');
        if (themeToggle) {
            const icon = themeToggle.querySelector('i');
            if (icon) {
                if (theme === 'dark') {
                    icon.className = 'bi bi-sun-fill';
                } else {
                    icon.className = 'bi bi-moon-fill';
                }
            }
        }
    }
    
    // Alternar tema
    function toggleTheme() {
        const currentTheme = document.documentElement.getAttribute('data-theme') || 'light';
        const newTheme = currentTheme === 'light' ? 'dark' : 'light';
        applyTheme(newTheme);
    }
    
    // Inicializar al cargar la página
    document.addEventListener('DOMContentLoaded', function() {
        const initialTheme = getInitialTheme();
        applyTheme(initialTheme);
        
        // Crear botón de cambio de tema si no existe
        if (!document.getElementById('themeToggle')) {
            const button = document.createElement('button');
            button.id = 'themeToggle';
            button.className = 'theme-toggle';
            button.setAttribute('aria-label', 'Cambiar tema');
            button.innerHTML = '<i class="bi bi-moon-fill"></i>';
            button.addEventListener('click', toggleTheme);
            document.body.appendChild(button);
        } else {
            // Si ya existe, agregar event listener
            document.getElementById('themeToggle').addEventListener('click', toggleTheme);
        }
    });
    
    // Escuchar cambios en la preferencia del sistema
    if (window.matchMedia) {
        window.matchMedia('(prefers-color-scheme: dark)').addEventListener('change', function(e) {
            // Solo aplicar si no hay preferencia guardada
            if (!localStorage.getItem('theme')) {
                applyTheme(e.matches ? 'dark' : 'light');
            }
        });
    }
})();
