import matplotlib
matplotlib.use('TkAgg')
import matplotlib.pyplot as plt
from matplotlib import style
from linear_regressor import *
from utils import get_intersection

fig = plt.figure(figsize=(18, 3))
ax1 = fig.add_subplot(1, 1, 1)
ax1.axis([-1, 8, 2.5, 4])
style.use("fivethirtyeight")
verbose = False

# Linear regression
segments = 11
regressor = segmentedLinearRegressor()
regressor.set_verbose(verbose)
regressor.get_points('0.pcd')
regressor.filter(float('-inf'), float('inf'), 2.5, 4)
regressor.process(segments) # set step 
parameters = regressor.get_result()

if verbose:
    print("\nSegments: " + str(regressor.param_count / 2))
    print("\nk and b: ")
    print([[round(i[0], 3), round(i[1], 3)]for i in parameters])
    print("\nInterval: ")
    print(regressor.interval)

# scatter stable points
xy = regressor.points
xs = [i[0] for i in xy]
ys = [i[1] for i in xy]
ax1.scatter(xs, ys, s=1)

# calculate intersections to plot
x, y = regressor.get_intersections()
plt.plot(x, y, color='red', linewidth=1)

if verbose:
    print("\npoints: ")
    print([[round(i, 3), round(j, 3)] for i, j in zip(x, y)])

# formatting the plot
ax1.text(-0.9, 3.85, 'Variance: {:8.4f}'.format(variance(regressor.points, regressor.parameters, regressor.segments)), fontsize=10)

ax1.set_title("Segmented Linear Regression(segments = {})".format(segments))
plt.savefig("Segemented_Linear_Regression_segments_{}.png".format(str(segments)), dpi=300)
plt.show()