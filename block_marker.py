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
        """
        需要被标记的点集
        """
        self.points = points

    def mark(self):
        """
        To be Implemented by subclasses
        @return: 包含Block的二维数组
        """
        pass


class BlockMarker(BlockMarkerInterface):

    def mark(self):
        """
        Implement here
        @return: 包含Block的二维数组
        """
        pass


class Block:

    """
    BlockMarker的输出，包含一个网格中的数据点，网格的位置（实际上是网格在二维数组中的二维索引），网格中点的斜率
    """

    def __init__(self, slope, points, position):
        """
        @param slope: 网格中点的斜率；若Block为空，则slope=null
        @param points: 网格中的数据点；若Block为空，则points=[]
        @param position: 网格的二维索引, [i， j]
        """
        self.slope = slope
        self.points = points
        self.position = position