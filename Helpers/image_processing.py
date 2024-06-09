from PIL import ImageFont, ImageDraw, Image

class ImageProcessing:
    
    def __init__(self):
        pass
    
    def resize_image(self, image_path, width:int=1080, height:int=1080, new_image_location:str=None):
        print(f'Resizing image to {width}x{height}...')
        # Define image size
        image_size = (width, height)
        
        # Open and resize the image
        image = Image.open(image_path)
        resized_image = image.resize(image_size, Image.LANCZOS)
        
        # Save the resized image, overwriting the original file if new image location is not provided
        resized_image.save(new_image_location if new_image_location else image_path)

    def __wrap_text(self, text, font, max_width):
        """Wrap text to fit within a specified width."""
        lines = []
        words = text.split()
        while words:
            line = ''
            while words and font.getbbox(line + words[0])[2] <= max_width:
                line += (words.pop(0) + ' ')
            lines.append(line.strip())
        return lines

    def add_caption_to_image(self, image_path:str, caption:str, output_path:str=None, resize_image:bool=True):
        # resize image for Instagram
        if resize_image:
            self.resize_image(image_path, 1080, 1080)
        
        # Load the image
        image = Image.open(image_path)
        width, height = image.size
        
        # Set up font and text size
        font_size = int(height / 20)
        font = ImageFont.truetype("arial.ttf", font_size)
        draw = ImageDraw.Draw(image)
        
        # Wrap the caption text
        max_text_width = width - 40  # 20 pixels padding on each side
        wrapped_lines = self.__wrap_text(caption, font, max_text_width)
        
        # Calculate text height
        line_height = font.getbbox('A')[3]
        text_height = line_height * len(wrapped_lines) + 20  # 10 pixels padding top and bottom
        
        # Create a semi-transparent background for the caption
        background = Image.new('RGBA', (width, text_height), (0, 0, 0, 150))  # Black background with 150 alpha
        
        # Position the background at the bottom of the image
        image.paste(background, (0, height - text_height), background)
        
        # Add the wrapped text lines
        y_offset = height - text_height + 10  # 10 pixels padding at the top
        for line in wrapped_lines:
            text_width = draw.textbbox((0, 0), line, font=font)[2]
            text_x = (width - text_width) / 2
            draw.text((text_x, y_offset), line, font=font, fill=(255, 255, 255, 255))  # White text with full opacity
            y_offset += line_height
        
        # Save the result
        image.save(output_path if output_path else image_path)