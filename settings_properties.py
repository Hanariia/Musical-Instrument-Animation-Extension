import bpy

from .miae_utils import refresh_overlay


class OverlaySettings(bpy.types.PropertyGroup):
    center_align_hand_poses: bpy.props.BoolProperty(name="Center Align", default=True, update=refresh_overlay)
