import bpy
from ..miae_utils import find_area


class SetupVideoReferenceOperator(bpy.types.Operator):
    """Adds an area with a video reference to the screen."""
    bl_idname = "screen.setup_video_reference"
    bl_label = "Setup Video Reference"
    bl_options = {'REGISTER', 'UNDO'}

    filepath: bpy.props.StringProperty(subtype='FILE_PATH')
    filename: bpy.props.StringProperty(subtype='FILE_NAME')

    @classmethod
    def poll(cls, context):
        for area in context.screen.areas.values():
            if area.type == 'VIEW_3D':
                return True
        return False

    def execute(self, context):
        self.__setup_preview_area(context)

        # add video to preview
        with context.temp_override(area=find_area(context, area_type='SEQUENCE_EDITOR')):
            bpy.ops.sequencer.select_all(action='SELECT')
            bpy.ops.sequencer.delete()
            bpy.ops.sequencer.movie_strip_add(
                filepath=self.filepath,
                show_multiview=False, frame_start=1, channel=1, fit_method='FIT', adjust_playback_rate=True, sound=True,
                use_framerate=False, replace_sel=True)
            bpy.context.scene.frame_end = max(context.sequences[0].frame_final_end - 1, bpy.context.scene.frame_end)
        return {'FINISHED'}

    def invoke(self, context, event):
        context.window_manager.fileselect_add(self)
        return {'RUNNING_MODAL'}

    def __setup_preview_area(self, context):
        # check if preview are is already present
        area_for_preview = find_area(context, 'SEQUENCE_EDITOR')
        if area_for_preview is not None and area_for_preview.spaces[0].view_type == 'PREVIEW':
            return area_for_preview

        area_for_preview = self.__choose_area_for_preview(context)
        with context.temp_override(area=area_for_preview):
            # add preview area to screen
            bpy.ops.screen.area_split(direction='VERTICAL')
            bpy.context.area.ui_type = 'SEQUENCE_EDITOR'
            bpy.context.space_data.view_type = 'PREVIEW'

    @staticmethod
    def __choose_area_for_preview(context):
        area = None
        if context.screen.name == 'Animation':
            area = find_area(context, 'DOPESHEET_EDITOR')
        if area is None:
            area = find_area(context, 'VIEW_3D')
        return area
