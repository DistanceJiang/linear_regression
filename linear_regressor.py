# coding=utf-8

import pypcd
from utils import variance, get_intersection, filter_points
import numpy as np
from math import floor, ceil

"""
TODO:
""" 

class segmentedLinearRegressor:

    def __init__(self, part=None, verbose=False):
        """
        @param part: ContinuousPart, contians the points to fit
        @param verbose: if True, print the mid results
        """
        self.points = []
        if part is not None: self.points = part.points
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

    def process(self, segments_count):
        """
        用拉格朗日乘数法，对点进行分段线性拟合
        @param segments_count: number of segments to process
        @return: list of intersections
        """
        self.clear_state() # ensure you to process multiple times without having to create a new instance of regressor
        self.segments_count = segments_count
        self.interval.append(int(min([i[0] for i in self.points])))
        self.interval.append(int(max([i[0] for i in self.points])))
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
        result = np.linalg.solve(A, b)
        self.parameters = [[result[i * 2], result[i * 2 + 1]] for i in range(segments_count)]

        if self.verbose:
            np.set_printoptions(precision=3, suppress=True)
            print("\nA: ")
            print(A)
            print("\nx: ")
            print(result)
            print("\nb: ")
            print(b)
            print("\nSegments: " + str(segments_count))
            print("\nk and b: ")
            print([[round(i[0], 3), round(i[1], 3)]for i in self.parameters])
            print("\nInterval: ")
            print(self.interval)

    def getRows(self, index, dimension):
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

    def get_parameters(self):
        return self.parameters

    def set_points(self, points):
        self.points = points

    def get_intersections(self):
        x = []
        y = []
        for i in range(len(self.parameters) + 1):
            if i == 0:
                param = self.parameters[0]
                x.append(self.interval[0])
                y.append(x[0] * param[0] + param[1])
            elif i == len(self.parameters):
                param = self.parameters[i - 1]
                x.append(self.interval[1])
                y.append(x[len(x) - 1] * param[0] + param[1])
            else:
                param1 = self.parameters[i - 1]
                param2 = self.parameters[i]
                intersection = get_intersection(param1, param2)
                x.append(intersection[0])
                y.append(intersection[1])
        return [[i, j] for i, j in zip(x, y)]

if __name__ == "__main__":
    regressor = segmentedLinearRegressor()
    regressor.points = [[i['x'], i['y']] for i in pypcd.PointCloud.from_path('0.pcd').pc_data]
    regressor.points = filter_points(regressor.points, float('-inf'), float('inf'), 2.5, 4)
    for segments_count in range(1, 13):
        regressor.process(segments_count)
        print("\nsegments_count: " + str(round(segments_count, 3)) + \
            "    variance: " + str(round(variance(regressor.points, regressor.parameters, regressor.segments), 3)))