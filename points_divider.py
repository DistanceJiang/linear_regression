# coding=utf-8

"""
ContinuousPart 为拟合需要调用的数据结构，每一个实例为一个需要单独拟合的点集
slope 为这个实例中包含的点集与x轴正方向的夹角，角度制， 例如，45表示是45度， 80表示80度
points 为一个二维数组，其中的数据为点的坐标，例如, [[1, 2], [3, 4]]表示两个点，坐标分别为(1, 2), (3, 4)
"""

from block_marker import BlockMarker, Block
from utils import get_points_from_pcd

class ContinuousPart:

    def __init__(self, slope, points):
        """
        @param slope: int, slope of all the points
        @param points: points to fit
        """
        self.slope = slope
        self.points = points


class PointsDividerInterface:

    """
    将点集分为需要拟合的部分，每个部分由ContinuousPart表示
    """

    def __init__(self):
        self.blocks = []
        self.points = []

    def set_points(self, points):
        """
        points为需要分块的点集
        """
        self.points = points

    def set_blocks(self):
        """
        blocks为包含block_marker.py中的Block的列表，包含对于小方格的标记
        """
        marker = BlockMarker()
        marker.get_points(self.points)
        self.blocks = marker.mark()

    def divide(self):
        """
        To be implemented by subclasses
        @return: list of ContinuousParts
        """
        pass