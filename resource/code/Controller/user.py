# coding=utf-8
"""
NowLoadY
"""
import threading
import time
from copy import deepcopy

import cv2
import keyboard
import numpy as np
import pyautogui as pag
import serial

from data import variables
variables._init()
import settings
import mediapipe as mp
from yolo import yolov5_model as yolo
from tools import motion_recognize

variables.set_val('have_hand', False)  # 是否画面有手
variables.set_val('roi_hand', 0)

mp_drawing = mp.solutions.drawing_utils  # 检测方法
mp_drawing_styles = mp.solutions.drawing_styles
mp_hands = mp.solutions.hands
hands = mp_hands.Hands(
    static_image_mode=False,
    max_num_hands=2,
    min_detection_confidence=0.5)

thread_lock = threading.Lock()
thread_exit = False
esp32cam_status = False
esp32cam_initial = False
class myThread(threading.Thread):
    def __init__(self, camera_id, img_height, img_width):
        super(myThread, self).__init__()
        self.camera_id = camera_id
        self.img_height = img_height
        self.img_width = img_width
        self.frame = np.zeros((img_height, img_width, 3), dtype=np.uint8)

    def get_frame(self):
        return deepcopy(self.frame)

    def run(self):
        global thread_exit
        cap = cv2.VideoCapture(self.camera_id)
        while not thread_exit:
            ret, frame = cap.read()
            if ret:
                frame = cv2.resize(frame, (self.img_width, self.img_height))
                thread_lock.acquire()
                self.frame = frame
                thread_lock.release()
            else:
                thread_exit = True
        cap.release()


def send_message_to_COM(Message):
    try:
        ser.write(Message.encode('utf-8'))
        print(Message)
    except:
        print('Tried:', Message, '\nBUT COM: {} IS NOT CORRECT\n'.format(settings.uart_to_spider))


def move_straight(D):
    time_b = time.time()
    global time_a
    if time_b - time_a > 0.08:
        message = "W,{}".format(str(D+90))
        send_message_to_COM(message)
        time_a = time.time()


def turnA(A):
    time_b = time.time()
    global time_a
    if time_b - time_a > 0.08:
        message = "T,{}".format(str(A))
        send_message_to_COM(message)
        time_a = time.time()


def pitch(B):
    time_b = time.time()
    global time_a
    if time_b - time_a > 0.08:
        message = "R,{},{},{}".format(0, int(-B), 0)
        send_message_to_COM(message)
        time_a = time.time()


def yaw(B):
    global YawAngle
    time_b = time.time()
    global time_a
    if time_b - time_a > 0.08:
        message = "R,{},{},{}".format(0, 0, int(B))
        send_message_to_COM(message)
        time_a = time.time()


def roll(B):
    time_b = time.time()
    global time_a
    if time_b - time_a > 0.08:
        message = "R,{},{},{}".format(int(-B), 0, 0)
        send_message_to_COM(message)
        time_a = time.time()


def height_change(BHC):
    global time_a
    time_b = time.time()
    if time_b - time_a > 0.08:
        message = "H,{}".format(str(BHC))
        send_message_to_COM(message)
        time_a = time.time()


def stop_moving():
    global time_a
    time_b = time.time()
    if time_b - time_a > 0.08:
        send_message_to_COM("S")
        time_a = time.time()


def draw_curve():
    global time_a
    time_b = time.time()
    if time_b - time_a > 0.08:
        send_message_to_COM("D")
        time_a = time.time()


def shiftback():
    global time_a
    time_b = time.time()
    if time_b - time_a > 0.08:
        message = "BF,10"
        send_message_to_COM(message)
        time_a = time.time()


def shiftforward():
    global time_a
    time_b = time.time()
    if time_b - time_a > 0.08:
        message = "BF,-10"
        send_message_to_COM(message)
        time_a = time.time()


def shrink_foot():
    global time_a
    time_b = time.time()
    if time_b - time_a > 0.08:
        message = "F,-10"
        send_message_to_COM(message)
        time_a = time.time()


def unfold_foot():
    global time_a
    time_b = time.time()
    if time_b - time_a > 0.08:
        message = "F,10"
        send_message_to_COM(message)
        time_a = time.time()


def open_esp32cam():
    global esp32cam_status
    esp32cam_status = not esp32cam_status


