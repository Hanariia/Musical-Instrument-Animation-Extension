import os
import bpy

from ..estimated_hand_poses import HandType
from ..miae_utils import find_area, get_abs_addon_dir
from ..hand_pose_image_manager import HandPoseImageManager, ImageStripData, HAND_POSES_DIRECTORY


class HandPoseOverlayOperator(bpy.types.Operator):
    """Imports hand data and creates an overlay of the estimated hand poses in the sequencer."""
    bl_idname = "sequencer.hand_pose_overlay"
    bl_label = "Hand Pose Overlay"
    bl_options = {'REGISTER', 'UNDO'}

    filepath: bpy.props.StringProperty(subtype='FILE_PATH')
    filename: bpy.props.StringProperty(subtype='FILE_NAME')

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
        if self.image_manager is None:
            self.__set_attributes(context)
        image_strips = self.image_manager.get_frames_image_strip_data(
            bpy.context.scene.frame_current, self.__get_fps(), 1, 2)
        for strip in image_strips:
            # handle the end of the last image strip
            if strip.end_frame is None:
                strip.end_frame = context.scene.sequence_editor.sequences[0].frame_final_end
            self.add_image_strip(context, strip)
        return {'RUNNING_MODAL'}

    def modal(self, context, event):
        if bpy.context.scene.frame_current != self.latest_current_frame:
            self.execute(context)
            self.latest_current_frame = bpy.context.scene.frame_current
        if event.type == 'ESC':  # TODO remove this?
            return {'CANCELLED'}

        return {'PASS_THROUGH'}

    def invoke(self, context, event):
        self.latest_current_frame = bpy.context.scene.frame_current  # TODO is correct?
        context.window_manager.fileselect_add(self)
        context.window_manager.modal_handler_add(self)
        return {'RUNNING_MODAL'}

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
        self.image_manager = HandPoseImageManager((image_height, image_width), self.filepath)

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
