def variance(y, y_pred):
    if len(y) == 0: return 0
    total = 0
    for (i, j) in zip(y, y_pred):
        total += (i - j) ** 2
    return total

def get_intersection(line1, line2):
    # y = ax + b, line = [a, b]
    if line1[0] == line2[0]:
        return
    else:
        intersection = []
        intersection.append((line2[1] - line1[1]) / float((line1[0] - line2[0]))) # (b2 - b1) / (a1 - a2)
        intersection.append(intersection[0] * line1[0] + line1[1]) # (b2 - b1) / (a1 - a2) * a1 + b1
        return intersection

if __name__ == "__main__":
    y = [1, 2, 3, 4]
    y_pred = [1, 1, 1, 1]
    print(variance(y, y_pred))

    line1 = [0.04215221435099827, 3.2913937185356628]
    line2 = [0.0363115245946237, 3.297234408292037]
    print(get_intersection(line1, line2))