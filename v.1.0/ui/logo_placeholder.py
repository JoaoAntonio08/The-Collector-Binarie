"""
Módulo para criar uma imagem de logo placeholder para o The Collector Binarie.
Este script gera uma imagem de logo simples que pode ser usada até que uma logo real seja fornecida.
"""

from PIL import Image, ImageDraw, ImageFont
import os

def create_logo(output_path="logo.png", size=(400, 400)):
    """
    Cria uma imagem de logo placeholder para o The Collector Binarie.
    
    Args:
        output_path: Caminho para salvar a imagem
        size: Tamanho da imagem (largura, altura)
    """
    # Cria uma nova imagem com fundo transparente
    img = Image.new('RGBA', size, (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)
    
    # Define cores
    bg_color = (40, 42, 54, 255)  # Fundo escuro
    accent_color = (80, 250, 123, 255)  # Verde neon
    text_color = (248, 248, 242, 255)  # Texto claro
    
    # Desenha um círculo de fundo
    circle_radius = min(size) // 2 - 20
    circle_center = (size[0] // 2, size[1] // 2)
    draw.ellipse(
        (
            circle_center[0] - circle_radius,
            circle_center[1] - circle_radius,
            circle_center[0] + circle_radius,
            circle_center[1] + circle_radius
        ),
        fill=bg_color
    )
    
    # Desenha um símbolo de binário (0s e 1s) no centro
    binary_size = circle_radius * 1.2
    binary_top_left = (
        circle_center[0] - binary_size // 2,
        circle_center[1] - binary_size // 2
    )
    
    # Desenha um símbolo estilizado para representar código binário
    line_width = 5
    spacing = binary_size // 8
    
    # Desenha linhas horizontais representando código binário
    for i in range(5):
        y = binary_top_left[1] + i * spacing * 1.5
        # Linha completa ou parcial (simulando 0s e 1s)
        if i % 2 == 0:
            # Linha completa (1)
            draw.line(
                (binary_top_left[0], y, binary_top_left[0] + binary_size, y),
                fill=accent_color,
                width=line_width
            )
        else:
            # Linha parcial (0)
            draw.line(
                (binary_top_left[0], y, binary_top_left[0] + binary_size * 0.4, y),
                fill=accent_color,
                width=line_width
            )
            draw.line(
                (binary_top_left[0] + binary_size * 0.6, y, binary_top_left[0] + binary_size, y),
                fill=accent_color,
                width=line_width
            )
    
    # Tenta carregar uma fonte, ou usa a fonte padrão se não conseguir
    try:
        # Tenta encontrar uma fonte no sistema
        font_path = None
        common_fonts = [
            '/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf',
            '/usr/share/fonts/TTF/DejaVuSans-Bold.ttf',
            '/usr/share/fonts/truetype/liberation/LiberationSans-Bold.ttf'
        ]
        
        for path in common_fonts:
            if os.path.exists(path):
                font_path = path
                break
        
        if font_path:
            title_font = ImageFont.truetype(font_path, size=circle_radius // 4)
        else:
            # Usa a fonte padrão se não encontrar as fontes específicas
            title_font = ImageFont.load_default()
    except Exception:
        # Fallback para a fonte padrão em caso de erro
        title_font = ImageFont.load_default()
    
    # Adiciona o texto "The Collector Binarie" na parte inferior
   # title_text = "The Collector Binarie"   
    # Salva a imagem
    img.save(output_path)
    print(f"Logo criado em: {output_path}")
    
    return output_path

if __name__ == "__main__":
    # Cria a logo no diretório atual
    create_logo()
