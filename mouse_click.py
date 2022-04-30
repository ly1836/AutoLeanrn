import mouse


def click():
    mouse.click()


def move_to_default():
    print("鼠标复位...")
    mouse.move(0, 0, duration=1)


class MouseUtil:

    def __init__(self, error_coefficient):
        # 鼠标点击坐标系误差系数，该鼠标操作依赖库获取后的坐标系是屏幕压缩后的分辨率，
        # 所以应该在输入坐标系中除以误差系数
        self.error_coefficient = error_coefficient

    # 鼠标移动到指定坐标单击
    def move_click(self, x, y):
        if self.error_coefficient != 0:
            x = x / self.error_coefficient
            y = y / self.error_coefficient
        # 移动到该坐标
        mouse.move(x, y, duration=1)
        click()

    # 关闭浏览器第二的table页
    def close_second_table(self):
        mouse.move(706 / self.error_coefficient, 24 / self.error_coefficient, duration=1)
        click()
        print("关闭浏览器第二的页签...")

    # 点击浏览器第一个标签页
    def click_first_table(self):
        mouse.move(180 / self.error_coefficient, 25 / self.error_coefficient, duration=1)
        click()
        print("点击浏览器第一个标签页...")

    # 点击浏览器第二个标签页
    def click_second_table(self):
        mouse.move(555 / self.error_coefficient, 25 / self.error_coefficient, duration=1)
        click()
        print("点击浏览器第一个标签页...")
