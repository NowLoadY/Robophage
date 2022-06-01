"""
用于生成绘画需要的点集，以左上角为原点，向下为x正，向右为y正
"""
import math


def Demo(Key, Scale=1, Fluence=160, R=25):  # 标准大小为1倍
    if Key == 'circle':
        LIST = ["put"]
        for i in range(Fluence):
            LIST.append([round(Scale * R * math.cos((i / Fluence) * 2 * math.pi), 2),
                         round(Scale * R * math.sin((i / Fluence) * 2 * math.pi), 2)])
        LIST.append("leave")
        return LIST
    # elif Key == 'Square':
    # R = 50
    # LIST = ["put"]
    # for i in range(Fluence):
    # LIST.append(Scale*[])
    else:
        return None


print("Curve_generator loaded")
