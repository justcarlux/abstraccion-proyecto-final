import os

ASSETS_ROOT = os.path.normpath(os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "..", "assets"))

def image_path(name: str):
    return os.path.join(ASSETS_ROOT, "images", name)

def thumbnail_path(name: str):
    return os.path.join(ASSETS_ROOT, "images", "thumbnails", name)

def font_path(name: str):
    return os.path.join(ASSETS_ROOT, "fonts", name)

def music_path(name: str):
    return os.path.join(ASSETS_ROOT, "music", name)