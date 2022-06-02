import math
import settings


class distance:
    def two_dimension(Point1, Point2):
        return ((Point1.x - Point2.x) ** 2 + (Point1.y - Point2.y) ** 2) ** 0.5

    def three_dimension(Point1, Point2):
        return ((Point1.x - Point2.x) ** 2 + (Point1.y - Point2.y) ** 2 + (Point1.z - Point2.z) ** 2) ** 0.5


def three_dimension_dis(Point1, Point2):
    return ((Point1[0] - Point2[0]) ** 2 + (Point1[1] - Point2[1]) ** 2 + (Point1[2] - Point2[2]) ** 2) ** 0.5


def angle(point1, point2, point3, point4):
    v1 = ((point1.x-point2.x), (point1.y-point2.y), (point1.z-point2.z))
    v2 = ((point3.x - point4.x), (point3.y - point4.y), (point3.z - point4.z))
    if three_dimension_dis(v1, (0, 0, 0))*three_dimension_dis(v2, (0, 0, 0)) != 0:
        cosA = ((v1[0]*v2[0])+(v1[1]*v2[1])+(v1[2]*v2[2]))/(three_dimension_dis(v1, (0, 0, 0))*three_dimension_dis(v2, (0, 0, 0)))
        return math.acos(cosA)*180/math.pi


def RPYchange_to_FacePoint(PointX, PointY):
    Pchange = math.atan2(settings.img_height/2-PointY, settings.cam_focal_pixel_length)*180/math.pi
    Ychange = math.atan2(settings.img_width/2-PointX, settings.cam_focal_pixel_length)*180/math.pi
    return [0, Pchange, Ychange]


def people_distance():
    pass
