import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation, PillowWriter
import os

# Auto-detect CSV file location
def find_csv_file():
    possible_paths = [
        'hko_tropical_warnings_1956_2024.csv',  # Current directory
        'HK_Typhoon_animation/hko_tropical_warnings_1956_2024.csv',  # Parent/child
        '../hko_tropical_warnings_1956_2024.csv',  # Parent directory
    ]
    
    for path in possible_paths:
        if os.path.exists(path):
            print(f"Found CSV file at: {path}")
            return path
    
    raise FileNotFoundError("Could not find hko_tropical_warnings_1956_2024.csv")

# Read data
csv_path = find_csv_file()
df = pd.read_csv(csv_path)
intensity = df['TotalHours'].values
norm = (intensity - intensity.min()) / (intensity.max() - intensity.min())

# Animation params
W, H = 8, 8  # figure size in inches
dpi = 100
fig, ax = plt.subplots(figsize=(W, H), dpi=dpi)
ax.set_facecolor('white')
ax.axis('off')

# --- Universe-like background (radial gradient + nebula blobs + starfield)
def create_universe_background(xmin=-400, xmax=400, ymin=-400, ymax=400, res=800, seed=42):
    import numpy as _np
    _np.random.seed(seed)
    xs = _np.linspace(xmin, xmax, res)
    ys = _np.linspace(ymin, ymax, res)
    X, Y = _np.meshgrid(xs, ys)
    R = _np.sqrt((X/ (xmax-xmin))**2 + (Y/ (ymax-ymin))**2)

    # base radial gradient (darker at edges)
    base = 0.08 + 0.6 * _np.exp(-3 * R)

    # add a few colored nebula blobs
    neb = _np.zeros_like(base)
    for cx, cy, amp, sigma, hue in [(-150, -50, 0.6, 120, 0.55), (120, 80, 0.45, 160, 0.65), (40, -120, 0.35, 90, 0.48)]:
        neb += amp * _np.exp(-((X-cx)**2 + (Y-cy)**2) / (2*sigma**2)) * (0.5 + 0.5*hue)

    img = _np.zeros((res, res, 3), dtype=_np.float32)
    # base color: deep blue -> purple tint
    img[..., 0] = base * 0.02 + neb * 0.05  # red channel small
    img[..., 1] = base * 0.12 + neb * 0.12  # green
    img[..., 2] = base * 0.25 + neb * 0.35  # blue

    # add subtle bright core
    img += _np.expand_dims(0.15 * _np.exp(-R*6), axis=2)

    # clip
    img = _np.clip(img, 0, 1)
    return img

# draw background image and a starfield
bg_img = create_universe_background(res=900)
ax.imshow(bg_img, extent=[-400,400,-400,400], origin='lower', zorder=0)

# starfield on zorder 1
rng = np.random.RandomState(0)
num_stars = 800
sx = rng.uniform(-380, 380, num_stars)
sy = rng.uniform(-380, 380, num_stars)
ss = rng.uniform(0.3, 2.5, num_stars)
alphas = rng.uniform(0.3, 1.0, num_stars)
star_colors = ['#ffffff'] * num_stars
ax.scatter(sx, sy, s=ss, c=star_colors, alpha=alphas, linewidths=0, zorder=1)


# Raindrops parameters
raindrops = 300
theta = np.linspace(0, 4*np.pi, raindrops)
r_base = np.linspace(20, 350, raindrops)
phases = np.random.RandomState(1).rand(raindrops) * 2*np.pi
speeds = 0.5 + np.random.RandomState(2).rand(raindrops) * 2.0
sizes = 2 + np.random.RandomState(3).rand(raindrops)*6

# Convert to axes coordinates
center = (0.5, 0.5)

# Create scatter for raindrops
xs = np.zeros(raindrops)
ys = np.zeros(raindrops)
sc = ax.scatter(xs, ys, s=sizes**2, c=np.zeros((raindrops,4)))

# Create spiral background as multiple lines
lines = []
for layer in range(6):
    ln, = ax.plot([], [], lw=8 - layer, alpha=0.25)
    lines.append(ln)

ax.set_xlim(-400, 400)
ax.set_ylim(-400, 400)
ax.set_aspect('equal')

# color blend function
def color_blend(t):
    # t in [0,1]
    t = np.clip(t, 0, 1)
    if t < 0.5:
        a = t/0.5
        c1 = np.array([0x00,0x3f,0x5c]) / 255.0
        c2 = np.array([0x2f,0x4b,0x7c]) / 255.0
        c = (1-a)*c1 + a*c2
    else:
        a = (t-0.5)/0.5
        c1 = np.array([0x2f,0x4b,0x7c]) / 255.0
        c2 = np.array([1.0,1.0,1.0])
        c = (1-a)*c1 + a*c2
    return tuple(c)

# Precompute colors for raindrops based on position fraction
tvals = np.linspace(0,1,raindrops)
base_colors = np.array([color_blend(t) for t in tvals])

frames = 80

# Update function
def update(frame):
    th = theta + frame*0.12*speeds
    r = r_base + 30*np.sin(0.5*th + phases) + frame*1.0
    x = r * np.cos(th)
    y = r * np.sin(th)
    sc.set_offsets(np.column_stack([x, y]))
    # set sizes and colors
    # Ensure positive values before power operation to avoid RuntimeWarning
    size_multiplier = np.abs(0.6 + 0.8*np.sin(0.1*frame + phases))
    sizes_now = (sizes * size_multiplier)**1.6
    sc.set_sizes(sizes_now)
    # alpha modulated
    alphas = 0.6 + 0.4*np.sin(0.1*frame + phases)
    colors = np.concatenate([base_colors, alphas[:,None]], axis=1)
    sc.set_facecolors(colors)
    sc.set_edgecolors(colors)

    # update spiral layers
    for li, ln in enumerate(lines):
        th2 = np.linspace(0, 2*np.pi*(2+li*0.8), 800)
        r2 = 20 + (li*50) * np.exp(0.15*th2) * 0.002
        x2 = r2 * np.cos(th2 + frame*0.03*(li+1))
        y2 = r2 * np.sin(th2 + frame*0.03*(li+1))
        ln.set_data(x2, y2)
        ln.set_color(color_blend(0.2 + li*0.12))
        ln.set_alpha(0.25+0.05*li)
    return [sc] + lines

anim = FuncAnimation(fig, update, frames=frames, interval=40, blit=True)

# Save to GIF using PillowWriter
out_path = 'cyclone_anim_py.gif'
writer = PillowWriter(fps=25)
anim.save(out_path, writer=writer)
print('Saved', out_path)

# Optionally show
if __name__ == '__main__':
    plt.show()
