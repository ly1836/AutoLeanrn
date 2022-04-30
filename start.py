import time
from datetime import datetime
from image_identification import getCoordByFLANN
from img_util import Capture, calc_ratio_error
from mouse_click import MouseUtil, move_to_default
from scheduler_job import addJob

targetPath = "./img/target/target.png"
templatePath = "./img/template/c1.png"

# 屏幕误差系数
error_coefficient = calc_ratio_error()


if __name__ == '__main__':
    # 添加切换章节任务
    # 第四章开始
    addJob(3)

    while True:
        try:
            capture = Capture(targetPath)
            mouseUtil = MouseUtil(error_coefficient)

            capture.window_capture()
            time.sleep(1)

            click_x, click_y = getCoordByFLANN(targetPath=targetPath, templatePath=templatePath)
            if click_x is not None and click_y is not None:
                print("==============================================")
                print("==============================================")
                dt = datetime.now()
                print(f'时间 => {dt.month}月{dt.day}日 {dt.hour}:{dt.minute}:{dt.second}')
                print("开始模拟鼠标点击:==>" + str(click_x) + "   click_y:==>" + str(click_y))
                print("x => " + str(click_x) + "   y:=> " + str(click_y))
                mouseUtil.move_click(1921, 1180)
                # 鼠标复位
                move_to_default()
                print("==============================================")
                print("==============================================")
        except Exception as ex:
            print("程序出现异常!" + str(ex))

