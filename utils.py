def get_intersection(line1, line2):
    # y = ax + b, line = [a, b]
    if line1[0] == line2[0]:
        return
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

if __name__ == "__main__":
    line1 = [0.04215221435099827, 3.2913937185356628]
    line2 = [0.0363115245946237, 3.297234408292037]
    print(get_intersection(line1, line2))