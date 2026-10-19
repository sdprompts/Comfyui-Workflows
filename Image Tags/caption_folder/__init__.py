"""Load a folder of images, save a matching caption, and preview each pair.

Copy this folder to ComfyUI/custom_nodes/caption_folder and restart ComfyUI.
The image folder can be anywhere on disk. Each .txt is written next to its image.
"""

import os
import uuid

import folder_paths
import node_helpers
import numpy as np
import torch
from PIL import Image

IMAGE_EXTENSIONS = (".png", ".jpg", ".jpeg", ".webp")
WEB_DIRECTORY = "./js"


def image_folder(path):
    directory = os.path.realpath(os.path.expanduser(path.strip()))
    if not os.path.isdir(directory):
        raise ValueError(f"Folder not found: {directory}")
    return directory


def flatten_text(value):
    if isinstance(value, (list, tuple)):
        values = []
        for item in value:
            values.extend(flatten_text(item))
        return values
    if value is None:
        return [""]
    return [str(value)]


def frames_from_image(image):
    if isinstance(image, (list, tuple)):
        frames = []
        for item in image:
            frames.extend(frames_from_image(item))
        return frames
    if not isinstance(image, torch.Tensor):
        raise ValueError(f"Expected an image tensor, got {type(image)}")
    if image.dim() == 4:
        return [image[index] for index in range(image.shape[0])]
    if image.dim() == 3:
        return [image]
    raise ValueError(f"Unexpected image shape {tuple(image.shape)}")


def tensor_to_pil(image):
    array = image.detach().cpu().clamp(0, 1).numpy()
    array = (array * 255).round().astype(np.uint8)
    if array.shape[-1] == 1:
        array = array.squeeze(-1)
    return Image.fromarray(array)


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


class ShowImageText:
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "image": ("IMAGE",),
                "text": ("STRING", {"forceInput": True}),
            }
        }

    RETURN_TYPES = ()
    OUTPUT_NODE = True
    INPUT_IS_LIST = True
    FUNCTION = "show"
    CATEGORY = "image"

    def show(self, image, text):
        frames = frames_from_image(image)
        captions = flatten_text(text)
        if len(captions) < len(frames):
            captions.extend([""] * (len(frames) - len(captions)))

        previews = []
        shown = []
        directory = folder_paths.get_temp_directory()
        os.makedirs(directory, exist_ok=True)
        for frame, caption in zip(frames, captions):
            preview = tensor_to_pil(frame)
            preview.thumbnail((384, 384))
            filename = f"caption_{uuid.uuid4().hex}.png"
            preview.save(os.path.join(directory, filename))
            previews.append({"filename": filename, "subfolder": "", "type": "temp"})
            shown.append(caption)
        return {"ui": {"images": previews, "text": shown}, "result": ()}


NODE_CLASS_MAPPINGS = {
    "LoadImagesFromFolder": LoadImagesFromFolder,
    "SaveCaptionText": SaveCaptionText,
    "ShowImageText": ShowImageText,
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "LoadImagesFromFolder": "Load Images From Folder",
    "SaveCaptionText": "Save Caption Text",
    "ShowImageText": "Show Image Text",
}

__all__ = ["NODE_CLASS_MAPPINGS", "NODE_DISPLAY_NAME_MAPPINGS", "WEB_DIRECTORY"]
