from PIL import Image, ImageDraw, ImageFont, ImageOps
import io
import requests
import logging
import os

logger = logging.getLogger(__name__)

class ImageGenerator:
    def __init__(self):
        # Rutas a recursos
        self.fonts_dir = 'bot/static/fonts'
        self.images_dir = 'bot/static/images'
        self.default_bg = os.path.join(self.images_dir, 'default_bg.png')
        
        # Asegurar directorios
        os.makedirs(self.fonts_dir, exist_ok=True)
        os.makedirs(self.images_dir, exist_ok=True)
        
        # Cargar fuentes (intentar cargar una fuente bonita si existe, sino default)
        try:
            # Intenta usar una fuente sans-serif común si está disponible en el sistema
            # Para producción, es mejor incluir un archivo .ttf en bot/static/fonts/
            self.font_large = ImageFont.truetype("arial.ttf", 60)
            self.font_small = ImageFont.truetype("arial.ttf", 40)
        except IOError:
            logger.warning("No se encontró arial.ttf, usando fuente por defecto. El texto podría verse pequeño.")
            self.font_large = ImageFont.load_default()
            # Intentar escalar la fuente por defecto si es posible (Pillow moderno)
            try:
                 self.font_large = ImageFont.load_default(size=60)
                 self.font_small = ImageFont.load_default(size=40)
            except TypeError:
                 # Fallback para versiones viejas de Pillow
                 self.font_large = ImageFont.load_default()
                 self.font_small = ImageFont.load_default()

    def generate(self, user_name, user_avatar_url, server_name, bg_color='#7289da', text_color='#ffffff', background_image_url=None, font_size=None):
        """Genera una imagen de bienvenida"""
        try:
            # 1. Configuración del lienzo
            width = 800
            height = 300  # Altura estándar para banners
            
            # 2. Crear fondo
            if background_image_url:
                try:
                    # Descargar imagen de fondo
                    response = requests.get(background_image_url, timeout=5)
                    response.raise_for_status()
                    background = Image.open(io.BytesIO(response.content)).convert('RGBA')
                    # Redimensionar y recortar para llenar el lienzo
                    background = ImageOps.fit(background, (width, height), method=Image.Resampling.LANCZOS, centering=(0.5, 0.5))
                except Exception as e:
                    logger.error(f"Error loading background image: {e}. Using color.")
                    background = Image.new('RGBA', (width, height), color=bg_color)
            else:
                # Usar color sólido
                background = Image.new('RGBA', (width, height), color=bg_color)

            # Crear capa de dibujo
            draw = ImageDraw.Draw(background)
            
            # 3. Procesar Avatar
            try:
                avatar_response = requests.get(user_avatar_url, timeout=5)
                avatar_response.raise_for_status()
                avatar = Image.open(io.BytesIO(avatar_response.content)).convert('RGBA')
                
                # Redimensionar avatar
                avatar_size = 180
                avatar = avatar.resize((avatar_size, avatar_size), Image.Resampling.LANCZOS)
                
                # Crear máscara circular
                mask = Image.new('L', (avatar_size, avatar_size), 0)
                draw_mask = ImageDraw.Draw(mask)
                draw_mask.ellipse((0, 0, avatar_size, avatar_size), fill=255)
                
                # Aplicar máscara
                avatar_circular = Image.new('RGBA', (avatar_size, avatar_size), (0, 0, 0, 0))
                avatar_circular.paste(avatar, (0, 0), mask=mask)
                
                # Pegar avatar en el fondo (centrado verticalmente a la izquierda)
                avatar_x = 60
                avatar_y = (height - avatar_size) // 2
                background.paste(avatar_circular, (avatar_x, avatar_y), mask=avatar_circular)
                
                # Definir inicio del texto a la derecha del avatar
                text_start_x = avatar_x + avatar_size + 40
                
            except Exception as e:
                logger.error(f"Error processing avatar: {e}")
                # Si falla el avatar, el texto empieza más a la izquierda
                text_start_x = 60

            # 4. Dibujar Texto
            welcome_text = "Bienvenido/a"
            username_text = user_name
            
            # Calcular el centro vertical del área de texto
            text_area_center_y = height // 2
            text_area_width = width - text_start_x - 20 # Espacio restante para texto

            # --- CORRECCIÓN DE POSICIÓN DEL TEXTO ---
            
            # Usamos 'anchor' para posicionar el texto más fácilmente.
            # 'ls' = left baseline (izquierda, línea base)
            # 'lt' = left top (izquierda, arriba)

            # Posición Y del texto de bienvenida (un poco más arriba del centro)
            welcome_y = text_area_center_y - 20
            
            draw.text(
                (text_start_x, welcome_y), 
                welcome_text, 
                font=self.font_large, 
                fill=text_color,
                anchor="ls" # Anclar la línea base del texto a la coordenada Y
            )

            # Posición Y del nombre de usuario (un poco más abajo del centro)
            username_y = text_area_center_y + 10

            draw.text(
                (text_start_x, username_y), 
                username_text, 
                font=self.font_small, 
                fill=text_color,
                anchor="lt" # Anclar la parte superior del texto a la coordenada Y
            )
            
            # 5. Guardar en buffer
            buffer = io.BytesIO()
            background.save(buffer, format='PNG')
            buffer.seek(0)
            
            return buffer

        except Exception as e:
            logger.error(f"Error generating image: {e}", exc_info=True)
            return None

# Instancia global
image_generator = ImageGenerator()