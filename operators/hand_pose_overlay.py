import os
import bpy

from ..estimated_hand_poses import HandType
from ..miae_utils import find_area, get_abs_addon_dir
from ..hand_pose_image_manager import HandPoseImageManager, ImageStripData, HAND_POSES_DIRECTORY


class HandPoseOverlayOperator(bpy.types.Operator):
    """Import estimated hand poses json and create an overlay of the data."""
    bl_idname = "mia.hand_pose_overlay"
    bl_label = "Hand Pose Overlay"
    bl_options = {'REGISTER', 'UNDO'}

    def __init__(self):
        super().__init__()
        self.image_manager = None
        self.latest_current_frame = -1

    @classmethod
    def poll(cls, context):
        sequence_editor = bpy.context.scene.sequence_editor
        if sequence_editor and len(sequence_editor.sequences) != 0:
            return True
        return False

    def execute(self, context):
        image_strips = self.image_manager.get_frames_image_strip_data(
            bpy.context.scene.frame_current, self.__get_fps(), 1, 3)
        for strip in image_strips:
            # handle the end of the last image strip
            if strip.end_frame is None:
                strip.end_frame = context.scene.sequence_editor.sequences[0].frame_final_end
            self.add_image_strip(context, strip)
        return {'RUNNING_MODAL'}

    def modal(self, context, event):
        overlay_properties = context.window_manager.overlay_properties

        if overlay_properties.refresh_overlay:
            self.__refresh_overlay(context)
            context.window_manager.overlay_properties.refresh_overlay = False
            self.report({'INFO'}, "Refreshing Hand Pose Overlay...")

        if overlay_properties.clear_overlay:
            self.cancel(context)
            self.report({'INFO'}, "Clearing Hand Pose Overlay...")
            return {'CANCELLED'}

        if bpy.context.scene.frame_current != self.latest_current_frame:
            self.execute(context)
            self.latest_current_frame = bpy.context.scene.frame_current

        return {'PASS_THROUGH'}

    def invoke(self, context, event):
        self.__set_attributes(context)
        context.window_manager.modal_handler_add(self)
        return {'RUNNING_MODAL'}

    def cancel(self, context):
        self.__clear_overlay(context)
        context.window_manager.overlay_properties.overlay_active = False
        context.window_manager.overlay_properties.clear_overlay = False

    @staticmethod
    def __get_current_timestamp():
        frame = bpy.context.scene.frame_current
        fps = bpy.context.scene.render.fps / bpy.context.scene.render.fps_base
        return frame / fps

    @staticmethod
    def __get_fps():
        return bpy.context.scene.render.fps / bpy.context.scene.render.fps_base

    def __set_attributes(self, context):
        sequence_editor = context.scene.sequence_editor
        image_height = sequence_editor.sequences[0].elements[0].orig_height
        image_width = sequence_editor.sequences[0].elements[0].orig_width
        filepath = context.window_manager.overlay_properties.filepath
        self.image_manager = HandPoseImageManager((image_height, image_width), filepath)

    def __refresh_overlay(self, context):
        # Clear previous overlay
        self.__clear_overlay(context)
        self.__set_attributes(context)

    def __clear_overlay(self, context):
        with context.temp_override(area=find_area(context, area_type='SEQUENCE_EDITOR')):
            bpy.ops.sequencer.select_all(action='SELECT')
            context.scene.sequence_editor.sequences[0].select = False
            bpy.ops.sequencer.delete()
        self.latest_current_frame = -1

    @staticmethod
    def add_image_strip(context, image_strip_data: ImageStripData):
        abs_directory_path = os.path.join(get_abs_addon_dir(), HAND_POSES_DIRECTORY)
        with context.temp_override(area=find_area(bpy.context, area_type='SEQUENCE_EDITOR')):
            bpy.ops.sequencer.image_strip_add(
                directory=abs_directory_path,
                relative_path=True,
                files=[{"name": image_strip_data.filename}],
                frame_start=image_strip_data.start_frame,
                frame_end=image_strip_data.end_frame,
                channel=2 if image_strip_data.hand_type == HandType.RIGHT else 3,
                show_multiview=False, fit_method='FIT')


class HandPoseOverlayProperties(bpy.types.PropertyGroup):
    refresh_overlay: bpy.props.BoolProperty(default=False)
    clear_overlay: bpy.props.BoolProperty(default=False)
    overlay_active: bpy.props.BoolProperty(default=False)
    filepath: bpy.props.StringProperty(subtype='FILE_PATH')
