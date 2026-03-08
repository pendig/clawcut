---
name: clawcut
description: Modular Agentic Video Editing Engine using FFmpeg. Supports JSON-driven edits, auto-scaling, and smart downloading.
---

# Clawcut Skill (v2.2.0) - Developer Guide

Clawcut is a modular, agentic video editing engine built as a declarative Python wrapper for **FFmpeg**. It was designed specifically as a "Sat-Set" (fast/efficient) alternative to heavier editing frameworks like `editly`, offering zero-configuration and high portability for AI agents.

## 🛠 System Dependencies

To use Clawcut, the following libraries must be installed on your system:

1.  **FFmpeg**: The core video processing engine.
2.  **yt-dlp**: For downloading and clipping videos from URLs.
3.  **python-dotenv**: For environment variable support.

## 📂 Structure

- `main.py`: The main CLI entry point.
- `clawcut/`:
    - `core/engine.py`: The main execution logic.
    - `core/filters.py`: FFmpeg filter construction factory.
    - `core/presets.py`: JSON and global preset manager.
    - `utils/helpers.py`: System verification and time utilities.
- `presets/`: Directory for JSON layout definitions.
- `assets/branding/`: Directory for your custom `watermark.png` and `poppins-bold.ttf`.

## ⚙️ Environment Configuration

Clawcut supports custom output directories via environment variables (e.g., in a `.env` file).

1.  Copy `.env.example` to `.env`.
2.  Set `CLAWCUT_OUTPUT_DIR` to your desired final media storage location.

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
python3 main.py --url "https://youtube.com/..." --preset reels
```

### 2. Branded Render with Title
```bash
python3 main.py --url "URL" --preset podcast-clip --title "My Awesome Headline" --watermark
```

## 📝 Developer Notes
- **Modular Filters**: Add new FFmpeg filters in `clawcut/core/filters.py`.
- **Engine Logic**: Modify core execution flow in `clawcut/core/engine.py`.
- **Font/Watermark**: Assets are managed via the `FilterFactory` class.
