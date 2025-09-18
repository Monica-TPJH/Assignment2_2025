import pygame
import math
import csv
import os
import datetime

# Load tidal data from a CSV file (datetime, value)
def load_tidal_data(csv_path):
    data = []
    with open(csv_path, 'r') as f:
        reader = csv.reader(f)
        next(reader)  # skip header if present
        for row in reader:
            try:
                dt = datetime.datetime.strptime(row[0], '%Y-%m-%d %H:%M')
                value = float(row[1])
                data.append((dt, value))
            except Exception:
                continue
    return data

# Spiral drawing function
def draw_spiral(screen, data, t, width, height):
    cx, cy = width // 2, height // 2
    n = len(data)
    max_radius = min(cx, cy) - 40
    values = [v for _, v in data]
    min_value = min(values)
    max_value = max(values)
    scale = max_radius / (n if n > 0 else 1)
    points = []
    petals = 8  # 花瓣数量，可调整
    for i, (dt, value) in enumerate(data):
        angle = 2 * math.pi * (i / n) + t
        # 花瓣调制：正弦函数叠加在主半径上
        base_radius = scale * i
        petal_wave = 30 * math.sin(petals * angle + t)
        delta = (value - min_value) / (max_value - min_value + 1e-6) * 20
        radius = base_radius + petal_wave + delta
        x = cx + radius * math.cos(angle)
        y = cy + radius * math.sin(angle)
        # 花瓣渐变色
        color = (int(180 + 75 * math.sin(petals * angle)), int(100 + 155 * (i / n)), 200)
        points.append((x, y))
        if i > 0:
            pygame.draw.aaline(screen, color, points[i-1], points[i], 2)

# Main animation loop
def main():
    pygame.init()
    width, height = 800, 800
    screen = pygame.display.set_mode((width, height))
    pygame.display.set_caption('Tidal Spiral Generative Art')
    clock = pygame.time.Clock()
    # 自动检测数据文件
    csv_path = os.getenv('TIDAL_CSV')
    if not csv_path:
        if os.path.exists('tides.csv'):
            csv_path = 'tides.csv'
        elif os.path.exists('tidal_data.csv'):
            csv_path = 'tidal_data.csv'
        else:
            print("未找到 tides.csv 或 tidal_data.csv，请检查数据文件！")
            return
    data = load_tidal_data(csv_path)
    print(f"使用数据文件: {csv_path}")
    print(f"Loaded {len(data)} data points.")
    if len(data) == 0:
        print("警告：没有读取到任何潮汐数据，请检查 CSV 文件路径和格式！")
        return
    print(f"前10条数据: {data[:10]}")
    values = [v for _, v in data]
    min_value = min(values)
    max_value = max(values)
    print(f"潮汐最小值: {min_value}, 最大值: {max_value}")
    if max_value - min_value < 1e-3:
        print("警告：潮汐数据波动极小，图像可能不明显！")
    t = 0
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        screen.fill((10, 10, 30))
        draw_spiral(screen, data, t, width, height)
        pygame.display.flip()
        t += 0.01
        clock.tick(60)
    pygame.quit()

if __name__ == '__main__':
    main()
