import os
from typing import Optional

import bpy


def find_area(context, area_type: str) -> Optional[bpy.types.Area]:
    for area in context.screen.areas:
        if area.type == area_type:
            return area
    return None


def get_abs_addon_dir() -> str:
    return os.path.dirname(os.path.abspath(__file__))


def refresh_overlay(self, context):
    context.window_manager.overlay_properties.refresh_overlay = True
    