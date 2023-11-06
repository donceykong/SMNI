import matplotlib.pyplot as plt

# Initialize lists to hold the x and y values
x_values = []
y_values = []

# Open the file for reading
with open('roadpoints.txt', 'r') as file:
    # Read each line in the file
    for line in file:
        # Split the line into x and y values based on space
        x, y, z = line.split()
        # Append the x and y values to their respective lists
        x_values.append(float(x))
        y_values.append(float(y))

# Plot the points
plt.scatter(x_values, y_values)
plt.xlabel('X')
plt.ylabel('Y')
plt.title('Plot of X and Y Points')
plt.show()

# Initialize lists to hold the x and y values
x_values = []
y_values = []

# Open the file for reading
with open('roadpoints_voxelized.txt', 'r') as file:
    # Read each line in the file
    for line in file:
        # Split the line into x and y values based on space
        x, y = line.split()
        # Append the x and y values to their respective lists
        x_values.append(float(x))
        y_values.append(float(y))

# Plot the points
plt.scatter(x_values, y_values)
plt.xlabel('X')
plt.ylabel('Y')
plt.title('Plot of X and Y Points')
plt.show()