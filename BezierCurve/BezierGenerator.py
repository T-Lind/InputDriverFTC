import math


class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def add(self, other):
        return Point(self.x + other, self.y + other)

    def distance_to(self, other):
        return math.hypot(abs(other.x-self.x), abs(other.y-self.y))

    def __add__(self, other):
        return Point(self.x + other.x, self.y + other.y)

    def mul(self, other):
        return Point(self.x * other, self.y * other)

    def __str__(self):
        return "X: " + str(self.x) + " Y: " + str(self.y) + "\n"


def lerp(point0, point1, t):
    """
    Perform linear interpolation between two points. ex. t=0.5 is halfway between them
    :param point0:
    :param point1:
    :param t: the time to interpolate at
    :return: the linear interpolated point
    """
    return point0.mul(1 - t) + point1.mul(t)


def recursive_lerp(points, time):
    """
    Recursively perform linear interpolation between a list of control points given a time along the bezier curve (t is 0-1)
    :param points: The list of control points to perform recursive linear interpolation on
    :param time: the moment in time to grab the current point
    :return: The point into the curve based on the time and set of control points
    """
    if time >= 1:
        return points[-1]

    if len(points) == 2:
        return lerp(points[0], points[1], time)

    index = 0
    list_of_lerps = []
    while index < len(points) - 1:
        point1 = lerp(points[index], points[index + 1], time)
        list_of_lerps.append(point1)
        index += 1

    return recursive_lerp(list_of_lerps, time)
