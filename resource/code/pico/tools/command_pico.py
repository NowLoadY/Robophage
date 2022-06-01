import random
from data import variables as var
import numpy


class command_generator:
    def move_straight(self, direction, height, length):
        commands = []
        for i in range(0, length):
            var.set_val('height', height)
            commands = numpy.append(commands, "s" + "," + str(direction) + "," + str(height) + ",")
        commands = numpy.append(commands, "end")
        return commands

    def turn(self, angle, height):
        commands = []
        length = abs(angle//45)+1
        if angle > 0:
            LorR = 1
        else:
            LorR = -1
        if length > 1:
            for i in range(0, length-1):
                var.set_val('height', height)
                commands = numpy.append(commands, "t" + "," + str(45*LorR) + "," + str(height) + ",")
            commands = numpy.append(commands, "t" + "," + str((angle-(angle//45)*45)*LorR) + "," + str(height) + ",")
        else:
            commands = numpy.append(commands, "t" + "," + str(angle) + "," + str(height) + ",")
        commands = numpy.append(commands, "end")
        return commands

    def watch_over_round(self, length):
        commands = []
        if var.get_val('com_len') == 3:
            commands = numpy.append(commands, "com_len,4,,")
        for i in range(0, length):
            var.set_val('move_rpy', [random.randint(3, 8), random.randint(3, 8), random.randint(15, 45)])
            commands = numpy.append(commands, "rpy," + str(var.get_val('move_rpy')[0]) + ',' + str(var.get_val('move_rpy')[1]) + ',' + str(
                var.get_val('move_rpy')[2]) + ',')
        commands = numpy.append(commands, "rpy,0,0,0,")
        var.set_val('move_rpy', [var.get_val('default_rpy')[0], var.get_val('default_rpy')[1], var.get_val('default_rpy')[2]])
        commands = numpy.append(commands, "com_len,3,,,")
        commands = numpy.append(commands, "end")
        return commands

    def look_at_finger8(self, landmarks, hand_id):  # 基于像素点偏差的瞄准
        pass
