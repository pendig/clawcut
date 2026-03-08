---
name: clawcut
description: Agentic Video Editing Engine using FFmpeg. Supports JSON-driven edits, auto-scaling, and smart downloading.
---

# Clawcut Skill (v1.7) - Developer Guide

Clawcut is an agentic video editing engine designed for programmatic content creation. It features a flexible **JSON Preset System**, allowing users and organizations to define their own visual standards.

## Features
- **JSON Presets**: Define custom resolutions, zoom levels, render modes, and vertical offsets.
- **Smart Clipping**: Download and trim specific segments from URLs (YouTube, TikTok, Instagram).
- **Auto-Scaling**: Intelligent "contain" and "pad" logic to maintain aspect ratios.
- **Elevated Style**: Move video positioning vertically (y-offset) to make room for captions/branding.

## Parameters

| Argument | Example | Description |
| :--- | :--- | :--- |
| `--preset` | `podcast-clip`, `reels` | Use a built-in or custom JSON preset from `presets/` folder. |
| `--zoom` | `1.25` | Override the zoom factor for this render. |
| `--mode` | `cover` / `fit` | Override render mode (Fill vs Contain). |
| `--output` | `final.mp4` | Custom output filename. |

## Creating Custom Presets
Users can create their own visual identity by adding a JSON file to the `presets/` directory.

Example `my-vibe.json`:
```json
{
  "width": 1080,
  "height": 1920,
  "mode": "fit",
  "zoom": 1.1,
  "y_offset": 200,
  "description": "My custom centered style"
}
```

## Quick Usage Examples

### 1. Using the "Podcast Clip" Preset (Elevated style)
```bash
python3 clawcut.py --url "URL" --start 01:15 --duration 90 --preset podcast-clip
```

### 2. Standard 16:9 YouTube Clip
```bash
python3 clawcut.py --url "URL" --preset youtube --output "quick_clip.mp4"
```

## Output Locations
- **Pendig Server**: `/media/clawcut/` (Accessible via Public Tunnel).
- **Local/Public Use**: Stored in the `outputs/` folder.
