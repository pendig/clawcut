# 🎬 Clawcut

**Clawcut** is a modular, agentic video editing engine designed for the Clawhub AI ecosystem. It provides a "Sat-Set" (fast and efficient) alternative to heavy editing frameworks by leveraging a declarative Python wrapper for **FFmpeg**.

---

## 🚀 Why Clawcut?

- **Modular Architecture**: Easy to extend filters, presets, and engine logic.
- **Zero-Config**: No complex system dependencies. Just FFmpeg and Python.
- **Agentic-First**: Designed to be controlled by AI agents via JSON presets and CLI.
- **Fast ("Sat-Set")**: Native FFmpeg execution for high-speed rendering.

## 📂 Project Structure

- `main.py`: CLI entry point.
- `clawcut/`: Core package containing engine, filters, and utilities.
- `presets/`: Folder for layout definitions (JSON).
- `assets/branding/`: Place your `watermark.png` and `poppins-bold.ttf` here.
- `outputs/`: Default directory for rendered videos.

## 🛠 Installation

1. **Requirements**:
   - FFmpeg
   - yt-dlp
   - python-dotenv (optional)

2. **Setup**:
   ```bash
   git clone https://github.com/pendig/clawcut.git
   cd clawcut
   pip install -r requirements.txt
   ```

## 🏁 Quick Start

Render a branded Podcast Clip:
```bash
python3 main.py --url "YOUTUBE_URL" --preset podcast-clip --title "Modular Power" --watermark
```

---

## 📄 License
MIT License. Created by **Pena Digital**.
