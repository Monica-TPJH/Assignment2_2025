# Assignment2_2025

## Typhoon animation (`typhoon_animation.py`)

The script `typhoon_animation.py` in this project reads `hko_tropical_warnings_1956_2024.csv` and generates a blue/white gradient cyclone animation (GIF).

Key features:
- Reads the CSV (annual tropical cyclone warning totals) and maps intensity to animation parameters.
- Uses Matplotlib's `FuncAnimation` to draw a cyclone background and many raindrop particles, and saves the result as `cyclone_anim_py.gif`.

Dependencies (install in your virtualenv or system Python):
```
pip install numpy pandas matplotlib pillow
```

How to run:
```
cd Assignment2_2025
python typhoon_animation.py
```

Output: `cyclone_anim_py.gif` (saved to the project root)

Note: For higher-quality video (MP4) you can install `imageio-ffmpeg` and modify the script to use an ffmpeg writer.


## Tidal spiral (`tidal_spiral.py`)

`tidal_spiral.py` is a Pygame-based generative-art script that reads a tidal CSV (datetime,value) and renders a colorful spiral driven by the data.

Supported environment variables:
- `TIDAL_CSV` — path to the CSV file to use. If not provided the script prefers `tides.csv` or `tidal_data.csv` in the repository root.
- `RUN_FRAMES` — run loop for a limited number of frames (useful for automated captures / CI).
- `EXPORT_GIF` — filename to save an exported GIF (e.g. `preview.gif`). When set, frames are captured and a GIF is written after the run.
- `GIF_FRAMES` — optional integer limit to the number of frames saved in the GIF.
- `GIF_SCALE` — optional float to scale exported frames (e.g. `0.5` to halve width/height and reduce file size).
- `GIF_ONLY_WHEN_DONE` — if set to `1` / `true` / `yes`, frames are only captured after the main loop ends (default captures during the run).

Example commands:

Capture a 60-frame GIF at half resolution:
```zsh
RUN_FRAMES=60 EXPORT_GIF=preview_small.gif GIF_FRAMES=60 GIF_SCALE=0.5 python tidal_spiral.py
```

Quick 3-frame smoke test (no GIF):
```zsh
RUN_FRAMES=3 python tidal_spiral.py
```

Notes:
- The script falls back to a sample `tidal_data.csv` if `tides.csv` is missing; ensure your CSV has at least two columns (datetime, value).
- For better compression than animated GIFs, consider post-processing with `ffmpeg` or adding MP4 export using `imageio-ffmpeg`.

