import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation, PillowWriter

# We'll implement 6 simple variants derived from simple_animation.py
# Each variant will save a GIF: variant1.gif ... variant6.gif

def variant_pulsing_circle(out_path='variant1.gif'):
    fig, ax = plt.subplots(figsize=(4,4))
    ax.set_xlim(-1,1); ax.set_ylim(-1,1); ax.axis('off')
    circle = plt.Circle((0,0), 0.1, color='navy')
    ax.add_patch(circle)
    def update(f):
        r = 0.05 + 0.95 * (0.5*(1+np.sin(2*np.pi*f/60)))
        circle.set_radius(r)
        circle.set_color(plt.cm.Blues(f%60/60))
        return (circle,)
    anim = FuncAnimation(fig, update, frames=120, interval=30)
    anim.save(out_path, writer=PillowWriter(fps=25))
    plt.close(fig)

def variant_rotating_square(out_path='variant2.gif'):
    fig, ax = plt.subplots(figsize=(4,4))
    ax.set_xlim(-1,1); ax.set_ylim(-1,1); ax.axis('off')
    square = plt.Polygon([[-0.5,-0.5],[-0.5,0.5],[0.5,0.5],[0.5,-0.5]], fill=None, edgecolor='teal')
    ax.add_patch(square)
    import matplotlib.transforms as transforms
    def update(f):
        trans = transforms.Affine2D().rotate_deg(3*f) + ax.transData
        square.set_transform(trans)
        return (square,)
    anim = FuncAnimation(fig, update, frames=120, interval=30)
    anim.save(out_path, writer=PillowWriter(fps=25))
    plt.close(fig)

def variant_expanding_rings(out_path='variant3.gif'):
    fig, ax = plt.subplots(figsize=(4,4))
    ax.set_xlim(-1,1); ax.set_ylim(-1,1); ax.axis('off')
    circles = [plt.Circle((0,0), 0.1+i*0.15, fill=False, lw=2, color='royalblue', alpha=0.6) for i in range(6)]
    for c in circles: ax.add_patch(c)
    def update(f):
        for i,c in enumerate(circles):
            c.set_radius(((f/10.0)+i)%3*0.33+0.05)
            c.set_alpha(0.2+0.8*((i+f/10)%3/3))
        return circles
    anim = FuncAnimation(fig, update, frames=120, interval=30)
    anim.save(out_path, writer=PillowWriter(fps=25))
    plt.close(fig)

def variant_spinning_petals(out_path='variant4.gif'):
    fig, ax = plt.subplots(figsize=(4,4))
    ax.set_xlim(-1,1); ax.set_ylim(-1,1); ax.axis('off')
    petals = []
    for i in range(8):
        pet = plt.Polygon([[0,0],[0.1,0.2],[0.2,0.05]], color=plt.cm.Blues(i/8), alpha=0.8)
        petals.append(pet)
        ax.add_patch(pet)
    import matplotlib.transforms as transforms
    def update(f):
        for i,p in enumerate(petals):
            trans = transforms.Affine2D().rotate_deg(f*2 + i*45) + ax.transData
            p.set_transform(trans)
        return petals
    anim = FuncAnimation(fig, update, frames=120, interval=30)
    anim.save(out_path, writer=PillowWriter(fps=25))
    plt.close(fig)

def variant_orbiting_dots(out_path='variant5.gif'):
    fig, ax = plt.subplots(figsize=(4,4))
    ax.set_xlim(-1,1); ax.set_ylim(-1,1); ax.axis('off')
    n=40
    sc = ax.scatter(np.zeros(n), np.zeros(n), s=20, c=[plt.cm.Blues(i/n) for i in range(n)])
    def update(f):
        angles = np.linspace(0,2*np.pi,n) + f*0.1
        r = 0.2 + 0.6*np.abs(np.sin(angles*3 + f*0.05))
        x = r*np.cos(angles)
        y = r*np.sin(angles)
        sc.set_offsets(np.column_stack([x,y]))
        return (sc,)
    anim = FuncAnimation(fig, update, frames=120, interval=30)
    anim.save(out_path, writer=PillowWriter(fps=25))
    plt.close(fig)

def variant_bouncing_shapes(out_path='variant6.gif'):
    fig, ax = plt.subplots(figsize=(4,4))
    ax.set_xlim(-1,1); ax.set_ylim(-1,1); ax.axis('off')
    square = plt.Polygon([[-0.1,-0.1],[-0.1,0.1],[0.1,0.1],[0.1,-0.1]], color='navy')
    circ = plt.Circle((0,0.5), 0.08, color='lightblue')
    ax.add_patch(square); ax.add_patch(circ)
    def update(f):
        y = 0.5 * np.abs(np.sin(f*0.08))
        circ.center = (0, y)
        dx = 0.6*np.sin(f*0.05)
        trans = plt.matplotlib.transforms.Affine2D().translate(dx, 0) + ax.transData
        square.set_transform(trans)
        return (square, circ)
    anim = FuncAnimation(fig, update, frames=120, interval=30)
    anim.save(out_path, writer=PillowWriter(fps=25))
    plt.close(fig)

if __name__ == '__main__':
    variant_pulsing_circle('variant1.gif')
    variant_rotating_square('variant2.gif')
    variant_expanding_rings('variant3.gif')
    variant_spinning_petals('variant4.gif')
    variant_orbiting_dots('variant5.gif')
    variant_bouncing_shapes('variant6.gif')
    print('Generated 6 variant GIFs')
