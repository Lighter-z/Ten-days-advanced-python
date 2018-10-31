#-*- coding:utf-8 -*-
import sys
from PIL import Image

def generate_ascii(pixels, width, height):

    # grayscale
    color = ".,:;irsXA253hMHGS#9B&@ "
#   color = "$@B%8&WM#*oahkbdpqwmZO0QLCJUYXzcvunxrjft/\|()1{}[]?-_+~<>i!lI;:,\"^`'. "
#   color = "MNHQ$OC?7>!:-;. "

    length = len(color)
    string = ""
    # first go through the height,  otherwise will rotate
    for h in range(height):
        for w in range(width):

            rgba = pixels[w, h]
            rgb = rgba[:3]

            string += color[int(sum(rgb) / 3.0 / 256.0 * length)]

        string += "\n"

    return string


def load_image(imgname, antialias, maxLen, aspectRatio):

    if aspectRatio is None:
        aspectRatio = 1.0

    img = Image.open(imgname)

    if img.mode != 'RGBA':
        img = img.convert('RGBA')
    
    native_width, native_height = img.size
    new_width = native_width
    new_height = native_height

    if maxLen is not None or aspectRatio != 1.0:
        if aspectRatio != 1.0:
            new_height = int(float(aspectRatio) * new_height)

        if maxLen is not None:
            rate = float(maxLen) / max(new_width, new_height)
            new_width = int(rate * new_width)  
            new_height = int(rate * new_height)

        if native_width != new_width or native_height != new_height:
            img = img.resize((new_width, new_height), Image.ANTIALIAS if antialias else Image.NEAREST)

    return img, new_width,new_height

if __name__ == '__main__':
    img,new_width,new_height = load_image("example/wanmen.jpg", False, 200, None)
    new_asciis=generate_ascii(img.load(),new_width,new_height)
    result_file = open("ascii3.txt",'w')
    result_file.write(new_asciis)
    result_file.close()
