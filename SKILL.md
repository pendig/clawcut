---
name: clawcut
description: Agentic Video Editing Engine using FFmpeg. Supports JSON-driven edits, auto-scaling, and smart downloading.
---

# Clawcut Skill (v1.3)

Clawcut adalah engine pengeditan video yang dirancang untuk AI Agent. Mendukung pengolahan video dari URL atau file lokal dengan pengaturan resolusi otomatis.

## Fitur Utama
- **Smart Scaling**: Otomatis menyesuaikan video ke berbagai aspek rasio (Reels, YouTube, Instagram).
- **Resolution Presets**: Tersedia preset standar sosial media.
- **Deep Clipping**: Download dan potong bagian spesifik dari URL video.

## Parameter Resolusi
Gunakan argumen berikut untuk mengatur kualitas dan format output:

| Argument | Options / Example | Description |
| :--- | :--- | :--- |
| `--preset` | `reels`, `youtube`, `instagram`, `square`, `1080p`, `720p` | Preset resolusi standar |
| `--width` | `1080`, `1920`, etc | Custom lebar video (px) |
| `--height` | `1920`, `1080`, etc | Custom tinggi video (px) |

## Contoh Penggunaan

### 1. Render untuk Reels (9:16)
```bash
python3 clawcut.py --url "URL" --start 10 --duration 15 --preset reels --output "reels_pendig.mp4"
```

### 2. Render untuk YouTube (16:9)
```bash
python3 clawcut.py --url "URL" --start 60 --duration 120 --preset youtube --output "yt_pendig.mp4"
```

### 3. Custom Resolution
```bash
python3 clawcut.py --url "URL" --width 1000 --height 1000 --output "custom_square.mp4"
```

## Lokasi Output
- **Pena Digital Server**: `/media/clawcut/` (Accessible via Public Tunnel)
- **General/Public**: `/outputs/` (Local workspace)
