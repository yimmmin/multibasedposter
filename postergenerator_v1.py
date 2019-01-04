import imageio
from PIL import Image, ImageFile
import os
import numpy as np
import cv2

def targetpic_adjustment(mergex = 60, mergey = 60):
	"""
	picx, picy 目标图片长宽调整
	mergex, mergey 目标图标缩放后像素大小
	"""
	# im = imageio.imread('targetpic.jpg')
	# [imx, imy, n]=im.shape # im is a numpy array
	# print('im is a ' + str(im.shape) + ' matrix')
	# print(im[0,1])
	# im0 = im.copy()
	# mergex = int(picx/mergesize)
	# mergey = int(picy/mergesize)

	pic_target = Image.open('pic_target.jpg')
	# pic_target.resize((picx,picy)).save('pic_resized.jpg') #图片大小调整
	pic_target.resize((mergey,mergex)).save('pic_merge.jpg')
	# pic_target.resize((3,3)).save('pic_test.jpg')

def sourcepic_formalblock(formalsize = 100, blocksize = 3):
	"""
	图片库规格化、重命名、形成block
	"""
	ImageFile.LOAD_TRUNCATED_IMAGES = True #为什么
	sourcelist = os.listdir('./images')
	pic_num = len(sourcelist)
	i = 1
	for sourcepic in sourcelist:
		im = Image.open('./images/' + sourcepic)
		[x,y] = im.size
		if x>y:
			im0 = im.crop(((x-y)/2,0,y,y))
		else:
			im0 = im.crop((0,(y-x)/2,x,x))
		im0.resize((formalsize,formalsize)).save('./images_formalized/'+str(i)+'.jpg')
		im0.resize((blocksize,blocksize)).save('./images_blocken/'+str(i)+'.jpg')
		i = i+1
	return i-1
		# if i<10:
		# 	im0.resize((formalsize,formalsize)).save('./images_formalized/000'+str(i)+'.jpg')
		# 	im0.resize((blocksize,blocksize)).save('./images_blocken/000'+str(i)+'.jpg')
		# elif i<100:
		# 	im0.resize((formalsize,formalsize)).save('./images_formalized/00'+str(i)+'.jpg')
		# 	im0.resize((blocksize,blocksize)).save('./images_blocken/00'+str(i)+'.jpg')
		# elif i<1000:
		# 	im0.resize((formalsize,formalsize)).save('./images_formalized/0'+str(i)+'.jpg')
		# 	im0.resize((blocksize,blocksize)).save('./images_blocken/0'+str(i)+'.jpg')
		# else:
		# 	im0.resize((formalsize,formalsize)).save('./images_formalized/'+str(i)+'.jpg')
		# 	im0.resize((blocksize,blocksize)).save('./images_blocken/'+str(i)+'.jpg')
	# return pic_num
	"""
	我的平均化block方法
	pic_block = np.zeros((bxsize,bysize,3))
	pic_resized = imageio.imread('pic_resized.jpg').copy()
	print(type(pic_resized))
	for i in range(0,bxsize):
		for j in range(0,bysize):
			for m in range(0,blocksize):
				for n in range(0,blocksize):
					pic_block[i,j,0] += pic_resized[i*blocksize+m,j*blocksize+n,0]
					pic_block[i,j,1] += pic_resized[i*blocksize+m,j*blocksize+n,1]
					pic_block[i,j,2] += pic_resized[i*blocksize+m,j*blocksize+n,2]
	for i in range(0,bxsize):
		for j in range(0,bysize):
			pic_block[i,j,0] /= (blocksize*blocksize)
			pic_block[i,j,1] /= (blocksize*blocksize)
			pic_block[i,j,2] /= (blocksize*blocksize)
	print(pic_block[bxsize-1,bysize-1,0],pic_block[bxsize-1,bysize-1,1],pic_block[bxsize-1,bysize-1,2])
	imageio.imwrite(r"pic_block2.jpg",pic_block)
	"""

