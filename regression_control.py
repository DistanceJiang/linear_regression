# coding=utf-8

from linear_regressor import segmentedLinearRegressor
from points_divider import *
from utils import filter_points, get_rotation_matrix, get_intersection, rotate_line
import pypcd
import numpy as np

class regressionController():

    def __init__(self, path=None, segments_count=1, verbose=False):
        """
        Initialization
        @param path: pcd file path
        @param verbose: if True, print more information in the console
        """
        if path is None: self.points = []
        else: self.points = [[i['x'], i['y']] for i in pypcd.PointCloud.from_path(path).pc_data]
        self.segments_count = segments_count
        self.verbose = verbose
        self.regressors = []
        self.parts = []
        self.intersections = []

    def clear_state(self):
        self.regressors = []
        self.parts = []
        self.intersections = []

    def get_points(self):
        return self.points

    def set_points(self, points):
        self.points = points

    def fit(self):
        """
        Use linear regressor to fit the points
        @return: list of intersection list
        """
        count = 1
        print(self.parts)
        if len(self.parts) == 0: raise Exception("Nothing to fit, check if set_parts() method is called.")
        for part in self.parts:
            if self.verbose:
                print("\n\n************************ Fitting part {} ************************".format(count))
            self.intersections.append(self.rotated_fit(part))
            count += 1

    def rotated_fit(self, part):
        """
        1. Rotate points to horizontal according to ContinuousPart.slope
        2. Do normal fit using linear regressor
        3. Rotate everything back

        @param part: ContinuousPart
        @return: list of intersection points
        """
        slope = part.slope
        matrix = get_rotation_matrix(-slope)
        points = []
        for p in part.points:
            vec = np.array([p[0],p[1]])
            points.append(list(matrix.dot(vec)))
        new_part = ContinuousPart(0, points)
        regressor = segmentedLinearRegressor(new_part, self.verbose)
        self.regressors.append(regressor)
        regressor.process(self.segments_count)
        intersections = regressor.get_intersections()
        new_intersections = []
        matrix = get_rotation_matrix(slope)
        for p in intersections:
            vec = np.array([p[0], p[1]])
            new_intersections.append(list(matrix.dot(vec)))
        return new_intersections

    def set_parts(self, divider):
        """
        Divide all points into parts to fit
        @param divider: PointsDivider object, divide points into parts
        @return:
        """
        divider.set_points(self.points)
        self.parts = divider.divide()

    def get_intersections(self):
        if (len(self.regressors) == 0): raise Exception("No regression has been applied, please try to do a regression first.")
        return self.intersections


class simpleRegressionController(regressionController):
    # Manually marked region to fit
        
    def set_parts(self):
        limits = [[-2, -1, float('-inf'), float('inf')], \
            [4, 5, float('-inf'), float('inf')], \
            [float('-inf'), float('inf'), -1, -0.2], \
            [float('-inf'), float('inf'), 3, 4]]
        count = 0
        for limit in limits:
            points = filter_points(self.points, limit[0], limit[1], limit[2], limit[3])
            slope = 0
            if count < 2: slope = 90
            self.parts.append(ContinuousPart(slope, points)) 
            count += 1 

    def get_intersections(self):
        if (len(self.regressors) == 0): raise Exception("No regression has been applied, please try to do a regression first.")
        parameters = []
        for reg, part in zip(self.regressors, self.parts):
            parameters.append(rotate_line(reg.get_parameters()[0], part.slope))
        points = []
        points.append(get_intersection(parameters[0], parameters[2]))
        points.append(get_intersection(parameters[0], parameters[3]))
        points.append(get_intersection(parameters[1], parameters[2]))
        points.append(get_intersection(parameters[1], parameters[3]))
        intersections = []
        intersections.append([points[0], points[1]])
        intersections.append([points[0], points[2]])
        intersections.append([points[2], points[3]])
        intersections.append([points[3], points[1]])
        return intersections
