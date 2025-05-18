import bpy

from .miae_utils import refresh_overlay


class OverlaySettings(bpy.types.PropertyGroup):
    center_align_hand_poses: bpy.props.BoolProperty(
        name="Center Align",
        default=True,
        update=refresh_overlay
    )
    circle_radius: bpy.props.FloatProperty(
        name="Circle Radius",
        description="Set the radius of the circles at the hand landmark points.",
        default=6,
        min=1, soft_min=1, max=20, soft_max=20,
        precision=1, step=10,
        update=refresh_overlay
    )
    line_width: bpy.props.IntProperty(
        name="Line Width",
        description="Set the width of the lines connecting the hand landmark points.",
        min=1, soft_min=1, max=20, soft_max=20,
        default=5, update=refresh_overlay
    )
    # although Pillow allows compression up to 9,
    # the difference of the hand pose images size is insignificant in range 3-9
    compression: bpy.props.IntProperty(
        name="Compression Level",
        description="Set the compression level of the hand pose overlay images. "
                    "Lower compression should result in better time efficiency, "
                    "while higher compression results in better storage efficiency",
        default=2,
        min=0, soft_min=0, max=5, soft_max=5,
        update=refresh_overlay
    )


class VideoReferenceSettings(bpy.types.PropertyGroup):
    start_frame: bpy.props.IntProperty(name="Start Frame", default=1, min=1, soft_min=1,
                                       description="Set the desired starting frame of the video reference – "
                                                   "typically the starting frame of the MoCap animation.")

