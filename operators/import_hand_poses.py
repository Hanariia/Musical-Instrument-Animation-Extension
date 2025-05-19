import os
import bpy
from bpy_extras.io_utils import ImportHelper


class ImportHandPosesOperator(bpy.types.Operator, ImportHelper):
    """Import estimated hand poses json."""
    bl_idname = "mia.import_hand_poses"
    bl_label = "Import Hand Poses"
    bl_options = {'REGISTER', 'UNDO'}

    filepath: bpy.props.StringProperty(subtype='FILE_PATH')
    filename: bpy.props.StringProperty(subtype='FILE_NAME')

    # filters the file selection
    filter_glob: bpy.props.StringProperty(
        default="*.json",
        options={'HIDDEN'},
    )

    def execute(self, context):
        if not self.__is_selected_file_valid():
            self.report({'ERROR'}, "Please select a valid estimated hand poses JSON file.")
            return {'CANCELLED'}

        overlay_properties = context.window_manager.overlay_properties
        overlay_properties.filepath = self.filepath

        if overlay_properties.overlay_active:
            overlay_properties.refresh_overlay = True
        else:
            bpy.ops.mia.hand_pose_overlay('INVOKE_DEFAULT')
            overlay_properties.overlay_active = True
        return {'FINISHED'}

    @classmethod
    def poll(cls, context):
        sequence_editor = context.scene.sequence_editor
        return sequence_editor and len(sequence_editor.sequences) != 0

    def __is_selected_file_valid(self):
        return os.path.isfile(self.filepath) and os.path.splitext(self.filename)[1] == ".json"
