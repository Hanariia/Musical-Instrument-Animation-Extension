import bpy


class CheckSequencerAvailabilityOperator(bpy.types.Operator):
    """Checks the Video Sequencer availability.
    If occupied, the operator notifies the user that their work in the Video Sequencer will be deleted if they proceed
    and gives them the option to abort the import.
    Unless cancelled, the operator calls the Setup Video Reference operator."""
    bl_idname = "wm.check_sequencer_availability"
    bl_label = "Check Sequencer Availability"
    bl_options = {'REGISTER', 'UNDO'}
    bl_description = "Setup and Import Video Reference"

    def execute(self, context):
        bpy.ops.screen.setup_video_reference('INVOKE_DEFAULT')
        return {'FINISHED'}

    def invoke(self, context, event):
        if len(context.scene.sequence_editor.sequences) > 0:
            context.window_manager.invoke_confirm(
                self,
                event,
                title="The Video Sequencer is occupied.",
                message="If you proceed, the Video Sequencer contents will be deleted.",
                icon='WARNING',
                confirm_text='Delete Sequencer Contents and Continue')
            return {'RUNNING_MODAL'}
        return self.execute(context)
