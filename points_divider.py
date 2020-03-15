# coding=utf-8

"""
ContinuousPart 为拟合需要调用的数据结构，每一个实例为一个需要单独拟合的点集
points 为一个二维数组，其中的数据为点的坐标，例如, [[1, 2], [3, 4]]表示两个点，坐标分别为(1, 2), (3, 4)
"""

from block_marker import BlockMarker, Block
from utils import get_points_from_pcd, get_slope
from collections import deque

class ContinuousPart:

    def __init__(self, points):
        """
        @param points: points to fit
        """
        self.points = points

    def __str__(self):
        return str(len(self.points)) + "points"

    def __repr__(self):
        return str(self)


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
        marker = BlockMarker(0.5)
        marker.set_points(self.points)
        self.blocks = marker.mark()

    def get_block(self, pos):
        return self.blocks[pos[0]][pos[1]]

    def divide(self):
        """
        @return: list of ContinuousParts
        """
        
class PointsDivider(PointsDividerInterface):

    def divide(self):
        if (len(self.blocks) == 0): raise Exception("No blocks available, try to call set_blocks first.")
        blocks_count = len(self.blocks) * len(self.blocks[0])
        visited = list()
        edge = deque()
        parts = []
        start = [0, 0]
        while (len(visited) < blocks_count):
            part = ContinuousPart([])
            q = deque()
            q.append(start)
            always_empty_block = True
            while len(q) != 0:
                cur = q.pop()
                visited.append(cur)
                part.points.extend(self.get_block(cur).points)
                if self.get_block(cur).param is not None: always_empty_block = False
                surroundings = self.get_surroundings(cur)
                for pos in surroundings:
                    if pos in visited:
                        continue
                    if always_empty_block:
                        q.append(pos)
                        break
                    if self.is_connected(cur, pos):
                        if pos not in q:
                            q.append(pos)
                        if pos in edge:
                            edge.remove(pos)
                    else:
                        if pos not in q and pos not in edge: edge.append(pos)
            if len(part.points) != 0: parts.append(part)
            if len(edge) != 0:
                start = edge.pop()
            else: break
        return parts
    
    def is_connected(self, pos1, pos2):
        block1 = self.get_block(pos1)
        block2 = self.get_block(pos2)
        if (block1.param == None or block2.param == None): return False
        slope1 = block1.get_slope()
        slope2 = block2.get_slope()
        total_points = []
        total_points.extend(block1.points)
        total_points.extend(block2.points)
        slope = get_slope(total_points)
        if (abs(slope - slope1) + abs(slope - slope2) > 135):
            return False
        return True

    def get_surroundings(self, pos):
        row = len(self.blocks)
        col = len(self.blocks[0])

        def valid(position):
            if position == pos: return False
            if 0 <= position[0] < row and 0 <= position[1] < col: return True
            return False

        surroundings = []
        x_offset = 0
        y_offset = 0
        for x_offset in range(-1, 2):
            for y_offset in range(-1, 2):
                temp = [pos[0] + x_offset, pos[1] + y_offset]
                if valid(temp): surroundings.append(temp)
        return surroundings
        

