import argparse
import numpy as np
import math
from PIL import Image, ImageDraw, ImageFont

chars = "$@B%8&WM#*oahkbdpqwmZO0QLCJUYXzcvunxrjft/\\|()1{}[]?-_+~<>i!lI;:,\"^`'. "[::-1]
charArray = list(chars)
charLength = len(charArray)
interval = charLength / 256

oneCharWidth = 16
oneCharHeight = 24

def getChar(inputInt):
    return charArray[math.floor(inputInt * interval)]

def getAverageL(image):
    im = np.array(image)
    w, h = im.shape
    return np.average(im.reshape(w * h))

def convertImageToAscii(imgFile, cols, scale, moreLevels):
    image = Image.open(imgFile)
    W, H = image.size
    w = W / cols
    h = w / scale
    rows = int(H / h)

    if cols > W or rows > H:
        print("Image too small for specified cols!")
        exit(0)

    aimg = []

    try:
        fnt = ImageFont.truetype("arial.ttf", 15)  
    except IOError:
        fnt = ImageFont.load_default()  

    image = image.resize((int(scale * W), int(scale * H * (oneCharWidth / oneCharHeight))), Image.NEAREST)
    pix = image.load()

    outputImage = Image.new('RGB', (oneCharWidth * cols, oneCharHeight * rows), color=(0, 0, 0))
    d = ImageDraw.Draw(outputImage)

    for j in range(rows):
        y1 = int(j * h)
        y2 = int((j + 1) * h)
        if j == rows - 1:
            y2 = H

        aimg.append("")

        for i in range(cols):
            x1 = int(i * w)
            x2 = int((i + 1) * w)
            if i == cols - 1:
                x2 = W

            img = image.crop((x1, y1, x2, y2)).convert("L")  
            avg = int(getAverageL(img))

            r, g, b = pix[i, j]
            gsval = getChar(avg)
            aimg[j] += gsval
            d.text((i * oneCharWidth, j * oneCharHeight), gsval, font=fnt, fill=(r, g, b))

    return aimg, outputImage

def main():
    parser = argparse.ArgumentParser(description="This program converts an image into ASCII art with color grading.")
    parser.add_argument('--file', dest='imgFile', required=True)
    parser.add_argument('--scale', dest='scale', required=False)
    parser.add_argument('--out', dest='outFile', required=False)
    parser.add_argument('--cols', dest='cols', required=True)
    parser.add_argument('--morelevels', dest='moreLevels', action='store_true')

    args = parser.parse_args()

    imgFile = args.imgFile
    outFile = args.outFile if args.outFile else 'out.txt'
    scale = float(args.scale) if args.scale else 0.43
    cols = int(args.cols) if args.cols else 80

    print('Generating ASCII art...')
    aimg, outputImage = convertImageToAscii(imgFile, cols, scale, args.moreLevels)

    with open(outFile, 'w') as f:
        for row in aimg:
            f.write(row + '\n')

    outputImage.save('output.png')
    print(f"ASCII art written to {outFile} and saved as output.png")

if __name__ == '__main__':
    main()
