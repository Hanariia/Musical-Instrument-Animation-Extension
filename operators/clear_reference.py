import bpy


class ClearReferenceOperator(bpy.types.Operator):
    """Clear Video Reference and Overlay."""
    bl_idname = "mia.clear_reference"
    bl_label = "Clear Reference"
    bl_options = {'REGISTER'}
    bl_description = "Clear Video Reference and Overlay"

    @classmethod
    def poll(cls, context):
        return context.window_manager.reference_active

    def execute(self, context):
        # clear overlay if active
        if context.window_manager.overlay_properties.overlay_active:
            context.window_manager.overlay_properties.clear_overlay = True

        bpy.ops.sequencer.select_all(action='SELECT')
        bpy.ops.sequencer.delete()
        context.window_manager.reference_active = False

        for area in context.screen.areas:
            if area.type == 'VIEW_3D':
                area.tag_redraw()
        return {'FINISHED'}

    def invoke(self, context, event):
        return context.window_manager.invoke_confirm(
            self,
            event,
            title="Clear Reference",
            message="Are you sure you want to clear the reference?",
            icon='QUESTION'
        )

