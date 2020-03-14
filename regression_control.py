# coding=utf-8

from linear_regressor import SegmentedLinearRegressor
from points_divider import *
from utils import filter_points, get_rotation_matrix, get_intersection, rotate_line
import pypcd
import numpy as np

class RegressionController:

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
        if len(self.parts) == 0: raise Exception("Nothing to fit, check if set_parts() method is called.")
        for part in self.parts:
            if self.verbose:
                print("\n\n************************ Fitting part {} ************************".format(count))
            regressor = SegmentedLinearRegressor(part, self.verbose)
            self.regressors.append(regressor)
            regressor.process(self.segments_count)            
            regressor.get_intersections()
            self.intersections.append(regressor.get_intersections())
            count += 1

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


class SimpleRegressionController(RegressionController):
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
        for reg in self.regressors:
            parameters.append(reg.get_parameters()[0])
        points = []
        points.append(get_intersection(parameters[0], parameters[2]))
        points.append(get_intersection(parameters[0], parameters[3]))
        points.append(get_intersection(parameters[1], parameters[2]))
        points.append(get_intersection(parameters[1], parameters[3]))
        intersections = []
        intersections.append([[points[0][0], points[0][1] + 2], points[1]])
        intersections.append([points[0], points[2]])
        intersections.append([points[2], points[3]])
        intersections.append([points[3], points[1]])
        return intersections
