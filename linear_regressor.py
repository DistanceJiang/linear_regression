import pypcd
from utils import variance, get_intersection
import numpy as np
from math import floor, ceil

class segmentedLinearRegressor:

    def __init__(self, *args, **kwargs):
        self.points = []
        self.parameters = [] # y = k * x + b, [k, b]
        self.segments = []
        self.param_count = 0
        self.interval = []
        self.verbose = False

    def set_verbose(self, verbose):
        self.verbose = verbose

    def clear_state(self):
        self.parameters = []
        self.segments = []
        self.param_count = 0
        self.interval = []

    def process(self, segments_count):
        self.clear_state() # ensure you to process multiple times without having to create a new instance of regressor
        self.interval.append(int(floor(min([i[0] for i in self.points]))))
        self.interval.append(int(ceil(max([i[0] for i in self.points]))))
        step = (self.interval[1] - self.interval[0]) / float(segments_count)
        x = [i[0] for i in self.points]
        y = [i[1] for i in self.points]
        # get dimension 
        self.param_count = segments_count * 2
        dimension = segments_count * 3 - 1
        a = [] # Ax = b, a will be used to generate A
        b = []
        for i in range(segments_count): # generate the first segments_count * 2 rows
            two_rows,  two_elems = self.getRows(i, step, dimension) # i is the segment count
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

    def getRows(self, index, step, dimension):
        row1 = [0 for i in range(dimension)]
        row2 = [0 for i in range(dimension)]
        left = index * step + self.interval[0]
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

    def get_points(self, points):
        # points: [[x1, y1], [x2, y2]......[xn, yn]]
        self.points = points

    def get_points(self, path):
        pc = pypcd.PointCloud.from_path(path)
        self.points = [[i['x'], i['y']] for i in pc.pc_data]

    def filter(self, x_low, x_high, y_low, y_high):
        self.points = [i for i in self.points if x_low <= i[0] <= x_high and y_low <= i[1] <= y_high]

    def get_result(self):
        return self.parameters

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
        return x, y

if __name__ == "__main__":
    regressor = segmentedLinearRegressor()
    regressor.get_points('0.pcd')
    regressor.filter(float('-inf'), float('inf'), 2.5, 4)
    for segments_count in range(1, 13):
        regressor.process(segments_count)
        print("\nsegments_count: " + str(round(segments_count, 3)) + \
            "    variance: " + str(round(variance(regressor.points, regressor.parameters, regressor.segments), 3)))