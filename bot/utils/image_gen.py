from PIL import Image, ImageDraw, ImageFont, ImageFilter
import io
import aiohttp
import logging

logger = logging.getLogger(__name__)

class WelcomeImageGenerator:
    def __init__(self):
        self.width = 800
        self.height = 300
        self.avatar_size = 150
    
    async def generate(self, user_name: str, user_avatar_url: str, server_name: str, 
                      bg_color: str = '#7289da', text_color: str = '#ffffff'):
        """Generar imagen de bienvenida"""
        try:
            # Crear imagen base
            img = Image.new('RGB', (self.width, self.height), bg_color)
            draw = ImageDraw.Draw(img)
            
            # Descargar avatar del usuario
            avatar = await self._download_avatar(user_avatar_url)
            if avatar:
                # Hacer el avatar circular
                avatar = self._make_circular(avatar)
                # Pegar avatar en la imagen
                avatar_x = (self.width - self.avatar_size) // 2
                avatar_y = 30
                img.paste(avatar, (avatar_x, avatar_y), avatar)
            
            # Agregar texto
            try:
                # Intentar usar fuente personalizada
                title_font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 40)
                subtitle_font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 25)
            except:
                # Fallback a fuente por defecto
                title_font = ImageFont.load_default()
                subtitle_font = ImageFont.load_default()
            
            # Texto de bienvenida
            welcome_text = f"¡Bienvenido!"
            name_text = user_name
            server_text = f"a {server_name}"
            
            # Calcular posiciones centradas
            y_offset = avatar_y + self.avatar_size + 20
            
            # Dibujar textos
            self._draw_centered_text(draw, welcome_text, y_offset, title_font, text_color)
            self._draw_centered_text(draw, name_text, y_offset + 45, title_font, text_color)
            self._draw_centered_text(draw, server_text, y_offset + 90, subtitle_font, text_color)
            
            # Convertir a bytes
            img_bytes = io.BytesIO()
            img.save(img_bytes, format='PNG')
            img_bytes.seek(0)
            
            return img_bytes
        except Exception as e:
            logger.error(f"Error generating welcome image: {e}")
            return None
    
    async def _download_avatar(self, url: str):
        """Descargar avatar del usuario"""
        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(url) as resp:
                    if resp.status == 200:
                        data = await resp.read()
                        avatar = Image.open(io.BytesIO(data))
                        avatar = avatar.resize((self.avatar_size, self.avatar_size))
                        return avatar
        except Exception as e:
            logger.error(f"Error downloading avatar: {e}")
        return None
    
    def _make_circular(self, img):
        """Hacer una imagen circular"""
        # Crear máscara circular
        mask = Image.new('L', (self.avatar_size, self.avatar_size), 0)
        draw = ImageDraw.Draw(mask)
        draw.ellipse((0, 0, self.avatar_size, self.avatar_size), fill=255)
        
        # Aplicar máscara
        output = Image.new('RGBA', (self.avatar_size, self.avatar_size), (0, 0, 0, 0))
        output.paste(img, (0, 0))
        output.putalpha(mask)
        
        return output
    
    def _draw_centered_text(self, draw, text, y, font, color):
        """Dibujar texto centrado"""
        bbox = draw.textbbox((0, 0), text, font=font)
        text_width = bbox[2] - bbox[0]
        x = (self.width - text_width) // 2
        draw.text((x, y), text, font=font, fill=color)

# Instancia global
image_generator = WelcomeImageGenerator()