# Deprecated
class DeprecatedPointsDivider(PointsDividerInterface):

    def divide(self):
        self.set_blocks()
        row = len(self.blocks)
        col = len(self.blocks[0])
        flag_lists = [[0 for i in range(col)] for j in range(row)]

        def find_same(two_dimension_lists, x, y, sort_list):
            if x < 0 or x >= row or y < 0 or y >= col:
                return None
            elif two_dimension_lists[x][y].points == None:
                return None
            elif two_dimension_lists[x][y].slope == 0:
                if y > 0 and two_dimension_lists[x][y - 1].slope in [0, 45, 135] and flag_lists[x][y - 1] == 0:
                    sort_list.append(two_dimension_lists[x][y - 1])
                    flag_lists[x][y - 1] = 1
                    find_same(two_dimension_lists, x, y - 1, sort_list)
                if y < col - 1 and two_dimension_lists[x][y + 1].slope in [0, 45, 135] and flag_lists[x][y + 1] == 0:
                    sort_list.append(two_dimension_lists[x][y + 1])
                    flag_lists[x][y + 1] = 1
                    find_same(two_dimension_lists, x, y + 1, sort_list)
            elif two_dimension_lists[x][y].slope == 90:
                if x > 0 and two_dimension_lists[x - 1][y].slope in [90, 45, 135] and flag_lists[x - 1][y] == 0:
                    sort_list.append(two_dimension_lists[x - 1][y])
                    flag_lists[x - 1][y] = 1
                    find_same(two_dimension_lists, x - 1, y, sort_list)
                if x < row - 1 and two_dimension_lists[x + 1][y].slope in [90, 45, 135] and flag_lists[x + 1][y] == 0:
                    sort_list.append(two_dimension_lists[x + 1][y])
                    flag_lists[x + 1][y] = 1
                    find_same(two_dimension_lists, x + 1, y, sort_list)
            elif two_dimension_lists[x][y].slope == 45:
                if x > 0 and y < col - 1 and two_dimension_lists[x - 1][y + 1].slope == 45 and \
                        flag_lists[x - 1][y + 1] == 0:
                    sort_list.append(two_dimension_lists[x - 1][y + 1])
                    flag_lists[x - 1][y + 1] = 1
                    find_same(two_dimension_lists, x - 1, y + 1, sort_list)
                if x < row - 1 and y > 0 and two_dimension_lists[x + 1][y - 1].slope == 45 and \
                        flag_lists[x + 1][y - 1] == 0:
                    sort_list.append(two_dimension_lists[x + 1][y - 1])
                    flag_lists[x + 1][y - 1] = 1
                    find_same(two_dimension_lists, x + 1, y - 1, sort_list)
                if y > 0 and two_dimension_lists[x][y - 1].slope in [0, 135] and flag_lists[x][y - 1] == 0:
                    sort_list.append(two_dimension_lists[x][y - 1])
                    flag_lists[x][y - 1] = 1
                    find_same(two_dimension_lists, x, y - 1, sort_list)
                if y < col - 1 and two_dimension_lists[x][y + 1].slope in [0, 135] and flag_lists[x][y + 1] == 0:
                    sort_list.append(two_dimension_lists[x][y + 1])
                    flag_lists[x][y + 1] = 1
                    find_same(two_dimension_lists, x, y + 1, sort_list)
                if x > 0 and two_dimension_lists[x - 1][y].slope in [90, 135] and flag_lists[x - 1][y] == 0:
                    sort_list.append(two_dimension_lists[x - 1][y])
                    flag_lists[x - 1][y] = 1
                    find_same(two_dimension_lists, x - 1, y, sort_list)
                if x < row - 1 and two_dimension_lists[x + 1][y].slope in [90, 135] and flag_lists[x + 1][y] == 0:
                    sort_list.append(two_dimension_lists[x + 1][y])
                    flag_lists[x + 1][y] = 1
                    find_same(two_dimension_lists, x + 1, y, sort_list)
            elif two_dimension_lists[x][y].slope == 135:
                if x > 0 and y > 0 and two_dimension_lists[x - 1][y - 1].slope == 135 and flag_lists[x - 1][y - 1] == 0:
                    sort_list.append(two_dimension_lists[x - 1][y - 1])
                    flag_lists[x - 1][y - 1] = 1
                    find_same(two_dimension_lists, x - 1, y - 1, sort_list)
                if x < row - 1 and y < col - 1 and two_dimension_lists[x + 1][y + 1].slope == 135 and \
                        flag_lists[x + 1][y + 1] == 0:
                    sort_list.append(two_dimension_lists[x + 1][y + 1])
                    flag_lists[x + 1][y + 1] = 1
                    find_same(two_dimension_lists, x + 1, y + 1, sort_list)
                if y > 0 and two_dimension_lists[x][y - 1].slope in [0, 135] and flag_lists[x][y - 1] == 0:
                    sort_list.append(two_dimension_lists[x][y - 1])
                    flag_lists[x][y - 1] = 1
                    find_same(two_dimension_lists, x, y - 1, sort_list)
                if y < col - 1 and two_dimension_lists[x][y + 1].slope in [0, 45] and flag_lists[x][y + 1] == 0:
                    sort_list.append(two_dimension_lists[x][y + 1])
                    flag_lists[x][y + 1] = 1
                    find_same(two_dimension_lists, x, y + 1, sort_list)
                if x > 0 and two_dimension_lists[x - 1][y].slope in [90, 45] and flag_lists[x - 1][y] == 0:
                    sort_list.append(two_dimension_lists[x - 1][y])
                    flag_lists[x - 1][y] = 1
                    find_same(two_dimension_lists, x - 1, y, sort_list)
                if x < row - 1 and two_dimension_lists[x + 1][y].slope in [90, 45] and flag_lists[x + 1][y] == 0:
                    sort_list.append(two_dimension_lists[x + 1][y])
                    flag_lists[x + 1][y] = 1
                    find_same(two_dimension_lists, x + 1, y, sort_list)

        sort_lists = []
        k = -1
        for x in range(row):
            for y in range(col):
                if self.blocks[x][y].slope in [0, 90, 45, 135] and flag_lists[x][y] == 0:
                    sort_lists.append([])
                    k = k + 1
                    find_same(self.blocks, x, y, sort_lists[k])
        sort_lists = [t for t in sort_lists if t]
        contiPart_list = []
        for i in range(len(sort_lists)):
            contiPart_list.append(ContinuousPart(0,[]))
            for j in range(len(sort_lists[i])):
                contiPart_list[i].points.extend(sort_lists[i][j].points)
                contiPart_list[i].slope = get_slope(contiPart_list[i].points)
        return contiPart_list

if __name__ == "__main__":
    import matplotlib
    matplotlib.use('TkAgg')
    import matplotlib.pyplot as plt
    from utils import get_points_from_pcd, get_xy_lim, get_slope
    import numpy as np

    def abline(slope, intercept):
        """Plot a line from slope and intercept"""
        axes = plt.gca()
        x_vals = np.array(axes.get_xlim())
        y_vals = intercept + slope * x_vals
        plt.plot(x_vals, y_vals, '--')

    points = get_points_from_pcd("four_walls.pcd")

    padding = 0.2
    xy_lim = get_xy_lim(points)
    ratio = (xy_lim[3] - xy_lim[2]) / float(xy_lim[1] - xy_lim[0])
    fig = plt.figure(figsize=(10 * ratio, 10))
    ax1 = fig.add_subplot(1, 1, 1)
    ax1.grid(True, linewidth=0.5, color='#666666', linestyle='dotted')
    ax1.axis([xy_lim[0] - padding, xy_lim[1] + padding, xy_lim[2] - padding, xy_lim[3] + padding])
    ax1.set_color_cycle(['red', 'black', 'blue', 'brown', 'green'])

    divider = PointsDivider()
    divider.set_points(points)
    divider.set_blocks()
    parts = divider.divide()
    print(parts)
    print(len(parts))

    for part in parts:
        ax1.scatter([i[0] for i in part.points], [i[1] for i in part.points], s=1)

    plt.show()
