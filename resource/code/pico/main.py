#!/usr/bin/python
# -*- coding: UTF-8 -*-
"""
██████   ██████  ██████   ██████  ██████  ██   ██  █████   ██████  ███████ 
██   ██ ██    ██ ██   ██ ██    ██ ██   ██ ██   ██ ██   ██ ██       ██      
██████  ██    ██ ██████  ██    ██ ██████  ███████ ███████ ██   ███ █████   
██   ██ ██    ██ ██   ██ ██    ██ ██      ██   ██ ██   ██ ██    ██ ██      
██   ██  ██████  ██████   ██████  ██      ██   ██ ██   ██  ██████  ███████
            micropython对六足机器人的控制程序
程序编写：NowLoadY
简述：
    树莓派pico根据串口的消息对六足做出对应操作
动作：任意方向直行、转向、扭转身体
补充：因为是读表（data.move_list_static.py）加上实时参数生成步态,所以步态特性可以实时改变
"""

#################导入拓展包和子文件###################
from machine import Pin, UART, PWM, Timer, I2C
import utime

# 板载led初始化和亮灯
led = Pin(25, Pin.OUT)
led.value(1)
utime.sleep(1)  # 绝对不能删，不然以后thonny进不了pico
led.value(0)

import settings_pico
from data import variables
from data import move_list_static
from tools import Curve_generator as Curve
from tools.PCA9685.servo import Servos

if settings_pico.use_imu:
    from tools import imuread_pico
from tools import move_pico

# 全局变量定义
if True:
    variables._init()
    # 身体高度
    variables.set_val('height', -75)
    # 动作等待时间
    variables.set_val('delay_s', 2)
    variables.set_val('delay_move', 30)
    # 脚伸展到四周距离
    variables.set_val('leg_width', 70)
    # 抬脚高度
    variables.set_val('foot_up', 20)
    # 步长
    variables.set_val('step_length', 30)
    # 不可改，临时变量
    variables.set_val('move_rpy', [0, 0, 0])
    variables.set_val('body_shift', [[180, 90, 90], 0])  # 与x、y、z轴夹角，平移长度
    variables.set_val('gyro', [0, 0, 0])
    variables.set_val('default_rpy', [0, 0, 0])
    variables.set_val('last_pos', move_list_static.OriginalData())
    variables.set_val('first_time', True)
    variables.set_val("command_info", [])
    variables.set_val('last_move', '')
#####################GPIO设置##############################
if settings_pico.use_laser:  # 激光灯
    laser = Pin(settings_pico.laser_Pin, Pin.OUT)
    laser.value(1)
#####################PWM设置##############################
if settings_pico.use_propeller:  # 激光灯
    LXJ = PWM(Pin(settings_pico.propeller_Pin))  # PWM_A[5]
    LXJ.freq(50)
    LXJ.duty_u16(0)
    utime.sleep(1)
    LXJ.duty_u16(65535)
if settings_pico.use_beep:  # 蜂鸣器
    beep = PWM(Pin(settings_pico.beep_Pin))  # PWM_A[5]
    beep.freq(440)
    beep.duty_u16(65500)
    utime.sleep(1)


###############imu配置#####################
if settings_pico.use_imu:
    try:
        imuSer = UART(settings_pico.uart_to_imu, baudrate=settings_pico.uart_to_imu_baud, tx=Pin(8), rx=Pin(9))
        print("UART" + str(settings_pico.uart_to_imu) + " opened successfully")
    except:
        print("UART" + str(settings_pico.uart_to_imu) + " went wrong")

##############和电脑、手机通信的串口设置#############
try:
    uart1 = UART(settings_pico.uart_to_computer, baudrate=settings_pico.uart_to_computer_baud, tx=Pin(0), rx=Pin(1))
    print("UART" + str(settings_pico.uart_to_computer) + " opened successfully")
    uart1.write('uart0 is ok\r\n')
except:
    print("UART" + str(settings_pico.uart_to_computer) + " went wrong")


def send_message_to_COM(Message):
    try:
        uart1.write(Message.encode('utf-8'))
        uart1.write(b'\n\r')
        print(type(Message))

        print(Message)
    except:
        print("sent |" + Message + "| but " + settings_pico.uart_to_computer + " went wrong!")


try:
    def read_command(command_timer):
        rxData = bytes()
        if uart1.any():
            led.value(1)
            while uart1.any() > 0:
                rxData += uart1.read(1)
            try:
                command = rxData.decode('utf-8').split(',')
                print("uart1:{}".format(command))
                variables.set_val("command_info", command)
            except:
                pass
            led.value(0)

except:
    pass
try:
    def read_imu(imu_timer):
        rxData = bytes()
        while imuSer.any() > 0:
            rxData += imuSer.read(1)
        variables.set_val("imu_info", rxData.decode('utf-8'))
except:
    pass

# 初始化计时器中断
# tim.init(period, mode, callback)
# period:周期(ms)
# mode:工作模式，有Timer.ONE_SHOT(实行一次)和Timer.PERIODIC(规律性实行)二种
# callback:定时器中断的调用函数

# try:
command_timer = Timer()  # 接收指令的计时器
command_timer.init(period=100, mode=Timer.PERIODIC, callback=read_command)
if settings_pico.use_imu:
    imu_timer = Timer()  # 接收指令的计时器
    imu_timer.init(period=10, mode=Timer.PERIODIC, callback=read_imu)
