import numpy as np
import pandas as pd
from PIL import Image, ImageDraw, ImageFilter
import math

# Load data
df = pd.read_csv('hko_tropical_warnings_1956_2024.csv')
intensity = df['TotalHours'].values
norm = (intensity - intensity.min()) / (intensity.max() - intensity.min())

# Animation parameters
W = H = 800
center = (W//2, H//2)
frames = 80
raindrops = 300  # number of raindrops

# Precompute spiral positions for raindrops
theta = np.linspace(0, 4*math.pi, raindrops)
r_base = np.linspace(20, 350, raindrops)

# Each raindrop has random phase/speed
np.random.seed(1)
phases = np.random.rand(raindrops) * 2*math.pi
speeds = 0.5 + np.random.rand(raindrops) * 2.0
sizes = 2 + np.random.rand(raindrops)*6

# Color gradient function (blue -> white)
def color_blend(t):
    # t in [0,1]
    # deep blue #003f5c -> #2f4b7c -> white
    if t < 0.5:
        a = t/0.5
        c1 = np.array([0x00,0x3f,0x5c])
        c2 = np.array([0x2f,0x4b,0x7c])
        c = (1-a)*c1 + a*c2
    else:
        a = (t-0.5)/0.5
        c1 = np.array([0x2f,0x4b,0x7c])
        c2 = np.array([0xff,0xff,0xff])
        c = (1-a)*c1 + a*c2
    return tuple(c.astype(int))

# Build frames
images = []
for f in range(frames):
    im = Image.new('RGBA', (W,H), (255,255,255,255))
    draw = ImageDraw.Draw(im, 'RGBA')

    # Draw swirling translucent background bands (the spiral body)
    for layer in range(8):
        # map layer to intensity color
        t = layer/7.0
        col = color_blend(0.2 + 0.8*t)
        alpha = int(40 + 60*t)
        # draw arc segments as filled polygons
        for i in range(0, 360, 6):
            ang1 = math.radians(i + (f*1.5* (layer+1)))
            ang2 = math.radians(i+6 + (f*1.5* (layer+1)))
            r1 = 30 + layer*30
            r2 = r1 + 200
            x1 = center[0] + r1*math.cos(ang1)
            y1 = center[1] + r1*math.sin(ang1)
            x2 = center[0] + r1*math.cos(ang2)
            y2 = center[1] + r1*math.sin(ang2)
            x3 = center[0] + r2*math.cos(ang2)
            y3 = center[1] + r2*math.sin(ang2)
            x4 = center[0] + r2*math.cos(ang1)
            y4 = center[1] + r2*math.sin(ang1)
            draw.polygon([(x1,y1),(x2,y2),(x3,y3),(x4,y4)], fill=(col[0],col[1],col[2],alpha))

    # Draw raindrops along spiral
    for i in range(raindrops):
        t = (i/raindrops)
        th = theta[i] + f*0.1*speeds[i]
        r = r_base[i] + 50*math.sin(0.5*th + phases[i]) + f*1.0
        x = center[0] + r*math.cos(th)
        y = center[1] + r*math.sin(th)
        s = sizes[i]
        # raindrop shape: rotated ellipse+triangle tail
        drop = Image.new('RGBA', (int(4*s), int(4*s)), (0,0,0,0))
        ddraw = ImageDraw.Draw(drop)
        # body
        ddraw.ellipse((s*0.5,0, s*3.5, s*3.5), fill=color_blend(t)+ (200,))
        # tail triangle
        ddraw.polygon([(s*2, s*3.5),(s*1.1, s*4.5),(s*2.9, s*4.5)], fill=color_blend(t)+ (160,))
        # rotate slightly according to motion
        angle = math.degrees(math.atan2(y-center[1], x-center[0])) + 90
        drop = drop.rotate(angle, resample=Image.BICUBIC, expand=True)
        # composite
        im.paste(drop, (int(x - drop.width/2), int(y - drop.height/2)), drop)

    # Add eye and brighten center
    draw.ellipse((center[0]-40, center[1]-40, center[0]+40, center[1]+40), fill=(255,255,255,255))

    # Slight blur to smooth
    im = im.filter(ImageFilter.GaussianBlur(radius=0.8))
    images.append(im.convert('P'))

# Save as animated GIF
gif_path = 'cyclone_animation.gif'
images[0].save(gif_path, save_all=True, append_images=images[1:], duration=40, loop=0, optimize=True)
print('Saved', gif_path)
