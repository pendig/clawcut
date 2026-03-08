---
name: clawcut
description: Agentic Video Editing Engine using FFmpeg. Supports JSON-driven edits, auto-scaling, and smart downloading.
---

# Clawcut Skill (v2.1.1) - Developer Guide

Clawcut is a lightweight, agentic video editing engine built as a declarative Python wrapper for **FFmpeg**. It was designed specifically as a "Sat-Set" (fast/efficient) alternative to heavier editing frameworks like `editly`, offering zero-configuration and high portability for AI agents.

## 🛠 System Dependencies

To use Clawcut, the following libraries must be installed on your system:

1.  **FFmpeg**: The core video processing engine.
    *   Ubuntu/Debian: `sudo apt update && sudo apt install ffmpeg`
    *   MacOS: `brew install ffmpeg`
2.  **yt-dlp**: For downloading and clipping videos from URLs.
    *   Install via pip: `pip install yt-dlp`

## 📂 Structure

- `clawcut.py`: The main execution engine.
- `requirements.txt`: Python dependencies.
- `presets/`: Directory for JSON layout definitions.
- `assets/branding/`: Directory for your custom `watermark.png` and `poppins-bold.ttf`.

## ⚙️ Configuration (JSON Presets)

Users can define their own visual identity by adding a JSON file to the `presets/` directory.

Example `my-style.json`:
```json
{
  "width": 1080,
  "height": 1920,
  "mode": "fit",
  "zoom": 1.25,
  "y_offset": 300,
  "margin": 70,
  "watermark": true,
  "watermark_opacity": 0.75,
  "description": "My professional podcast style"
}
```

## 🚀 Usage

### 1. Simple Clip
```bash
python3 clawcut.py --url "https://youtube.com/..." --preset reels
```

### 2. Branded Render with Title
```bash
python3 clawcut.py --url "URL" --preset podcast-clip --title "My Awesome Headline" --watermark
```

## 📝 Developer Notes
- **Font Support**: Clawcut looks for a font at `assets/branding/poppins-bold.ttf`. If missing, titles will be skipped.
- **Watermark**: Looks for `assets/branding/watermark.png`. Supports opacity and custom X/Y positioning.
- **Auto-Scaling**: Use `mode: "cover"` to fill the screen or `mode: "fit"` for a centered letterboxed look.
