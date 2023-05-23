import os

from PIL import Image, ImageDraw, ImageFont

import folder_paths


def get_fonts_list():
    path = os.path.join(folder_paths.base_path, "comfy_extras/fonts")
    output_list = [f for (dirpath, dirnames, filenames) in os.walk(path) for f in filenames]
    output_list = filter(lambda x: x.endswith(".ttf") or x.endswith(".otf"), output_list)

    return sorted(list(output_list))


class ImageText:
    def __init__(self):
        pass

    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "text": ("STRING", {"multiline": False}),
                "font": (get_fonts_list(),),
                "size": ("INT", {
                    "default": 28,
                    "step": 1
                }),
                "red": ("INT", {
                    "default": 255,
                    "max": 255,
                    "step": 1
                }),
                "green": ("INT", {
                    "default": 255,
                    "max": 255,
                    "step": 1
                }),
                "blue": ("INT", {
                    "default": 255,
                    "max": 255,
                    "step": 1
                }),
                "alpha": ("FLOAT", {
                    "default": 1.0,
                    "max": 1.0,
                    "step": 0.01
                }),
                "margin_x": ("INT", {
                    "default": 0,
                    "step": 1
                }),
                "margin_y": ("INT", {
                    "default": 0,
                    "step": 1
                }),
            },
        }

    RETURN_TYPES = ("IMAGE",)
    FUNCTION = "image_text"
    CATEGORY = "image"

    def image_text(self, text, font, size, red, green, blue, alpha, margin_x, margin_y):
        font_path = os.path.join(folder_paths.base_path, "comfy_extras/fonts/", font)
        font = ImageFont.truetype(font_path, size, encoding="unic")

        (left, top, right, bottom) = font.getbbox(text)

        canvas = Image.new("RGBA", (right + margin_x * 2, bottom - top + margin_y * 2), (0, 0, 0, 0))

        draw = ImageDraw.Draw(canvas)
        draw.text((margin_x, margin_y - top), text, (red, green, blue, int(alpha * 255)), font)

        return (canvas.image_to_tensor().unsqueeze(0),)


class ImageTextOutlined:
    def __init__(self):
        pass

    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "text": ("STRING", {"multiline": False}),
                "font": (get_fonts_list(),),
                "size": ("INT", {
                    "default": 28,
                    "step": 1
                }),
                "red": ("INT", {
                    "default": 255,
                    "max": 255,
                    "step": 1
                }),
                "green": ("INT", {
                    "default": 255,
                    "max": 255,
                    "step": 1
                }),
                "blue": ("INT", {
                    "default": 255,
                    "max": 255,
                    "step": 1
                }),
                "outline_size": ("INT", {
                    "default": 1,
                    "step": 1
                }),
                "outline_red": ("INT", {
                    "default": 0,
                    "max": 255,
                    "step": 1
                }),
                "outline_green": ("INT", {
                    "default": 0,
                    "max": 255,
                    "step": 1
                }),
                "outline_blue": ("INT", {
                    "default": 0,
                    "max": 255,
                    "step": 1
                }),
                "alpha": ("FLOAT", {
                    "default": 1.0,
                    "max": 1.0,
                    "step": 0.01
                }),
                "margin_x": ("INT", {
                    "default": 0,
                    "step": 1
                }),
                "margin_y": ("INT", {
                    "default": 0,
                    "step": 1
                }),
            },
        }

    RETURN_TYPES = ("IMAGE",)
    FUNCTION = "image_text"
    CATEGORY = "image"

    def image_text(
            self, text, font, size, red, green, blue, outline_size, outline_red, outline_green, outline_blue, alpha,
            margin_x, margin_y
    ):
        font_path = os.path.join(folder_paths.base_path, "comfy_extras/fonts/", font)
        font = ImageFont.truetype(font_path, size, encoding="unic")

        (left, top, right, bottom) = font.getbbox(text)

        canvas = Image.new("RGBA", (
            right + (margin_x + outline_size) * 2,
            bottom - top + (margin_y + outline_size) * 2
        ), (0, 0, 0, 0))

        draw = ImageDraw.Draw(canvas)

        draw.text(
            (margin_x + outline_size, margin_y + outline_size - top),
            text=text, fill=(red, green, blue, int(alpha * 255)),
            stroke_fill=(outline_red, outline_green, outline_blue, int(alpha * 255)),
            stroke_width=outline_size, font=font
        )

        return (canvas.image_to_tensor().unsqueeze(0),)


NODE_CLASS_MAPPINGS = {
    "ImageText": ImageText,
    "ImageTextOutlined": ImageTextOutlined
}