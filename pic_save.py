import requests
import os
import base64
import  time
def get_picture(url):
    try:
        img = base64.urlsafe_b64decode(url + '=' * (4 - len(url) % 4))
        filename="./images/imageToSave" + time.strftime("%H_%M_%S", time.localtime()) + ".png"
        fh = open(filename, "wb")
        fh.write(img)
        fh.close()
        return filename
    except:
        print("爬取失败")
        return ""

def no_use(url):
    #url="http://p1.so.qhmsg.com/bdr/_240_/t01dab8b2e73fe661d6.jpg"
    root="./images"   #根目录
    #path=root+url.split('/')[-1] #根目录加上url中以反斜杠分割的最后一部分，即可以以图片原来的名字存储在本地
    path = ""

    if not os.path.exists(root):  # 判断当前根目录是否存在
        os.mkdir(root)  # 创建根目录
    if not os.path.exists(path):  # 判断文件是否存在
        r = requests.get(url)
        with open(path, 'wb')as f:
            f.write(r.content)
            f.close()
            print("文件保存成功")
    else:
        print("文件已存在")

    try:
        if not os.path.exists(root):#判断当前根目录是否存在
            os.mkdir(root)          #创建根目录
        if not os.path.exists(path):#判断文件是否存在
            r=requests.get(url)
            with open(path,'wb')as f:
                f.write(r.content)
                f.close()
                print("文件保存成功")
        else:
            print("文件已存在")
    except:
        print("爬取失败")


