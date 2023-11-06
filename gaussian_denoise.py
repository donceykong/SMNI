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

xx, yy = np.meshgrid(np.linspace(0, 96, 500), np.linspace(-48, 48, 500))
grid_points = np.c_[xx.ravel(), yy.ravel()]

# Function to compute the Euclidean distance transform
def euclidean_distance_transform_e(x_values, y_values, grid_points, sigma = 1):
    points = np.vstack((x_values, y_values)).T
    dist = sp_distance.cdist(grid_points, points, 'euclidean')
    dist = np.min(dist, axis=1)
    dist = dist.reshape(xx.shape)
    dist = gaussian_filter(dist, sigma=sigma)
    return dist

# Function to compute the Euclidean distance transform with Gaussian smoothing
def euclidean_distance_transform_m(x_values, y_values, grid_points, sigma=1):
    points = np.vstack((x_values, y_values)).T
    dist = sp_distance.cdist(grid_points, points, 'mahalanobis') 
    dist = np.min(dist, axis=1)
    dist = dist.reshape(xx.shape)
    dist = gaussian_filter(dist, sigma=sigma)
    return dist

# Function to add scaled uniform noise based on distance with a more shallow gradient
def add_uniform_noise_based_on_distance2(grid, distance_transform, max_noise_scale=1.0, decay_rate=1):
    noise_scale = max_noise_scale * np.exp(-distance_transform / decay_rate)
    return grid + np.random.uniform(low=0, high=noise_scale, size=grid.shape)

# Function to add scaled uniform noise based on distance with a more shallow gradient
def add_uniform_noise_based_on_distance(grid, distance_transform, max_noise_scale=1.0, decay_rate=1):
    noise_scale = np.clip(1 - distance_transform / decay_rate, 0, max_noise_scale)
    return grid + np.random.uniform(low=0, high=noise_scale, size=grid.shape)

# Compute the distance transform
distance_transform_m = euclidean_distance_transform_m(x_values, y_values, grid_points)
distance_transform_e = euclidean_distance_transform_e(x_values, y_values, grid_points)

# Init plot with two subplots
fig, (ax1, ax2, ax3) = plt.subplots(1, 3, figsize=(12, 6))  # Two subplots side by side

# Plot for original points
ax1.set_xlim(0, 96)
ax1.set_ylim(-48, 48)
line, = ax1.plot(x_values, y_values, 'o', markersize=3)
ax1.set_title('Input Points')

# Plot for noise map
ax2.set_xlim(0, 96)
ax2.set_ylim(-48, 48)
image = ax2.imshow(np.zeros_like(xx), extent=(0, 96, -48, 48), vmin=0, vmax=1,
                   origin='lower', cmap='viridis', alpha=0.7)
plt.colorbar(image, ax=ax2, label='Noise level')
ax2.set_title('Noise Map (variant 1)')

# Plot for noise map
ax3.set_xlim(0, 96)
ax3.set_ylim(-48, 48)
image2 = ax3.imshow(np.zeros_like(xx), extent=(0, 96, -48, 48), vmin=0, vmax=1,
                   origin='lower', cmap='viridis', alpha=0.7)
plt.colorbar(image2, ax=ax3, label='Noise level')
ax3.set_title('Noise Map (variant 2)')

# Parameters for the animation
blank_frames = 100  # Number of frames to show original points
original_frames = 200  # Number of frames to show original points
image1_frames = 400    # Total number of frames for the animation
total_frames = 600    # Total number of frames for the animation

# The animation update function
def animate(i):
    if i < blank_frames:
        # For initial frames, show only the original points
        line.set_alpha(0)
        image.set_alpha(0)
        image2.set_alpha(0)
    elif i < original_frames:
        # For initial frames, show only the original points
        line.set_alpha(1)
    elif i < image1_frames:
        # Transition to noise plot (variant 1)
        image.set_alpha(0.7)
        noisy_grid = add_uniform_noise_based_on_distance2(np.zeros_like(xx), distance_transform_m, max_noise_scale=1.0, decay_rate=(i+1-original_frames)*0.001)
        noisy_grid += add_uniform_noise_based_on_distance2(np.zeros_like(xx), distance_transform_e, max_noise_scale=1.0, decay_rate=(i+1-original_frames)*0.1)
        #noisy_grid /= 2  # Average the noise from both distance transforms
        image.set_data(noisy_grid)
        image.set_clim(0, 1)  # Ensure the color scale is between 0 and 1
    else:
        # Transition to noise plot (variant 2)
        image2.set_alpha(0.7)
        noisy_grid = add_uniform_noise_based_on_distance(np.zeros_like(xx), distance_transform_m, max_noise_scale=1.0, decay_rate=(i+1-image1_frames)*0.001)
        noisy_grid += add_uniform_noise_based_on_distance(np.zeros_like(xx), distance_transform_e, max_noise_scale=1.0, decay_rate=(i+1-image1_frames)*0.1)
        #noisy_grid /= 2  # Average the noise from both distance transforms
        image2.set_data(noisy_grid)
        image2.set_clim(0, 1)  # Ensure the color scale is between 0 and 1
    return line, image,

ani = animation.FuncAnimation(fig, animate, frames=total_frames, interval=20, blit=True)
ani.save('animation.gif', writer='pillow', fps=3*120)
plt.show()