def key_motion(x):
    forward = keyboard.KeyboardEvent('down', 0, 'w')
    back = keyboard.KeyboardEvent('down', 0, 's')
    left = keyboard.KeyboardEvent('down', 0, 'a')
    right = keyboard.KeyboardEvent('down', 0, 'd')
    Turn_left = keyboard.KeyboardEvent('down', 0, 'j')
    Turn_right = keyboard.KeyboardEvent('down', 0, 'k')
    up_watch = keyboard.KeyboardEvent('down', 0, 'up')
    down_watch = keyboard.KeyboardEvent('down', 0, 'down')
    left_yaw = keyboard.KeyboardEvent('down', 0, 'left')
    right_yaw = keyboard.KeyboardEvent('down', 0, 'right')
    left_roll = keyboard.KeyboardEvent('down', 0, 'h')
    right_roll = keyboard.KeyboardEvent('down', 0, 'l')
    face_recognize = keyboard.KeyboardEvent('down', 0, 'v')
    higher_body = keyboard.KeyboardEvent('down', 0, 'page up')
    lower_body = keyboard.KeyboardEvent('down', 0, 'page down')
    mouse_point = keyboard.KeyboardEvent('down', 0, 'p')
    stop = keyboard.KeyboardEvent('down', 0, 'q')
    draw = keyboard.KeyboardEvent('down', 0, 'x')
    back_shift = keyboard.KeyboardEvent('down', 0, 'g')
    forward_shift = keyboard.KeyboardEvent('down', 0, 't')
    shrink_f = keyboard.KeyboardEvent('down', 0, '<')
    unfold_f = keyboard.KeyboardEvent('down', 0, '>')
    esp32cam = keyboard.KeyboardEvent('down', 0, 'z')
    if x.event_type == 'down' and x.name == forward.name:
        move_straight(90)
    if x.event_type == 'down' and x.name == back.name:
        move_straight(-90)
    if x.event_type == 'down' and x.name == left.name:
        move_straight(180)
    if x.event_type == 'down' and x.name == right.name:
        move_straight(0)
    if x.event_type == 'down' and x.name == Turn_left.name:
        turnA(-30)
    if x.event_type == 'down' and x.name == Turn_right.name:
        turnA(30)
    if x.event_type == 'down' and x.name == up_watch.name:
        pitch(6)
    if x.event_type == 'down' and x.name == down_watch.name:
        pitch(-6)
    if x.event_type == 'down' and x.name == left_yaw.name:
        yaw(6)
    if x.event_type == 'down' and x.name == right_yaw.name:
        yaw(-6)
    if x.event_type == 'down' and x.name == left_roll.name:
        roll(-6)
    if x.event_type == 'down' and x.name == right_roll.name:
        roll(6)
    if x.event_type == 'down' and x.name == higher_body.name:
        height_change(-10)
    if x.event_type == 'down' and x.name == lower_body.name:
        height_change(10)
    if x.event_type == 'down' and x.name == face_recognize.name:
        face_recognize_move()
    if x.event_type == 'down' and x.name == mouse_point.name:
        follow_mouse()
    if x.event_type == 'down' and x.name == stop.name:
        stop_moving()
    if x.event_type == 'down' and x.name == draw.name:
        draw_curve()
    if x.event_type == 'down' and x.name == back_shift.name:
        shiftback()
    if x.event_type == 'down' and x.name == forward_shift.name:
        shiftforward()
    if x.event_type == 'down' and x.name == shrink_f.name:
        shrink_foot()
    if x.event_type == 'down' and x.name == unfold_f.name:
        unfold_foot()
    if x.event_type == 'down' and x.name == esp32cam.name:
        open_esp32cam()


