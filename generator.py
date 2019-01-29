import baidu_pic
import postergenerator

baidu_pic.baidu_picget('新垣结衣',30) # 关键字，页数（每页30张），图片文件夹名
postergenerator.poster_generator(200,200,5) # 目标图片参考像素高，宽，block大小