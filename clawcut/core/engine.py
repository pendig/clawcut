import subprocess
import os
from ..utils.helpers import verify_system, add_duration
from .presets import PresetManager
from .filters import FilterFactory

class ClawcutEngine:
    def __init__(self, workspace=None):
        if workspace is None:
            # 3 levels up: engine.py -> core -> clawcut (pkg) -> clawcut (root)
            self.workspace = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
        else:
            self.workspace = workspace
            
        self.assets = os.path.join(self.workspace, "assets")
        self.temp = os.path.join(self.workspace, "temp")
        self.preset_dir = os.path.join(self.workspace, "presets")
        self.outputs = os.path.join(self.workspace, "outputs")
        
        # Environment based overrides
        env_output = os.environ.get("CLAWCUT_OUTPUT_DIR")
        if env_output:
            self.outputs = env_output
        
        # Branding assets
        self.branding_dir = os.path.join(self.assets, "branding")
        self.font_path = os.path.join(self.branding_dir, "poppins-bold.ttf")
        self.watermark_path = os.path.join(self.branding_dir, "watermark.png")
        
        # Create folder structure
        os.makedirs(self.outputs, exist_ok=True)
        os.makedirs(self.assets, exist_ok=True)
        os.makedirs(self.temp, exist_ok=True)
        os.makedirs(self.preset_dir, exist_ok=True)
        os.makedirs(self.branding_dir, exist_ok=True)
        
        # Managers
        self.presets = PresetManager(self.preset_dir)
        self.filters = FilterFactory(self.font_path)
        
        # System checks
        ready, msg, self.ytdlp_cmd = verify_system()
        if not ready:
            print(f"Warning: {msg}")

    def run_command(self, cmd):
        print(f"Executing: {' '.join(cmd)}")
        result = subprocess.run(cmd, capture_output=True, text=True)
        if result.returncode != 0:
            print(f"Error: {result.stderr}")
            return False, result.stderr
        return True, result.stdout

    def download_clip(self, url, start_time=None, duration=None, filename="downloaded_clip.mp4"):
        target_path = os.path.join(self.assets, filename)
        cmd = self.ytdlp_cmd + [
            "-f", "bestvideo[ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4]/best",
            "--merge-output-format", "mp4",
            url,
            "-o", target_path
        ]
        if start_time and duration:
            end_time = add_duration(start_time, duration)
            cmd.extend(["--download-sections", f"*{start_time}-{end_time}"])
            
        success, _ = self.run_command(cmd)
        return target_path if success else None

    def build_render(self, clips, output_name="output.mp4", options=None):
        if options is None: options = {}
        output_path = os.path.join(self.outputs, output_name)
        
        # 1. Build basic video filters
        vf_list = self.filters.build_video_filters(options)
        
        # 2. Build inputs list
        list_path = os.path.join(self.temp, "clips.txt")
        with open(list_path, "w") as f:
            for clip in clips:
                f.write(f"file '{os.path.abspath(clip)}'\n")
        
        inputs = ["-f", "concat", "-safe", "0", "-i", list_path]
        
        # 3. Complex filters (Video + Watermark)
        watermark = options.get("watermark", False)
        if watermark and os.path.exists(self.watermark_path):
            inputs.extend(["-i", self.watermark_path])
            filter_complex, map_v = self.filters.build_watermark_complex(f"[0:v]{','.join(vf_list)}", options, self.watermark_path)
        else:
            filter_complex = f"[0:v]{','.join(vf_list)}[v_processed]"
            map_v = "[v_processed]"

        cmd = [
            "ffmpeg", "-y",
            *inputs,
            "-filter_complex", filter_complex,
            "-map", map_v,
            "-map", "0:a?",
            "-c:v", "libx264", "-pix_fmt", "yuv420p",
            "-preset", "fast",
            output_path
        ]
        
        success, _ = self.run_command(cmd)
        return output_path if success else None
