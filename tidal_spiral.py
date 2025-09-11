# 可视化绘制五角星
import turtle

def draw_star(size=200):
    t = turtle.Turtle()
    t.pensize(3)
    t.color('gold')
    t.speed(3)
    for _ in range(5):
        t.forward(size)
        t.right(144)
    turtle.done()

# 如果直接运行本文件，则绘制五角星
if __name__ == "__main__":
    draw_star()
import pygame
import pandas as pd
import math
import sys

# Load tidal data from CSV
tidal_data = pd.read_csv('tides.csv')
if 'tide' in tidal_data.columns:
    tide_values = tidal_data['tide'].tolist()
else:
    tide_values = tidal_data.iloc[:, 1].tolist()  # fallback: use second column

# Pygame setup
WIDTH, HEIGHT = 800, 800
CENTER = (WIDTH // 2, HEIGHT // 2)
BG_COLOR = (10, 10, 30)

pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('Tidal Spiral Visualization')
clock = pygame.time.Clock()

running = True
frame = 0
num_points = len(tide_values)

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    screen.fill(BG_COLOR)

    # Draw spiral
    for i in range(num_points):
        angle = 0.1 * i + frame * 0.01
        radius = 100 + 200 * (tide_values[i] / max(tide_values))
        x = CENTER[0] + int(radius * math.cos(angle))
        y = CENTER[1] + int(radius * math.sin(angle))
        color = (100 + int(155 * (tide_values[i] / max(tide_values))), 100, 255)
        pygame.draw.circle(screen, color, (x, y), 4)

    pygame.display.flip()
    frame += 1
    clock.tick(30)

pygame.quit()
sys.exit()
