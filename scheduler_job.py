from functools import reduce
import time
import datetime
from apscheduler.schedulers.background import BackgroundScheduler
from img_util import calc_ratio_error
from mouse_click import MouseUtil

# 章节时间间隔
time_minute = [1, 2, 3, 4, 83, 119, 127, 100, 85, 89, 14, 87, 52, 114, 74, 125, 98, 34, 36, 126, 82, 100, 13, 13, 11]
# 章节坐标y轴递增高度
section_coord = [0, 0, 0, 0, 54, 54, 54, 54, 115, 54, 54, 54, 54, 115, 54, 54, 54, 115, 115, 115, 54, 54, 115, 54, 54]

# 当前起始章节X轴  (第四章)
current_section_x = 2575
# 当前起始章节Y轴  (第四章)
current_section_y = 325

# 屏幕误差系数
error_coefficient = calc_ratio_error()

scheduler = BackgroundScheduler()
scheduler.start()


# 切换章节
def switch_section_job(section_index):
    print("开始切换到第[" + str(section_index + 1) + "]章节")
    print("时间 ==>> "+ time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())))
    mouseUtil = MouseUtil(error_coefficient)

    # 关闭浏览器第二的table页
    mouseUtil.close_second_table()
    # 点击浏览器第一个标签页
    mouseUtil.click_first_table()

    # 点击具体章节
    sum = reduce(lambda x, y: x + y, section_coord[0: section_index + 1])
    y = current_section_y + sum
    print(str(y))
    mouseUtil.move_click(current_section_x, y)

    # 点击浏览器第二个标签页
    mouseUtil.click_second_table()
    print("---------------------------------------------------------")


# 添加切换章节任务   current_section_index = 当前第几个章节开始
def addJob(current_section_index):
    print("---------------------------------------------------------")
    print("从第[" + str(current_section_index + 1) + "]章节开始")
    print("时间[" + time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())) + "]")
    for index, val in enumerate(time_minute):
        if index >= current_section_index:
            print("第[" + str(index + 1) + "]章需要[" + str(time_minute[index]) + "]分钟")
            # 计算章节时间
            time_sum = reduce(lambda x, y: x + y, time_minute[0: index + 1])

            if index == current_section_index:
                # 当前章节20s后直接切换章节
                run_date = datetime.datetime.now() + datetime.timedelta(seconds=20)
            else:
                run_date = datetime.datetime.now() + datetime.timedelta(minutes=time_sum)
            # 当前时间+章节时间(分钟)执行任务
            scheduler.add_job(
                switch_section_job,
                args=[index],
                trigger='date',
                run_date=run_date
            )

            print("添加任务 - 第[" + str(index + 1) + "]章 - 切换章节时间[" + str(run_date.strftime('%Y-%m-%d %H:%M:%S')) + "]")
            print("---------------------------------------------------------")
        else:
            time_minute[index] = 0
    time_count = reduce(lambda x, y: x + y, time_minute[0:])
    print("总共【" + str(time_count) + "】分钟")