from PIL import Image

im = Image.open('./images/0.jpg')
im = im.convert('RGB')
[x,y] = im.size
print(im.size)
if x>y:
    im0 = im.crop(((x-y)/2,0,(x+y)/2,y))
    print(im0.size)
else:
    im0 = im.crop((0,(y-x)/2,x,(x+y)/2))
im0.save('./images_formalized/1.jpg')