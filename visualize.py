import matplotlib
matplotlib.use('TkAgg')
import matplotlib.pyplot as plt
from matplotlib import style
from utils import get_intersection, get_xy_lim
from regression_control import simpleRegressionController

"""
TODO:
1. show background grid
"""

verbose = True

# Linear regression
controller = simpleRegressionController('four_walls.pcd', verbose)
intersections = controller.fit()

# set figure
padding = 0.5
xy_lim = get_xy_lim(controller.points)
fig = plt.figure(figsize=(20, 20))
ax1 = fig.add_subplot(1, 1, 1)
ax1.axis([xy_lim[0] - padding, xy_lim[1] + padding, xy_lim[2] - padding, xy_lim[3] + padding])
style.use("fivethirtyeight")
verbose = False

# scatter stable points
xy = controller.points
xs = [i[0] for i in xy]
ys = [i[1] for i in xy]
ax1.scatter(xs, ys, s=1)

# calculate intersections to plot
for points in intersections:
    plt.plot([i[0] for i in points], [i[1] for i in points], color='red', linewidth=1)

# formatting the plot
# ax1.text(-0.9, 3.85, 'Variance: {:8.4f}'.format(variance(regressor.points, regressor.parameters, regressor.segments)), fontsize=10)

# ax1.set_title("Segmented Linear Regression(segments = {})".format(segments))
# plt.savefig("Segemented_Linear_Regression_segments_{}.png".format(str(segments)), dpi=300)
plt.show()