import textwrap
import os

class FilterFactory:
    def __init__(self, font_path=None):
        self.font_path = font_path

    def build_video_filters(self, options):
        w = options.get("width", 1080)
        h = options.get("height", 1920)
        zoom = options.get("zoom", 1.0)
        mode = options.get("mode", "cover")
        y_offset = options.get("y_offset", 0)
        title = options.get("title", "")
        font_size = options.get("font_size", 60)
        margin = options.get("margin", 30)

        scale_type = "increase" if mode == "cover" else "decrease"
        
        vf_chain = [
            f"scale={w}:{h}:force_original_aspect_ratio={scale_type}",
            f"scale={zoom}*iw:-1",
            "setsar=1",
            f"crop=min(iw\,{w}):min(ih\,{h})",
            f"pad={w}:{h}:(ow-iw)/2:(oh-ih)/2-{y_offset}"
        ]
        
        if title:
            if self.font_path and os.path.exists(self.font_path):
                available_pixel_width = w - (2 * margin)
                approx_char_width = font_size * 0.52
                wrap_chars = int(available_pixel_width / approx_char_width)
                wrapped_title = "\n".join(textwrap.wrap(title, width=wrap_chars))
                safe_title = wrapped_title.replace(":", "\\:").replace("'", "").replace("%", "\\%")
                
                drawtext_filter = (
                    f"drawtext=fontfile='{self.font_path}':"
                    f"text='{safe_title}':"
                    f"fontcolor=white:fontsize={font_size}:"
                    f"x=(w-text_w)/2:y=(h/2)+150:"
                    f"line_spacing=10"
                )
                vf_chain.append(drawtext_filter)
            else:
                print(f"Warning: Font not found at {self.font_path}. Skipping title.")
                
        return vf_chain

    def build_watermark_complex(self, v_processed, options, wm_path):
        # Shorthand Position Logic
        pos_map = {
            "top-left": {"x": "20", "y": "20"},
            "top-right": {"x": "main_w-overlay_w-20", "y": "20"},
            "top-center": {"x": "(main_w-overlay_w)/2", "y": "20"},
            "bottom-left": {"x": "20", "y": "main_h-overlay_h-20"},
            "bottom-right": {"x": "main_w-overlay_w-20", "y": "main_h-overlay_h-20"},
            "bottom-center": {"x": "(main_w-overlay_w)/2", "y": "main_h-overlay_h-20"}
        }
        
        pos = options.get("watermark_pos", "")
        default_x = pos_map.get(pos, {}).get("x", "(main_w-overlay_w)/2")
        default_y = pos_map.get(pos, {}).get("y", "100")

        wm_x = options.get("watermark_x", default_x)
        wm_y = options.get("watermark_y", default_y)
        wm_opacity = options.get("watermark_opacity", 1.0)
        wm_scale = options.get("watermark_scale", 450)
        
        # Overlay logic
        filter_complex = f"{v_processed}[v_main];[1:v]scale={wm_scale}:-1,format=rgba,colorchannelmixer=aa={wm_opacity}[wm];[v_main][wm]overlay={wm_x}:{wm_y}[final]"
        return filter_complex, "[final]"
