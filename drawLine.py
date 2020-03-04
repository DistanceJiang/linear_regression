# coding=utf-8

import numpy as np
import matplotlib
matplotlib.use('TkAgg')
import matplotlib.pyplot as plt
import math
from itertools import chain


class Line:

    def __init__(self, row, col, least_count):
        self.row = row
        self.col = col
        self.min_x = float("inf")
        self.min_y = float("inf")
        self.max_x = float("-inf")
        self.max_y = float("-inf")
        self.raw_path = ""
        self.new_path = ""
        self.x_span = 0
        self.y_span = 0
        self.nums = 0
        self.list_points = list()
        self.least_count = least_count
        self.line_state = list()
        self.line_coordinate = list()
        self.two_dimension = list()

    def generate_new_points(self, raw_path, new_path):
        self.raw_path = raw_path
        self.new_path = new_path
        new_file = open(new_path, "w")
        points = list()
        with open(raw_path, "r") as raw_file:
            for line in raw_file.readlines()[12:]:
                self.nums += 1
                row_array = line.split(" ")
                x = format(float(row_array[0]) * 1000, '.2f')
                self.min_x = min(self.min_x, float(x))
                self.max_x = max(self.max_x, float(x))
                y = format(float(row_array[1]) * 1000, '.2f')
                self.min_y = min(self.min_y, float(y))
                self.max_y = max(self.max_y, float(y))
                points.append([x, y])
        x_span = (self.max_x - self.min_x) // self.col
        y_span = (self.max_y - self.min_y) // self.row

        for m in range(self.row):
            temp_dimension = list()
            for n in range(self.col):
                count = 0
                x_start = x_span * n + self.min_x
                x_end = x_span * (n + 1) + self.min_x
                y_start = y_span * m + self.min_y
                y_end = y_span * (m + 1) + self.min_y
                one_file_points = ""
                one_list_points = list()
                for i in range(self.nums):
                    x0 = float(points[i][0])
                    y0 = float(points[i][1])
                    if (x_start < x0 < x_end and y_start < y0 < y_end):
                        count += 1
                        one_file_points = one_file_points + points[i][0] + "," + points[i][1] + " "
                        one_list_points.append((x0, y0))
                if count > self.least_count:
                    new_file.write((one_file_points + "\n").decode('string-escape'))
                    self.list_points.append(one_list_points)
                    temp_dimension.append("有")
                else:
                    temp_dimension.append("无")
            self.two_dimension.append(temp_dimension)
            self.two_dimension = list(chain(*self.two_dimension))
        new_file.close()

    def draw_line_from_file(self, line_coordinate_path):
        x_points = list()
        y_points = list()

        with open(self.new_path, "r") as file:
            for line in file.readlines():
                row = line.split(" ")
                x_points_one = list()
                y_points_one = list()
                for i in range(len(row[:-1])):
                    temp = row[i].split(",")
                    x_points_one.append(float(temp[0]))
                    y_points_one.append(float(temp[1]))
                x_std = np.std(x_points_one)
                y_std = np.std(y_points_one)
                x_mean = np.mean(x_points_one)
                y_mean = np.mean(y_points_one)
                x_start = min(x_points_one)
                x_end = max(x_points_one)
                y_start = min(y_points_one)
                y_end = max(y_points_one)

                x_distance = 0
                y_distance = 0
                if abs(y_std - x_std) < 20:
                    for x, y in zip(x_points_one, y_points_one):
                        x_distance += self.get_dis(x, y, x_start, y_start, x_end, y_end)
                        y_distance += self.get_dis(x, y, x_start, y_end, x_end, y_start)
                    if x_distance < y_distance:
                        plt.plot([x_start, x_end], [y_start, y_end], linewidth='3')
                        self.line_state.append("正斜线")
                        self.line_coordinate.append([x_start, y_start, x_end, y_end ])
                    else:
                        plt.plot([x_start, x_end], [y_end, y_start], linewidth='3')
                        self.line_state.append("反斜线")
                        self.line_coordinate.append([x_start, y_end, x_end, y_start])
                else:
                    if y_std < x_std:
                        plt.plot([x_start, x_end], [y_mean, y_mean], linewidth='2')
                        self.line_state.append("横线")
                        self.line_coordinate.append([x_start, y_mean, x_end, y_mean])
                    else:
                        plt.plot([x_mean, x_mean], [y_start, y_end], linewidth='2')
                        self.line_state.append("竖线")
                        self.line_coordinate.append([x_mean, y_start, x_mean, y_end])
                plt.scatter(x_points_one, y_points_one, s=0.3, alpha=1.0)
                x_points.extend(x_points_one)
                y_points.extend(y_points_one)
            plt.xlim(self.min_x-400, self.max_x+400)
            plt.ylim(self.min_y-400, self.max_y+400)
            plt.show()
        with open(line_coordinate_path, "w") as file:
            for state,coordinate in zip(self.line_state, self.line_coordinate):
                file.write((state + " " + str(coordinate) + "\n").decode('string-escape'))

    def draw_line_from_list(self, line_coordinate_path):
        x_points = list()
        y_points = list()

        for line in self.list_points:
            x_points_one = list()
            y_points_one = list()
            for point in line:
                x_points_one.append(point[0])
                y_points_one.append(point[1])
            x_std = np.std(x_points_one)
            y_std = np.std(y_points_one)
            x_mean = np.mean(x_points_one)
            y_mean = np.mean(y_points_one)
            x_start = min(x_points_one)
            x_end = max(x_points_one)
            y_start = min(y_points_one)
            y_end = max(y_points_one)

            x_distance = 0
            y_distance = 0
            if abs(y_std - x_std) < 20:
                for x, y in zip(x_points_one, y_points_one):
                    x_distance += self.get_dis(x, y, x_start, y_start, x_end, y_end)
                    y_distance += self.get_dis(x, y, x_start, y_end, x_end, y_start)
                if (x_distance < y_distance):
                    plt.plot([x_start, x_end], [y_start, y_end], linewidth='3')
                    self.line_state.append("正斜线")
                    self.line_coordinate.append([x_start, y_start, x_end, y_end])
                else:
                    plt.plot([x_start, x_end], [y_end, y_start], linewidth='3')
                    self.line_state.append("反斜线")
                    self.line_coordinate.append([x_start, y_end, x_end, y_start])
            else:
                if y_std < x_std:
                    plt.plot([x_start, x_end], [y_mean, y_mean], linewidth='2')
                    self.line_state.append("横线")
                    self.line_coordinate.append([x_start, y_mean, x_end, y_mean])
                else:
                    plt.plot([x_mean, x_mean], [y_start, y_end], linewidth='2')
                    self.line_state.append("竖线")
                    self.line_coordinate.append([x_mean, y_start, x_mean, y_end])
            plt.scatter(x_points_one, y_points_one, s=0.3, alpha=1.0)
            x_points.extend(x_points_one)
            y_points.extend(y_points_one)
        plt.xlim(self.min_x-400, self.max_x+400)
        plt.ylim(self.min_y-400, self.max_y+400)
        plt.show()
        # 最后存入文件的数据结构为：竖线 【x0,y0,x1,y1】
        with open(line_coordinate_path, "w") as file:
            for state,coordinate in zip(self.line_state, self.line_coordinate):
                file.write((state + " " + str(coordinate) + "\n").encode('string-escape'))

    def write_state_to_file(self, two_dimension_path):
        count = 0
        for index, state in enumerate(self.two_dimension):
            if state == "有":
                self.two_dimension[index] = self.line_state[count]
                count += 1
        temp = list()
        for i in range(self.row):
            temp.insert(0, self.two_dimension[self.col*i : self.col*(i+1)])
        self.two_dimension = temp

        with open(two_dimension_path, "w") as file:
            for i in self.two_dimension:
                file.write((str(i) + '\n').decode('string-escape'))

    def get_dis(self, point_X, point_Y, line_X1, line_Y1, line_X2, line_Y2):
        a = line_Y2 - line_Y1
        b = line_X1 - line_X2
        c = line_X2 * line_Y1 - line_X1 * line_Y2
        dis = (math.fabs(a * point_X + b * point_Y + c)) / (math.pow(a * a + b * b, 0.5))
        return dis


if __name__ == "__main__":
    # line = Line(12, 11, 15)
    line = Line(8, 11, 15)
    line.generate_new_points("0.pcd", "new_line_point_file.txt")
    # line.draw_line_from_file("line_coordinate.txt")
    line.draw_line_from_list("line_coordinate.txt")
    line.write_state_to_file("two_dimension.txt")
