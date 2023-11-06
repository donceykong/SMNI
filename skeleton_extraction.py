import matplotlib.pyplot as plt
import matplotlib.animation as animation
import numpy as np
from scipy.spatial import distance as sp_distance
from scipy.ndimage import gaussian_filter

# Read points from file
x_values = []
y_values = []
with open('roadpoints_voxelized.txt', 'r') as file:
    for line in file:
        x, y = line.split()
        x_values.append(float(x))
        y_values.append(float(y))

x_values = np.array(x_values)
y_values = np.array(y_values)

#print(f"x_values: {x_values}")

x_window, y_window = np.meshgrid(np.linspace(0, 96, 500), np.linspace(-48, 48, 500))
grid_points = np.c_[x_window.ravel(), y_window.ravel()]

def euclidean_distance_transform_e(x_values, y_values, grid_points, sigma = 1):
    points = np.vstack((x_values, y_values)).T
    dist = sp_distance.cdist(grid_points, points, 'euclidean') # cool function!!
    dist = np.min(dist, axis=1)
    dist = dist.reshape(x_window.shape)
    dist = gaussian_filter(dist, sigma=sigma)
    return dist

distance_transform_e = euclidean_distance_transform_e(x_values, y_values, grid_points)