import sys
import os
import pyimgur
from PIL import Image

def handImage(ims):
    CLIENT_ID = "fa37e007405ff2d"
    pyim = pyimgur.Imgur(CLIENT_ID)

    if os.path.exists('assets/hand.png'):
        os.remove('assets/hand.png',*,dir_fd=None)

    images = []
    for im in ims:
        images.append("assets/" + im + ".png")
    images = list(map(Image.open, images))
    widths, heights = zip(*(i.size for i in images))

    total_width = sum(widths)
    max_height = max(heights)

    new_im = Image.new('RGB', (total_width, max_height))

    x_offset = 0
    for im in images:
        new_im.paste(im, (x_offset,0))
        x_offset += im.size[0]

    new_im.save('assets/hand.png')

    PATH = "assets/hand.png"
    uploaded_image = pyim.upload_image(PATH, title="Blackjeck Hand Uploaded with PyImgur")

    return uploaded_image.link
