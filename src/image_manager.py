import sys
import pyimgur
from PIL import Image

CLIENT_ID = "fa37e007405ff2d"
im = pyimgur.Imgur(CLIENT_ID)

def handImage(ims):
    images = []
    for im in ims:
        images.append("../assets/" + im + ".png")
    images = map(Image.open, images)
    widths, heights = zip(*(i.size for i in images))

    total_width = sum(widths)
    max_height = max(heights)

    new_im = Image.new('RGB', (total_width, max_height))

    x_offset = 0
    for im in images:
        im += ".png"
        new_im.paste(im, (x_offset,0))
        x_offset += im.size[0]

    new_im.save('hand.png')

    PATH = "../assets/hand.png"
    uploaded_image = im.upload_image(PATH, title="Blackjeck Hand Uploaded with PyImgur")

    return uploaded_image.link
