import json
import subprocess
import os
import argparse
import sys

class ClawcutEngine:
    # Resolution Presets (Standard Social Media)
    PRESETS = {
        "reels": {"w": 1080, "h": 1920},
        "instagram": {"w": 1080, "h": 1350},
        "youtube": {"w": 1920, "h": 1080},
        "square": {"w": 1080, "h": 1080},
        "720p": {"w": 1280, "h": 720},
        "1080p": {"w": 1920, "h": 1080}
    }

    def __init__(self, workspace=None):
        if workspace is None:
            self.workspace = os.path.dirname(os.path.abspath(__file__))
        else:
            self.workspace = workspace
            
        self.assets = os.path.join(self.workspace, "assets")
        self.temp = os.path.join(self.workspace, "temp")
        
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
            self.ytdlp_path = f"python3 {potential_ytdlp}"
        
        os.makedirs(self.outputs, exist_ok=True)
        os.makedirs(self.assets, exist_ok=True)
        os.makedirs(self.temp, exist_ok=True)
        
    def run_command(self, cmd):
        cmd_str = " ".join(cmd)
        print(f"Executing: {cmd_str}")
        result = subprocess.run(cmd_str, shell=True, capture_output=True, text=True)
        if result.returncode != 0:
            print(f"Error: {result.stderr}")
            return False, result.stderr
        return True, result.stdout

    def _get_resolution(self, width, height, preset):
        if preset in self.PRESETS:
            return self.PRESETS[preset]["w"], self.PRESETS[preset]["h"]
        return width or 1080, height or 1920

    def download_clip(self, url, start_time=None, duration=None, filename="downloaded_clip.mp4"):
        target_path = os.path.join(self.assets, filename)
        cmd = [
            self.ytdlp_path,
            "-f", "bestvideo[ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4]/best",
            "--merge-output-format", "mp4",
            f"'{url}'",
            "-o", f"'{target_path}'"
        ]
        if start_time and duration:
            end_time = self._add_duration(start_time, duration)
            cmd.extend(["--download-sections", f"'*{start_time}-{end_time}'"])
            
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

    def build_render(self, clips, output_name="output.mp4", width=None, height=None, preset=None):
        output_path = os.path.join(self.outputs, output_name)
        w, h = self._get_resolution(width, height, preset)
        
        # Scaling logic: contain with black bars (Smart Auto-scaling)
        # filter: scale=w:h:force_original_aspect_ratio=decrease,pad=w:h:(ow-iw)/2:(oh-ih)/2
        vf_scale = f"scale={w}:{h}:force_original_aspect_ratio=decrease,pad={w}:{h}:(ow-iw)/2:(oh-ih)/2"
        
        list_path = os.path.join(self.temp, "clips.txt")
        with open(list_path, "w") as f:
            for clip in clips:
                f.write(f"file '{os.path.abspath(clip)}'\n")
        
        cmd = [
            "ffmpeg", "-y",
            "-f", "concat", "-safe", "0",
            "-i", f"'{list_path}'",
            "-vf", f"\"{vf_scale}\"",
            "-c:v", "libx264", "-pix_fmt", "yuv420p",
            "-preset", "fast",
            f"'{output_path}'"
        ]
        
        success, _ = self.run_command(cmd)
        return output_path if success else None

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Clawcut Engine v1.3 - Dynamic Resolution")
    parser.add_argument("--url", help="URL to download")
    parser.add_argument("--start", help="Start time")
    parser.add_argument("--duration", help="Duration")
    parser.add_argument("--preset", choices=ClawcutEngine.PRESETS.keys(), help="Resolution preset (reels, youtube, etc)")
    parser.add_argument("--width", type=int, help="Custom width")
    parser.add_argument("--height", type=int, help="Custom height")
    parser.add_argument("--output", default="clawcut_render.mp4", help="Output filename")
    
    args = parser.parse_args()
    engine = ClawcutEngine()
    
    if args.url:
        clip_path = engine.download_clip(args.url, args.start, args.duration, "temp_clip.mp4")
        if clip_path:
            final = engine.build_render([clip_path], args.output, args.width, args.height, args.preset)
            if final:
                print(f"Success: {final}")
                if "/pendig-editor/media/" in final:
                    print(f"MEDIA: https://claw-br1dg3.penadigital.tech/editor/media/clawcut/{args.output}")
