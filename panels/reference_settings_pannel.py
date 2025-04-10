import bpy


class VideoReferenceSettingsPanel(bpy.types.Panel):
    """Creates video reference settings panel in the sidebar of the preview."""
    bl_label = "Video Reference Settings"
    bl_idname = "SEQUENCE_EDITOR_PT_video_reference_settings"
    bl_space_type = 'SEQUENCE_EDITOR'
    bl_region_type = 'UI'
    bl_category = "Video Reference"

    def draw(self, context):
        layout = self.layout
        layout.label(text="Hand Visibility")
        layout.prop(context.scene.sequence_editor.channels['Channel 2'], "mute", text="Right Hand", invert_checkbox=True)
        layout.prop(context.scene.sequence_editor.channels['Channel 3'], "mute", text="Left Hand", invert_checkbox=True)

        layout.label(text="Hand Pose Alignment")
        row = layout.row(align=True)
        row.prop(context.scene.overlay_settings, "center_align_hand_poses", toggle=True)
        row.prop(context.scene.overlay_settings, "center_align_hand_poses", text="Edge Align", toggle=True,
                 invert_checkbox=True)
