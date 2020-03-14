# coding=utf-8

"""
ContinuousPart 为拟合需要调用的数据结构，每一个实例为一个需要单独拟合的点集
slope 为这个实例中包含的点集与x轴正方向的夹角，角度制， 例如，45表示是45度， 80表示80度
points 为一个二维数组，其中的数据为点的坐标，例如, [[1, 2], [3, 4]]表示两个点，坐标分别为(1, 2), (3, 4)
block中没有点时，slope与points都为None
"""

from block_marker import BlockMarker, Block
from utils import get_points_from_pcd, get_slope
from Queue import Queue

class ContinuousPart:

    def __init__(self, slope, points):
        """
        @param slope: int, slope of all the points
        @param points: points to fit
        """
        self.slope = slope
        self.points = points

    def __str__(self):
        return str(len(self.points)) + ": " + str(self.slope)

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
        marker = BlockMarker()
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
        visited = set()
        edge = list()
        parts = []
        start = [0, 0]
        while (len(visited) < blocks_count):
            part = ContinuousPart(None, [])
            q = Queue()
            q.put(start)
            while len(q) != 0:
                cur = q.get()
                visited.add(cur)
                part.points.extend(self.get_block(cur).points)
                if self.get_block(cur).slope is None: continue
                surroundings = get_surroundings(cur)
                for pos in surroundings:
                    if pos in visited:
                        continue
                    if is_connected(cur, pos):
                        q.put(pos)
                        if pos in edge:
                            edge.remove(pos)
                    else:
                        edge.append(pos)
            part.slope = get_slope(part.points)
            parts.append(part)
            start = edge[0]
            edge.remove(start)
        return parts

    
    @staticmethod
    def is_connected(block1, block2):
        pass

    def get_surroundings(self, pos):
        pass
        

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
    divider = PointsDivider()
    divider.set_points(get_points_from_pcd('four_walls.pcd'))
    print(divider.divide())
