import win32gui
import win32print
import win32ui
import win32api

from win32.lib import win32con

# 计算屏幕缩放误差系数
def calc_ratio_error():
    hdc = win32gui.GetDC(0)
    # 屏幕真实宽高
    real_w = win32print.GetDeviceCaps(hdc, win32con.DESKTOPHORZRES)
    real_h = win32print.GetDeviceCaps(hdc, win32con.DESKTOPVERTRES)
    print("屏幕真实宽 =>" + str(real_w) + "   屏幕真实高 => " + str(real_h))

    # 压缩后的宽高
    w = int(win32api.GetSystemMetrics(0))
    h = int(win32api.GetSystemMetrics(1))
    print("屏幕压缩后宽 =>" + str(w) + "   屏幕压缩后高 => " + str(h))

    error_coefficient = float(real_w / w)
    print("误差系数 ==> " + str(error_coefficient))
    return error_coefficient


class Capture:

    def __init__(self, filename):
        hdc = win32gui.GetDC(0)
        self.w = win32print.GetDeviceCaps(hdc, win32con.DESKTOPHORZRES)
        self.h = win32print.GetDeviceCaps(hdc, win32con.DESKTOPVERTRES)
        self.filename = filename

    # 截图
    def window_capture(self):
        hwnd = 0  # 窗口的编号，0号表示当前活跃窗口
        # 根据窗口句柄获取窗口的设备上下文DC（Divice Context）
        hwndDC = win32gui.GetWindowDC(hwnd)
        # 根据窗口的DC获取mfcDC
        mfcDC = win32ui.CreateDCFromHandle(hwndDC)
        # mfcDC创建可兼容的DC
        saveDC = mfcDC.CreateCompatibleDC()
        # 创建bigmap准备保存图片
        saveBitMap = win32ui.CreateBitmap()

        # print w,h　　　#图片大小
        # 为bitmap开辟空间
        saveBitMap.CreateCompatibleBitmap(mfcDC, self.w, self.h)
        # 高度saveDC，将截图保存到saveBitmap中
        saveDC.SelectObject(saveBitMap)
        # 截取从左上角（0，0）长宽为（w，h）的图片
        saveDC.BitBlt((0, 0), (self.w, self.h), mfcDC, (0, 0), win32con.SRCCOPY)
        saveBitMap.SaveBitmapFile(saveDC, self.filename)

    # 计算屏幕缩放与真实分辨率的误差系数


if __name__ =='__main__':
    capture = Capture("img/target/target2.png")
    #capture.window_capture()
    calc_ratio_error()
