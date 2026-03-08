import json
import subprocess
import os
import argparse
import sys

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
        # 1. Check if it's a global preset
        if preset_name in self.GLOBAL_PRESETS:
            return {
                "width": self.GLOBAL_PRESETS[preset_name]["w"],
                "height": self.GLOBAL_PRESETS[preset_name]["h"]
            }
        
        # 2. Check if it's a JSON file in presets/
        json_path = os.path.join(self.preset_dir, f"{preset_name}.json")
        if os.path.exists(json_path):
            with open(json_path, "r") as f:
                return json.load(f)
        
        # 3. Check if it's a direct path to a JSON file
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
        y_offset = options.get("y_offset", 0) # Support for "Elevated" style
        
        scale_type = "increase" if mode == "cover" else "decrease"
        
        vf_chain = [
            f"scale={w}:{h}:force_original_aspect_ratio={scale_type}",
            f"scale={zoom}*iw:-1",
            "setsar=1",
            f"crop=min(iw\,{w}):min(ih\,{h})",
            f"pad={w}:{h}:(ow-iw)/2:(oh-ih)/2-{y_offset}"
        ]
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
    parser = argparse.ArgumentParser(description="Clawcut Engine v1.7 - Dynamic JSON Presets")
    parser.add_argument("--url", help="URL to download")
    parser.add_argument("--start", help="Start time")
    parser.add_argument("--duration", help="Duration")
    parser.add_argument("--preset", help="Built-in preset name or JSON filename in presets/")
    parser.add_argument("--zoom", type=float, help="Override zoom factor")
    parser.add_argument("--mode", choices=["cover", "fit"], help="Override render mode")
    parser.add_argument("--output", default="clawcut_render.mp4", help="Output filename")
    
    args = parser.parse_args()
    engine = ClawcutEngine()
    
    # Load Preset Data
    render_options = {"width": 1080, "height": 1920, "zoom": 1.0, "mode": "cover"}
    if args.preset:
        loaded = engine.load_preset(args.preset)
        if loaded:
            render_options.update(loaded)
        else:
            print(f"Warning: Preset '{args.preset}' not found. Using defaults.")

    # CLI Overrides
    if args.zoom: render_options["zoom"] = args.zoom
    if args.mode: render_options["mode"] = args.mode

    if args.url:
        clip_path = engine.download_clip(args.url, args.start, args.duration, "temp_clip.mp4")
        if clip_path:
            final = engine.build_render([clip_path], args.output, render_options)
            if final:
                print(f"MEDIA: https://claw-br1dg3.penadigital.tech/editor/media/clawcut/{args.output}")
