import Image
import glob

def yuantongpng(f):
    img = Image.open(f)
    img0 = img.convert("L")
    img1 = img0.point(lambda i: 0 if i < 120 else 255)
    img1.save(f)

map(yuantongpng,glob.glob('*.png'))
