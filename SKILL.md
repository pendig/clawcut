---
name: clawcut
description: Modular Agentic Video Editing Engine using FFmpeg. Supports JSON-driven edits, auto-scaling, and smart downloading.
---

# Clawcut Skill (v2.3.0) - Developer Guide

Clawcut is a modular, agentic video editing engine. It handles complex FFmpeg operations through a simple JSON-based "Elements" system.

## 🎨 Visual Elements

Clawcut treats visual overlays as "Elements" that can be positioned and styled dynamically.

### 1. Title Element (`title`)
The primary text overlay.
- **`title`**: The text content.
- **`font_size`**: Size in pixels.
- **`margin`**: Side padding to force text wrapping.
- **`y_offset`**: Moves the text block vertically.

### 2. Logo/Watermark Element (`watermark`)
The branding overlay (e.g., Pena Digital logo).
- **`watermark_pos`**: Shorthand positions (`top-left`, `top-right`, `top-center`, `bottom-left`, `bottom-right`, `bottom-center`).
- **`watermark_x`**: Fine-tuned X coordinate (FFmpeg syntax supported, e.g., `main_w-overlay_w-50`).
- **`watermark_y`**: Fine-tuned Y coordinate.
- **`watermark_opacity`**: Transparency from `0.0` to `1.0`.
- **`watermark_scale`**: Width of the logo in pixels (maintains aspect ratio).

## 📂 Project Structure

- `main.py`: The main CLI entry point.
- `clawcut/`:
    - `core/engine.py`: The main execution logic.
    - `core/filters.py`: **The Element Factory** (Where visual components are built).
    - `core/presets.py`: JSON and global preset manager.
- `presets/`: Directory for JSON layout definitions.
- `assets/branding/`: Directory for your custom `watermark.png` and `poppins-bold.ttf`.

## 🚀 Usage

### Position Logo at Top-Right
```bash
python3 main.py --url "URL" --watermark --wm_pos top-right --wm_opacity 0.8
```

### Manual X/Y Overrides (Element Control)
```bash
python3 main.py --url "URL" --watermark --wm_x 50 --wm_y 50
```

## ⚙️ Configuration (JSON Presets)

```json
{
  "width": 1080,
  "height": 1920,
  "watermark": true,
  "watermark_pos": "top-center",
  "watermark_y": 50,
  "watermark_opacity": 0.9,
  "description": "Standard Pendig Header Style"
}
```
