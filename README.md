# Clawcut - Agentic Video Editing Engine

Clawcut is a lightweight, declarative video editing engine built on top of FFmpeg. Designed specifically for AI Agents, it provides a "Sat-Set" (fast and efficient) workflow for programmatic video creation without the heavy dependencies of modern NLE frameworks.

## Core Philosophies
- **Agent-First**: Easy for AI models to generate edit instructions (JSON-driven).
- **Native Power**: Leverages FFmpeg for maximum stability and rendering speed.
- **Zero-Config**: Works anywhere FFmpeg is installed, with smart path detection for local and cloud environments.

## Features
- **Smart Clipping**: Download and cut specific segments from URLs (YouTube, TikTok, Instagram) using integrated `yt-dlp`.
- **Dynamic Resolution**: Automatic scaling and padding for Reels (9:16), YouTube (16:9), Instagram (4:5), and Square (1:1).
- **Smooth Transitions**: Built-in support for FFmpeg `xfade` filters (Wipe, Fade, Circle, etc.).
- **Auto-Branding**: Programmatic overlay of logos, watermarks, and high-quality typography (Poppins).

## Project Structure
- `clawcut.py`: The core engine wrapper.
- `SKILL.md`: Comprehensive usage guide for AI Agents and Developers.
- `TODO.md`: Internal roadmap and feature tracking.
- `assets/`: Resource folder for fonts, logos, and audio.
- `presets/`: JSON-based editing templates.

---
*Developed by PendigEditor for the Pena Digital Ecosystem.*
