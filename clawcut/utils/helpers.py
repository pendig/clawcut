import subprocess
import os
import shutil

def verify_system():
    """Check for FFmpeg and yt-dlp"""
    if not shutil.which("ffmpeg"):
        return False, "FFmpeg not found in PATH. Please install FFmpeg.", None
    
    # Try both 'yt-dlp' and 'python3 -m yt_dlp'
    ytdlp_cmd = None
    if shutil.which("yt-dlp"):
        ytdlp_cmd = ["yt-dlp"]
    else:
        try:
            subprocess.run(["python3", "-m", "yt_dlp", "--version"], capture_output=True, check=True)
            ytdlp_cmd = ["python3", "-m", "yt_dlp"]
        except:
            # Check for local skill fallback
            # (In a real package, you'd want yt-dlp in the path or as a python lib)
            # But let's keep the user's specific fallback for compatibility
            potential_ytdlp = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../../skills/downloader/scripts/yt-dlp"))
            if os.path.exists(potential_ytdlp):
                ytdlp_cmd = ["python3", potential_ytdlp]
            else:
                return False, "yt-dlp not found. Install via 'pip install yt-dlp'.", None
    
    return True, "System ready.", ytdlp_cmd

def add_duration(start, dur):
    try:
        if ":" in str(start):
            parts = list(map(int, start.split(":")))
            seconds = parts[-1] + parts[-2]*60 + (parts[-3]*3600 if len(parts)>2 else 0)
            return str(seconds + float(dur))
        return str(float(start) + float(dur))
    except:
        return "inf"
