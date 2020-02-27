import matplotlib
matplotlib.use('TkAgg')
import matplotlib.pyplot as plt
from matplotlib import style
from regression_processor import *
from utils import get_intersection

fig = plt.figure(figsize=(18, 3))
ax1 = fig.add_subplot(1, 1, 1)
ax1.axis([-1, 8, 2.5, 4])
style.use("fivethirtyeight")

# Linear regression
step = 4
processor = segmentedLinearRegressor()
processor.get_points('0.pcd')
processor.filter(float('-inf'), float('inf'), 2.5, 4)
processor.process(step) # set step 
metrics = processor.get_metrics()
parameters = processor.get_result()
print("\nSegments: " + str(processor.param_count / 2))
print("\nk and b: ")
print([[round(i[0], 3), round(i[1], 3)]for i in parameters])
print("\nInterval: ")
print(processor.interval)

# scatter stable points
xy = processor.points
xs = [i[0] for i in xy]
ys = [i[1] for i in xy]
ax1.scatter(xs, ys, s=1)

# calculate intersections to plot
x, y = processor.get_intersections()
print("\npoints: ")
print([[round(i, 3), round(j, 3)] for i, j in zip(x, y)])
plt.plot(x, y, color='red', linewidth=1)

# formatting the plot
# ax1.text(8.1, 3.8, 'Mean Absolute Error: {:8.4f}'.format(metrics['mean_absolute_error']), fontsize=6)
# ax1.text(8.1, 3.7, 'Mean Squared Error: {:8.4f}'.format(metrics['mean_squared_error']), fontsize=6)
# ax1.text(8.1, 3.6, 'Variance: {:8.4f}'.format(metrics['variance']), fontsize=6)

ax1.set_title("Segmented Linear Regression(step = {})".format(step))
# plt.savefig("Segemented_Linear_Regression_step_{}.png".format(str(step)), dpi=300)
plt.show()