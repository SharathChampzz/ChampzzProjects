import requests
import json
from PIL import ImageFont, ImageDraw, Image
import os

NEWS_COUNT = 5

# API endpoint
url = f'https://web-cdn.api.bbci.co.uk/xd/content-collection/1a3cd4db-fe3d-46f2-9c9a-927a01b00c91?country=in&page=0&size={NEWS_COUNT}'

# Make GET request to the API
response = requests.get(url)
response_data = response.json()

# Save response to response.json
with open('response.json', 'w') as f:
    json.dump(response_data, f, indent=4)

# Function to download an image from a URL
def download_image(url, filename):
    img_response = requests.get(url, stream=True)
    if img_response.status_code == 200:
        with open(filename, 'wb') as img_file:
            for chunk in img_response.iter_content(1024):
                img_file.write(chunk)

def resize_for_instagram(image_path):
    # Define Instagram post size
    instagram_size = (1080, 1080)
    
    # Open and resize the image to fit Instagram post size
    image = Image.open(image_path)
    resized_image = image.resize(instagram_size, Image.LANCZOS)
    
    # Save the resized image, overwriting the original file
    resized_image.save(image_path)

def wrap_text(text, font, max_width):
    """Wrap text to fit within a specified width."""
    lines = []
    words = text.split()
    while words:
        line = ''
        while words and font.getbbox(line + words[0])[2] <= max_width:
            line += (words.pop(0) + ' ')
        lines.append(line.strip())
    return lines

# add caption to image
def add_caption_with_wrapping(image_path, output_path, caption):
    # resize image for Instagram
    resize_for_instagram(image_path)
    
    # Load the image
    image = Image.open(image_path)
    width, height = image.size
    
    # Set up font and text size
    font_size = int(height / 20)
    font = ImageFont.truetype("arial.ttf", font_size)
    draw = ImageDraw.Draw(image)
    
    # Wrap the caption text
    max_text_width = width - 40  # 20 pixels padding on each side
    wrapped_lines = wrap_text(caption, font, max_text_width)
    
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
    image.save(output_path)

# Process each article in the response data
for i, article in enumerate(response_data['data']):
    image_url = article['indexImage']['model']['blocks']['src']
    summary = article['summary']
    
    # Define image file paths
    download_directory = os.path.join(os.path.dirname(os.path.abspath(__file__)), "downloads")
    image_path = os.path.join(download_directory, f"image_{i}.jpg")
    
    # Download the image
    download_image(image_url, image_path)
    
    # Add summary to the image
    add_caption_with_wrapping(image_path, image_path, summary)
