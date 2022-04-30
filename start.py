import time

from image_identification import getCoordByFLANN
from img_util import Capture, calc_ratio_error
from mouse_click import MouseUtil, move_to_default

targetPath = "./img/target/target.png"
templatePath = "./img/template/continue.png"

capture = Capture(targetPath)
# 屏幕误差系数
error_coefficient = calc_ratio_error()
mouseUtil = MouseUtil(error_coefficient)

if __name__ == '__main__':

    while True:
        capture.window_capture()
        time.sleep(1)

        click_x, click_y = getCoordByFLANN(targetPath=targetPath, templatePath=templatePath)
        if click_x is not None and click_y is not None:
            print("开始模拟鼠标点击:==>" + str(click_x) + "   click_y:==>" + str(click_y))
            print("x => " + str(click_x) + "   y:=> " + str(click_y))
            mouseUtil.move_click(click_x, click_y)
            # 鼠标复位
            move_to_default()

