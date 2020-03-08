# coding=utf-8
import numpy as np
from utils import get_points_from_pcd, get_xy_lim, filter_points, get_slope
from math import ceil

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
        blocks = []
        xy_lim = get_xy_lim(self.points) # [x_min, x_max, y_min, y_max]
        origin = [xy_lim[0], xy_lim[2]]
        row = int(ceil((xy_lim[3] - xy_lim[2]) / self.resolution))
        col = int(ceil((xy_lim[1] - xy_lim[0]) / self.resolution))
        for i in range(row):
            for j in range(col):
                position = [i, j]
                cordinate = self.pos2cordinate(position, origin, self.resolution)
                points = filter_points(self.points, cordinate[0], cordinate[0] + self.resolution, \
                    cordinate[1] - self.resolution, cordinate[1])
                if len(points) == 0:
                    blocks.append(Block(None, [], position))
                else:
                    slope = self.clamp_slope(get_slope(points))
                    blocks.append(Block(slope, points, position))
        return blocks

    @staticmethod
    def pos2cordinate(pos, origin, step):
        return [pos[0] * step + origin[0], pos[1] * step + origin[1]]

    @staticmethod
    def clamp_slope(slope):
        return int(round(slope / 45)) * 45


# Deprecated
class DeprecatedBlockMarker(BlockMarkerInterface):

    def __init__(self, row, col, least_count):
        self.row = row
        self.col = col
        self.least_count = least_count
        self.nums = 0
        self.list_points = list()
        self.min_x = float("inf")
        self.min_y = float("inf")
        self.max_x = float("-inf")
        self.max_y = float("-inf")
        self.x_span = 0
        self.y_span = 0

    def mark(self):
        """
        Implement here
        @return: 包含Block的二维数组
        """
        self.cal_import_message()
        return self.filter_points()

    def cal_import_message(self):
        x_points = list()
        y_points = list()
        for point in self.points:
            self.min_x = min(self.min_x, point[0])
            self.max_x = max(self.max_x, point[0])
            self.min_y = min(self.min_y, point[1])
            self.max_y = max(self.max_y, point[1])
            self.nums += 1
        self.x_span = (self.max_x - self.min_x) // self.col
        self.y_span = (self.max_y - self.min_y) // self.row

    def filter_points(self):
        res = []

        for m in range(self.row-1, -1, -1):
            temp = list()
            for n in range(self.col):
                count = 0
                one_list_points = list()
                block = Block()
                x_points_one = list()
                y_points_one = list()
                x_start = self.x_span * n + self.min_x
                x_end = self.x_span * (n + 1) + self.min_x
                y_start = self.y_span * m + self.min_y
                y_end = self.y_span * (m + 1) + self.min_y
                for i in range(self.nums):
                    x = self.points[i][0]
                    y = self.points[i][1]
                    if x_start < x < x_end and y_start < y < y_end:
                        count += 1
                        x_points_one.append(x)
                        y_points_one.append(y)
                        one_list_points.append((x, y))
                if count > self.least_count:
                    x_std = np.std(x_points_one)
                    y_std = np.std(y_points_one)
                    x_start = min(x_points_one)
                    x_end = max(x_points_one)
                    y_start = min(y_points_one)
                    y_end = max(y_points_one)
                    x_distance = 0
                    y_distance = 0
                    if abs(y_std - x_std) < 20:
                        for x, y in zip(x_points_one, y_points_one):
                            x_distance += self.get_dis(x, y, x_start, y_start, x_end, y_end)
                            y_distance += self.get_dis(x, y, x_start, y_end, x_end, y_start)
                        if x_distance < y_distance:
                            block.set_slope(45)
                        else:
                            block.set_slope(135)
                    else:
                        if y_std < x_std:
                            block.set_slope(0)
                        else:
                            block.set_slope(90)
                    self.list_points.append(one_list_points)
                    block.set_points(one_list_points[:])
                    block.set_position((m, n))
                else:
                    block.set_points([])
                    block.set_slope("null")
                    block.set_position((m, n))
                temp.append(block)
            res.append(temp)
        return res

    def get_dis(self, point_X, point_Y, line_X1, line_Y1, line_X2, line_Y2):
        """
        计算点A到直线的距离,直线用两点(B,C)即可描述
        @param point_X:点A横坐标
        @param point_Y:点A纵坐标
        @param line_X1:B点横坐标
        @param line_Y1:B点纵坐标
        @param line_X2:C点横坐标
        @param line_Y2:C点纵坐标
        @return: 点到直线的距离
        """
        a = line_Y2 - line_Y1
        b = line_X1 - line_X2
        c = line_X2 * line_Y1 - line_X1 * line_Y2
        dis = (math.fabs(a * point_X + b * point_Y + c)) / (math.pow(a * a + b * b, 0.5))
        return dis

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

    def __str__(self):
        return str(self.slope) + " degrees at " + str(self.position)

    def __repr__(self):
        return str(self)

if __name__ == "__main__":
    marker = BlockMarker()
    marker.set_points(get_points_from_pcd("four_walls.pcd"))
    print(marker.mark())