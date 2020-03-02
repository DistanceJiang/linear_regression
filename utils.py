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

def filter(points, x_low=float('-inf'), x_high=float('inf'), y_low=float('-inf'), y_high=float('inf')):
    result = [i for i in points if x_low <= i[0] < x_high and y_low <= i[1] < y_high]
    return result

def get_xy_lim(points):
    x = [i[0] for i in points]
    y = [i[1] for i in points]
    return [min(x), max(x), min(y), max(y)]

if __name__ == "__main__":
    line1 = [0.04215221435099827, 3.2913937185356628]
    line2 = [0.0363115245946237, 3.297234408292037]
    print(get_intersection(line1, line2))