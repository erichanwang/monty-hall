import os
from PIL import Image, ImageDraw, ImageFont

def create_image_with_text(filepath, text, size=(100, 150), bg_color="brown", text_color="white"):
    """Creates an image with centered text."""
    if not os.path.exists(os.path.dirname(filepath)):
        os.makedirs(os.path.dirname(filepath))

    img = Image.new('RGB', size, color=bg_color)
    draw = ImageDraw.Draw(img)

    try:
        # Use a basic font if a specific one isn't found
        font = ImageFont.truetype("arial.ttf", 40)
    except IOError:
        font = ImageFont.load_default()

    # Calculate text size and position
    text_bbox = draw.textbbox((0, 0), text, font=font)
    text_width = text_bbox[2] - text_bbox[0]
    text_height = text_bbox[3] - text_bbox[1]
    position = ((size[0] - text_width) / 2, (size[1] - text_height) / 2)

    draw.text(position, text, font=font, fill=text_color)
    img.save(filepath)

if __name__ == "__main__":
    # Door Image
    create_image_with_text("assets/door.png", "?", bg_color="#8B4513") # SaddleBrown

    # Goat Image
    create_image_with_text("assets/goat.png", "Goat", bg_color="grey")

    # Car Image
    create_image_with_text("assets/car.png", "Car", bg_color="green")

    print("Image assets created successfully in the 'assets' directory.")
