import bpy

from .miae_utils import refresh_overlay


class OverlaySettings(bpy.types.PropertyGroup):
    center_align_hand_poses: bpy.props.BoolProperty(name="Center Align", default=True, update=refresh_overlay)


class VideoReferenceSettings(bpy.types.PropertyGroup):
    start_frame: bpy.props.IntProperty(name="Start Frame", default=1, min=1, soft_min=1,
                                       description="Set the desired starting frame of the video reference – "
                                                   "typically the starting frame of the MoCap animation.")

