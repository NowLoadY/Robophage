import settings_pico
import utime
from tools import calculate_pico
from data import variables
from data import move_list_static
import math


def servo_move(SERVO, ANGLE, AngleRange):
    SERVO.duty_u16(int(calculate_pico.angle_to_pwm(ANGLE, AngleRange)))


def move_leg(ID, foot_pos):  # 传入足尖在身体坐标系下的坐标，驱动指定足尖移动到指定位置
    PCAservos = variables.get_val('PCAservos')
    #print("pos_ori:{}".format(foot_pos))
    if ID == 1:
        servo_list = variables.get_val('servo_list')
        foot_pos = calculate_pico.foot_pos(ID, foot_pos)  # 计算出脚尖在单腿坐标系下的坐标值（x，y，z）
        servo_angle = calculate_pico.angle_solver(foot_pos)  # （x，y，z）逆解三个舵机角度
        servo_move(servo_list[0], 90 - servo_angle[0], 180)  # 驱动最里面的舵机
        PCAservos.position(settings_pico.servo_pcapin[0][1], 90 - servo_angle[1])
        PCAservos.position(settings_pico.servo_pcapin[0][2], 90 - servo_angle[2])
        if settings_pico.print_info:
            print("1 foot_pos:" + str(foot_pos) + "\n")
            print("1 servo_angle:" + str(servo_angle) + "\n")
    elif ID == 2:
        servo_list = variables.get_val('servo_list')
        foot_pos = calculate_pico.foot_pos(ID, foot_pos)
        servo_angle = calculate_pico.angle_solver(foot_pos)
        servo_move(servo_list[1], 90 - servo_angle[0], 180)
        PCAservos.position(settings_pico.servo_pcapin[1][1], 90 - servo_angle[1])
        PCAservos.position(settings_pico.servo_pcapin[1][2], 90 - servo_angle[2])
        if settings_pico.print_info:
            print("2 foot_pos:" + str(foot_pos) + "\n")
            print("2 servo_angle:" + str(servo_angle) + "\n")
            
    elif ID == 3:
        foot_pos = calculate_pico.foot_pos(ID, foot_pos)
        servo_angle = calculate_pico.angle_solver(foot_pos)
        PCAservos.position(settings_pico.servo_pcapin[2][0], 90 - servo_angle[0])
        PCAservos.position(settings_pico.servo_pcapin[2][1], 90 - servo_angle[1])
        PCAservos.position(settings_pico.servo_pcapin[2][2], 90 - servo_angle[2])
        if settings_pico.print_info:
            print("3 foot_pos:" + str(foot_pos) + "\n")
            print("3 servo_angle:" + str(servo_angle) + "\n")
            
    elif ID == 4:
        foot_pos = calculate_pico.foot_pos(ID, foot_pos)
        servo_angle = calculate_pico.angle_solver(foot_pos)
        PCAservos.position(settings_pico.servo_pcapin[3][0], 90 - servo_angle[0])
        PCAservos.position(settings_pico.servo_pcapin[3][1], 90 - servo_angle[1])
        PCAservos.position(settings_pico.servo_pcapin[3][2], 90 - servo_angle[2])
        if settings_pico.print_info:
            print("4 foot_pos:" + str(foot_pos) + "\n")
            print("4 servo_angle:" + str(servo_angle) + "\n")
    elif ID == 5:
        foot_pos = calculate_pico.foot_pos(ID, foot_pos)
        servo_angle = calculate_pico.angle_solver(foot_pos)
        PCAservos.position(settings_pico.servo_pcapin[4][0], 90 - servo_angle[0])
        PCAservos.position(settings_pico.servo_pcapin[4][1], 90 - servo_angle[1])
        PCAservos.position(settings_pico.servo_pcapin[4][2], 90 - servo_angle[2])
        if settings_pico.print_info:
            print("5 foot_pos:" + str(foot_pos) + "\n")
            print("5 servo_angle:" + str(servo_angle) + "\n")
            
    elif ID == 6:
        foot_pos = calculate_pico.foot_pos(ID, foot_pos)
        servo_angle = calculate_pico.angle_solver(foot_pos)
        PCAservos.position(settings_pico.servo_pcapin[5][0], 90 - servo_angle[0])
        PCAservos.position(settings_pico.servo_pcapin[5][1], 90 - servo_angle[1])
        PCAservos.position(settings_pico.servo_pcapin[5][2], 90 - servo_angle[2])
        if settings_pico.print_info:
            print("6 foot_pos:" + str(foot_pos) + "\n")
            print("6 servo_angle:" + str(servo_angle) + "\n")
            