def targetpic_match(mergex = 60, mergey = 60, blocksize = 3, pic_num = 1582):
	blockx = int(mergex/blocksize)
	blocky = int(mergey/blocksize)
	targetpic = imageio.imread('pic_merge.jpg')
	pic_nearby = np.zeros((blockx,blocky,2)) #确保相邻的图片不重复，上左
	block = np.zeros((blockx*blocky+1),np.int)
	for x in range(0, blockx):
		for y in range(0, blocky):
			n = x*blocky+y+1
			fewest_cost = np.power(255,2)*3*np.power(blocksize,2)
			# print(type(fewest_cost))
			#block = 0
			# sourceblocklist = os.listdir('./images_blocken')
			# sourceblocklist = os.listdir('./block')
			for i in range(1,pic_num+1):
				# for sourceblock in sourceblocklist:
				if (i!=pic_nearby[x,y,0] and i!=pic_nearby[x,y,1]):
					# sourceblockpic = imageio.imread('./images_blocken/' + sourceblock)
					sourceblock = imageio.imread('./images_blocken/' + str(i) + '.jpg')
					cost = 0
					# print(int(sourceblock[0,0,0]))
					# cost = int(sourceblock[0,0,0]-sourceblock[0,0,0])
					# print(cost,type(cost))
					# print(type(sourceblock[0,0,0]))
					for bx in range(0,blocksize):
						for by in range(0,blocksize):
							for k in range(0,3):
								if targetpic[x*blocksize+bx,y*blocksize+by,k]>sourceblock[bx,by,k]:
									cost += np.int32(targetpic[x*blocksize+bx,y*blocksize+by,k]-sourceblock[bx,by,k])
								else:
									cost += np.int32(sourceblock[bx,by,k]-targetpic[x*blocksize+bx,y*blocksize+by,k])
									# cost += np.power(int(targetpic[x*blocksize+bx,y*blocksize+by,k]-sourceblock[bx,by,k]),2)
									# print(targetpic[x*blocksize+bx,y*blocksize+by,k]-sourceblock[bx,by,k])
									# print(sourceblock[bx,by,k])
					# print(cost,type(cost))
					# print(cost<fewest_cost)
					if cost<fewest_cost:
						fewest_cost = cost
						block[n] = i
			# Image.open('./images_blocken/'+str(block)+'.jpg').save('./target_block/'+str(x*blocky+y+1)+'.jpg')
			# Image.open('./images_formalized/'+str(block)+'.jpg').save('./target_blockpic/'+str(x*blocky+y+1)+'.jpg')
			if x!=(blockx-1):
				pic_nearby[x+1,y,0] = block[n] #记录在邻接下block处
			if y!=(blocky-1):
				pic_nearby[x,y+1,1] = block[n] #记录在邻接右block处
	return block

def targetblockcompose(mergex = 60, mergey = 60, blocksize = 3):
	blockmerge = np.zeros((mergex,mergey,3),np.uint8)
	# targetblocklist = os.listdir('./target_block')
	# targetblocklist = os.listdir('./block')
	# i = 1
	# for targetblock in targetblocklist:
	for i in range(1,int(mergex/blocksize*mergey/blocksize+1)):
		# targetblockpic = imageio.imread('./target_block/' + targetblock)
		# targetblockpic = imageio.imread('./block/' + targetblock)
		targetblockpic = imageio.imread('./target_block/' + str(i) + '.jpg')
		for bx in range(0,blocksize):
			for by in range(0,blocksize):
				for k in range(0,3):
					blockmerge[int((i-1)/(mergex/blocksize))*blocksize+bx,int((i-1)%(mergey/blocksize))*blocksize+by,k] = targetblockpic[bx,by,k]
		# i = i+1
	imageio.imwrite(r"targetblockmerge.jpg",blockmerge)

def targetdecompose():
	# targetpic = cv2.imread('pic_merge.jpg',-1)
	# for i in range(0,20):
	# 	for j in range(0,20):
	# 		cv2.imwrite('block/'+str(j*20+i+1)+'.jpg',targetpic[j*3:(j+1)*3,i*3:(i+1)*3,:])

	targetpic = imageio.imread('pic_merge.jpg')
	block = np.zeros((3,3,3),np.uint8)
	for i in range(1,401):
		for bx in range(0,3):
			for by in range(0,3):
				for k in range(0,3):
					block[bx,by,k] = targetpic[int((i-1)/20)*3+bx,int((i-1)%20)*3+by,k]
					# print(targetpic[int((i-1)/20)*3+bx,int((i-1)%20)*3+by,k])
		imageio.imwrite(r"block/"+str(i)+".jpg",block)
	# print (targetpic[int((1-1)/20)*3,int((1-1)%20)*3,0])
	# print(int((1-1)/20)*3,int((1-1)%20),0)
	# print(imageio.imread('block/1.jpg'))

def targetpiccompose(block, x_num = 20, y_num = 20, picsize = 100):
	picmerge = np.zeros((x_num*picsize,y_num*picsize,3),np.uint8)
	for i in range(1,int(x_num*y_num+1)):
		targetpic = imageio.imread('./images_formalized/' + str(block[i]) + '.jpg')
		for bx in range(0,picsize):
			for by in range(0,picsize):
				for k in range(0,3):
					picmerge[int((i-1)/y_num)*picsize+bx,int((i-1)%y_num)*picsize+by,k] = targetpic[bx,by,k]
	imageio.imwrite(r"targetpicmerge.jpg",picmerge)

def postergenerator(mergex = 60, mergey = 60, blocksize = 3):
	# targetdecompose()
	targetpic_adjustment(mergex, mergey)
	n = sourcepic_formalblock(100,blocksize)
	print(str(n)+" pictures have been formalized.")
	block = targetpic_match(mergex, mergey, blocksize, n)
	print("Pictures' positions have been chosen.")
	# targetblockcompose(mergex, mergey, blocksize)
	targetpiccompose(block,int(mergex/blocksize), int(mergey/blocksize))

postergenerator(66,60,3)