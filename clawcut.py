import json
import subprocess
import os
import argparse
import sys
import textwrap

class ClawcutEngine:
    # Built-in Standard Presets
    GLOBAL_PRESETS = {
        "reels": {"w": 1080, "h": 1920},
        "instagram": {"w": 1080, "h": 1350},
        "youtube": {"w": 1920, "h": 1080},
        "square": {"w": 1080, "h": 1080}
    }

    def __init__(self, workspace=None):
        if workspace is None:
            self.workspace = os.path.dirname(os.path.abspath(__file__))
        else:
            self.workspace = workspace
            
        self.assets = os.path.join(self.workspace, "assets")
        self.temp = os.path.join(self.workspace, "temp")
        self.preset_dir = os.path.join(self.workspace, "presets")
        
        # Font paths
        self.font_path = "/home/node/.openclaw/workspace/pendig-editor/skills/pendig-style/assets/fonts/Poppins-Bold.ttf"
        
        # Pendig Server vs Public Output
        pendig_media_root = "/home/node/.openclaw/workspace/pendig-editor/media/clawcut"
        if os.path.exists(os.path.dirname(pendig_media_root)):
            self.outputs = pendig_media_root
        else:
            self.outputs = os.path.join(self.workspace, "outputs")
            
        # yt-dlp path detection
        self.ytdlp_path = "yt-dlp"
        potential_ytdlp = os.path.abspath(os.path.join(self.workspace, "../skills/downloader/scripts/yt-dlp"))
        if os.path.exists(potential_ytdlp):
            self.ytdlp_cmd = ["python3", potential_ytdlp]
        else:
            self.ytdlp_cmd = ["yt-dlp"]
        
        os.makedirs(self.outputs, exist_ok=True)
        os.makedirs(self.assets, exist_ok=True)
        os.makedirs(self.temp, exist_ok=True)
        os.makedirs(self.preset_dir, exist_ok=True)
        
    def run_command(self, cmd):
        print(f"Executing: {' '.join(cmd)}")
        result = subprocess.run(cmd, capture_output=True, text=True)
        if result.returncode != 0:
            print(f"Error: {result.stderr}")
            return False, result.stderr
        return True, result.stdout

    def load_preset(self, preset_name):
        if preset_name in self.GLOBAL_PRESETS:
            return {
                "width": self.GLOBAL_PRESETS[preset_name]["w"],
                "height": self.GLOBAL_PRESETS[preset_name]["h"]
            }
        json_path = os.path.join(self.preset_dir, f"{preset_name}.json")
        if os.path.exists(json_path):
            with open(json_path, "r") as f:
                return json.load(f)
        if os.path.exists(preset_name):
            with open(preset_name, "r") as f:
                return json.load(f)
        return None

    def download_clip(self, url, start_time=None, duration=None, filename="downloaded_clip.mp4"):
        target_path = os.path.join(self.assets, filename)
        cmd = self.ytdlp_cmd + [
            "-f", "bestvideo[ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4]/best",
            "--merge-output-format", "mp4",
            url,
            "-o", target_path
        ]
        if start_time and duration:
            end_time = self._add_duration(start_time, duration)
            cmd.extend(["--download-sections", f"*{start_time}-{end_time}"])
            
        success, _ = self.run_command(cmd)
        return target_path if success else None

    def _add_duration(self, start, dur):
        try:
            if ":" in str(start):
                parts = list(map(int, start.split(":")))
                seconds = parts[-1] + parts[-2]*60 + (parts[-3]*3600 if len(parts)>2 else 0)
                return str(seconds + float(dur))
            return str(float(start) + float(dur))
        except: return "inf"

    def build_render(self, clips, output_name="output.mp4", options=None):
        if options is None: options = {}
        
        output_path = os.path.join(self.outputs, output_name)
        w = options.get("width", 1080)
        h = options.get("height", 1920)
        zoom = options.get("zoom", 1.0)
        mode = options.get("mode", "cover")
        y_offset = options.get("y_offset", 0)
        title = options.get("title", "")
        font_size = options.get("font_size", 60)
        margin = options.get("margin", 30) # Default margin
        
        scale_type = "increase" if mode == "cover" else "decrease"
        
        # 1. Base Scaling and Positioning
        vf_chain = [
            f"scale={w}:{h}:force_original_aspect_ratio={scale_type}",
            f"scale={zoom}*iw:-1",
            "setsar=1",
            f"crop=min(iw\,{w}):min(ih\,{h})",
            f"pad={w}:{h}:(ow-iw)/2:(oh-ih)/2-{y_offset}"
        ]
        
        # 2. Add Title Text if present
        if title:
            # Calculate char width roughly (font_size * 0.6)
            # Available width = total_width - (2 * margin)
            available_pixel_width = w - (2 * margin)
            approx_char_width = font_size * 0.55
            wrap_chars = int(available_pixel_width / approx_char_width)
            
            wrapped_title = "\n".join(textwrap.wrap(title, width=wrap_chars))
            # Escape for FFmpeg drawtext
            safe_title = wrapped_title.replace(":", "\\:").replace("'", "").replace("%", "\\%")
            
            drawtext_filter = (
                f"drawtext=fontfile='{self.font_path}':"
                f"text='{safe_title}':"
                f"fontcolor=white:fontsize={font_size}:"
                f"x=(w-text_w)/2:y=(h/2)+150:" # Positioned below the center
                f"line_spacing=10"
            )
            vf_chain.append(drawtext_filter)

        vf_str = ",".join(vf_chain)
        
        list_path = os.path.join(self.temp, "clips.txt")
        with open(list_path, "w") as f:
            for clip in clips:
                f.write(f"file '{os.path.abspath(clip)}'\n")
        
        cmd = [
            "ffmpeg", "-y",
            "-f", "concat", "-safe", "0",
            "-i", list_path,
            "-vf", vf_str,
            "-c:v", "libx264", "-pix_fmt", "yuv420p",
            "-preset", "fast",
            output_path
        ]
        
        success, _ = self.run_command(cmd)
        return output_path if success else None

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Clawcut Engine v1.9 - Margin Support")
    parser.add_argument("--url", help="URL to download")
    parser.add_argument("--start", help="Start time")
    parser.add_argument("--duration", help="Duration")
    parser.add_argument("--preset", help="Built-in preset name or JSON filename")
    parser.add_argument("--zoom", type=float, help="Override zoom factor")
    parser.add_argument("--mode", choices=["cover", "fit"], help="Override render mode")
    parser.add_argument("--title", help="Title text to overlay")
    parser.add_argument("--fontsize", type=int, help="Font size for title")
    parser.add_argument("--margin", type=int, help="Margin left/right for title")
    parser.add_argument("--output", default="clawcut_render.mp4", help="Output filename")
    
    args = parser.parse_args()
    engine = ClawcutEngine()
    
    render_options = {"width": 1080, "height": 1920, "zoom": 1.0, "mode": "cover"}
    if args.preset:
        loaded = engine.load_preset(args.preset)
        if loaded:
            render_options.update(loaded)

    if args.zoom: render_options["zoom"] = args.zoom
    if args.mode: render_options["mode"] = args.mode
    if args.title: render_options["title"] = args.title
    if args.fontsize: render_options["font_size"] = args.fontsize
    if args.margin: render_options["margin"] = args.margin

    if args.url:
        clip_path = engine.download_clip(args.url, args.start, args.duration, "temp_clip.mp4")
        if clip_path:
            final = engine.build_render([clip_path], args.output, render_options)
            if final:
                print(f"MEDIA: https://claw-br1dg3.penadigital.tech/editor/media/clawcut/{args.output}")
