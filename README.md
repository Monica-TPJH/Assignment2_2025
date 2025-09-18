# Assignment2_2025

## simple_animation.py 示例代码

```python
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.animation import FuncAnimation
import matplotlib.transforms as transforms

fig = plt.figure(figsize=(7, 7))
ax = fig.add_axes([0, 0, 1, 1], frameon=False)
ax.set_xlim(-1, 1), ax.set_xticks([])
ax.set_ylim(-1, 1), ax.set_yticks([])

# add a circle to the plot
circle1 = plt.Circle((0, 0), 0.1, color='r')
ax.add_patch(circle1)
square = [[-0.5, -0.5], [-0.5, 0.5], [0.5, 0.5], [0.5, -0.5]]

trans = (transforms.Affine2D().rotate_deg(45) + ax.transData)
square = plt.Polygon(square, fill=None, transform=trans)
ax.add_patch(square)

max_loop = 100
full_circle_radius = 1

reverse = False

def update(frame):
    global reverse
    if frame % max_loop == 0:
        reverse = not reverse
    if reverse:
        frame = frame % max_loop
    else:
        frame = max_loop - frame % max_loop

    # normalized frame value (0 to 1)
    # useful to scale things linearly
    norm_frame = frame/max_loop
    
    # set the radius of the circle based on the frame value
    circle1.set_radius(full_circle_radius*norm_frame)

    # set the color of the circle based on the frame value
    circle1.set_color(plt.cm.viridis(norm_frame))

    # create the transformation matrix adding a rotation
    transform = transforms.Affine2D().rotate_deg(90*norm_frame) + ax.transData

    # set the transformation matrix to the square
    square.set_transform(transform)
    
animation = FuncAnimation(fig, update, interval=10)
plt.show()
```

---

如需推送到 GitHub，请在终端运行：
```zsh
cd Assignment2_2025
git add README.md
git commit -m "更新 README 内容"
git push origin main
```

## Typhoon animation (typhoon_animation.py)

`typhoon_animation.py` 在本專案中用來讀取 `hko_tropical_warnings_1956_2024.csv`，並生成一個藍白色漸變的旋風動態動畫（GIF）。

主要功能：
- 讀取 CSV（每年熱帶氣旋信號總時段）並把強度用作動畫參數。
- 使用 matplotlib 的 `FuncAnimation` 繪製旋風背景與許多雨滴粒子，匯出為 `cyclone_anim_py.gif`。

依賴（請在虛擬環境或系統環境安裝）：
```
pip install numpy pandas matplotlib pillow
```

如何運行：
```
cd Assignment2_2025
python typhoon_animation.py
```

輸出：`cyclone_anim_py.gif`（保存在專案根目錄）

註：如果要更高品質的影片（MP4），可以安裝 `imageio-ffmpeg` 並修改腳本以使用 ffmpeg writer。

