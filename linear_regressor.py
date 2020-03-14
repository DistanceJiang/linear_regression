# coding=utf-8

import pypcd
from utils import *
import numpy as np
import sys
from math import floor, ceil
from points_divider import ContinuousPart

"""
TODO:
""" 

class RegressorBase(object):

    def __init__(self, part, verbose=False):
        self.part = part
        self.parameters = [] # y = k * x + b, [k, b]
        self.verbose = verbose

    def get_parameters(self):
        return self.parameters

    def get_intersections(self):
        pass

    def process(self):
        pass


class SegmentedLinearRegressor(RegressorBase):

    def __init__(self, part, verbose=False):
        """
        @param part: ContinuousPart, contians the points to fit
        @param verbose: if True, print the mid results
        """
        self.part = part
        self.points = []
        self.parameters = [] # y = k * x + b, [k, b]
        self.segments = []
        self.param_count = 0
        self.interval = []
        self.verbose = verbose
        self.segments_count = 0

    def clear_state(self):
        """
        Used to clear the result of processing, to allow process with different segments_count multiple times
        """
        self.parameters = []
        self.segments = []
        self.param_count = 0
        self.interval = []

    def rotate_part(self):
        slope = self.part.slope
        matrix = get_rotation_matrix(-slope)
        points = []
        for p in self.part.points:
            vec = np.array([p[0],p[1]])
            points.append(list(matrix.dot(vec)))
        return points

    def process(self, segments_count=1):
        """
        用拉格朗日乘数法，对点进行分段线性拟合
        @param segments_count: number of segments to process
        @return: list of intersections
        """
        self.clear_state() # ensure to process multiple times without having to create a new instance of regressor
        self.segments_count = segments_count
        self.points = self.rotate_part()
        self.interval.append(min([i[0] for i in self.points]))
        self.interval.append(max([i[0] for i in self.points]))
        step = (self.interval[1] - self.interval[0]) / float(segments_count)
        x = [i[0] for i in self.points]
        y = [i[1] for i in self.points]
        # get dimension 
        self.param_count = segments_count * 2
        dimension = segments_count * 3 - 1
        a = [] # Ax = b, a will be used to generate A
        b = []
        for i in range(segments_count): # generate the first segments_count * 2 rows
            two_rows,  two_elems = self.getRows(i, dimension) # i is the segment count
            a += two_rows
            b += two_elems
        for i in range(segments_count - 1):
            temp = [0 for j in range(dimension)]
            temp[i * 2] = self.interval[0] + step * (i + 1)
            temp[i * 2 + 1] = 1
            temp[i * 2 + 2] = -temp[i * 2]
            temp[i * 2 + 3] = -1
            a.append(temp)
            b.append(0)
        A = np.matrix(a)
        b = np.array(b)
        singular = False
        if np.linalg.cond(A) < 1/sys.float_info.epsilon: # to avoid singular matrix
            result = np.linalg.solve(A, b)
            parameters = [[result[i * 2], result[i * 2 + 1]] for i in range(segments_count)]
            for i in range(len(parameters)):
                self.parameters.append(rotate_line(parameters[i], self.part.slope))
        else:
            singular = True

        if self.verbose:
            np.set_printoptions(precision=3, suppress=True)
            print("\nA: ")
            print(A)
            if not singular:
                print("\nx: ")
                print(result)
            else:
                print("\nNOTICE: A is singular, no result is available.")
            print("\nb: ")
            print(b)
            print("\nSegments: " + str(segments_count))
            print("\nk and b: ")
            print([[round(i[0], 3), round(i[1], 3)]for i in self.parameters])
            print("\nInterval: ")
            print(self.interval)

    def getRows(self, index, dimension):
        """
        计算矩阵的每一行，一次计算两行
        """
        row1 = [0 for i in range(dimension)]
        row2 = [0 for i in range(dimension)]
        step = (self.interval[1] - self.interval[0]) / float(self.segments_count)
        left = self.interval[0] + step * index
        right = left + step
        self.segments.append([left, right])
        points = [p for p in self.points if left <= p[0] < right]
        row1[index * 2] = sum([i[0] * i[0] for i in points])
        row1[index * 2 + 1] = sum([i[0] for i in points])
        row2[index * 2] = row1[index * 2 + 1]
        row2[index * 2 + 1] = len(points)
        if index != 0: 
            row1[self.param_count + index - 1] = -0.5
            row2[self.param_count + index - 1] = 0.5
        if index != self.param_count / 2 - 1: 
            row1[self.param_count + index] = 0.5
            row2[self.param_count + index] = -0.5
        two_elems = [0, 0]
        two_elems[0] = sum([i[0] * i[1] for i in points])
        two_elems[1] = sum([i[1] for i in points])
        return [row1, row2], two_elems

    def get_intersections(self):
        """
        由于是分段线性拟合，所以需要给出折点让绘图部分绘制出折线
        """
        if len(self.parameters) == 0: return []
        xy_lim = get_xy_lim(self.part.points)
        self.interval[0] = xy_lim[0]
        self.interval[1] = xy_lim[1]
        x = []
        y = []
        for i in range(len(self.parameters) + 1):
            if i == 0: # 左边端点
                param = self.parameters[0]
                x.append(self.interval[0])
                y.append(x[0] * param[0] + param[1])
            elif i == len(self.parameters): # 右边端点
                param = self.parameters[i - 1]
                x.append(self.interval[1])
                y.append(x[len(x) - 1] * param[0] + param[1])
            else: # 两条折线的交点
                param1 = self.parameters[i - 1]
                param2 = self.parameters[i]
                intersection = get_intersection(param1, param2)
                x.append(intersection[0])
                y.append(intersection[1])
        return [[i, j] for i, j in zip(x, y)]


class LinearRegressor(RegressorBase):
    
    def process(self):
        k, b = get_k_b(self.part.points)
        self.parameters = [[k, b]]

    def get_intersections(self):
        k = self.parameters[0][0]
        b = self.parameters[0][1]
        xy_lim = get_xy_lim(self.part.points)
        x = [xy_lim[0], xy_lim[1], (xy_lim[2] - b) / k, (xy_lim[3] - b) / k]
        x.sort()
        return [[i, k * i + b] for i in x if x[0] < i < x[3]]


if __name__ == "__main__":
    import matplotlib
    matplotlib.use('TkAgg')
    import matplotlib.pyplot as plt
    from utils import get_points_from_pcd, get_xy_lim, get_slope

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

    points = filter_points(points, 4, 5, 2, 3)
    # points = [[4, 2.0], [4.003, 2.3], [4.05, 2.6], [4.1, 2.9]]
    part = ContinuousPart(0, points)
    reg = LinearRegressor(part, verbose=True)
    reg.process()
    ax1.scatter([p[0] for p in points], [p[1] for p in points], color='red', s=4)

    param = reg.get_parameters()[0]
    print(param)
    # abline(param[0], param[1])

    intersections = reg.get_intersections()
    ax1.plot([i[0] for i in intersections], [i[1] for i in intersections], color='blue', linewidth=2)

    plt.show()