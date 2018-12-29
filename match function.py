import imageio
from PIL import Image
import numpy as np

# im = imageio.imread('targetpic.jpg')
# [imx, imy, n]=im.shape # im is a numpy array
# print('im is a ' + str(im.shape) + ' matrix')
# print(im[0,1])

# im0 = im.copy()
picx = picy = 300 #目标图片大小
blocksize = 5 #合并格大小
bxsize = int(picx/blocksize)
bysize = int(picy/blocksize)

pic_target = Image.open('pic_target.jpg')
pic_target.resize((picx,picy)).save('pic_resized.jpg') #图片大小调整
pic_target.resize((bxsize,bysize)).save('pic_block.jpg')
pic_target.resize((3,3)).save('pic_test.jpg')


#我的平均化block方法
# pic_block = np.zeros((bxsize,bysize,3))
# pic_resized = imageio.imread('pic_resized.jpg').copy()
# print(type(pic_resized))
# for i in range(0,bxsize):
# 	for j in range(0,bysize):
# 		for m in range(0,blocksize):
# 			for n in range(0,blocksize):
# 				pic_block[i,j,0] += pic_resized[i*blocksize+m,j*blocksize+n,0]
# 				pic_block[i,j,1] += pic_resized[i*blocksize+m,j*blocksize+n,1]
# 				pic_block[i,j,2] += pic_resized[i*blocksize+m,j*blocksize+n,2]
# for i in range(0,bxsize):
# 	for j in range(0,bysize):
# 		pic_block[i,j,0] /= (blocksize*blocksize)
# 		pic_block[i,j,1] /= (blocksize*blocksize)
# 		pic_block[i,j,2] /= (blocksize*blocksize)
# print(pic_block[bxsize-1,bysize-1,0],pic_block[bxsize-1,bysize-1,1],pic_block[bxsize-1,bysize-1,2])
# imageio.imwrite(r"pic_block2.jpg",pic_block)