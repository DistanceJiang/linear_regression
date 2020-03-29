from points_divider import PointsDivider
from linear_regressor import LinearRegressor
from regression_control import RegressionController

from utils import *

class PointsGenerator:

    def __init__(self, intensity=20):
        """
        @param intensity: how many points should we have given the length of 1 meter
        """
        self.intensity = float(intensity)

    def generate(self, points):
        divider = PointsDivider()
        controller = RegressionController()
        controller.set_parts(divider, 0.5)
        reg = LinearRegressor()
        controller.fit(reg)
        result = []
        
        index = 0
        for part in controller.parts:
            if not part.isolated: 
                result.append(self.generate_for_line(controller.parameters[index], controller.intersections[index], self.get_linewidth(part.points)))
                index += 1
        return result

    def generate_for_line(self, line, ends, linewidth):
        """
        @param line: the line to generate points, [k, b], for y = k * x + b
        @param ends: two ends of the line
        @param linewidth: the width of the line
        @return: points generated to mimic the line
        """
        length = dist(ends[0], ends[1])
        linewidth *= self.intensity
        points = [[i / self.intensity, j / self.intensity] for i in range(0, length * self.intensity) for j in range(-linewidth / 2.0, linewidth / 2.0)]
        points = rotate_points(points, k2slope(line[0]))
        lower_end = []
        if ends[0][1] < ends[1][1]:
            lower_end = ends[0]
        else: lower_end = ends[1]
        points = translate_points(points, [-lower_end[0], -lower_end[1]])
        return points

    @staticmethod
    def get_linewidth(points, line):
        a = line[0]
        b = -1
        c = line[1]
        temp = sum([abs(a * p[0] + b * p[1] + c) for p in points])
        return temp / np.sqrt(a ** 2 + b ** 2) / len(points) * 2



if __name__ == "__main__":
    

        