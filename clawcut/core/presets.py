import json
import os

GLOBAL_PRESETS = {
    "reels": {"w": 1080, "h": 1920},
    "instagram": {"w": 1080, "h": 1350},
    "youtube": {"w": 1920, "h": 1080},
    "square": {"w": 1080, "h": 1080}
}

class PresetManager:
    def __init__(self, preset_dir):
        self.preset_dir = preset_dir

    def load(self, preset_name):
        # 1. Check Global
        if preset_name in GLOBAL_PRESETS:
            return {
                "width": GLOBAL_PRESETS[preset_name]["w"],
                "height": GLOBAL_PRESETS[preset_name]["h"]
            }
        
        # 2. Check JSON
        json_path = os.path.join(self.preset_dir, f"{preset_name}.json")
        if os.path.exists(json_path):
            with open(json_path, "r") as f:
                return json.load(f)
        
        return None
