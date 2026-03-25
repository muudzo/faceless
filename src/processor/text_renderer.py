from PIL import Image, ImageDraw, ImageFont
import numpy as np

class TextRenderer:
    def __init__(self, default_font="Arial"):
        self.default_font = default_font

    def create_text_image(self, text, width, height, fontsize=70, color="white", bgcolor=(0,0,0,128)):
        """
        Renders text onto a PIL image and returns it as a numpy array.
        """
        img = Image.new("RGBA", (width, height), bgcolor)
        draw = ImageDraw.Draw(img)
        
        try:
            font = ImageFont.truetype(self.default_font, fontsize)
        except:
            font = ImageFont.load_default()
            
        bbox = draw.textbbox((0, 0), text, font=font)
        tw, th = bbox[2] - bbox[0], bbox[3] - bbox[1]
        draw.text(((width - tw) / 2, (height - th) / 2), text, font=font, fill=color)
        
        return np.array(img)
