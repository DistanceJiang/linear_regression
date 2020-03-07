# coding=utf-8

import matplotlib
matplotlib.use('TkAgg')
import matplotlib.pyplot as plt
from utils import get_intersection, get_xy_lim
from regression_control import simpleRegressionController

"""
TODO:
"""

verbose = False

# Linear regression
controller = simpleRegressionController(path='four_walls.pcd', verbose=verbose, segments_count=1)
controller.set_parts()
controller.fit()

# set figure
padding = 0.5
xy_lim = get_xy_lim(controller.points)
fig = plt.figure(figsize=(20, 20))
ax1 = fig.add_subplot(1, 1, 1)
ax1.grid(True, linewidth=0.5, color='#666666', linestyle='dotted')
ax1.axis([xy_lim[0] - padding, xy_lim[1] + padding, xy_lim[2] - padding, xy_lim[3] + padding])

# scatter points
xy = controller.points
xs = [i[0] for i in xy]
ys = [i[1] for i in xy]
ax1.scatter(xs, ys, s=1)

# calculate intersections to plot
intersections = controller.get_intersections()
for points in intersections:
    plt.plot([i[0] for i in points], [i[1] for i in points], color='red', linewidth=15)

# formatting the plot
# ax1.text(-0.9, 3.85, 'Variance: {:8.4f}'.format(variance(regressor.points, regressor.parameters, regressor.segments)), fontsize=10)

# ax1.set_title("Segmented Linear Regression(segments = {})".format(segments))
# plt.savefig("Segemented_Linear_Regression_segments_{}.png".format(str(segments)), dpi=300)
plt.show()