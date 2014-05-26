import Image
import glob

def pngtrans(f):
    img = Image.open(f)
    img1 = img.crop((15,0,30,25))
    img2 = img.crop((30,0,45,25))
    img3 = img.crop((45,0,60,25))
    img1 = img1.offset(xoffset=0,yoffset=2)
    img2 = img2.offset(xoffset=0,yoffset=-1)
    img3 = img3.offset(xoffset=0,yoffset=1)
    img.paste(img1,box=(15,0))
    img.paste(img2,box=(30,0))
    img.paste(img3,box=(45,0))
    img0 = img.crop((0,6,60,21))
    img0.save(f)

if __name__ == '__main__':
    map(pngtrans,glob.glob('*.png'))
