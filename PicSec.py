from flask import Flask, render_template
from os.path import isfile
from base64 import b64encode
from PIL import Image
from io import BytesIO

PICTURE_ROOT_FOLDER = '/files/Photos/'
ALLOWED_EXTENSIONS = {'jpg','jpeg'}
TILE_COUNT_X = 10
TILE_COUNT_Y = TILE_COUNT_X

app = Flask(__name__)
 
@app.route('/<path:filename>')
def show_picture(filename):
    if filename_is_valid(filename):
        return generate_html_for_file(filename)
    else:
        return render_template('missing_picture_template')
 
def filename_is_valid(filename):
    return '.' in filename and \
        filename[0] != '.' and \
        filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS and \
        isfile(PICTURE_ROOT_FOLDER + filename)

def generate_html_for_file(filename):
    kwargs = {'filename': filename}
    image = Image.open(PICTURE_ROOT_FOLDER + filename)
    kwargs['width'], kwargs['height'] = image.size
    
    kwargs['tiles'] = get_image_tiles(image)

    return render_template('picture_template', **kwargs)

def get_image_tiles(image):
    current_x = 0
    current_y = 0
    tiles = []
    tile_width = image.width // TILE_COUNT_X
    tile_height = image.height // TILE_COUNT_Y

    while current_x < image.width:
        while current_y < image.height:            
            currentTile = ImageTile(image, current_x, current_y, current_x + tile_width, current_y + tile_height)            
            tiles.append(currentTile)

            current_y += tile_height
        current_y = 0
        current_x += tile_width
    return tiles

class ImageTile:
    PosX = 0
    PosY = 0
    UTF8Base64String = None

    def __init__(self, original_image, left, up, right, down):
        cropped_image = original_image.crop((left, up, right, down))

        image_bytes = BytesIO()
        cropped_image.save(image_bytes, 'JPEG')
        
        self.UTF8Base64String = b64encode(image_bytes.getvalue()).decode('utf8') 
        self.PosX = left
        self.PosY = up

if __name__ == "__main__":
    app.run()