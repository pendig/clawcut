import argparse
import sys
import os
from clawcut import ClawcutEngine

# Try to load environment variables from .env if python-dotenv is installed
try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    pass

def main():
    parser = argparse.ArgumentParser(description="Clawcut Engine v2.2.0 - Modular Package")
    parser.add_argument("--url", help="URL to download")
    parser.add_argument("--start", help="Start time")
    parser.add_argument("--duration", help="Duration")
    parser.add_argument("--preset", help="Built-in preset name or JSON filename")
    parser.add_argument("--zoom", type=float, help="Override zoom factor")
    parser.add_argument("--mode", choices=["cover", "fit"], help="Override render mode")
    parser.add_argument("--title", help="Title text to overlay")
    parser.add_argument("--fontsize", type=int, help="Font size for title")
    parser.add_argument("--margin", type=int, help="Margin left/right for title")
    parser.add_argument("--watermark", action="store_true", help="Add watermark")
    parser.add_argument("--wm_x", help="Watermark X position")
    parser.add_argument("--wm_y", help="Watermark Y position")
    parser.add_argument("--wm_opacity", type=float, help="Watermark opacity (0.0-1.0)")
    parser.add_argument("--output", default="clawcut_render.mp4", help="Output filename")
    
    args = parser.parse_args()
    engine = ClawcutEngine()
    
    render_options = {"width": 1080, "height": 1920, "zoom": 1.0, "mode": "cover", "watermark": False}
    
    # 1. Load Preset
    if args.preset:
        loaded = engine.presets.load(args.preset)
        if loaded:
            render_options.update(loaded)
        else:
            print(f"Warning: Preset '{args.preset}' not found. Using defaults.")

    # 2. CLI Overrides
    if args.zoom: render_options["zoom"] = args.zoom
    if args.mode: render_options["mode"] = args.mode
    if args.title: render_options["title"] = args.title
    if args.fontsize: render_options["font_size"] = args.fontsize
    if args.margin: render_options["margin"] = args.margin
    if args.watermark: render_options["watermark"] = True
    if args.wm_x: render_options["watermark_x"] = args.wm_x
    if args.wm_y: render_options["watermark_y"] = args.wm_y
    if args.wm_opacity: render_options["watermark_opacity"] = args.wm_opacity

    # 3. Execution
    if args.url:
        clip_path = engine.download_clip(args.url, args.start, args.duration, "temp_clip.mp4")
        if clip_path:
            final = engine.build_render([clip_path], args.output, render_options)
            if final:
                print(f"OUTPUT: {final}")
                # For Pendig Tunnel Compatibility
                if "media/clawcut" in final:
                    public_url = "https://claw-br1dg3.penadigital.tech/editor/media/clawcut/" + os.path.basename(final)
                    print(f"MEDIA: {public_url}")

if __name__ == "__main__":
    main()
