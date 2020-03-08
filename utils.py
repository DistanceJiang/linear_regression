# coding=utf-8

import pypcd
import numpy as np
from sklearn.linear_model import LinearRegression

def get_points_from_pcd(path):
    return [[i['x'], i['y']] for i in pypcd.PointCloud.from_path(path).pc_data]

def get_intersection(line1, line2):
    # y = ax + b, line = [a, b]
    if line1[0] == line2[0]:
        raise Exception("Line 1 and line 2 are parallel, NO intersection can be found.")
    else:
        intersection = []
        intersection.append((line2[1] - line1[1]) / float((line1[0] - line2[0]))) # (b2 - b1) / (a1 - a2)
        intersection.append(intersection[0] * line1[0] + line1[1]) # (b2 - b1) / (a1 - a2) * a1 + b1
        return intersection

def diff_vertically(point, line):
    return abs(point[1] - line[0] * point[0] - line[1])

def variance(points, lines, segements):
    result = 0.0
    for segment, line in zip(segements, lines):
        points_seg = [i for i in points if segment[0] <= i[0] < segment[1]]
        for point in points_seg:
            result += pow(diff_vertically(point, line), 2)
    return result

def filter_points(points, x_low=float('-inf'), x_high=float('inf'), y_low=float('-inf'), y_high=float('inf')):
    result = [i for i in points if x_low <= i[0] < x_high and y_low <= i[1] < y_high]
    return result

def get_xy_lim(points):
    x = [i[0] for i in points]
    y = [i[1] for i in points]
    return [min(x), max(x), min(y), max(y)]

def get_rotation_matrix(deg):
    # counter-clockwise rotation matrix
    theta = np.radians(deg)
    c, s = np.cos(theta), np.sin(theta)
    R = np.array([[c, -s], [s, c]])
    return R

def rotate_line(line, deg):
    """
    @param line: [k, b]
    @param deg: degrees to rotate, counter clockwise
    """
    theta = np.deg2rad(deg)
    coef_a = line[0] * np.cos(theta) + np.sin(theta)
    coef_b = np.cos(theta) - line[0] * np.sin(theta)
    k = coef_a / coef_b
    b = line[1] / coef_b
    return [k, b]

def get_slope(points):
    """
    Calculate the overall slope for points, 0 ~ 180
    """
    x = np.array([i[0] for i in points]).reshape(-1, 1)
    y = np.array([i[1] for i in points]).reshape(-1, 1)
    reg = LinearRegression()
    reg.fit(x, y)
    k = reg.coef_[0][0]
    print("k: ", k)
    deg = np.rad2deg(np.arctan(k))
    if deg < 0: deg += 180
    return deg


if __name__ == "__main__":
    points = [[0, 0], [-2, 1]]
    print(get_slope(points))