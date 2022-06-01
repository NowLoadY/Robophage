import math
import settings_pico
from data import variables


# 舵机
def angle_to_pwm(ANGLE, angle_range):  # 目标转动角度 舵机机械转动范围
    return (0.5 + (ANGLE / angle_range * 2)) / settings_pico.servo_T * 65535


# 坐标变换
def rotate_around_z(rotateANGLE, SET):  # 输入坐标，旋转角度(顺时针)，输出坐标
    X = int((SET[0] * math.cos(rotateANGLE * math.pi / 180)) + (SET[1] * math.sin(rotateANGLE * math.pi / 180)))
    Y = int((SET[1] * math.cos(rotateANGLE * math.pi / 180)) - (SET[0] * math.sin(rotateANGLE * math.pi / 180)))
    return [X,Y,SET[2]]


def rotate_around_x(rotateANGLE, SET):  # 输入坐标，旋转角度(顺时针)，输出坐标
    Y = int((SET[1] * math.cos(rotateANGLE * math.pi / 180)) + (SET[2] * math.sin(rotateANGLE * math.pi / 180)))
    Z = int((SET[2] * math.cos(rotateANGLE * math.pi / 180)) - (SET[1] * math.sin(rotateANGLE * math.pi / 180)))
    return [SET[0],Y,Z]


def rotate_around_y(rotateANGLE, SET):  # 输入坐标，旋转角度(顺时针)，输出坐标
    X = int((SET[0] * math.cos(rotateANGLE * math.pi / 180)) - (SET[2] * math.sin(rotateANGLE * math.pi / 180)))
    Z = int((SET[2] * math.cos(rotateANGLE * math.pi / 180)) + (SET[0] * math.sin(rotateANGLE * math.pi / 180)))
    return [X,SET[1],Z]


def rpy(RPY, SET):
    SET = rotate_around_x(RPY[0], SET)
    SET = rotate_around_y(RPY[1], SET)
    SET = rotate_around_z(RPY[2], SET)
    return SET


def shift(Direction, Distance, SET):  # 角度制
    return [SET[0] + Distance * math.cos(Direction[0] * math.pi / 180),
            SET[1] + Distance * math.cos(Direction[1] * math.pi / 180),
            SET[2] + Distance * math.cos(Direction[2] * math.pi / 180)]


def foot_pos(FOOT_ID, BODY_SET, gyro=None):  # 传入一个脚尖在身体坐标系的坐标，计算该脚尖在单腿坐标系下的坐标
    if gyro is None:
        gyro = [0, 0, 0]
    # 陀螺仪修正平衡
    BODY_SET = rpy(gyro, BODY_SET)
    # 自身主动旋转
    BODY_SET = rpy(variables.get_val('move_rpy'), BODY_SET)
    BS = variables.get_val('body_shift')
    # 平移
    BODY_SET[0] += math.cos((BS[0][0]))*BS[1]
    BODY_SET[1] += math.cos((BS[0][1])) * BS[1]
    BODY_SET[2] += math.cos((BS[0][2])) * BS[1]
    if FOOT_ID == 1:
        # 平移
        BODY_SET[0] += settings_pico.Trans[FOOT_ID - 1][0]
        BODY_SET[1] += settings_pico.Trans[FOOT_ID - 1][1]
        BODY_SET[2] += 0
        # z轴旋转
        BODY_SET = rpy((0, 0, 120), BODY_SET)
        
        
    elif FOOT_ID == 2:
        # 平移
        BODY_SET[0] += settings_pico.Trans[FOOT_ID - 1][0]
        BODY_SET[1] += settings_pico.Trans[FOOT_ID - 1][1]
        BODY_SET[2] += 0
        # z轴旋转
        BODY_SET = rpy((0, 0, 60), BODY_SET)
        
        
    elif FOOT_ID == 3:
        # 平移
        BODY_SET[0] += settings_pico.Trans[FOOT_ID - 1][0]
        BODY_SET[1] += settings_pico.Trans[FOOT_ID - 1][1]
        BODY_SET[2] += 0
        # z轴旋转
        BODY_SET = rpy((0, 0, 180), BODY_SET)
        
    elif FOOT_ID == 4:
        # 平移
        BODY_SET[0] += settings_pico.Trans[FOOT_ID - 1][0]
        BODY_SET[1] += settings_pico.Trans[FOOT_ID - 1][1]
        BODY_SET[2] += 0
        # z轴旋转
        BODY_SET = rpy((0, 0, 0), BODY_SET)
        
    elif FOOT_ID == 5:
        # 平移
        BODY_SET[0] += settings_pico.Trans[FOOT_ID - 1][0]
        BODY_SET[1] += settings_pico.Trans[FOOT_ID - 1][1]
        BODY_SET[2] += 0
        # z轴旋转
        BODY_SET = rpy((0, 0, -120), BODY_SET)
        
    elif FOOT_ID == 6:
        # 平移
        BODY_SET[0] += settings_pico.Trans[FOOT_ID - 1][0]
        BODY_SET[1] += settings_pico.Trans[FOOT_ID - 1][1]
        BODY_SET[2] += 0
        # z轴旋转
        BODY_SET = rpy((0, 0, -60), BODY_SET)
        
    return BODY_SET


def angle_solver(FOOT_POS):  # 舵机旋转角度计算,输入单腿坐标系下的坐标，逆算舵机角度
    pi = math.pi
    try:
        angle1 = math.atan2(FOOT_POS[0], FOOT_POS[1]) * 180 / pi
        D1 = math.sqrt(FOOT_POS[0] ** 2 + FOOT_POS[1] ** 2)
        aerfa2 = math.atan2(-FOOT_POS[2], (D1 - settings_pico.leg_length[0]))
        D2 = math.sqrt(FOOT_POS[2] ** 2 + (D1 - settings_pico.leg_length[0]) ** 2)
        aerfa1 = math.acos(((settings_pico.leg_length[1] ** 2) + D2 ** 2 - (settings_pico.leg_length[2] ** 2)) / (
                2 * settings_pico.leg_length[1] * D2))
        aerfa3 = math.acos(((D2 ** 2 + settings_pico.leg_length[2] ** 2 - settings_pico.leg_length[1] ** 2) / (
                2 * settings_pico.leg_length[2] * D2)))
        angle2 = (aerfa1 - aerfa2) * 180 / pi
        angle3 = (aerfa1 + aerfa3 - pi / 2) * 180 / pi
        return [angle1, angle2, angle3]
    except:
        return [0, 0, 0]
