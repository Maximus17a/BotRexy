/**
 * Translations for BotRexy
 * Soporte multiidioma: Español, Inglés, Portugués
 */

const translations = {
    es: {
        // Navbar
        'nav.home': 'Inicio',
        'nav.dashboard': 'Dashboard',
        'nav.logout': 'Cerrar Sesión',
        'nav.login': 'Iniciar Sesión',
        'nav.invite': 'Invitar Bot',
        
        // Footer
        'footer.description': 'Bot de Discord con automoderación, niveles y más.',
        'footer.legal': 'Legal',
        'footer.privacy': 'Política de Privacidad',
        'footer.terms': 'Términos de Servicio',
        'footer.rights': 'Todos los derechos reservados.',
        
        // Welcome Config
        'welcome.title': 'Configurar Bienvenida',
        'welcome.back': 'Volver',
        'welcome.config': 'Configuración',
        'welcome.status': 'Estado',
        'welcome.enable': 'Activar mensajes de bienvenida',
        'welcome.channel': 'Canal de Bienvenida',
        'welcome.channel.loading': 'Cargando canales...',
        'welcome.channel.select': 'Selecciona un canal',
        'welcome.channel.help': 'Selecciona el canal donde se enviarán los mensajes de bienvenida.',
        'welcome.channel.manual': 'O ingresa el ID del canal manualmente:',
        'welcome.channel.manual.placeholder': 'ID del canal (ej: 1234567890)',
        'welcome.channel.manual.use': 'Usar',
        'welcome.channel.manual.help': 'Para obtener el ID: Discord → Configuración → Avanzado → Modo Desarrollador → Clic derecho en canal → Copiar ID',
        'welcome.channel.manual.option': '⚙️ Ingresar ID manualmente',
        'welcome.message': 'Mensaje de Bienvenida',
        'welcome.message.placeholder': '¡Bienvenido {user} a {server}!',
        'welcome.message.variables': 'Variables disponibles:',
        'welcome.image': 'Imagen de Bienvenida',
        'welcome.image.enable': 'Incluir imagen personalizada',
        'welcome.image.background': 'Imagen de Fondo',
        'welcome.image.background.help': 'Sube una imagen personalizada para el fondo (máx. 5MB). Si no subes ninguna, se usará el color de fondo.',
        'welcome.image.current': 'Imagen actual:',
        'welcome.image.remove': 'Eliminar',
        'welcome.image.bgcolor': 'Color de Fondo (alternativo)',
        'welcome.image.bgcolor.help': 'Se usa si no hay imagen de fondo',
        'welcome.image.textcolor': 'Color de Texto',
        'welcome.save': 'Guardar Cambios',
        'welcome.preview': 'Vista Previa',
        'welcome.preview.title': 'Vista Previa',
        'welcome.preview.text': 'Haz clic en "Vista Previa" para ver cómo se verá la imagen de bienvenida.',
        'welcome.help': 'Ayuda',
        'welcome.help.variables': 'Variables de Mensaje:',
        'welcome.help.customization': 'Personalización de Imagen:',
        'welcome.help.customization.text': 'Puedes personalizar los colores de fondo y texto de la imagen de bienvenida para que coincidan con el tema de tu servidor.',
        
        // Alerts
        'alert.file.size': 'El archivo es demasiado grande',
        'alert.file.maxsize': 'El tamaño máximo es 5MB.',
        'alert.file.yoursize': 'Tu archivo:',
        'alert.upload.error': 'Error al subir la imagen:',
        'alert.upload.success': 'Imagen subida correctamente',
        'alert.save.success': 'Configuración guardada correctamente',
        'alert.save.error': 'Error al guardar configuración',
        'alert.preview.error': 'Error al generar vista previa',
        'alert.remove.confirm': '¿Estás seguro de que quieres eliminar la imagen de fondo?',
        'alert.remove.success': 'Imagen de fondo eliminada correctamente',
        'alert.remove.error': 'Error al eliminar la imagen de fondo',
        'alert.channel.invalid': 'Por favor ingresa un ID de canal válido (solo números)',
        
        // Common
        'common.loading': 'Cargando...',
        'common.error': 'Error',
        'common.success': 'Éxito',
    },
    
    en: {
        // Navbar
        'nav.home': 'Home',
        'nav.dashboard': 'Dashboard',
        'nav.logout': 'Logout',
        'nav.login': 'Login',
        'nav.invite': 'Invite Bot',
        
        // Footer
        'footer.description': 'Discord bot with automoderation, levels and more.',
        'footer.legal': 'Legal',
        'footer.privacy': 'Privacy Policy',
        'footer.terms': 'Terms of Service',
        'footer.rights': 'All rights reserved.',
        
        // Welcome Config
        'welcome.title': 'Configure Welcome',
        'welcome.back': 'Back',
        'welcome.config': 'Configuration',
        'welcome.status': 'Status',
        'welcome.enable': 'Enable welcome messages',
        'welcome.channel': 'Welcome Channel',
        'welcome.channel.loading': 'Loading channels...',
        'welcome.channel.select': 'Select a channel',
        'welcome.channel.help': 'Select the channel where welcome messages will be sent.',
        'welcome.channel.manual': 'Or enter the channel ID manually:',
        'welcome.channel.manual.placeholder': 'Channel ID (e.g.: 1234567890)',
        'welcome.channel.manual.use': 'Use',
        'welcome.channel.manual.help': 'To get the ID: Discord → Settings → Advanced → Developer Mode → Right click on channel → Copy ID',
        'welcome.channel.manual.option': '⚙️ Enter ID manually',
        'welcome.message': 'Welcome Message',
        'welcome.message.placeholder': 'Welcome {user} to {server}!',
        'welcome.message.variables': 'Available variables:',
        'welcome.image': 'Welcome Image',
        'welcome.image.enable': 'Include custom image',
        'welcome.image.background': 'Background Image',
        'welcome.image.background.help': 'Upload a custom image for the background (max 5MB). If you don\'t upload one, the background color will be used.',
        'welcome.image.current': 'Current image:',
        'welcome.image.remove': 'Remove',
        'welcome.image.bgcolor': 'Background Color (alternative)',
        'welcome.image.bgcolor.help': 'Used if there is no background image',
        'welcome.image.textcolor': 'Text Color',
        'welcome.save': 'Save Changes',
        'welcome.preview': 'Preview',
        'welcome.preview.title': 'Preview',
        'welcome.preview.text': 'Click "Preview" to see how the welcome image will look.',
        'welcome.help': 'Help',
        'welcome.help.variables': 'Message Variables:',
        'welcome.help.customization': 'Image Customization:',
        'welcome.help.customization.text': 'You can customize the background and text colors of the welcome image to match your server theme.',
        
        // Alerts
        'alert.file.size': 'The file is too large',
        'alert.file.maxsize': 'Maximum size is 5MB.',
        'alert.file.yoursize': 'Your file:',
        'alert.upload.error': 'Error uploading image:',
        'alert.upload.success': 'Image uploaded successfully',
        'alert.save.success': 'Configuration saved successfully',
        'alert.save.error': 'Error saving configuration',
        'alert.preview.error': 'Error generating preview',
        'alert.remove.confirm': 'Are you sure you want to remove the background image?',
        'alert.remove.success': 'Background image removed successfully',
        'alert.remove.error': 'Error removing background image',
        'alert.channel.invalid': 'Please enter a valid channel ID (numbers only)',
        
        // Common
        'common.loading': 'Loading...',
        'common.error': 'Error',
        'common.success': 'Success',
    },
    
    pt: {
        // Navbar
        'nav.home': 'Início',
        'nav.dashboard': 'Painel',
        'nav.logout': 'Sair',
        'nav.login': 'Entrar',
        'nav.invite': 'Convidar Bot',
        
        // Footer
        'footer.description': 'Bot do Discord com automoderação, níveis e mais.',
        'footer.legal': 'Legal',
        'footer.privacy': 'Política de Privacidade',
        'footer.terms': 'Termos de Serviço',
        'footer.rights': 'Todos os direitos reservados.',
        
        // Welcome Config
        'welcome.title': 'Configurar Boas-vindas',
        'welcome.back': 'Voltar',
        'welcome.config': 'Configuração',
        'welcome.status': 'Status',
        'welcome.enable': 'Ativar mensagens de boas-vindas',
        'welcome.channel': 'Canal de Boas-vindas',
        'welcome.channel.loading': 'Carregando canais...',
        'welcome.channel.select': 'Selecione um canal',
        'welcome.channel.help': 'Selecione o canal onde as mensagens de boas-vindas serão enviadas.',
        'welcome.channel.manual': 'Ou insira o ID do canal manualmente:',
        'welcome.channel.manual.placeholder': 'ID do canal (ex: 1234567890)',
        'welcome.channel.manual.use': 'Usar',
        'welcome.channel.manual.help': 'Para obter o ID: Discord → Configurações → Avançado → Modo Desenvolvedor → Clique com botão direito no canal → Copiar ID',
        'welcome.channel.manual.option': '⚙️ Inserir ID manualmente',
        'welcome.message': 'Mensagem de Boas-vindas',
        'welcome.message.placeholder': 'Bem-vindo {user} ao {server}!',
        'welcome.message.variables': 'Variáveis disponíveis:',
        'welcome.image': 'Imagem de Boas-vindas',
        'welcome.image.enable': 'Incluir imagem personalizada',
        'welcome.image.background': 'Imagem de Fundo',
        'welcome.image.background.help': 'Envie uma imagem personalizada para o fundo (máx. 5MB). Se você não enviar uma, a cor de fundo será usada.',
        'welcome.image.current': 'Imagem atual:',
        'welcome.image.remove': 'Remover',
        'welcome.image.bgcolor': 'Cor de Fundo (alternativa)',
        'welcome.image.bgcolor.help': 'Usado se não houver imagem de fundo',
        'welcome.image.textcolor': 'Cor do Texto',
        'welcome.save': 'Salvar Alterações',
        'welcome.preview': 'Visualizar',
        'welcome.preview.title': 'Visualização',
        'welcome.preview.text': 'Clique em "Visualizar" para ver como a imagem de boas-vindas ficará.',
        'welcome.help': 'Ajuda',
        'welcome.help.variables': 'Variáveis de Mensagem:',
        'welcome.help.customization': 'Personalização de Imagem:',
        'welcome.help.customization.text': 'Você pode personalizar as cores de fundo e texto da imagem de boas-vindas para combinar com o tema do seu servidor.',
        
        // Alerts
        'alert.file.size': 'O arquivo é muito grande',
        'alert.file.maxsize': 'O tamanho máximo é 5MB.',
        'alert.file.yoursize': 'Seu arquivo:',
        'alert.upload.error': 'Erro ao enviar imagem:',
        'alert.upload.success': 'Imagem enviada com sucesso',
        'alert.save.success': 'Configuração salva com sucesso',
        'alert.save.error': 'Erro ao salvar configuração',
        'alert.preview.error': 'Erro ao gerar visualização',
        'alert.remove.confirm': 'Tem certeza de que deseja remover a imagem de fundo?',
        'alert.remove.success': 'Imagem de fundo removida com sucesso',
        'alert.remove.error': 'Erro ao remover imagem de fundo',
        'alert.channel.invalid': 'Por favor, insira um ID de canal válido (apenas números)',
        
        // Common
        'common.loading': 'Carregando...',
        'common.error': 'Erro',
        'common.success': 'Sucesso',
    }
};

