# coding=utf-8

"""
ContinuousPart 为拟合需要调用的数据结构，每一个实例为一个需要单独拟合的点集
points 为一个二维数组，其中的数据为点的坐标，例如, [[1, 2], [3, 4]]表示两个点，坐标分别为(1, 2), (3, 4)
"""

from block_marker import BlockMarker, Block
from utils import get_points_from_pcd, get_slope, get_k_b, dist, k2slope
from collections import deque
from numpy import average

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
        self.marker = None

    def set_points(self, points):
        """
        points为需要分块的点集
        """
        self.points = points

    def set_blocks(self):
        """
        blocks为包含block_marker.py中的Block的列表，包含对于小方格的标记
        """
        self.marker = BlockMarker(float(1))
        self.marker.set_points(self.points)
        self.blocks = self.marker.mark()

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
            ks = [] # k of the blocks, y = k * x + b
            q = deque()
            cur = start
            # 在Block为空的地方漫游，直到找到第一个不为空的Block
            while self.get_block(cur).param is None:
                visited.append(cur)
                surroundings = self.get_surroundings(cur)
                for pos in surroundings:
                    if pos not in edge and pos not in visited:
                        edge.append(pos)
                if len(edge) != 0: cur = edge.popleft()
                else: return parts
            # 找到不为空的Block，开始向part中填充点，并向四周扩张
            q.append(cur)
            while len(q) != 0:
                cur = q.pop()
                visited.append(cur)
                part.points.extend(self.get_block(cur).points)
                surroundings = self.get_surroundings(cur)
                if self.get_block(cur).param is None: 
                    for pos in surroundings:
                        if pos not in edge and pos not in q and pos not in visited:
                            edge.append(pos)
                    continue
                else:
                    ks.append(self.get_block(cur).param[0])
                    for pos in surroundings:
                        if pos in visited:
                            continue
                        elif self.is_connected(cur, pos, ks):
                            if pos not in q:
                                q.append(pos)
                            if pos in edge:
                                edge.remove(pos)
                        else:
                            if pos not in q and pos not in edge: edge.append(pos)
            if len(part.points) != 0: parts.append(part)
            if len(edge) != 0:
                start = edge.popleft()
            else: break
        return parts
    
    def is_connected(self, pos1, pos2, ks):
        """
        Check if two blocks are connected.
        @param pos1: position of first block
        @param pos2: position of second block
        @param ks: all the k of the blocks currently in that part
        """
        block1 = self.get_block(pos1)
        block2 = self.get_block(pos2)

        # 两个格子只要有一个是空，则认为不连接
        if (block1.param == None or block2.param == None): return False

        # 若两个格子中的线的两个端点之间的距离最小值大于分辨率，则认为两个格子不连接
        intersection1 = block1.get_intersections()
        intersection2 = block2.get_intersections()
        dists = []
        for p1 in intersection1:
            for p2 in intersection2:
                dists.append(dist(p1, p2))
        if min(dists) < self.marker.resolution / 3: return True

        # 若pos2的方向与整体的方向差别过大，则认为pos2与整体不应该连接
        slope2 = block2.get_slope()
        slope = average([k2slope(k) for k in ks])
        if abs(slope - slope2) < 45: return True

        return False

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

    # for part in parts:
    #     ax1.scatter([i[0] for i in part.points], [i[1] for i in part.points], s=1)

    index = 6
    ax1.scatter([i[0] for i in parts[index].points], [i[1] for i in parts[index].points], s=1)

    plt.show()
