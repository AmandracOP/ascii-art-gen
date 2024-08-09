from PIL import Image, ImageDraw, ImageFont
import math

chars = "$@B%8&WM#*oahkbdpqwmZO0QLCJUYXzcvunxrjft/\\|()1{}[]?-_+~<>i!lI;:,\"^`'. "[::-1]
charArray = list(chars)
charLength = len(charArray)
interval = charLength / 256

scaleFactor = 0.09
oneCharWidth = 10
oneCharHeight = 18

def getChar(inputInt):
    return charArray[math.floor(inputInt * interval)]

text_file = open("Output.txt", "w")

im = Image.open("/home/navarch/Downloads/WhatsApp Image 2024-08-08 at 3.30.33 AM(1).jpeg")


try:
    fnt = ImageFont.truetype('arial.ttf', 15)  
except IOError:
    fnt = ImageFont.load_default()  #

width, height = im.size
im = im.resize((int(scaleFactor * width), int(scaleFactor * height * (oneCharWidth / oneCharHeight))), Image.NEAREST)
width, height = im.size
pix = im.load()

outputImage = Image.new('RGB', (oneCharWidth * width, oneCharHeight * height), color=(0, 0, 0))
d = ImageDraw.Draw(outputImage)

for i in range(height):
    for j in range(width):
        r, g, b = pix[j, i]
        h = int(r / 3 + g / 3 + b / 3)
        pix[j, i] = (h, h, h)
        text_file.write(getChar(h))
        d.text((j * oneCharWidth, i * oneCharHeight), getChar(h), font=fnt, fill=(r, g, b))

    text_file.write('\n')

text_file.close()
outputImage.save('output.png')