// Función para obtener traducción
function t(key, lang = null) {
    const currentLang = lang || getCurrentLanguage();
    return translations[currentLang]?.[key] || translations['es'][key] || key;
}

// Obtener idioma actual
function getCurrentLanguage() {
    return localStorage.getItem('language') || 'es';
}

// Cambiar idioma
function setLanguage(lang) {
    if (!translations[lang]) {
        console.error('Language not supported:', lang);
        return;
    }
    
    localStorage.setItem('language', lang);
    updatePageLanguage();
}

// Actualizar idioma de la página
function updatePageLanguage() {
    const lang = getCurrentLanguage();
    document.documentElement.setAttribute('lang', lang);
    
    // Actualizar todos los elementos con data-i18n
    document.querySelectorAll('[data-i18n]').forEach(element => {
        const key = element.getAttribute('data-i18n');
        const translation = t(key);
        
        if (element.tagName === 'INPUT' && element.type === 'text') {
            element.placeholder = translation;
        } else {
            element.textContent = translation;
        }
    });
    
    // Actualizar placeholders
    document.querySelectorAll('[data-i18n-placeholder]').forEach(element => {
        const key = element.getAttribute('data-i18n-placeholder');
        element.placeholder = t(key);
    });
    
    // Actualizar títulos
    document.querySelectorAll('[data-i18n-title]').forEach(element => {
        const key = element.getAttribute('data-i18n-title');
        element.title = t(key);
    });
}

