import requests,json
import os
import re

def uncompile(url):
    # 百度Objurl地址解码

    res = ''
    c = ['_z2C$q', '_z&e3B', 'AzdH3F']
    d= {'w':'a', 'k':'b', 'v':'c', '1':'d', 'j':'e', 'u':'f', '2':'g', 'i':'h', 't':'i', '3':'j', 'h':'k', 's':'l', '4':'m', 'g':'n', '5':'o', 'r':'p', 'q':'q', '6':'r', 'f':'s', 'p':'t', '7':'u', 'e':'v', 'o':'w', '8':'1', 'd':'2', 'n':'3', '9':'4', 'c':'5', 'm':'6', '0':'7', 'b':'8', 'l':'9', 'a':'0', '_z2C$q':':', '_z&e3B':'.', 'AzdH3F':'/'}
    if(url==None or 'http' in url):
        return url
    else:
        j= url
        for m in c:
            j=j.replace(m,d[m])
        for char in j:
            if re.match('^[a-w\d]+$',char):
                char = d[char]
            res= res+char
        return res


def baidu_picget(keyword, page = 10, folder = 'images'):
    # 获取百度图片，keyword多个关键字用加号连接，page页数（每页30张），folder文件夹名
    if not os.path.exists(folder):
        os.mkdir(folder)
    pic_num = 0
    for i in range(page):
        url = 'http://image.baidu.com/search/acjson'
        params = {'tn':'resultjson_com',
                  'ipn':'rj',
                  'ct':201326592,
                  'is':'',
                  'fp':'result',
                  'queryWord':keyword, # 搜索关键字
                  'cl':2,
                  'lm':'-1',
                  'ie':'utf-8',
                  'oe':'utf-8',
                  'adpicid':'',
                  'st':'',
                  'z':'',
                  'ic':'',
                  'hd':'',
                  'latest':'',
                  'copyright':'',
                  'word':keyword, # 搜索关键字
                  's':'',
                  'se':'',
                  'tab':'',
                  'width':'',
                  'height':'',
                  'face':'',
                  'istype':'',
                  'qc':'',
                  'nc':1,
                  'fr':'',
                  'expermode':'',
                  'force':'',
                  'pn':i*30, # 页数
                  'rn':30, # 每次加载总数
                  'gsm':'1e' #十六进制形式的当前加载起始位置
                  }
        headers = {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36',
                   # 'Upgrade-Insecure-Requests':1,
                   'Referer': 'https://image.baidu.com/search/index?tn=baiduimage',
                   'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
                   'Accept-Encoding':'gzip, deflate, sdch',
                   'Accept-Language':'zh-CN,zh;q=0.8,en;q=0.6',
                   'Cache-Control':'no-cache'
                   }
        # datas = requests.get(url,params=params,headers=headers).json().get('data')
        web = requests.get(url,params=params,headers=headers).text.encode('utf-8')
        datas = json.loads(web,strict=False)['data']
        for data in datas:
            try:
                objurl = uncompile(data['objURL']) 
                print('正在载入'+objurl)
                # pic_con = requests.get(data.get('thumbURL'))
                pic_con = requests.get(objurl,timeout=3)

                with open(folder+'/'+str(pic_num)+'.jpg','wb') as pic:
                    pic.write(pic_con.content)
                pic_num +=1
            except:
                continue
        print('Page '+str(i+1)+' is finished.')
    print(str(pic_num)+' pictures of '+str(keyword)+' are downloaded.')

# baidu_picget('周星驰+电影',5,'images2')