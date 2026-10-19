"""Load every image in a folder and save a matching caption beside it.

Copy this file to ComfyUI/custom_nodes/caption_folder.py and restart ComfyUI.
The folder can be anywhere on disk. Each .txt is written next to its image.
"""

import os

import node_helpers
import numpy as np
import torch
from PIL import Image

IMAGE_EXTENSIONS = (".png", ".jpg", ".jpeg", ".webp")


def image_folder(path):
    directory = os.path.realpath(os.path.expanduser(path.strip()))
    if not os.path.isdir(directory):
        raise ValueError(f"Folder not found: {directory}")
    return directory


class LoadImagesFromFolder:
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "folder": (
                    "STRING",
                    {
                        "default": "",
                        "tooltip": "Full path to the image folder. Captions are saved in this same folder.",
                    },
                ),
            }
        }

    RETURN_TYPES = ("IMAGE", "STRING", "STRING")
    RETURN_NAMES = ("image", "filename", "folder")
    OUTPUT_IS_LIST = (True, True, False)
    FUNCTION = "load"
    CATEGORY = "image"

    def load(self, folder):
        directory = image_folder(folder)
        names = sorted(
            name
            for name in os.listdir(directory)
            if name.lower().endswith(IMAGE_EXTENSIONS)
            and os.path.isfile(os.path.join(directory, name))
        )
        if not names:
            raise ValueError(f"No images found in {directory}")

        images = []
        stems = []
        for name in names:
            img = node_helpers.pillow(Image.open, os.path.join(directory, name))
            if img.mode == "I":
                img = img.point(lambda value: value * (1 / 255))
            img = img.convert("RGB")
            array = np.array(img).astype(np.float32) / 255.0
            images.append(torch.from_numpy(array)[None,])
            stems.append(os.path.splitext(name)[0])
        return (images, stems, directory)


class SaveCaptionText:
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "text": ("STRING", {"forceInput": True}),
                "filename": ("STRING", {"forceInput": True}),
                "folder": ("STRING", {"forceInput": True}),
            }
        }

    RETURN_TYPES = ("STRING",)
    OUTPUT_NODE = True
    FUNCTION = "save"
    CATEGORY = "image"

    def save(self, text, filename, folder):
        directory = image_folder(folder)
        stem = os.path.splitext(os.path.basename(filename))[0]
        if not stem or stem in {".", ".."}:
            raise ValueError("Missing caption filename.")
        path = os.path.realpath(os.path.join(directory, stem + ".txt"))
        if os.path.commonpath([directory, path]) != directory:
            raise ValueError("Caption path must stay inside the image folder.")
        with open(path, "w", encoding="utf-8", newline="\n") as handle:
            handle.write(text.strip() + "\n")
        return {"ui": {"text": [text]}, "result": (text,)}


NODE_CLASS_MAPPINGS = {
    "LoadImagesFromFolder": LoadImagesFromFolder,
    "SaveCaptionText": SaveCaptionText,
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "LoadImagesFromFolder": "Load Images From Folder",
    "SaveCaptionText": "Save Caption Text",
}
