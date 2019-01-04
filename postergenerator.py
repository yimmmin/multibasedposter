import imageio
from PIL import Image, ImageFile
import os
import numpy as np


def targetpic_adjustment(mergex = 100, mergey = 100):
	# 调整目标像素大小

	pic_target = Image.open('pic_target.jpg')
	pic_target.resize((mergey,mergex)).save('pic_merge.jpg')


def sourcepic_formalblock(formalsize=100, blocksize=5):
	# 图片库规格化、重命名、形成block

	ImageFile.LOAD_TRUNCATED_IMAGES = True #为什么
	sourcelist = os.listdir('./images')
	i = 1
	for sourcepic in sourcelist:
		im = Image.open('./images/'+sourcepic)
		[x,y] = im.size
		if x>y:
			im0 = im.crop(((x-y)/2,0,y,y))
		else:
			im0 = im.crop((0,(y-x)/2,x,x))
		im0.resize((formalsize,formalsize)).save('./images_formalized/'+str(i)+'.jpg')
		im0.resize((blocksize,blocksize)).save('./images_blocken/'+str(i)+'.jpg')
		i = i+1
	return i-1


def targetpic_match(mergex=100, mergey=100, blocksize=5, pic_num=100):
	# 通过计算目标图片每个block与图片库block的差值，返回差值最小的图片号数组
	# pic_num为图片库图片数目

	blockx = int(mergex/blocksize)
	blocky = int(mergey/blocksize)
	targetpic = imageio.imread('pic_merge.jpg')
	pic_nearby = np.zeros((blockx,blocky,2)) #确保相邻的图片不重复，上左
	block = np.zeros((blockx*blocky + 1),np.int)

	for x in range(0, blockx):
		for y in range(0, blocky):
			n = x*blocky+y+1
			fewest_cost = np.power(255,2) * 3 * np.power(blocksize,2)

			for i in range(1,pic_num+1):
				if (i!=pic_nearby[x,y,0] and i!=pic_nearby[x,y,1]):
					sourceblock = imageio.imread('./images_blocken/' + str(i) + '.jpg')
					cost = 0

					for bx in range(0,blocksize):
						for by in range(0,blocksize):
							for k in range(0,3):
								if targetpic[x*blocksize+bx,y*blocksize+by,k]>sourceblock[bx,by,k]:
									cost += np.int32(targetpic[x*blocksize+bx,y*blocksize+by,k]-sourceblock[bx,by,k])
								else:
									cost += np.int32(sourceblock[bx,by,k]-targetpic[x*blocksize+bx,y*blocksize+by,k])
					if cost<fewest_cost:
						fewest_cost = cost
						block[n] = i

			if x!=(blockx-1):
				pic_nearby[x+1,y,0] = block[n] # 记录在邻接下block处
			if y!=(blocky-1):
				pic_nearby[x,y+1,1] = block[n] # 记录在邻接右block处

	return block


def targetpic_compose(block, x_num = 20, y_num = 20, picsize = 100):
	# 将数组对应的图片拼接成一张大图片

	picmerge = np.zeros((x_num*picsize,y_num*picsize,3),np.uint8)
	for i in range(1,int(x_num*y_num+1)):
		targetpic = imageio.imread('./images_formalized/' + str(block[i]) + '.jpg')
		for bx in range(0,picsize):
			for by in range(0,picsize):
				for k in range(0,3):
					picmerge[int((i-1)/y_num)*picsize+bx,int((i-1)%y_num)*picsize+by,k] = targetpic[bx,by,k]
	imageio.imwrite(r"targetpicmerge.jpg",picmerge)


def poster_generator(mergex = 100, mergey = 100, blocksize = 5):
	# 主程序
	#mergex为目标图片参考像素高，mergey为宽，blocksize为block大小

	targetpic_adjustment(mergex, mergey)
	n = sourcepic_formalblock(100,blocksize)
	print(str(n)+" pictures have been formalized.")
	block = targetpic_match(mergex, mergey, blocksize, n)
	print("Pictures' positions have been chosen.")
	targetpic_compose(block, int(mergex/blocksize), int(mergey/blocksize))

poster_generator(110,100,5)