# except:
# print("Timer wrong")
# 初始化pca9685的控制
i2c = I2C(0, sda=Pin(12), scl=Pin(13), freq=10000)
PCAservos = Servos(i2c, address=0x40)
# 定义舵机引脚
servo_pin = settings_pico.servo_pin
variables.set_val('PCAservos', PCAservos)
leg11_servo = PWM(Pin(servo_pin[0][0]))  # PWM_A[1]
leg21_servo = PWM(Pin(servo_pin[1][0]))  # PWM_B[2]
servo_list = [leg11_servo, leg21_servo]
for servo in servo_list:
    servo.freq(settings_pico.servo_f)  # 产生50Hz的PWM波，周期20ms
variables.set_val('servo_list', servo_list)
#PCAservos.position(settings_pico.servo_pcapin[0][1], 90)
#PCAservos.position(settings_pico.servo_pcapin[0][2], 90)

#PCAservos.position(settings_pico.servo_pcapin[1][1], 90)
#PCAservos.position(settings_pico.servo_pcapin[1][2], 90)

#PCAservos.position(settings_pico.servo_pcapin[2][0], 90)
#PCAservos.position(settings_pico.servo_pcapin[2][1], 90)
#PCAservos.position(settings_pico.servo_pcapin[2][2], 90)

#PCAservos.position(settings_pico.servo_pcapin[3][0], 90)
#PCAservos.position(settings_pico.servo_pcapin[3][1], 90)
#PCAservos.position(settings_pico.servo_pcapin[3][2], 90)

#PCAservos.position(settings_pico.servo_pcapin[4][0], 90)
#PCAservos.position(settings_pico.servo_pcapin[4][1], 90)
#PCAservos.position(settings_pico.servo_pcapin[4][2], 90)

#PCAservos.position(settings_pico.servo_pcapin[5][0], 90)
#PCAservos.position(settings_pico.servo_pcapin[5][1], 90)
#PCAservos.position(settings_pico.servo_pcapin[5][2], 90)
move_pico.Init()

##########################################################################################
while True:
    # 例子
    # 直走
    # move_pico.Walk(90)
    # 转向
    # move_pico.Turn(45)
    # 单独控制1、2号腿的1号舵机（PCA9685有16路，而舵机有18个）
    #move_pico.servo_move(leg11_servo, 60, 180)
    #move_pico.servo_move(leg21_servo, 60, 180)
    # 通过PCA9685控制1号腿的3号舵机
    #PCAservos.position(settings_pico.servo_pcapin[0][2], 90)
    #utime.sleep(1)
    # roll、pitch、yaw的更改
    # for num in range(2):
    # variables.set_val('move_rpy', [-10+num*2, -10+num*2, -10+num*2])
    # variables.set_val('move_rpy', [0, 0, -10+num*10])
    # move_pico.Init()  # 立即实际执行以上参数更改
    # for num in range(2):
    # variables.set_val('move_rpy', [10-num*2, 10-num*2, 10-num*2])
    # variables.set_val('move_rpy', [0, 0, 10-num*10])
    # move_pico.Init()
    # 绘制圆圈
    # move_pico.Draw(Curve.Demo('circle'))
    # 移动1号腿到指定坐标（物体坐标系，身体为参考）
    # move_pico.move_leg(1,[60,60,-85])
    # print("ok")
    # 分析当前来自全局变量的指令，并驱动机器人
    command = variables.get_val("command_info")
    if len(command) > 0:
        try:
            if command[0] == 'W':  # 朝一个方向直行
                move_pico.Walk(int(command[1]))
                variables.set_val('last_move', 'Walk')
            elif command[0] == 'T':  # 转向
                move_pico.Turn(int(command[1]))
                variables.set_val('last_move', 'Turn')
            elif command[0] == 'S':  # 停止
                variables.set_val("command_info", [])
                variables.set_val('last_move', '')
                move_pico.Init()
            elif command[0] == 'D':  # 绘制图案
                move_pico.Draw(Curve.Demo('circle'))
                variables.set_val('last_move', 'Draw')
                variables.set_val("command_info", [])
            elif command[0] == 'R':  # 扭转身体
                move_rpy = variables.get_val('move_rpy')
                variables.set_val('move_rpy', [move_rpy[0] + int(command[1]), move_rpy[1] + int(command[2]), move_rpy[2] + int(command[3])])
                variables.set_val("command_info", [])
                move_pico.Init()
                variables.set_val('last_move', 'rpy')
                print(variables.get_val('move_rpy'))
            elif command[0] == 'H':  # 改变身体高度
                height = variables.get_val('height')
                variables.set_val('height', height + int(command[1]))
                variables.set_val("command_info", [])
                move_pico.Init()
                variables.set_val('last_move', 'height')
            elif command[0] == 'F':  # 改变腿宽
                legwidth = variables.get_val('leg_width')
                variables.set_val('leg_width', legwidth + int(command[1]))
                variables.set_val("command_info", [])
                move_pico.Turn(0)
                variables.set_val('last_move', 'lw')
            elif command[0] == 'BF':  # Back、Front，后倾或前倾，后倾为正
                body_shift = variables.get_val('body_shift')
                variables.set_val('body_shift', [[0, 90, 90], body_shift[1] + int(command[1])])  # 与x、y、z轴夹角，平移长度
                variables.set_val("command_info", [])
                move_pico.Init()
                variables.set_val('last_move', 'BorF')
            else:
                variables.set_val("command_info", [])
                pass
        except:  # 比较保险的写法，可能有一点多余
            variables.set_val("command_info", [])
            pass
