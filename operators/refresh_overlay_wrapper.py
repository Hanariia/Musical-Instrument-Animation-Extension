import bpy


# This functionality is wrapped into an operator to aid the UI creation.
class RefreshOverlayWrapperOperator(bpy.types.Operator):
    """Refresh the estimated hand poses overlay."""
    bl_idname = "mia.refresh_overlay"
    bl_label = "Refresh Overlay"
    bl_options = {'REGISTER'}

    @classmethod
    def poll(cls, context):
        return context.window_manager.overlay_properties.overlay_active

    def execute(self, context):
        context.window_manager.overlay_properties.refresh_overlay = True
        return {'FINISHED'}
