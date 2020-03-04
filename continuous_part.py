# coding=utf-8

"""
ContinuousPart 为拟合需要调用的数据结构，每一个实例为一个需要单独拟合的点集
slope 为这个实例中包含的点的倾斜角度，角度制， 例如，45表示是45度， 80表示80度
points 为一个二维数组，其中的数据为点的坐标，例如, [[1, 2], [3, 4]]表示两个点，坐标分别为(1, 2), (3, 4)
"""

class ContinuousPart:

    def __init__(self, slope, points):
        """
        @param slope: int, slope of all the points
        @param points: points to fit
        """
        self.slope = slope
        self.points = points


class PointsDividerInterface:

    def __init__(self):
        self.points = []

    def set_points(self, points):
        self.points = points

    def divide(self):
        """
        To be implemented by subclasses
        @return: list of ContinuousParts
        """
        pass