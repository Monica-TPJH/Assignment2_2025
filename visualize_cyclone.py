import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.colors import LinearSegmentedColormap

# Read CSV
csv_path = 'hko_tropical_warnings_1956_2024.csv'
df = pd.read_csv(csv_path)

# We'll compute an "intensity" per year. Use total hours as proxy.
intensity = df['TotalHours'].values
# Normalize to 0..1
norm = (intensity - intensity.min()) / (intensity.max() - intensity.min())

# Create a logarithmic spiral influenced by the number of years
n_years = len(df)

# Parameters for the spiral
turns = 6  # number of spiral turns
points_per_turn = 500
theta = np.linspace(0, 2*np.pi*turns, points_per_turn*turns)

# radius grows with theta
a = 0.5
b = 0.2
r = a * np.exp(b * theta)

# Create color gradient blue->white
colors = [(0.0, '#003f5c'), (0.5, '#2f4b7c'), (1.0, '#ffffff')]
cmap = LinearSegmentedColormap.from_list('blue_white', [c for _,c in colors])

# Create figure
fig, ax = plt.subplots(figsize=(8,8), facecolor='white')
ax.set_facecolor('white')

# Plot spiral as many segments, modulating linewidth and color by mapped yearly intensities
# We'll map each year to an interval of theta
per_year = len(theta) // n_years

for i in range(n_years):
    start = i * per_year
    end = start + per_year if i < n_years-1 else len(theta)
    th_seg = theta[start:end]
    r_seg = r[start:end]
    x = r_seg * np.cos(th_seg)
    y = r_seg * np.sin(th_seg)
    val = norm[i]
    # color and linewidth
    color = cmap(val)
    lw = 1 + 4*val
    ax.plot(x, y, color=color, linewidth=lw, alpha=0.9)

# Add an eye (white circle)
ax.add_artist(plt.Circle((0,0), 0.4, color='white', zorder=10))
ax.set_aspect('equal')
ax.axis('off')
plt.tight_layout()
out_path = 'cyclone_visualization.png'
plt.savefig(out_path, dpi=300, bbox_inches='tight', facecolor=fig.get_facecolor())
print('Saved', out_path)
