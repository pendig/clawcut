---
name: clawcut
description: Agentic Video Editing Engine using FFmpeg. Supports JSON-driven edits, auto-scaling, and smart downloading.
---

# Clawcut Skill (v1.3) - Developer Guide

Clawcut is a lightweight video editing engine designed for AI Agents to programmatically generate and edit video content. It supports automated clip downloading, trimming, and multi-format rendering.

## Core Capabilities
- **Smart Clipping**: Download and trim specific segments from various social media platforms (YouTube, Instagram, TikTok, etc.).
- **Resolution Presets**: One-click formatting for social media aspect ratios (Reels, Stories, Posts, YouTube).
- **Auto-Scaling**: Intelligent "contain" and "pad" logic to prevent distorted video when switching aspect ratios.

## Parameters

| Argument | Options / Examples | Description |
| :--- | :--- | :--- |
| `--url` | `https://youtube.com/watch?v=...` | URL to download and process. |
| `--start` | `75` or `01:15` | Clip start time (seconds or HH:MM:SS). |
| `--duration` | `10` | Duration of the clip in seconds. |
| `--preset` | `reels`, `youtube`, `instagram`, `square`, `1080p`, `720p` | Standard resolution presets. |
| `--width` | `1080` | Custom video width (px). |
| `--height` | `1920` | Custom video height (px). |
| `--output` | `final_video.mp4` | Custom output filename. |

## Quick Usage Examples

### 1. Create a Reel (9:16) from YouTube
```bash
python3 clawcut.py --url "URL" --start 10 --duration 15 --preset reels --output "apple_reel.mp4"
```

### 2. Prepare a YouTube Clip (16:9)
```bash
python3 clawcut.py --url "URL" --start 60 --duration 120 --preset youtube --output "yt_clip.mp4"
```

### 3. Custom Square Post (1:1)
```bash
python3 clawcut.py --url "URL" --width 1000 --height 1000 --output "square_promo.mp4"
```

## Output Locations
- **Pendig Server (Production)**: Automatically delivered to `/media/clawcut/` (Accessible via Public Tunnel).
- **Local/Public Use**: Stored in the `outputs/` folder relative to the script location.
