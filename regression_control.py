from linear_regressor import segmentedLinearRegressor
from utils import filter_points
import pypcd

class regressionControllerBase():

    def __init__(self, path, verbose=False):
        """
        Initialization
        @param path: pcd file path
        @param verbose: if True, print more information in the console
        """
        self.points = [[i['x'], i['y']] for i in pypcd.PointCloud.from_path(path).pc_data]
        self.verbose = verbose
        self.regressors = []

    def clear_state(self):
        self.regressors = []

    def get_points(self):
        return self.points

    def fit(self):
        """
        Use linear regressor to fit the points
        @return: list of intersection list
        """
        pass

    def get_parts(self):
        """
        Divide all points into parts to fit
        @return: list of points list
        """
        pass


class simpleRegressionController(regressionControllerBase):
    # Manually marked region to fit
    
    def fit(self):
        self.clear_state()
        parts = self.get_parts()
        intersections = []
        count = 1
        for part in parts:
            if self.verbose:
                print("\n\n************************ Fitting part {} ************************".format(count))
            regressor = segmentedLinearRegressor(self.verbose)
            self.regressors.append(regressor)
            regressor.set_points(part)
            regressor.process(4)
            intersections.append(regressor.get_intersections())
            count += 1
        return intersections
        
    def get_parts(self):
        limits = [[-2, -1, float('-inf'), float('inf')], \
            [4, 5, float('-inf'), float('inf')], \
            [float('-inf'), float('inf'), -1, -0.2], \
            [float('-inf'), float('inf'), 3, 4]]
        parts = []
        for limit in limits:
            parts.append(filter_points(self.points, limit[0], limit[1], limit[2], limit[3]))
        return parts
        
