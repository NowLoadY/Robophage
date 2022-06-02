import cv2
import mediapipe as mp

import settings
from tools import motion_recognize
from data import variables

#cap = cv2.VideoCapture("http://192.168.137.58:81/stream")

#cap = cv2.VideoCapture(0)
cap = cv2.VideoCapture(settings.camera_id)
variables._init()
variables.set_val('have_hand', False)  # 是否画面有手
variables.set_val('roi_hand', 0)
mp_drawing = mp.solutions.drawing_utils
mp_drawing_styles = mp.solutions.drawing_styles
# 检测方法
# 手标记点
mp_hands = mp.solutions.hands
hands = mp_hands.Hands(
    static_image_mode=False,
    max_num_hands=2,
    min_detection_confidence=0.5)
# 物体3d姿势
mp_objectron = mp.solutions.objectron
objectron = mp_objectron.Objectron(static_image_mode=False,
                            max_num_objects=2,
                            min_detection_confidence=0.6,
                            min_tracking_confidence=0.9,
                            model_name='Cup')
# 脸部mash
mp_face_mesh = mp.solutions.face_mesh
face_mesh = mp_face_mesh.FaceMesh(
    max_num_faces=1,
    refine_landmarks=True,
    min_detection_confidence=0.8,
    min_tracking_confidence=0.8)
def demo():
    while True:
        ret, frame = cap.read()
        if ret:
            frame.flags.writeable = False
            RGB = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            hand_results = hands.process(RGB)
            objectron_results = objectron.process(RGB)
            face_mesh_results = face_mesh.process(RGB)
            #print('Handedness:', hand_results.multi_handedness)
            frame.flags.writeable = True
            if hand_results.multi_hand_landmarks:
                multi_hand = hand_results.multi_hand_landmarks
                for hand_landmarks in multi_hand:
                    mp_drawing.draw_landmarks(
                        frame,
                        hand_landmarks,
                        mp_hands.HAND_CONNECTIONS,
                        mp_drawing_styles.get_default_hand_landmarks_style(),
                        mp_drawing_styles.get_default_hand_connections_style())
                if motion_recognize.is_hand_ok(multi_hand):
                    print('ok')
                if motion_recognize.is_hand_finger8(multi_hand):
                    i = variables.get_val('roi_hand')
                    variables.set_val('follow_point', multi_hand[i].landmark[8])
                    print('point')
                    print(variables.get_val('follow_point'))

            if objectron_results.detected_objects:
                for detected_object in objectron_results.detected_objects:
                    mp_drawing.draw_landmarks(
                        frame, detected_object.landmarks_2d, mp_objectron.BOX_CONNECTIONS)
                    mp_drawing.draw_axis(frame, detected_object.rotation,
                                         detected_object.translation)
            if face_mesh_results.multi_face_landmarks:
                for face_landmarks in face_mesh_results.multi_face_landmarks:
                    mp_drawing.draw_landmarks(
                        image=frame,
                        landmark_list=face_landmarks,
                        connections=mp_face_mesh.FACEMESH_TESSELATION,
                        landmark_drawing_spec=None,
                        connection_drawing_spec=mp_drawing_styles
                            .get_default_face_mesh_tesselation_style())
                    mp_drawing.draw_landmarks(
                        image=frame,
                        landmark_list=face_landmarks,
                        connections=mp_face_mesh.FACEMESH_CONTOURS,
                        landmark_drawing_spec=None,
                        connection_drawing_spec=mp_drawing_styles
                            .get_default_face_mesh_contours_style())
                    mp_drawing.draw_landmarks(
                        image=frame,
                        landmark_list=face_landmarks,
                        connections=mp_face_mesh.FACEMESH_IRISES,
                        landmark_drawing_spec=None,
                        connection_drawing_spec=mp_drawing_styles
                            .get_default_face_mesh_iris_connections_style())
            cv2.imshow('frame', frame)
            cv2.waitKey(1)
        #if cv2.waitKey(1) & 0xFF == ord('q'):
            #break

    cap.release()
    cv2.destroyAllWindows()

demo()
