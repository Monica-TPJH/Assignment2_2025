# Assignment2_2025

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

