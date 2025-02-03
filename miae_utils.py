import os

import bpy


def find_area(context, area_type: str) -> bpy.types.Area:
    for area in context.screen.areas:
        if area.type == area_type:
            return area
    return None


def get_abs_addon_dir() -> str:
    return os.path.dirname(os.path.abspath(__file__))
