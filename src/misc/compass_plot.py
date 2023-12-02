import pandas as pd
import matplotlib.pyplot as plt

# Load CSV file
filename = 'compass_readings.csv'
data = pd.read_csv(filename)

# Filter out rows where x is greater than 20 (if needed)
# filtered_data = data[data['X'] <= 20]

# Extracting data
x = data['X']
y = data['Y']
z = data['Z']  # Assuming your CSV has a Z column

# Plotting
plt.figure(figsize=(18, 6))  # Adjusted figure size for 3 subplots

# Scatterplot of X and Y
plt.subplot(1, 3, 1)  # 1 row, 3 columns, subplot 1
plt.scatter(x, y)
plt.title('Scatter Plot of X vs Y')
plt.xlabel('X')
plt.ylabel('Y')

# Scatterplot of Y and Z
plt.subplot(1, 3, 2)  # 1 row, 3 columns, subplot 2
plt.scatter(y, z)
plt.title('Scatter Plot of Y vs Z')
plt.xlabel('Y')
plt.ylabel('Z')

# Scatterplot of X and Z
plt.subplot(1, 3, 3)  # 1 row, 3 columns, subplot 3
plt.scatter(x, z)
plt.title('Scatter Plot of X vs Z')
plt.xlabel('X')
plt.ylabel('Z')

plt.tight_layout()
plt.show()