// Inicializar al cargar la página
document.addEventListener('DOMContentLoaded', function() {
    updatePageLanguage();
    
    // Crear selector de idioma si no existe
    if (!document.getElementById('languageSelector')) {
        createLanguageSelector();
    }
});

// Crear selector de idioma
function createLanguageSelector() {
    const currentLang = getCurrentLanguage();
    
    const selector = document.createElement('div');
    selector.id = 'languageSelector';
    selector.className = 'language-selector';
    selector.innerHTML = `
        <button class="language-btn ${currentLang === 'es' ? 'active' : ''}" data-lang="es" title="Español">🇪🇸</button>
        <button class="language-btn ${currentLang === 'en' ? 'active' : ''}" data-lang="en" title="English">🇺🇸</button>
        <button class="language-btn ${currentLang === 'pt' ? 'active' : ''}" data-lang="pt" title="Português">🇧🇷</button>
    `;
    
    // Agregar event listeners
    selector.querySelectorAll('.language-btn').forEach(btn => {
        btn.addEventListener('click', function() {
            const lang = this.getAttribute('data-lang');
            setLanguage(lang);
            
            // Actualizar botones activos
            selector.querySelectorAll('.language-btn').forEach(b => b.classList.remove('active'));
            this.classList.add('active');
            
            // Recargar la página para aplicar cambios
            location.reload();
        });
    });
    
    document.body.appendChild(selector);
}

// Exportar funciones
window.t = t;
window.setLanguage = setLanguage;
window.getCurrentLanguage = getCurrentLanguage;
