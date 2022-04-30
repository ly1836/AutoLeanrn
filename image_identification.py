#opencv模板匹配----单目标匹配
import cv2
import numpy
import numpy as np
from matplotlib import pyplot as plt

# 获取图片中火匹配到的坐标x、y轴
def getCoord(targetPath = "./img/target/t3.png", templatePath = "./img/template/c3.png"):
    #读取目标图片
    target = cv2.imread(targetPath)
    #读取模板图片
    template = cv2.imread(templatePath)
    #获得模板图片的高宽尺寸
    theight, twidth = template.shape[:2]
    #执行模板匹配，采用的匹配方式cv2.TM_SQDIFF_NORMED
    result = cv2.matchTemplate(target,template,cv2.TM_SQDIFF_NORMED)
    #归一化处理
    cv2.normalize( result, result, 0, 1, cv2.NORM_MINMAX, -1 )
    #寻找矩阵（一维数组当做向量，用Mat定义）中的最大值和最小值的匹配结果及其位置
    min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(result)
    #匹配值转换为字符串
    #对于cv2.TM_SQDIFF及cv2.TM_SQDIFF_NORMED方法min_val越趋近与0匹配度越好，匹配位置取min_loc
    #对于其他方法max_val越趋近于1匹配度越好，匹配位置取max_loc
    strmin_val = str(min_val)
    #绘制矩形边框，将匹配区域标注出来
    #min_loc：矩形定点
    #(min_loc[0]+twidth,min_loc[1]+theight)：矩形的宽高

    x = (int)(min_loc[0]+ (twidth / 2))
    y = (int)(min_loc[1] + (theight / 2))


    #(0,0,225)：矩形的边框颜色；2：矩形边框宽度
    cv2.rectangle(target,min_loc,(min_loc[0]+twidth, min_loc[1] + theight),(0,0,225),2)
    cv2.rectangle(target,min_loc,(x, y),(0,225,0),2)

    #显示结果,并将匹配值显示在标题栏上
    cv2.imshow("MatchResult----MatchingValue="+strmin_val,target)
    cv2.waitKey()
    cv2.destroyAllWindows()

    return x, y


def batchGetCoord(targetPath = "./img/target/t1.png", templatePath = "./img/template/continue.png"):
    #opencv模板匹配----多目标匹配
    #读取目标图片
    target = cv2.imread(targetPath)
    #读取模板图片
    template = cv2.imread(templatePath)
    #获得模板图片的高宽尺寸
    theight, twidth = template.shape[:2]
    #执行模板匹配，采用的匹配方式cv2.TM_SQDIFF_NORMED
    result = cv2.matchTemplate(target,template,cv2.TM_SQDIFF_NORMED)
    #归一化处理
    #cv2.normalize( result, result, 0, 1, cv2.NORM_MINMAX, -1 )
    #寻找矩阵（一维数组当做向量，用Mat定义）中的最大值和最小值的匹配结果及其位置
    min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(result)
    #绘制矩形边框，将匹配区域标注出来
    #min_loc：矩形定点
    #(min_loc[0]+twidth,min_loc[1]+theight)：矩形的宽高
    #(0,0,225)：矩形的边框颜色；2：矩形边框宽度
    cv2.rectangle(target,min_loc,(min_loc[0]+twidth,min_loc[1]+theight),(0,0,225),2)
    #匹配值转换为字符串
    #对于cv2.TM_SQDIFF及cv2.TM_SQDIFF_NORMED方法min_val越趋近与0匹配度越好，匹配位置取min_loc
    #对于其他方法max_val越趋近于1匹配度越好，匹配位置取max_loc
    strmin_val = str(min_val)
    #初始化位置参数
    temp_loc = min_loc
    other_loc = min_loc
    numOfloc = 1
    #第一次筛选----规定匹配阈值，将满足阈值的从result中提取出来
    #对于cv2.TM_SQDIFF及cv2.TM_SQDIFF_NORMED方法设置匹配阈值为0.01
    threshold = 0.01
    loc = numpy.where(result<threshold)
    #遍历提取出来的位置
    for other_loc in zip(*loc[::-1]):
        #第二次筛选----将位置偏移小于5个像素的结果舍去
        if (temp_loc[0]+5<other_loc[0])or(temp_loc[1]+5<other_loc[1]):
            numOfloc = numOfloc + 1
            temp_loc = other_loc
            cv2.rectangle(target,other_loc,(other_loc[0]+twidth,other_loc[1]+theight),(0,0,225),2)
    str_numOfloc = str(numOfloc)
    #显示结果,并将匹配值显示在标题栏上
    strText = "MatchResult----MatchingValue="+strmin_val+"----NumberOfPosition="+str_numOfloc
    cv2.imshow(strText,target)
    cv2.waitKey()
    cv2.destroyAllWindows()



# 获取图片中匹配到的坐标x、y轴
def getCoordByFLANN(targetPath = "./img/target/t1.png", templatePath = "./img/template/continue.png"):
    MIN_MATCH_COUNT = 10  # 设置最低特征点匹配数量为10
    template = cv2.imread(templatePath, 0)  # queryImage
    target = cv2.imread(targetPath, 0)  # trainImage
    # Initiate SIFT detector创建sift检测器
    sift = cv2.xfeatures2d.SIFT_create()
    # find the keypoints and descriptors with SIFT
    kp1, des1 = sift.detectAndCompute(template, None)
    kp2, des2 = sift.detectAndCompute(target, None)
    # 创建设置FLANN匹配
    FLANN_INDEX_KDTREE = 0
    index_params = dict(algorithm=FLANN_INDEX_KDTREE, trees=5)
    search_params = dict(checks=50)
    flann = cv2.FlannBasedMatcher(index_params, search_params)
    matches = flann.knnMatch(des1, des2, k=2)
    # store all the good matches as per Lowe's ratio test.
    good = []
    # 舍弃大于0.7的匹配
    for m, n in matches:
        if m.distance < 0.7 * n.distance:
            good.append(m)
    if len(good) > MIN_MATCH_COUNT:
        # 获取关键点的坐标
        src_pts = np.float32([kp1[m.queryIdx].pt for m in good]).reshape(-1, 1, 2)
        dst_pts = np.float32([kp2[m.trainIdx].pt for m in good]).reshape(-1, 1, 2)
        # 计算变换矩阵和MASK
        M, mask = cv2.findHomography(src_pts, dst_pts, cv2.RANSAC, 5.0)
        matchesMask = mask.ravel().tolist()
        h, w = template.shape
        # 使用得到的变换矩阵对原图像的四个角进行变换，获得在目标图像上对应的坐标
        pts = np.float32([[0, 0], [0, h - 1], [w - 1, h - 1], [w - 1, 0]]).reshape(-1, 1, 2)
        dst = cv2.perspectiveTransform(pts, M)
        print("识别匹配到的图像坐标为：")
        print(dst)
        print("计算图像区域中心点...")
        D0 = int(dst[3][0][0])
        A0 = int(dst[0][0][0])
        B1 = int(dst[1][0][1])
        A1 = int(dst[0][0][1])
        click_x = ((D0 - A0) / 2) + A0
        click_y = ((B1 - A1) / 2) + A1

        return click_x, click_y
    else:
        print("未识别出符合误差的图片，误差 - %d/%d" % (len(good), MIN_MATCH_COUNT))
        return None, None