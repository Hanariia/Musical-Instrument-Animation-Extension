import os
from typing import List
import bpy
from bpy_extras.io_utils import ImportHelper
from ..miae_utils import find_area


class SetupVideoReferenceOperator(bpy.types.Operator, ImportHelper):
    """Adds an area with a video reference to the screen."""
    bl_idname = "mia.setup_video_reference"
    bl_label = "Setup Video Reference"
    bl_options = {'REGISTER', 'UNDO'}

    filepath: bpy.props.StringProperty(subtype='FILE_PATH')
    filename: bpy.props.StringProperty(subtype='FILE_NAME')

    # filters the file selection
    accepted_file_extensions: List[str] = [".mp4", ".avi", ".mov", ".mkv", ".webm", ".mpg", ".mpeg",
                                           ".ogg", ".ogv", ".dv", ".dvd", ".vob", ".flv"]
    extensions_string = "*" + ";*".join(accepted_file_extensions)
    filter_glob: bpy.props.StringProperty(
        default=extensions_string,
        options={'HIDDEN'},
    )

    @classmethod
    def poll(cls, context):
        for area in context.screen.areas.values():
            if area.type == 'VIEW_3D':
                return True
        return False

    def execute(self, context):
        if not self.__is_selected_file_valid():
            self.report({'ERROR'}, 'Please select a video file.')
            return {'CANCELLED'}

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

    def __is_selected_file_valid(self):
        if not os.path.isfile(self.filepath):
            return False
        if os.path.splitext(self.filename)[1] not in self.accepted_file_extensions:
            return False
        return True

    def __setup_preview_area(self, context):
        # check if preview area is already present
        area_for_preview = find_area(context, 'SEQUENCE_EDITOR')
        if area_for_preview is not None and area_for_preview.spaces[0].view_type == 'PREVIEW':
            return

        # split the 3D view area into two
        area_for_preview = find_area(context, 'VIEW_3D')
        with context.temp_override(area=area_for_preview):
            if context.screen.name == 'Animation':
                bpy.ops.screen.area_split(direction='HORIZONTAL', factor=0.45)
            else:
                bpy.ops.screen.area_split(direction='VERTICAL', factor=0.4)

        # change the new 3d view area to the preview
        area_for_preview = self.__find_last_area_type_in_screen(context, area_for_preview.type)
        with context.temp_override(area=area_for_preview):
            bpy.context.area.ui_type = 'SEQUENCE_EDITOR'
            bpy.context.space_data.view_type = 'PREVIEW'

    @staticmethod
    def __find_last_area_type_in_screen(context, area_type: str) -> bpy.types.Area:
        area = None
        for area in context.screen.areas.values():
            if area.type == area_type:
                area = area
        return area
