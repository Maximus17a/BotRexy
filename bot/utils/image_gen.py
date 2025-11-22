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
        
        # Asegurar directorios
        os.makedirs(self.fonts_dir, exist_ok=True)
        os.makedirs(self.images_dir, exist_ok=True)
        
        # --- CONFIGURACIÓN DE FUENTES ---
        # Intentamos cargar las fuentes Montserrat para un estilo "bello".
        # Si no están, se usará una fuente por defecto (que no se verá igual).
        try:
            # Fuente GRANDE y NEGRITA para el nombre de usuario (ej. 110px)
            self.font_username = ImageFont.truetype(os.path.join(self.fonts_dir, "Montserrat-Bold.ttf"), 110)
            # Fuente más pequeña para "Bienvenido/a" (ej. 50px)
            self.font_welcome = ImageFont.truetype(os.path.join(self.fonts_dir, "Montserrat-Regular.ttf"), 50)
        except IOError:
            logger.warning("NO SE ENCONTRARON LAS FUENTES MONTSERRAT EN bot/static/fonts/. Usando fuente por defecto. El resultado NO será como la imagen de ejemplo.")
            # Fallback para que no rompa si faltan las fuentes
            try:
                 self.font_username = ImageFont.load_default(size=110)
                 self.font_welcome = ImageFont.load_default(size=50)
            except TypeError: # Para versiones viejas de Pillow
                 self.font_username = ImageFont.load_default()
                 self.font_welcome = ImageFont.load_default()

    def generate(self, user_name, user_avatar_url, server_name, bg_color='#7289da', text_color='#ffffff', background_image_url=None, font_size=None):
        """Genera una imagen de bienvenida estilo profesional"""
        try:
            # 1. Configuración del lienzo
            width = 1000 # Lienzo más ancho para fuentes grandes
            height = 400 # Lienzo más alto
            
            # 2. Crear fondo
            if background_image_url:
                try:
                    # Descargar imagen de fondo
                    response = requests.get(background_image_url, timeout=5)
                    response.raise_for_status()
                    background = Image.open(io.BytesIO(response.content)).convert('RGBA')
                    # Redimensionar y recortar para llenar el lienzo (Cover)
                    background = ImageOps.fit(background, (width, height), method=Image.Resampling.LANCZOS, centering=(0.5, 0.5))
                except Exception as e:
                    logger.error(f"Error loading background image: {e}. Using color.")
                    background = Image.new('RGBA', (width, height), color=bg_color)
            else:
                # Usar color sólido
                background = Image.new('RGBA', (width, height), color=bg_color)

            # --- APLICAR CAPA OSCURA (OVERLAY) ---
            # Esto oscurece el fondo para que el texto blanco resalte, igual que en el ejemplo.
            # (0, 0, 0, 130) significa negro con una opacidad de ~50%
            overlay = Image.new('RGBA', background.size, (0, 0, 0, 130))
            background = Image.alpha_composite(background, overlay)

            # Crear capa de dibujo sobre el fondo oscurecido
            draw = ImageDraw.Draw(background)
            
            # 3. Procesar Avatar
            avatar_size = 250 # Avatar más grande
            try:
                avatar_response = requests.get(user_avatar_url, timeout=5)
                avatar_response.raise_for_status()
                avatar = Image.open(io.BytesIO(avatar_response.content)).convert('RGBA')
                
                # Redimensionar avatar con alta calidad
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
                text_start_x = avatar_x + avatar_size + 50
                
            except Exception as e:
                logger.error(f"Error processing avatar: {e}")
                text_start_x = 60

            # 4. Dibujar Texto (Layout preciso)
            welcome_text = "Bienvenido/a"
            username_text = user_name
            
            # --- CÁLCULO PARA CENTRAR EL BLOQUE DE TEXTO VERTICALMENTE ---
            # Obtenemos la altura real de cada línea de texto
            welcome_bbox = draw.textbbox((0, 0), welcome_text, font=self.font_welcome)
            welcome_height = welcome_bbox[3] - welcome_bbox[1]
            
            username_bbox = draw.textbbox((0, 0), username_text, font=self.font_username)
            username_height = username_bbox[3] - username_bbox[1]
            
            # Espacio entre las dos líneas
            text_padding = 15
            
            # Altura total del bloque de texto (Bienvenido + Espacio + Nombre)
            total_text_height = welcome_height + text_padding + username_height
            
            # Calculamos la posición Y inicial para que todo el bloque quede centrado
            block_start_y = (height - total_text_height) // 2
            
            # Dibujar "Bienvenido/a"
            draw.text(
                (text_start_x, block_start_y), 
                welcome_text, 
                font=self.font_welcome, 
                fill=text_color
            )

            # Dibujar Nombre de Usuario (debajo del anterior)
            username_y = block_start_y + welcome_height + text_padding
            draw.text(
                (text_start_x, username_y), 
                username_text, 
                font=self.font_username, 
                fill=text_color
            )
            
            # 5. Guardar en buffer
            buffer = io.BytesIO()
            # Guardar con alta calidad
            background.save(buffer, format='PNG', quality=95)
            buffer.seek(0)
            
            return buffer

        except Exception as e:
            logger.error(f"Error generating image: {e}", exc_info=True)
            return None

# Instancia global
image_generator = ImageGenerator()