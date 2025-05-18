import bpy


# This functionality is wrapped into an operator to aid the UI creation.
class ClearOverlayWrapperOperator(bpy.types.Operator):
    """Clear the estimated hand poses overlay."""
    bl_idname = "mia.clear_overlay"
    bl_label = "Clear Overlay"
    bl_options = {'REGISTER'}

    @classmethod
    def poll(cls, context):
        return context.window_manager.overlay_properties.overlay_active

    def execute(self, context):
        context.window_manager.overlay_properties.clear_overlay = True
        return {'FINISHED'}
