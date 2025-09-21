import pygame
import math
import csv
import os
import datetime
import random
import colorsys
from PIL import Image

# Load tidal data from a CSV file (datetime, value)
def load_tidal_data(csv_path):
    data = []
    # guard: file must exist and be non-empty
    if not os.path.exists(csv_path) or os.path.getsize(csv_path) == 0:
        return data

    with open(csv_path, 'r') as f:
        reader = csv.reader(f)
        rows = list(reader)

    if not rows:
        return data

    # detect header: try parsing first row[0]; if fails, assume header present
    start_idx = 0
    def try_parse_date(s):
        # try several common formats
        for fmt in ('%Y-%m-%d %H:%M', '%Y/%m/%d %H:%M', '%Y-%m-%dT%H:%M:%S', '%Y-%m-%d'):
            try:
                return datetime.datetime.strptime(s, fmt)
            except Exception:
                continue
        try:
            return datetime.datetime.fromisoformat(s)
        except Exception:
            return None

    if try_parse_date(rows[0][0]) is None:
        start_idx = 1

    for row in rows[start_idx:]:
        if not row:
            continue
        try:
            dt = try_parse_date(row[0])
            if dt is None:
                continue
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
        # rainbow color along the spiral (smooth)
        def rainbow(f, shift=0.0):
            # f in [0,1] -> RGB using HSV for stronger/smoother rainbow
            h = (f + shift) % 1.0
            s = 0.95
            v = 0.98
            r, g, b = colorsys.hsv_to_rgb(h, s, v)
            return (int(r*255), int(g*255), int(b*255))

        # add a slight time-based hue shift for animation smoothness
        color = rainbow(i / max(1, n-1), shift=(t*0.02))
        points.append((x, y))
        if i > 0:
            # line width based on normalized data value
            try:
                width_val = int(1 + 5 * (value - min_value) / (max_value - min_value + 1e-6))
            except Exception:
                width_val = 2
            width_val = max(1, min(12, width_val))
            # draw a thicker anti-aliased line by using draw.line and endpoint circles
            # draw a slightly-smoothed segment by interpolating a few subsegments
            seg_steps = 3
            x0, y0 = points[i-1]
            x1, y1 = points[i]
            for s in range(seg_steps):
                fa = s / seg_steps
                fb = (s+1) / seg_steps
                ax = x0 * (1-fa) + x1 * fa
                ay = y0 * (1-fa) + y1 * fa
                bx = x0 * (1-fb) + x1 * fb
                by = y0 * (1-fb) + y1 * fb
                subf = (i-1 + fa) / max(1, n-1)
                subcol = rainbow(subf)
                subw = max(1, int(width_val * (0.8 + 0.4*(s/seg_steps))))
                try:
                    pygame.draw.line(screen, subcol, (ax, ay), (bx, by), subw)
                except Exception:
                    pass

    # magical glow: draw soft circles with additive blending on a separate surface
        try:
            # draw glow as wide semi-transparent lines between sampled points (no circles)
            glow = pygame.Surface((width, height), flags=pygame.SRCALPHA)
            glow.fill((0,0,0,0))
            step = max(1, len(points)//80)
            for j in range(0, len(points)-step, step):
                a = points[j]
                b = points[min(j+step, len(points)-1)]
                val = data[j][1]
                gw = int(6 + 12 * ((val - min_value) / (max_value - min_value + 1e-6)))
                # rainbow-tinted glow with low alpha
                gcol = rainbow(j / max(1, len(points)-1)) + (28,)
                try:
                    pygame.draw.line(glow, gcol, a, b, gw)
                except Exception:
                    pass
            screen.blit(glow, (0,0), special_flags=pygame.BLEND_ADD)
        except Exception:
            pass

    # small spark particles
    # we will generate a few transient particles based on t
    for j in range(12):
        ang = t*0.5 + j * (2*math.pi/12)
        r_j = max_radius * 0.6 * (0.5 + 0.5*math.sin(t*0.3 + j))
        sx = cx + r_j * math.cos(ang + 0.2*math.sin(t + j))
        sy = cy + r_j * math.sin(ang + 0.2*math.sin(t + j))
        sw = 2 + int(3 * (0.5 + 0.5*math.sin(t + j)))
        # draw small rectangular spark (no circle)
        try:
            rect = pygame.Rect(int(sx-sw//2), int(sy-sw//2), sw, max(1, sw//2))
            col = (200, 220, 255)
            surf = pygame.Surface((rect.w, rect.h), flags=pygame.SRCALPHA)
            surf.fill(col + (150,))
            screen.blit(surf, rect.topleft, special_flags=pygame.BLEND_ADD)
        except Exception:
            pass

# Main animation loop
def main():
    pygame.init()
    width, height = 800, 800
    screen = pygame.display.set_mode((width, height))
    pygame.display.set_caption('Tidal Spiral Generative Art')
    clock = pygame.time.Clock()
    # 自动检测数据文件
    # Prefer an env var, but only if it points to a non-empty file
    csv_path = os.getenv('TIDAL_CSV')
    if csv_path and (not os.path.exists(csv_path) or os.path.getsize(csv_path) == 0):
        csv_path = None

    if not csv_path:
        # prefer non-empty candidates
        for cand in ('tides.csv', 'tidal_data.csv'):
            if os.path.exists(cand) and os.path.getsize(cand) > 0:
                csv_path = cand
                break
        # fallback to any existing file (even if empty) so we can show better message
        if not csv_path:
            if os.path.exists('tidal_data.csv'):
                csv_path = 'tidal_data.csv'
            elif os.path.exists('tides.csv'):
                csv_path = 'tides.csv'
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
    run_frames = os.getenv('RUN_FRAMES')
    if run_frames:
        try:
            run_frames = int(run_frames)
        except Exception:
            run_frames = None
    frame_count = 0
    # GIF export options
    export_gif = os.getenv('EXPORT_GIF')  # provide a filename to export, e.g. preview.gif
    gif_frames = None
    gif_only_when_done = False
    frames = []
    if export_gif:
        try:
            gf = os.getenv('GIF_FRAMES')
            if gf:
                gif_frames = int(gf)
        except Exception:
            gif_frames = None
        try:
            if os.getenv('GIF_ONLY_WHEN_DONE', '').lower() in ('1', 'true', 'yes'):
                gif_only_when_done = True
        except Exception:
            gif_only_when_done = False
        # optional scale (float <1 reduce size, >1 enlarge)
        gif_scale = None
        try:
            gs = os.getenv('GIF_SCALE')
            if gs:
                gif_scale = float(gs)
        except Exception:
            gif_scale = None
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        screen.fill((10, 10, 30))
        draw_spiral(screen, data, t, width, height)
        pygame.display.flip()
        # optional GIF capture
        if export_gif and (not gif_only_when_done):
            try:
                raw = pygame.image.tostring(screen, 'RGB')
                img = Image.frombytes('RGB', (width, height), raw)
                img = img.transpose(Image.FLIP_TOP_BOTTOM)
                frames.append(img)
            except Exception:
                pass
        t += 0.01
        clock.tick(60)
        frame_count += 1
        if run_frames and frame_count >= run_frames:
            running = False
    pygame.quit()
    # if exporting GIF, save collected frames (or render final frames if none)
    if export_gif:
        try:
            if not frames:
                print('No frames captured for GIF; skipping save.')
            else:
                # limit frames to requested GIF_FRAMES if set
                if gif_frames and len(frames) > gif_frames:
                    frames = frames[:gif_frames]
                # optionally scale frames to reduce final GIF resolution
                if gif_scale and gif_scale > 0 and gif_scale != 1.0:
                    try:
                        new_frames = []
                        for fr in frames:
                            nw = max(1, int(fr.width * gif_scale))
                            nh = max(1, int(fr.height * gif_scale))
                            new_frames.append(fr.resize((nw, nh), Image.LANCZOS))
                        frames = new_frames
                    except Exception:
                        pass
                # save as GIF
                out_path = export_gif
                frames[0].save(out_path, save_all=True, append_images=frames[1:], duration=int(1000/60), loop=0, optimize=False)
                print(f'Saved GIF: {out_path} ({len(frames)} frames)')
        except Exception as e:
            print('Failed to save GIF:', e)

if __name__ == '__main__':
    main()
