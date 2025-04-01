import bpy


class VideoReferenceSettingsPanel(bpy.types.Panel):
    """Creates video reference settings panel in the sidebar of the preview."""
    bl_label = "Video Reference Settings"
    bl_idname = "SEQUENCE_EDITOR_PT_video_reference_settings"
    bl_space_type = 'SEQUENCE_EDITOR'
    bl_region_type = 'UI'
    bl_category = "Video Reference"
    bl_options = set()  # overwrite the default option {'DEFAULT_CLOSED'} to set panel to open
    # bl_context = "scene"

    def draw(self, context):
        layout = self.layout
        row = layout.row()
        row.label(text="Hand Visibility")
        row = layout.row()
        row.prop(context.scene.sequence_editor.channels['Channel 2'], "mute", text="Right Hand", invert_checkbox=True)
        row = layout.row()
        row.prop(context.scene.sequence_editor.channels['Channel 3'], "mute", text="Left Hand", invert_checkbox=True)
        row = layout.row()

        row.label(text="Hand Pose Alignment")
        row = layout.row()
        row.prop(context.scene.overlay_settings, "center_align_hand_poses", text="Center Align", toggle=True)
        row.prop(context.scene.overlay_settings, "center_align_hand_poses", text="Edge Align", toggle=True,
                 invert_checkbox=True)
