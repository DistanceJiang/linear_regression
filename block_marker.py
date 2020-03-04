# coding=utf-8

"""
block_marker.py 主要用来实现对地图点分网格进行标记
"""

class BlockMarkerInterface:

    """
    需要实现这个接口，来对点进行标记
    """

    def __init__(self, resolution=1):
        """
        @param resolution: int, in meters, the length of a block's edge
        """
        self.resolution = resolution

    def set_points(self, points):
        self.points = points

    def mark(self):
        """
        To be Implemented by subclasses
        @return: list of blocks
        """
        pass


class Block:

    """
    BlockMarker的输出，包含一个网格中的数据点，网格的位置（以左上角点的坐标为准），网格中点的斜率
    """

    def __init__(self, slope, points, position):
        """
        @param slope: 网格中点的斜率
        @param points: 网格中的数据点
        @param position: 网格左上角的坐标
        """
        self.slope = slope
        self.points = points
        self.position = position