def Init():
    LIST = move_list_static.OriginalData()
    for i in range(len(LIST[0])):  # 时间轴长度内依次执行
        for j, LegPos_With_Time in enumerate(LIST):  # 腿
            move_leg(j + 1, LegPos_With_Time[i])
    variables.set_val('last_move', 'Init')
        


def Walk(Direction):  # Direction给z平面内角度，角度制
    LIST = move_list_static.straightData(Direction)
    # print(LIST)
    for i in range(len(LIST[0])):  # 时间轴长度内依次执行
        # print('i:'+str(i))
        for j, LegPos_With_Time in enumerate(LIST):  # 腿
            # print('LegPos:'+str(LegPos_With_Time[i]))
            # print('j:'+str(j))
            move_leg(j + 1, LegPos_With_Time[i])
        utime.sleep_ms(40)  # 加了延迟, 减缓动作
    variables.set_val('last_move', 'Walk')


def Turn(ANGLE):  # ANGLE给左转为正的角度
    LIST = move_list_static.Turn_Round(ANGLE)
    fluence = 30

    #def curve(j):
        #return (math.cos((j + 1) / fluence * math.pi - math.pi) + 1) / 2  # 时间响应递增曲线函数，值域(0,1]

    #for i in range(fluence):
        #variables.set_val('move_rpy', [0, 0, -curve(i)*ANGLE])
        #Init()
        #utime.sleep_ms(1)  # 加了延迟, 减缓动作
    
    for i in range(len(LIST[0])):  # 时间轴长度内执行

        for j, LegPos_With_Time in enumerate(LIST):  # 腿
            move_leg(j + 1, LegPos_With_Time[i])
        #utime.sleep_ms(40)  # 加了延迟, 减缓动作
    #variables.set_val('move_rpy', [0, 0, 0])
    #for i in range(fluence):
        #variables.set_val('move_rpy', [0, 0, -curve(fluence-i)*ANGLE])
        #Init()
        #utime.sleep_ms(1)  # 加了延迟, 减缓动作
    variables.set_val('last_move', 'Turn')


def Rpy(RPY):
    pass


def Draw(Curve):  # 一系列点，组成曲线轨迹
    for Info in Curve:
        if Info == "leave":
            variables.set_val('leg_width', variables.get_val('leg_width') - 10)
            height = variables.get_val('height')
            for i in range(13):
                variables.set_val('height', height - i)
                Init()
                utime.sleep(0.01)
            variables.set_val('body_shift', [[0, 90, 90], 0])
        elif Info == "put":
            variables.set_val('leg_width', variables.get_val('leg_width') + 10)
            height = variables.get_val('height')
            for i in range(13):
                variables.set_val('height', height + i)
                Init()
                utime.sleep(0.01)
        else:
            variables.set_val('height', -39)
            variables.set_val('body_shift', [(math.atan2(Info[1], Info[0]), math.atan2(Info[0], Info[1]), 90),
                                             math.sqrt(Info[0] ** 2 + Info[1] ** 2)])
            Init()
        # utime.sleep_ms(50)  # 加了延迟, 减缓动作
        print(variables.get_val('height'))


print("move_pico loaded")
