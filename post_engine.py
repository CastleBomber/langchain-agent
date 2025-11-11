from PIL import Image
import imageio
import numpy as np
import re, os

class PoseEngine:
    """Detects pose or motion commands and handles them"""

    def __init__(self):
        self.pose_keywords = {
            "pixelate": "Generate pixelated character",
            "walk": "Generate walking pose sequence",
            "run": "Generate running animation",
            "sit": "Generate seated pose",
            "jump": "Generate jumping pose",
            "turn": "Generate turning motion"
        }

    def detect_pose(self, text: str):
        """Return the matched pose keyword if found"""
        for keyword in self.pose_keywords:
            if re.search(rf"\b{keyword}\b", text.lower()):
                return keyword
        return None

    def handle_pose(self, keyword, user_input=None):
        """Handle a detected pose command and act on an image if provided"""
        action = self.pose_keywords[keyword]

        # --- detect optional custom size (e.g., "64x64")
        size_match = re.search(r"(\d+)\s*x\s*(\d+)", user_input or "")
        custom_size = (int(size_match.group(1)), int(size_match.group(2))) if size_match else None

        # --- detect filename (e.g., "zeus.png" or "hero.jpg")
        match = re.search(r"([A-Za-z0-9_\-./]+\.(png|jpg|jpeg|gif))", user_input or "", re.IGNORECASE)
        image_path = match.group(1) if match else None

        if not image_path:
            return f"❗ PoseEngine: No image filename detected in your command."
        if not os.path.exists(image_path):
            return f"❌ PoseEngine: Image file not found — check the name or path: {image_path}"

        # --- pixelate command
        if keyword == "pixelate":
            return self.pixelate_image(image_path, custom_size)

        # --- motion commands
        elif keyword in ["walk", "run", "jump"]:
            return self.create_motion_gif(image_path, keyword)

        return f"🩰 PoseEngine: {action} (simulation only for now)."

    def pixelate_image(self, image_path, custom_size=None, pixel_size=10):
        """
        Pixelates image.
        Example usage:
            pixelate zeus.png
            pixelate 64x64 zeus.png
        """
        img = Image.open(image_path)

        if custom_size:
            # Use fixed dimensions like 64x64
            small = img.resize(custom_size, Image.NEAREST)
        else:
            small = img.resize((img.width // pixel_size, img.height // pixel_size), Image.NEAREST)

        pixelated = small.resize(img.size, Image.NEAREST)
        out_path = f"pixelated_{os.path.basename(image_path)}"
        pixelated.save(out_path)

        return f"🩰 Pixelated image saved as {out_path}"

    def create_motion_gif(self, image_path, keyword):
        """Create a basic movement GIF stub (placeholder for animation)"""
        img = Image.open(image_path)
        frames = []

        for i in range(5):  # 5-frame demo
            frame = img.copy()
            frame = frame.rotate(i * 5)  # simple rotation
            frames.append(frame)

        out_gif = f"{keyword}_{os.path.basename(image_path).split('.')[0]}.gif"
        frames[0].save(out_gif, save_all=True, append_images=frames[1:], duration=200, loop=0)

        return f"🩰 GIF for '{keyword}' saved as {out_gif}"

    