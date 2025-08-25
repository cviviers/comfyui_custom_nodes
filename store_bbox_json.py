import json
import os
import torch

class SaveBBoxAsJSON:
    @classmethod
    def INPUT_TYPES(cls):
        # allow scalar torch.Tensor, float or int
        number_types = ("INT")
        return {
            "required": {
                "image":    ("IMAGE",),                   # the image to pass through
                "class": ("STRING", {"default": "object"}),
                "x":    ("INT", {"default": 0}),
                "y":    ("INT", {"default": 0}),
                "width": ("INT", {"default": 0}),
                "height": ("INT", {"default": 0}),
                "filename": ("STRING", {"default": "image_xx.json"}),
                "directory":("STRING", {"default": "./bbox_data"})
            }
        }

    RETURN_TYPES = ("IMAGE",)      # we return exactly one IMAGE
    RETURN_NAMES = ("image",)      # name it “image”
    FUNCTION = "save_json"
    CATEGORY = "utils"

    def save_json(self, image, x, y, width, height, filename, object_class, directory):
        print(f"Received the following params: x={x}, y={y}, width={width}, height={height}, class={object_class}, filename={filename}, directory={directory}")
        # if Tensor, convert to Python number
        def to_num(v):
            return v.item() if isinstance(v, torch.Tensor) else v

        bbox_data = {
            "class":  object_class,
            "x":      to_num(x),
            "y":      to_num(y),
            "width":  to_num(width),
            "height": to_num(height)
        }

        os.makedirs(directory, exist_ok=True)
        filepath = os.path.join(directory, filename)
        with open(filepath, "w") as f:
            json.dump(bbox_data, f, indent=4)

        print(f"[SaveBBoxAsJSON] Saved to: {filepath}")
        
        return (image,)  # pass the image right back out

JSON_CLASS_MAPPINGS = {
    "SaveBBoxAsJSON": SaveBBoxAsJSON
}

JSON_NAME_MAPPINGS = {
    "SaveBBoxAsJSON": "🔧 Save BBox as JSON"
}
