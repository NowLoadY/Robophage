from tools import calculate
from data import variables


def is_hand_ok(landmarks):
    if landmarks:
        for i in range(0, len(landmarks)):
            distance_12_8 = calculate.distance.three_dimension(Point1=landmarks[i].landmark[12],
                                                               Point2=landmarks[i].landmark[8])
            if distance_12_8 != 0:
                distance_8_4 = calculate.distance.three_dimension(Point1=landmarks[i].landmark[8],
                                                                  Point2=landmarks[i].landmark[4])
                if distance_8_4 / distance_12_8 < 0.3:
                    angle_20_o_16 = calculate.angle(landmarks[i].landmark[20], landmarks[i].landmark[17],
                                                    landmarks[i].landmark[16], landmarks[i].landmark[13])
                    angle_16_o_12 = calculate.angle(landmarks[i].landmark[16], landmarks[i].landmark[13],
                                                    landmarks[i].landmark[12], landmarks[i].landmark[9])
                    if angle_16_o_12 > 12 or angle_20_o_16 > 6:
                        if min(angle_20_o_16, angle_16_o_12) / max(angle_20_o_16, angle_16_o_12) > 0.7:
                            variables.set_val('roi_hand', i)
                            return True


def is_hand_victory(landmarks):
    if landmarks:
        for i in range(0, len(landmarks)):
            angle_12_o_8 = calculate.angle(landmarks[i].landmark[12], landmarks[i].landmark[9],
                                           landmarks[i].landmark[8], landmarks[i].landmark[5])
            if angle_12_o_8 > 12:
                distance_12_0 = calculate.distance.three_dimension(Point1=landmarks[i].landmark[12],
                                                                    Point2=landmarks[i].landmark[0])
                distance_8_0 = calculate.distance.three_dimension(Point1=landmarks[i].landmark[8],
                                                                    Point2=landmarks[i].landmark[0])
                if distance_12_0/distance_8_0 > 0.7:
                    distance_20_16 = calculate.distance.three_dimension(Point1=landmarks[i].landmark[20],
                                                                        Point2=landmarks[i].landmark[16])
                    distance_12_8 = calculate.distance.three_dimension(Point1=landmarks[i].landmark[12],
                                                                       Point2=landmarks[i].landmark[8])
                    if distance_20_16 / distance_12_8 < 0.6:
                        distance_8_4 = calculate.distance.three_dimension(Point1=landmarks[i].landmark[8],
                                                                          Point2=landmarks[i].landmark[4])
                        distance_4_16 = calculate.distance.three_dimension(Point1=landmarks[i].landmark[4],
                                                                           Point2=landmarks[i].landmark[16])
                        if distance_4_16 / distance_8_4 < 0.4:
                            variables.set_val('roi_hand', i)
                            return True


def is_hand_finger8(landmarks):
    if landmarks:
        for i in range(0, len(landmarks)):
            distance_8_0 = calculate.distance.three_dimension(Point1=landmarks[i].landmark[8],
                                                                    Point2=landmarks[i].landmark[0])
            distance_20_0 = calculate.distance.three_dimension(Point1=landmarks[i].landmark[20],
                                                              Point2=landmarks[i].landmark[0])
            if distance_20_0/distance_8_0 < 0.5:
                distance_12_0 = calculate.distance.three_dimension(Point1=landmarks[i].landmark[12],
                                                              Point2=landmarks[i].landmark[0])
                if distance_12_0/distance_8_0 < 0.5:
                    distance_4_0 = calculate.distance.three_dimension(Point1=landmarks[i].landmark[4],
                                                              Point2=landmarks[i].landmark[0])
                    if distance_4_0/distance_8_0 < 0.6:
                        variables.set_val('roi_hand', i)
                        return True
