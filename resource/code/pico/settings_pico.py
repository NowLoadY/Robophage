################总体设置##################

import math

print_info = False
use_laser = False
use_imu = False  # 使用imu
use_propeller = False
use_beep = False
##############串口设置##############
uart_to_computer = 0  # 和机器人小脑通信的串口
uart_to_computer_baud = 115200  # 和机器人小脑通信的串口波特率
uart_to_imu = 1  # 和imu通信的串口
uart_to_imu_baud = 115200  # 和imu通信的串口波特率
##############GPIO设置#############
Laser_Light_Pin = 4  # 激光灯+极引脚编号
##############PWM设置#############
propeller_Pin = 7  # 螺旋桨的pwm控制引脚
beep_Pin = 10  # 蜂鸣器的pwm控制引脚
##############一些常量##############
# 身体
br = 55  # 6底盘的半径
leg_length = [28, 46, 90]  # 腿三段长度
# 舵机
servo_pin = [[3, 6, 10],
             [2, 7, 11],
             [20, 8, 14],
             [21, 9, 15]]
servo_pcapin = [[0, 9, 8],
                [0, 6, 7],
                [15, 14, 13],
                [5, 11, 4],
                [12, 3, 2],
                [0, 1, 10]]
pca9685_pin = [4, 5]  # sda scl
servo_f = 50  # 50hz
servo_T = 1000 / servo_f  # ms
# 装备
laser_Pin = 6  # 可以是继电器，或者蜂鸣器
Equipment1_Pin = 13

# 坐标变换
Z_rotateANGLE = [-150, 150, -90, 90, -30, 30]

Trans = [[int(-br*math.cos(Z_rotateANGLE[0]*math.pi/180)), int(-br*math.sin(Z_rotateANGLE[0]*math.pi/180))],
         [int(-br*math.cos(Z_rotateANGLE[1]*math.pi/180)), int(-br*math.sin(Z_rotateANGLE[1]*math.pi/180))],
         [int(-br*math.cos(Z_rotateANGLE[2]*math.pi/180)), int(-br*math.sin(Z_rotateANGLE[2]*math.pi/180))],
         [int(-br*math.cos(Z_rotateANGLE[3]*math.pi/180)), int(-br*math.sin(Z_rotateANGLE[3]*math.pi/180))],
         [int(-br*math.cos(Z_rotateANGLE[4]*math.pi/180)), int(-br*math.sin(Z_rotateANGLE[4]*math.pi/180))],
         [int(-br*math.cos(Z_rotateANGLE[5]*math.pi/180)), int(-br*math.sin(Z_rotateANGLE[5]*math.pi/180))]]
print(Trans)
print("settings loaded")
