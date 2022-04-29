from image_identification import getCoord, batchGetCoord, getCoord2
from screenshot import window_capture
import time

if __name__ =='__main__':

    # targetPath = "./img/target/target.png"
    # while(True):
    #     window_capture(targetPath)
    #     time.sleep(1)
    #
    #     x,y = getCoord(targetPath = targetPath)
    #     print("x:==>" + str(x) + "   y:==>" + str(y))
    #     time.sleep(1)

    getCoord2(targetPath= "./img/target/t1.png", templatePath = "./img/template/c1.png")