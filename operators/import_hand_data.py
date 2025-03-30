import os

import bpy


class ImportHandDataOperator(bpy.types.Operator):
    """Import estimated hand poses json."""
    bl_idname = "mia.import_hand_data"
    bl_label = "Import Hand Data"
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
            overlay_properties.hand_pose_file_updated = True
        else:
            bpy.ops.mia.hand_pose_overlay('INVOKE_DEFAULT')
            overlay_properties.overlay_active = True
        return {'FINISHED'}

    @classmethod
    def poll(cls, context):
        sequence_editor = bpy.context.scene.sequence_editor
        if sequence_editor and len(sequence_editor.sequences) != 0:
            return True
        return False

    def invoke(self, context, event):
        context.window_manager.fileselect_add(self)
        return {'RUNNING_MODAL'}

    def __is_selected_file_valid(self):
        if not os.path.isfile(self.filepath):
            return False
        if os.path.splitext(self.filename)[1] != ".json":
            return False
        return True
