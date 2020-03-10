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
    LOWEST_POINTS_COUNT = 10

    def __init__(self, resolution=1):
        """
        @param resolution: int, in meters, the length of a block's edge
        """
        self.resolution = resolution
        self.origin = []

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

    def pos2cordinate(self, pos):
        """
        Convert position of the block to coordinate system
        @pos: position of the block in the 2d array
        """
        return [pos[0] * self.resolution + self.origin[0], pos[1] * self.resolution + self.origin[1]]


class BlockMarker(BlockMarkerInterface):

    def mark(self):
        blocks = []
        xy_lim = get_xy_lim(self.points) # [x_min, x_max, y_min, y_max]
        self.origin = [xy_lim[0], xy_lim[2]]
        row = int(ceil((xy_lim[3] - xy_lim[2]) / self.resolution))
        col = int(ceil((xy_lim[1] - xy_lim[0]) / self.resolution))
        for i in range(row):
            row_blocks = []
            for j in range(col):
                position = [i, j]
                cordinate = self.pos2cordinate(position)
                points = filter_points(self.points, cordinate[0], cordinate[0] + self.resolution, \
                    cordinate[1], cordinate[1] + self.resolution)
                if len(points) < self.LOWEST_POINTS_COUNT: # very few points in the block, slope is None
                    row_blocks.append(Block(None, points, position))
                else:
                    slope = self.clamp_slope(get_slope(points))
                    row_blocks.append(Block(slope, points, position))
            blocks.append(row_blocks)
        return blocks

    @staticmethod
    def clamp_slope(slope):
        """
        make slope either 0, 45, 90, 135
        """
        return int(round(slope / 45)) * 45 % 180


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
        return str(self.position) + ": " + str(self.slope)

    def __repr__(self):
        return str(self)

if __name__ == "__main__":
    import matplotlib
    matplotlib.use('TkAgg')
    import matplotlib.pyplot as plt

    points = get_points_from_pcd("four_walls.pcd")
    
    # Config figure
    padding = 0.2
    xy_lim = get_xy_lim(points)
    ratio = (xy_lim[3] - xy_lim[2]) / float(xy_lim[1] - xy_lim[0])
    fig = plt.figure(figsize=(10 * ratio, 10))
    ax1 = fig.add_subplot(1, 1, 1)
    ax1.grid(True, linewidth=0.5, color='#666666', linestyle='dotted')
    ax1.axis([xy_lim[0] - padding, xy_lim[1] + padding, xy_lim[2] - padding, xy_lim[3] + padding])
    ax1.set_color_cycle(['red', 'black', 'blue', 'brown', 'green'])
    # ax1.scatter([p[0] for p in points], [p[1] for p in points], color='red', s=1)

    # Marking
    resolution = 0.4
    marker = BlockMarker(resolution)
    marker.set_points(points)
    blocks = marker.mark()
    
    for row in blocks:
        for block in row:
            cordinate = marker.pos2cordinate(block.position)
            line_to_draw = []
            if block.slope is None:
                ax1.scatter([p[0] for p in block.points], [p[1] for p in block.points], s=1)
                continue
            elif block.slope == 0:
                line_to_draw = [[cordinate[0], cordinate[1] + resolution / 2], \
                    [cordinate[0] + resolution, cordinate[1] + resolution / 2]]
            elif block.slope == 45:
                line_to_draw = [cordinate, [cordinate[0] + resolution, cordinate[1] + resolution]]
            elif block.slope == 90:
                line_to_draw = [[cordinate[0] + resolution / 2, cordinate[1]], \
                    [cordinate[0] + resolution / 2, cordinate[1] + resolution]]
            elif block.slope == 135:
                line_to_draw = [[cordinate[0], cordinate[1] + resolution], \
                    [cordinate[0] + resolution, cordinate[1]]]
            ax1.scatter([p[0] for p in block.points], [p[1] for p in block.points], s=1)
            ax1.plot([i[0] for i in line_to_draw], [i[1] for i in line_to_draw], linewidth=1)

    plt.show()
