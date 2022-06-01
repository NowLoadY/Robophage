import math
from data import variables
from tools import calculate_pico
import settings_pico


gen3 = math.sqrt(3)
pi = math.pi


def R_z(R_ANGLE, SET):  # 输入坐标，旋转角度(顺时针)，输出坐标
    X = int((SET[0] * math.cos(R_ANGLE * math.pi / 180)) + (SET[1] * math.sin(R_ANGLE * math.pi / 180)))
    Y = int((SET[1] * math.cos(R_ANGLE * math.pi / 180)) - (SET[0] * math.sin(R_ANGLE * math.pi / 180)))
    return [X, Y, SET[2]]


def OriginalData():
    lw = variables.get_val('leg_width')
    H = variables.get_val('height')
    br = settings_pico.br
    return [[[-(lw+br) * gen3 / 2, -(lw+br) / 2, H]],
            [[-(lw+br) * gen3 / 2, (lw+br) / 2, H]],
            [[0, -(lw+br), H]],
            [[0, (lw+br), H]],
            [[(lw+br) * gen3 / 2, -(lw+br) / 2, H]],
            [[(lw+br) * gen3 / 2, (lw+br) / 2, H]]]
    

#def Init():
    #pass


def straightData(Direction):  # z平面内的角度，角度制
    D = Direction/180*math.pi
    sL = variables.get_val('step_length')  # 步长
    lw = variables.get_val('leg_width')
    H = variables.get_val('height')
    fU = variables.get_val('foot_up')/2
    br = settings_pico.br
    foot = [[-(lw+br) * gen3 / 2, -(lw+br) / 2, H],
            [-(lw+br)*gen3 / 2, (lw+br) / 2, H],
            [0, -(lw+br), H],
            [0, (lw+br), H],
            [(lw+br)*gen3 / 2, -(lw+br) / 2, H],
            [(lw+br)*gen3 / 2, (lw+br) / 2, H]]
    """ 腿数，动作数，单腿舵机数  """
    return [[  # 腿1
            [foot[0][0], foot[0][1], foot[0][2] + fU],
            [foot[0][0] - sL * math.cos(D + pi), foot[0][1] - sL * math.sin(D + pi), foot[0][2] + fU],
            [foot[0][0] - sL * math.cos(D + pi), foot[0][1] - sL * math.sin(D + pi), foot[0][2] + fU],
            [foot[0][0] - sL * math.cos(D + pi), foot[0][1] - sL * math.sin(D + pi), foot[0][2]],
            [foot[0][0] - sL * math.cos(D + pi), foot[0][1] - sL * math.sin(D + pi), foot[0][2]],
            [foot[0][0] - sL * math.cos(D + pi), foot[0][1] - sL * math.sin(D + pi), foot[0][2]],
            [foot[0][0], foot[0][1], foot[0][2]],
            [foot[0][0] + sL * math.cos(D + pi), foot[0][1] + sL * math.sin(D + pi), foot[0][2]],
            [foot[0][0] + sL * math.cos(D + pi), foot[0][1] + sL * math.sin(D + pi), foot[0][2]],
            [foot[0][0] + sL * math.cos(D + pi), foot[0][1] + sL * math.sin(D + pi), foot[0][2]],
            ],

            [  # 腿2
            [foot[1][0], foot[1][1], foot[1][2]],
            [foot[1][0], foot[1][1], foot[1][2]],
            [foot[1][0] + sL * math.cos(D + pi), foot[1][1] + sL * math.sin(D + pi), foot[1][2]],
            [foot[1][0] + sL * math.cos(D + pi), foot[1][1] + sL * math.sin(D + pi), foot[1][2]],
            [foot[1][0] + sL * math.cos(D + pi), foot[1][1] + sL * math.sin(D + pi), foot[1][2] + fU],
            [foot[1][0] - sL * math.cos(D + pi), foot[1][1] - sL * math.sin(D + pi), foot[1][2] + fU],
            [foot[1][0] - sL * math.cos(D + pi), foot[1][1] - sL * math.sin(D + pi), foot[1][2] + fU],
            [foot[1][0] - sL * math.cos(D + pi), foot[1][1] - sL * math.sin(D + pi), foot[1][2] + fU],
            [foot[1][0] - sL * math.cos(D + pi), foot[1][1] - sL * math.sin(D + pi), foot[1][2] + fU//2],
            [foot[1][0] - sL * math.cos(D + pi), foot[1][1] - sL * math.sin(D + pi), foot[1][2]]
            ],

            [  # 腿3
            [foot[2][0], foot[2][1], foot[2][2]],
            [foot[2][0], foot[2][1], foot[2][2]],
            [foot[2][0] + sL * math.cos(D + pi), foot[2][1] + sL * math.sin(D + pi), foot[2][2]],
            [foot[2][0] + sL * math.cos(D + pi), foot[2][1] + sL * math.sin(D + pi), foot[2][2]],
            [foot[2][0] + sL * math.cos(D + pi), foot[2][1] + sL * math.sin(D + pi), foot[2][2] + fU],
            [foot[2][0] - sL * math.cos(D + pi), foot[2][1] - sL * math.sin(D + pi), foot[2][2] + fU],
            [foot[2][0] - sL * math.cos(D + pi), foot[2][1] - sL * math.sin(D + pi), foot[2][2] + fU],
            [foot[2][0] - sL * math.cos(D + pi), foot[2][1] - sL * math.sin(D + pi), foot[2][2] + fU],
            [foot[2][0] - sL * math.cos(D + pi), foot[2][1] - sL * math.sin(D + pi), foot[2][2] + fU//2],
            [foot[2][0] - sL * math.cos(D + pi), foot[2][1] - sL * math.sin(D + pi), foot[2][2]]
            ],

            [  # 腿4
            [foot[3][0], foot[3][1], foot[3][2] + fU],
            [foot[3][0] - sL * math.cos(D + pi), foot[3][1] - sL * math.sin(D + pi), foot[3][2] + fU],
            [foot[3][0] - sL * math.cos(D + pi), foot[3][1] - sL * math.sin(D + pi), foot[3][2] + fU],
            [foot[3][0] - sL * math.cos(D + pi), foot[3][1] - sL * math.sin(D + pi), foot[3][2]],
            [foot[3][0] - sL * math.cos(D + pi), foot[3][1] - sL * math.sin(D + pi), foot[3][2]],
            [foot[3][0] - sL * math.cos(D + pi), foot[3][1] - sL * math.sin(D + pi), foot[3][2]],
            [foot[3][0], foot[3][1], foot[3][2]],
            [foot[3][0] + sL * math.cos(D + pi), foot[3][1] + sL * math.sin(D + pi), foot[3][2]],
            [foot[3][0] + sL * math.cos(D + pi), foot[3][1] + sL * math.sin(D + pi), foot[3][2]],
            [foot[3][0] + sL * math.cos(D + pi), foot[3][1] + sL * math.sin(D + pi), foot[3][2]]
            ],

            [  # 腿5
            [foot[4][0], foot[4][1], foot[4][2] + fU],
            [foot[4][0] - sL * math.cos(D + pi), foot[4][1] - sL * math.sin(D + pi), foot[4][2] + fU],
            [foot[4][0] - sL * math.cos(D + pi), foot[4][1] - sL * math.sin(D + pi), foot[4][2] + fU],
            [foot[4][0] - sL * math.cos(D + pi), foot[4][1] - sL * math.sin(D + pi), foot[4][2]],
            [foot[4][0] - sL * math.cos(D + pi), foot[4][1] - sL * math.sin(D + pi), foot[4][2]],
            [foot[4][0] - sL * math.cos(D + pi), foot[4][1] - sL * math.sin(D + pi), foot[4][2]],
            [foot[4][0], foot[4][1], foot[4][2]],
            [foot[4][0] + sL * math.cos(D + pi), foot[4][1] + sL * math.sin(D + pi), foot[4][2]],
            [foot[4][0] + sL * math.cos(D + pi), foot[4][1] + sL * math.sin(D + pi), foot[4][2]],
            [foot[4][0] + sL * math.cos(D + pi), foot[4][1] + sL * math.sin(D + pi), foot[4][2]]
            ],

            [  # 腿6
            [foot[5][0], foot[5][1], foot[5][2]],
            [foot[5][0], foot[5][1], foot[5][2]],
            [foot[5][0] + sL * math.cos(D + pi), foot[5][1] + sL * math.sin(D + pi), foot[5][2]],
            [foot[5][0] + sL * math.cos(D + pi), foot[5][1] + sL * math.sin(D + pi), foot[5][2]],
            [foot[5][0] + sL * math.cos(D + pi), foot[5][1] + sL * math.sin(D + pi), foot[5][2] + fU],
            [foot[5][0] - sL * math.cos(D + pi), foot[5][1] - sL * math.sin(D + pi), foot[5][2] + fU],
            [foot[5][0] - sL * math.cos(D + pi), foot[5][1] - sL * math.sin(D + pi), foot[5][2] + fU],
            [foot[5][0] - sL * math.cos(D + pi), foot[5][1] - sL * math.sin(D + pi), foot[5][2] + fU],
            [foot[5][0] - sL * math.cos(D + pi), foot[5][1] - sL * math.sin(D + pi), foot[5][2] + fU//2],
            [foot[5][0] - sL * math.cos(D + pi), foot[5][1] - sL * math.sin(D + pi), foot[5][2]]
            ]
            ]


def Turn_Round(ANGLE):
    A = ANGLE
    lw = variables.get_val('leg_width')
    H = variables.get_val('height')
    fU = variables.get_val('foot_up')
    br = settings_pico.br
    foot = [[-(lw+br) * gen3 / 2, -(lw+br) / 2, H],
            [-(lw+br) * gen3 / 2, (lw+br) / 2, H],
            [0, -(lw+br), H],
            [0, (lw+br), H],
            [(lw+br) * gen3 / 2, -(lw+br) / 2, H],
            [(lw+br) * gen3 / 2, (lw+br) / 2, H]]
    foot_rotate = [[R_z(A/4, foot[0]),
                   R_z(A/4, foot[1]),
                   R_z(A/4, foot[2]),
                   R_z(A/4, foot[3]),
                   R_z(A/4, foot[4]),
                   R_z(A/4, foot[5])],

                   [R_z(A/2, foot[0]),
                    R_z(A/2, foot[1]),
                    R_z(A/2, foot[2]),
                    R_z(A/2, foot[3]),
                    R_z(A/2, foot[4]),
                    R_z(A/2, foot[5])],
                   
                   [R_z(-A/4, foot[0]),
                   R_z(-A/4, foot[1]),
                   R_z(-A/4, foot[2]),
                   R_z(-A/4, foot[3]),
                   R_z(-A/4, foot[4]),
                   R_z(-A/4, foot[5])],
                   
                   [R_z(-A/2, foot[0]),
                   R_z(-A/2, foot[1]),
                   R_z(-A/2, foot[2]),
                   R_z(-A/2, foot[3]),
                   R_z(-A/2, foot[4]),
                   R_z(-A/2, foot[5])]]
    return [
            # 腿1
            [[foot_rotate[0][0][0], foot_rotate[0][0][1], foot[0][2] + fU],
             [foot_rotate[1][0][0], foot_rotate[1][0][1], foot[0][2]],
             [foot_rotate[0][0][0], foot_rotate[0][0][1], foot[0][2]],
             [foot[0][0],foot[0][1],foot[0][2]]],
            # 腿2
            [[foot_rotate[2][1][0], foot_rotate[2][1][1], foot[1][2]],
             [foot_rotate[3][1][0], foot_rotate[3][1][1], foot[1][2]],
             [foot_rotate[2][1][0], foot_rotate[2][1][1], foot[1][2] + fU],
             [foot[1][0],foot[1][1],foot[1][2]]],
            # 腿3
            [[foot_rotate[2][2][0], foot_rotate[2][2][1], foot[2][2]],
             [foot_rotate[3][2][0], foot_rotate[3][2][1], foot[2][2]],
             [foot_rotate[2][2][0], foot_rotate[2][2][1], foot[2][2] + fU],
             [foot[2][0],foot[2][1],foot[2][2]]],
            # 腿4
            [[foot_rotate[0][3][0], foot_rotate[0][3][1], foot[3][2] + fU],
             [foot_rotate[1][3][0], foot_rotate[1][3][1], foot[3][2]],
             [foot_rotate[0][3][0], foot_rotate[0][3][1], foot[3][2]],
             [foot[3][0],foot[3][1],foot[3][2]]],
            # 腿5
            [[foot_rotate[0][4][0], foot_rotate[0][4][1], foot[4][2] + fU],
             [foot_rotate[1][4][0], foot_rotate[1][4][1], foot[4][2]],
             [foot_rotate[0][4][0], foot_rotate[0][4][1], foot[4][2]],
             [foot[4][0],foot[4][1],foot[4][2]]],
            # 腿6
            [[foot_rotate[2][5][0], foot_rotate[2][5][1], foot[5][2]],
             [foot_rotate[3][5][0], foot_rotate[3][5][1], foot[5][2]],
             [foot_rotate[2][5][0], foot_rotate[2][5][1], foot[5][2] + fU],
             [foot[5][0],foot[5][1],foot[5][2]]]
            ]
