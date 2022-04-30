#opencv模板匹配----单目标匹配
import cv2
import numpy as np
import gc

# 设置最低特征点匹配数量为10
MIN_MATCH_COUNT = 30
# 创建设置FLANN匹配
FLANN_INDEX_KDTREE = 0

template = None
target = None
sift = None
kp1 = None
des1 = None
kp2 = None
des2 = None

# 获取图片中匹配到的坐标x、y轴
def getCoordByFLANN(targetPath = "./img/target/t1.png", templatePath = "./img/template/continue.png"):
    template = cv2.imread(templatePath, 0)  # queryImage
    target = cv2.imread(targetPath, 0)  # trainImage
    # Initiate SIFT detector创建sift检测器
    sift = cv2.xfeatures2d.SIFT_create()
    # find the keypoints and descriptors with SIFT
    kp1, des1 = sift.detectAndCompute(template, None)
    kp2, des2 = sift.detectAndCompute(target, None)
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
        h, w = template.shape
        # 使用得到的变换矩阵对原图像的四个角进行变换，获得在目标图像上对应的坐标
        pts = np.float32([[0, 0], [0, h - 1], [w - 1, h - 1], [w - 1, 0]]).reshape(-1, 1, 2)
        dst = cv2.perspectiveTransform(pts, M)
        print("识别匹配到的图像：误差 - %d/%d" % (len(good), MIN_MATCH_COUNT))
        print(dst)
        print("计算图像区域中心点...")
        D0 = int(dst[3][0][0])
        A0 = int(dst[0][0][0])
        B1 = int(dst[1][0][1])
        A1 = int(dst[0][0][1])
        click_x = ((D0 - A0) / 2) + A0
        click_y = ((B1 - A1) / 2) + A1

        gc.collect()
        return click_x, click_y
    else:
        gc.collect()
        return None, None
