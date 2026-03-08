# 🎬 Clawcut

**Clawcut** is a lightweight, agentic video editing engine designed for the Clawhub AI ecosystem. It provides a "Sat-Set" (fast and efficient) alternative to heavy editing frameworks by leveraging a declarative Python wrapper for **FFmpeg**.

Built specifically for AI agents and programmatic content creators who need precision, speed, and zero-configuration portability.

---

## 🚀 Why Clawcut?

Unlike other engines like `editly`, Clawcut is:
- **Zero-Config**: No complex system dependencies (libcairo, pkg-config, etc.). Just FFmpeg and Python.
- **Agentic-First**: Designed to be controlled by AI agents via JSON presets and CLI.
- **Fast ("Sat-Set")**: Native FFmpeg execution for high-speed rendering and clipping.
- **Portable**: Easy to integrate as an OpenClaw Skill or a standalone tool.

## ✨ Core Features

- **Smart URL Clipping**: Instant downloading and trimming from YouTube, TikTok, etc., using `yt-dlp`.
- **JSON Preset System**: Define your visual identity (resolution, zoom, margins) in simple JSON files.
- **Dynamic Framing**: Support for `cover` (fill) and `fit` (letterbox) modes.
- **Auto-Branding**: Integrated watermark support with opacity control and Poppins-Bold typography.
- **Elevated Layouts**: Vertical offsets (y-offset) specifically designed for Podcast and News clips.

## 🛠 Installation

1. **System Requirements**:
   - [FFmpeg](https://ffmpeg.org/download.html)
   - [yt-dlp](https://github.com/yt-dlp/yt-dlp)

2. **Clone & Setup**:
   ```bash
   git clone https://github.com/pendig/clawcut.git
   cd clawcut
   pip install -r requirements.txt
   ```

## 📂 Project Structure

- `clawcut.py`: The main execution engine.
- `presets/`: Folder for layout definitions (e.g., `reels.json`, `podcast-clip.json`).
- `assets/branding/`: Place your `watermark.png` and `poppins-bold.ttf` here.
- `SKILL.md`: Detailed developer and OpenClaw integration guide.

## 🏁 Quick Start

Render a branded Podcast Clip with a custom title:
```bash
python3 clawcut.py --url "YOUTUBE_URL" --preset podcast-clip --title "My Viral News" --watermark
```

---

## 📄 License
MIT License. Created with 🎬 and 🚀 by the **Pena Digital** team.
