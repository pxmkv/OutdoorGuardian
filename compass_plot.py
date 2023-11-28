import pandas as pd
import matplotlib.pyplot as plt

# Load CSV file
filename = 'readings.csv'
data = pd.read_csv(filename)

# Extracting data
x = data['X']
y = data['Y']
heading = data['Heading']

# Plotting
plt.figure(figsize=(12, 6))

# Plot X and Y
plt.subplot(1, 2, 1)
plt.plot(x, label='X')
plt.plot(y, label='Y')
plt.title('X and Y Readings')
plt.xlabel('Sample')
plt.ylabel('Reading')
plt.legend()

# Plot Heading
plt.subplot(1, 2, 2)
plt.plot(heading, label='Heading', color='green')
plt.title('Heading Over Time')
plt.xlabel('Sample')
plt.ylabel('Degrees')
plt.legend()

plt.tight_layout()
plt.show()
