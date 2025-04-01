import bpy

from .miae_utils import refresh_overlay


class OverlaySettings(bpy.types.PropertyGroup):
    center_align_hand_poses: bpy.props.BoolProperty(default=True, update=refresh_overlay)
