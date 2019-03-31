import cv2
import numpy as np
import matplotlib.pyplot as plt


def process_morphy(img):
    #Image = np.zeros(img.shape, np.uint8) 
    Image=cv2.morphologyEx(img,cv2.MORPH_CLOSE,cv2.getStructuringElement(cv2.MORPH_ELLIPSE,(10,10)))
    ret,thresh = cv2.threshold(Image,127,255,0)
    _,contours, hierarchy = cv2.findContours(thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    # find the max area of all the contours and fill it with 0
    area = []
    for i in range(len(contours)):
        area.append(cv2.contourArea(contours[i]))
    max_idx = np.argmax(area)
    cv2.drawContours(img, contours, max_idx, (0, 0, 255), 3)
    M=cv2.moments(contours[max_idx])
    cx = int(M['m10'] / M['m00'])
    cy = int(M['m01'] / M['m00'])
    #cv2.imshow("big1", big)
    print(cx,' ',cy)
    #cv2.waitKey()
    return cx,cy,contours,max_idx,Image









def is_pixel_equal( img1, img2, x, y):
    """
    判断两个像素是否相同  未使用
    :param image1: 图片1
    :param image2: 图片2
    :param x: 位置x
    :param y: 位置y
    :return: 像素是否相同
    """
    # 取两个图片的像素点
    pix1 = img1[x, y]
    pix2 = img2[x, y]
    threshold = 100
    if (abs(int(pix1[0]) - int(pix2[0])) < threshold and abs(int(pix1[1]) - int(pix2[1])) < threshold and abs(
            int(pix1[2]) - int(pix2[2])) < threshold):
        print("True",abs(int(pix1[0]) - int(pix2[0]))," ",abs(int(pix1[1]) - int(pix2[1]))," ",int(pix1[2]) - int(pix2[2]))
        return True
    else:
        print("False",abs(int(pix1[0]) - int(pix2[0]))," ",abs(int(pix1[1]) - int(pix2[1]))," ",int(pix1[2]) - int(pix2[2]))
        return False

def if_is_s(img_1, img_2):#判断是不是跟比较的是一张图
    a = 0

    for i in range(1, img_1.shape[1]):
        for j in range(1, 3):
            #print(img_1.shape[1]," ",i," ",j)
            rgb1 = img_1[j,i ]
            rgb2 = img_2[j,i]
            res1 = abs(int(rgb1[0]) - int(rgb2[0]))
            res2 = abs(int(rgb1[1]) - int(rgb2[1]))
            res3 = abs(int(rgb1[2]) - int(rgb2[2]))
            if res1 < 10 and res2 < 10 and res3 < 10:
                a += 1
            else:
                a = 0
            if a > 50:
                return a
    return -1

def get_gap_sub(img1, img2):
    sub=np.zeros(img1.shape, np.uint8)
    cv2.subtract(img1,img2,sub)
    #cv2.imshow("sub", sub)
    #cv2.waitKey()

    gray = cv2.cvtColor(sub, cv2.COLOR_RGB2GRAY)
    #cv2.imshow ("gray",gray)
    #cv2.waitKey()
    th_bin,bin = cv2.threshold(gray, 8, 255, cv2.THRESH_BINARY )

    #th_bin,bin = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
    #print(th_bin)
    #cv2.imshow ("bin",bin)

    #cv2.waitKey()

    return bin



def piture_lib(path):
    import os
    lib_list=[]
    g = os.walk(path)
    for path, d, filelist in g:
        for filename in filelist:
            if filename.endswith('png'):
                lib_list.append(os.path.join(path, filename))

    return lib_list

def calculate_distance(source):
    origin=np.zeros(source.shape, np.uint8)
    for template in piture_lib("./origin"):
        origin_find=cv2.imread(template)
        if if_is_s(source, origin_find) >0 :
            origin=origin_find.copy()
            print(template)
            break

    bin=get_gap_sub(origin,source)
    cx,cy,contours,max_idx,morphy_image=process_morphy(bin)
    #cv2.imshow ("morphy_image",morphy_image)
    cv2.drawContours(source, contours, max_idx, (0, 0, 255), 3)
    cv2.circle(source,(cx,cy),3,(0,255,0),1)
    #cv2.imshow ("big_contour",source)

    #cv2.imshow("source", source)
   #cv2.imshow("origin", origin)

    #cv2.waitKey()
    return cx-20,cy



if __name__ == '__main__':

    source = cv2.imread("./images/source23.png")
    print(calculate_distance(source))



def no_use():
    # moving_value(source)
    source = cv2.imread("./images/source14.png")

    template = cv2.imread("./images/small8.png")
    origin = cv2.imread("./origin/1.png")

    cv2.imshow("source", source)
    cv2.imshow("origin", origin)

    print(if_is_s(source, origin))
    cv2.waitKey()

    crop = template[10:50, 10:40]
    cv2.imshow("crop", crop)
    a = cv2.meanStdDev(crop)
    print(crop.shape, a)

    result = cv2.matchTemplate(source, crop, cv2.TM_CCOEFF_NORMED)

    min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(result)
    print(max_loc)
    cv2.imshow("result", result)
    print(result.shape)
    x, y = np.unravel_index(result.argmax(), result.shape)
    print(x, " ", y)
    # cv2.rectangle(source, (x + 15, y + 20), (x + 30 + 15,y + 40 + 20), (0, 0, 255))

    # cv2.rectangle(source, (y + 20,x + 15 ), (y + 40 + 20,x + 30 + 15), (0, 0, 255))
    cv2.rectangle(source, (x + 15, y + 20), (x + 30 + 15, y + 40 + 20), (0, 0, 255))
    cv2.rectangle(template, (10, 10), (40, 50), (0, 0, 255))

    cv2.imshow("source", source)
    cv2.imshow("template", template)
    cv2.waitKey()


def get_gap(img1, img2):
    """
    获取缺口偏移量
    :param img1: 不带缺口图片
    :param img2: 带缺口图片
    :return:
    """
    left = 45
    y=-1
    for i in range(left, img1.shape[0]):
        for j in range(img1.shape[1]):
            cv2.circle(img2,(i,j),2,(0,255,0),2)
            cv2.imshow("dot",img2)
            cv2.waitKey()
            if not is_pixel_equal(img1, img2, i, j):
                left = i
                y=j
                cv2.waitKey()
                return left,y
    return left,y


def access_pixels(img):
    """遍历图像每个像素的每个通道"""
    print(img.shape)  # 打印图像的高，宽，通道数（返回一个3元素的tuple）
    height = img.shape[0]  # 将tuple中的元素取出，赋值给height，width，channels
    width = img.shape[1]


    channels = img.shape[2]
    emptyImage = np.zeros(img.shape, np.uint8)
    print("height:%s,width:%s,channels:%s" % (height, width, channels))
    print(img.size)  # 打印图像数组内总的元素数目（总数=高X宽X通道数）
    for row in range(height):  # 遍历每一行
        for col in range(width):  # 遍历每一列
            for channel in range(channels):  # 遍历每个通道（三个通道分别是BGR）
                if 28 < img[row][col][channel] and img[row][col][channel] < 40:
                    emptyImage[row][col][channel] = 255
                # 通过数组索引访问该元素，并作出处理
    cv2.imshow("processed img", emptyImage)  # 将处理后的图像显示出来
    return emptyImage


def access_pixels_gray(img):
    """遍历图像每个像素的每个通道"""
    print(img.shape)              #打印图像的高，宽，通道数（返回一个3元素的tuple）
    height = img.shape[0]        #将tuple中的元素取出，赋值给height，width，channels
    width = img.shape[1]
    emptyImage = np.zeros(img.shape, np.uint8)
    print("height:%s,width:%s,channels:%s" % (height,width,1))
    print(img.size)              #打印图像数组内总的元素数目（总数=高X宽X通道数）
    for row in range(height):    #遍历每一行
        for col in range(width): #遍历每一列
                if 0<img[row][col] and img[row][col]<60:
                    emptyImage[row][col] = 255
                #通过数组索引访问该元素，并作出处理
    cv2.imshow("processed img",emptyImage) #将处理后的图像显示出来
    return  emptyImage


def moving_value(img):
    half_width = 22
    #big=cv2.imread("./index.png")
    #cv2.imshow ("big",big)
    gray = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)
    hsv = cv2.cvtColor(img, cv2.COLOR_RGB2HSV)
    h,s,v=cv2.split(hsv)
    cv2.imshow("h", h)
    cv2.imshow("s", s)
    cv2.imshow("v", v)
    cv2.imshow ("gray",gray)
    cv2.imwrite("gray.png",gray)
    afterimg=access_pixels_gray(v)
    cv2.imshow ("afterimg",afterimg)
    cv2.waitKey()
    cx,cy,contours,max_idx,morphy_image=process_morphy(afterimg)
    cv2.imshow ("morphy_image",morphy_image)
    cv2.drawContours(img, contours, max_idx, (0, 0, 255), 3)
    cv2.circle(img,(cx,cy),3,(0,255,0),1)
    cv2.imshow ("big_contour",img)

    # gauss = cv2.GaussianBlur(gray, (3, 3), 1)
    # canny = cv2.Canny(gauss, position, position*2.5)
    # cv2.imshow("Canny", canny)
    cv2.waitKey()
    return cx-half_width
