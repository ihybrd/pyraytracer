from PIL import Image

img = Image.new('RGB', (32,32), (128,128,255))

for h in xrange(img.height):
    for w in xrange(img.width):
        img.putpixel((h,w), (h*2, w*2, 128))

img.show()
