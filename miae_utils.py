import os
from typing import Optional

import bpy


def find_area(context, area_type: str) -> Optional[bpy.types.Area]:
    """Finds an area of the given area type in the given context
    :param context: the context in which the area will be searched for.
    :param area_type: the type of area to be searched for.
    :return: the area object or None if the area is not found.
    """
    for area in context.screen.areas:
        if area.type == area_type:
            return area
    return None


def get_abs_addon_dir() -> str:
    return os.path.dirname(os.path.abspath(__file__))


def refresh_overlay(self, context):
    """An update function for refreshing the overlay."""
    context.window_manager.overlay_properties.refresh_overlay = True
    