def face_recognize_move():
    print("人脸识别程序(按q退出模式）")
    time_a = time.time()
    stop = 0
    while True:
        global thread_exit
        thread_exit = False
        camera_id = settings.camera_id
        img_height = 720
        img_width = 1080
        print("正在打开摄像头...")
        thread = myThread(camera_id, img_height, img_width)
        thread.start()

        while not thread_exit:
            thread_lock.acquire(); img = thread.get_frame(); thread_lock.release()
            time_b = time.time()
            #######################mediapipe###########################
            img.flags.writeable = False
            RGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
            hand_results = hands.process(RGB)
            img.flags.writeable = True
            ###########################yolo###########################
            yolo_results = yolo.detect(img)
            #########################################################
            if hand_results.multi_hand_landmarks:
                multi_hand = hand_results.multi_hand_landmarks
                if motion_recognize.is_hand_ok(multi_hand):
                    if time_b - time_a > 0.2:
                        message = "O"
                        send_message_to_COM(message)
                        time_a = time.time()
                if motion_recognize.is_hand_victory(multi_hand):
                    if time_b - time_a > 0.2:
                        message = "V"
                        send_message_to_COM(message)
                        time_a = time.time()
                if motion_recognize.is_hand_finger8(multi_hand):
                    i = variables.get_val('roi_hand')
                    finger = multi_hand[i].landmark[8]
                    message = "R,{},{},{}".format(0, int((finger.y-0.5)*18), int((finger.x-0.5)*18))
                    cv2.circle(img, (int(finger.x*img_width), int(finger.y*img_height)), 20, (200, 100, 100), -1)
                    if time_b - time_a > 0.2:
                        send_message_to_COM(message)
                        time_a = time.time()
            #########################draw#########################
            if settings.show_img_on_screen:
                if hand_results.multi_hand_landmarks:
                    for hand_landmarks in multi_hand:
                        mp_drawing.draw_landmarks(
                            img,
                            hand_landmarks,
                            mp_hands.HAND_CONNECTIONS,
                            mp_drawing_styles.get_default_hand_landmarks_style(),
                            mp_drawing_styles.get_default_hand_connections_style())
                for result in yolo_results:
                    xywh = result['position']
                    cv2.rectangle(img, (xywh[0], xywh[1]), (xywh[0]+xywh[2], xywh[1]+xywh[3]), (100,255,255),3)
                    cv2.putText(img, "{}".format(result['class']), (xywh[0], xywh[1]-10), font, 2, (100, 255, 255), 5)
            ##########################show#########################
            if settings.show_img_on_screen:
                cv2.imshow('camera', img)
            if cv2.waitKey(1) & 0xFF == ord('q'):
                stop = 1
                thread_exit = True
                thread.join()
                cv2.destroyAllWindows()
        if stop == 1:
            break


def follow_mouse():
    command = [0,0,0]
    print("按q退出")
    time_a = time.time()
    stop = False
    command[1] = command[2] = 250
    background = np.ones([300, 300, 3], np.uint8) * 255
    cv2.circle(background, (150, 150), 8, (50, 255, 50), -1)
    cv2.imshow("control_helper", background); cv2.moveWindow("control_helper", 90, 60)
    while True:
        if stop == True:
            break
        x, y = pag.position()
        cv2.waitKey(1)
        if 100 < x < 400 and 100 < y < 400:
            while True:
                time_b = time.time()
                background = np.ones([300, 300, 3], np.uint8) * 255
                x, y = pag.position()
                if 100 < x < 400 and 100 < y < 400:
                    command[1] = x
                    command[2] = y
                    cv2.circle(background, (x - 100, y - 100), 8, (50, 255, 50), -1)
                cv2.imshow("control_helper", background)
                cv2.moveWindow("control_helper", 90, 60)
                if time_b - time_a > 0.25:
                    message = "BS,{},{}".format(str(((command[2] - 100) // 5) - 30), str(
                        ((command[1] - 100) // 5) - 30))
                    send_message_to_COM(message)
                    time_a = time.time()
                if cv2.waitKey(1) & 0xFF == ord('q'):
                    cv2.destroyAllWindows()
                    stop = True
                    break


if __name__ == "__main__":
    screenWidth, screenHeight = pag.size()
    font = cv2.FONT_HERSHEY_SIMPLEX
    serialPort = 'COM' + str(settings.uart_to_spider)  # 串口
    print("串口为：" + str(settings.uart_to_spider))
    try:
        print("打开串口...")
        ser = serial.Serial(serialPort, settings.uart_to_spider_baud, timeout=0.5)
        print("串口已连接")
    except:
        print("串口错误")

    while True:
        time_a = time.time()
        keyboard.hook(key_motion)
        keyboard.wait('')
        if esp32cam_status:
            if not esp32cam_initial:
                thread_exit = False
                camera_id = settings.camera_id
                img_height = 720
                img_width = 1080
                print("正在打开摄像头...")
                thread = myThread(camera_id, img_height, img_width)
                thread.start()
                esp32cam_initial = True
            else:
                thread_lock.acquire()
                img = thread.get_frame()
                thread_lock.release()
                if settings.show_img_on_screen:
                    cv2.imshow('camera', img)
                if cv2.waitKey(1) & 0xFF == ord('q'):
                    thread_exit = True
                    thread.join()
                    cv2.destroyAllWindows()

