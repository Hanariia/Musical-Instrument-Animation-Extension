import bpy


class CheckSequencerAvailabilityOperator(bpy.types.Operator):
    """Checks the Video Sequencer availability.
    If occupied, the operator notifies the user that their work in the Video Sequencer will be deleted if they proceed
    and gives them the option to abort the import.
    Unless cancelled, the operator calls the Setup Video Reference operator.
    """
    bl_idname = "mia.check_sequencer_availability"
    bl_label = "Check Sequencer Availability"
    bl_options = {'REGISTER', 'UNDO'}
    bl_description = "Setup and Import Video Reference"

    def execute(self, context):
        # clear overlay if active
        if context.window_manager.overlay_properties.overlay_active:
            context.window_manager.overlay_properties.clear_overlay = True

        bpy.ops.mia.setup_video_reference('INVOKE_DEFAULT')
        return {'FINISHED'}

    def invoke(self, context, event):
        if len(context.scene.sequence_editor.sequences) > 0:
            return context.window_manager.invoke_confirm(
                self,
                event,
                title="The Video Sequencer is occupied.",
                message="If you proceed, the Video Sequencer contents will be deleted.",
                icon='WARNING',
                confirm_text='Delete Sequencer Contents and Continue')
        return self.execute(context)
