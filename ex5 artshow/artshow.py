from PIL import Image
from PIL import ImageFilter
from PIL import ImageEnhance
from PIL import ImageOps
from PIL import ImageDraw, ImageFont
from imager2 import Imager


def inverse255(val):
    return 255 - val

def sharpen(img):
    img = img.get_image()
    img = img.filter(ImageFilter.SHARPEN)
    return Imager(image=img)

def edge_enhance(img):
    img = img.get_image()
    img = img.filter(ImageFilter.EDGE_ENHANCE_MORE)
    return Imager(image=img)

def blur(img, radius=5):
    img = img.get_image()
    img = img.filter(ImageFilter.GaussianBlur(radius=radius))
    return Imager(image=img)

def find_edges(img): # Uses ImageFilter
    im_edge = img.get_image()
    im_edge = im_edge.filter(ImageFilter.FIND_EDGES)
    im_edge = Imager(image=im_edge)
    return im_edge

def contour_edges(imager, rgb=(255, 255, 255), threshold=150):
    edge_imager = find_edges(imager)
    return_imag = Imager(width = edge_imager.xmax, height = edge_imager.ymax)
    for y in range(0, edge_imager.ymax):
        for x in range(0, edge_imager.xmax):
            pix1 = edge_imager.get_pixel(x, y)
            if sum(pix1) > 230:
                return_imag.set_pixel(x, y, rgb)
            else:
                return_imag.set_pixel(x, y, imager.get_pixel(x, y))
    return return_imag

def transform_image_bands(rgb, imager):
    func = lambda pix: (pix[0]*rgb[0], pix[1]*rgb[1], pix[2]*rgb[2])
    ret_imager = imager.map_image2(func = func)
    return ret_imager


def create4x4(img1, img2, img3, img4):
    hor1 = img1.concat_horiz(img2)
    hor2 = img3.concat_horiz(img4)
    return hor1.concat_vert(hor2)

def get_grayscale(img): # Uses ImageOps
    img = img.get_image()
    img = ImageOps.grayscale(img)
    return Imager(image=img)

def create4x4GRGB(img):
    gray = get_grayscale(img)  # Uses ImageOps
    red = transform_image_bands((1, 0, 0), img)
    green = transform_image_bands((0, 1, 0), img)
    blue = transform_image_bands((0, 0, 1), img)
    return create4x4(gray, red, green, blue)



def sign_image(img):
    base = img.get_image()
    base = base.convert('RGBA')
    # make a blank image for the text, initialized to transparent text color
    txt = Image.new('RGBA', base.size, (255, 255, 255, 0))
    # get a font
    font_size = 20
    fnt = ImageFont.truetype("arial.ttf", font_size)
    # get a drawing context
    d = ImageDraw.Draw(txt)
    # draw text, full opacity
    d.text((0, img.ymax - font_size*1.5), "Snorre Børtnes", font=fnt, fill=(255, 255, 255, 255))
    out = Image.alpha_composite(base, txt)
    return Imager(image=out)


image_name = "trail.jpeg"
path_name = "./imager/images/" + image_name

print(path_name)
img = Imager(path_name)
img.load_image()

### Option 1
# grgb = create4x4GRGB(img)
# result_image = grgb

### Option 2
# blurred = blur(img, radius=2)
# edge_orig = find_edges(img)
# edge_blurred = find_edges(blurred)
# edge_compare = create4x4(img, blurred, edge_orig, edge_blurred)
# result_image = edge_compare

## Option 3
edge_orig = find_edges(img)
result_image = contour_edges(img)







result_image = sign_image(result_image)
result_image.display()